"""
Gestión avanzada de concurrencia para el Gestor de Eventos Locales
Incluye: locks por recurso, reintentos, worker threads, y procesamiento en paralelo
"""

import threading
import queue
import time
from typing import Callable, Optional, Any, Dict, List
from functools import wraps
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResourceLockManager:
    """
    Gestor de locks por recurso para sincronización de acceso
    Permite bloquear recursos específicos (ej: eventos, participantes) de forma individual
    """
    
    def __init__(self):
        self._locks: Dict[str, threading.RLock] = {}
        self._global_lock = threading.RLock()
    
    def get_lock(self, resource_id: str) -> threading.RLock:
        """Obtiene o crea un lock para un recurso específico"""
        if resource_id not in self._locks:
            with self._global_lock:
                if resource_id not in self._locks:
                    self._locks[resource_id] = threading.RLock()
        return self._locks[resource_id]
    
    def acquire(self, resource_id: str, timeout: Optional[float] = None) -> bool:
        """Adquiere el lock de un recurso con timeout opcional"""
        lock = self.get_lock(resource_id)
        return lock.acquire(timeout=timeout)
    
    def release(self, resource_id: str):
        """Libera el lock de un recurso"""
        if resource_id in self._locks:
            try:
                self._locks[resource_id].release()
            except RuntimeError:
                # El lock no está adquirido, ignorar
                pass
    
    def __enter__(self, resource_id: str):
        """Context manager para locks"""
        self.acquire(resource_id)
        return self
    
    def __exit__(self, resource_id: str, exc_type, exc_val, exc_tb):
        """Libera el lock al salir del contexto"""
        self.release(resource_id)


# Instancia global del gestor de locks
_resource_lock_manager = ResourceLockManager()


def with_resource_lock(resource_id_getter: Callable[[Any], str], timeout: float = 30.0):
    """
    Decorador para usar locks de recursos en funciones
    
    Args:
        resource_id_getter: Función que extrae el ID del recurso de los argumentos
        timeout: Tiempo máximo de espera para adquirir el lock (segundos)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obtener el ID del recurso
            resource_id = resource_id_getter(*args, **kwargs)
            lock = _resource_lock_manager.get_lock(resource_id)
            
            # Intentar adquirir el lock con timeout
            acquired = lock.acquire(timeout=timeout)
            if not acquired:
                raise TimeoutError(f"No se pudo adquirir el lock para el recurso {resource_id} en {timeout}s")
            
            try:
                return func(*args, **kwargs)
            finally:
                lock.release()
        
        return wrapper
    return decorator


def retry_with_backoff(max_retries: int = 3, base_delay: float = 0.1, max_delay: float = 2.0, 
                      exceptions: tuple = (Exception,)):
    """
    Decorador para reintentar operaciones con backoff exponencial
    
    Args:
        max_retries: Número máximo de reintentos
        base_delay: Retraso inicial en segundos
        max_delay: Retraso máximo en segundos
        exceptions: Tupla de excepciones que deben activar el reintento
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"Intento {attempt + 1}/{max_retries + 1} falló para {func.__name__}: {e}. Reintentando en {delay}s...")
                        time.sleep(delay)
                        delay = min(delay * 2, max_delay)  # Backoff exponencial
                    else:
                        logger.error(f"Todos los reintentos fallaron para {func.__name__}")
                        raise
            
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


class ParallelSubscriptionProcessor:
    """
    Procesador de suscripciones en paralelo usando worker threads
    Permite procesar múltiples inscripciones simultáneamente de forma segura
    """
    
    def __init__(self, num_workers: int = 5, max_queue_size: int = 100):
        """
        Inicializa el procesador de suscripciones
        
        Args:
            num_workers: Número de threads worker para procesar suscripciones
            max_queue_size: Tamaño máximo de la cola de tareas
        """
        self.num_workers = num_workers
        self.task_queue = queue.Queue(maxsize=max_queue_size)
        self.result_queue = queue.Queue()
        self.workers: List[threading.Thread] = []
        self.stop_event = threading.Event()
        self._started = False
        self._lock = threading.Lock()
    
    def start(self):
        """Inicia los worker threads"""
        if self._started:
            return
        
        with self._lock:
            if self._started:
                return
            
            self.stop_event.clear()
            for i in range(self.num_workers):
                worker = threading.Thread(
                    target=self._worker_loop,
                    name=f"SubscriptionWorker-{i}",
                    daemon=True
                )
                worker.start()
                self.workers.append(worker)
            
            self._started = True
            logger.info(f"Iniciados {self.num_workers} worker threads para procesamiento paralelo")
    
    def stop(self, timeout: float = 5.0):
        """Detiene los worker threads"""
        if not self._started:
            return
        
        with self._lock:
            if not self._started:
                return
            
            self.stop_event.set()
            
            # Esperar a que los workers terminen
            for worker in self.workers:
                worker.join(timeout=timeout)
            
            self.workers.clear()
            self._started = False
            logger.info("Worker threads detenidos")
    
    def _worker_loop(self):
        """Loop principal de cada worker thread"""
        while not self.stop_event.is_set():
            try:
                # Obtener tarea de la cola con timeout para poder verificar stop_event
                try:
                    task = self.task_queue.get(timeout=0.5)
                except queue.Empty:
                    continue
                
                try:
                    # Ejecutar la tarea
                    func, args, kwargs, callback = task
                    result = func(*args, **kwargs)
                    
                    # Si hay callback, ejecutarlo
                    if callback:
                        callback(result)
                    
                    # Enviar resultado a la cola de resultados
                    self.result_queue.put((True, result, None))
                except Exception as e:
                    logger.error(f"Error en worker thread al procesar tarea: {e}")
                    self.result_queue.put((False, None, e))
                finally:
                    self.task_queue.task_done()
            
            except Exception as e:
                logger.error(f"Error en worker loop: {e}")
    
    def submit(self, func: Callable, *args, callback: Optional[Callable] = None, **kwargs) -> bool:
        """
        Envía una tarea a la cola de procesamiento
        
        Args:
            func: Función a ejecutar
            *args: Argumentos posicionales
            callback: Función opcional a ejecutar con el resultado
            **kwargs: Argumentos con nombre
        
        Returns:
            True si la tarea fue encolada, False si la cola está llena
        """
        if not self._started:
            self.start()
        
        try:
            self.task_queue.put((func, args, kwargs, callback), block=False)
            return True
        except queue.Full:
            logger.warning("Cola de tareas llena, no se pudo encolar la tarea")
            return False
    
    def submit_batch(self, tasks: List[tuple]) -> int:
        """
        Envía múltiples tareas a la cola
        
        Args:
            tasks: Lista de tuplas (func, args, kwargs, callback)
        
        Returns:
            Número de tareas encoladas exitosamente
        """
        if not self._started:
            self.start()
        
        count = 0
        for task in tasks:
            func, args, kwargs, callback = task
            if self.submit(func, *args, callback=callback, **kwargs):
                count += 1
            else:
                break
        
        return count
    
    def wait_for_results(self, num_tasks: int, timeout: Optional[float] = None) -> List[Any]:
        """
        Espera a que se completen un número de tareas
        
        Args:
            num_tasks: Número de tareas a esperar
            timeout: Tiempo máximo de espera (None = infinito)
        
        Returns:
            Lista de resultados (éxito, resultado, error)
        """
        results = []
        start_time = time.time()
        
        for i in range(num_tasks):
            if timeout:
                remaining = timeout - (time.time() - start_time)
                if remaining <= 0:
                    break
                try:
                    result = self.result_queue.get(timeout=remaining)
                except queue.Empty:
                    break
            else:
                result = self.result_queue.get()
            
            results.append(result)
        
        return results
    
    def wait_all(self, timeout: Optional[float] = None):
        """Espera a que se completen todas las tareas en la cola"""
        self.task_queue.join()
        # Recoger todos los resultados pendientes
        results = []
        while True:
            try:
                result = self.result_queue.get_nowait()
                results.append(result)
            except queue.Empty:
                break
        return results


# Instancia global del procesador de suscripciones
_subscription_processor: Optional[ParallelSubscriptionProcessor] = None


def get_subscription_processor() -> ParallelSubscriptionProcessor:
    """Obtiene la instancia global del procesador de suscripciones"""
    global _subscription_processor
    if _subscription_processor is None:
        from config.config import CONCURRENCY_CONFIG
        num_workers = CONCURRENCY_CONFIG.get('subscription_workers', 5)
        max_queue = CONCURRENCY_CONFIG.get('max_queue_size', 100)
        _subscription_processor = ParallelSubscriptionProcessor(
            num_workers=num_workers,
            max_queue_size=max_queue
        )
        _subscription_processor.start()
    return _subscription_processor


class EventNotificationSystem:
    """
    Sistema de notificaciones de eventos usando threading.Event
    Permite notificar a múltiples listeners cuando ocurren cambios
    """
    
    def __init__(self):
        self._events: Dict[str, threading.Event] = {}
        self._lock = threading.Lock()
        self._callbacks: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable):
        """Suscribe un callback a un tipo de evento"""
        with self._lock:
            if event_type not in self._callbacks:
                self._callbacks[event_type] = []
            self._callbacks[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """Desuscribe un callback de un tipo de evento"""
        with self._lock:
            if event_type in self._callbacks:
                try:
                    self._callbacks[event_type].remove(callback)
                except ValueError:
                    pass
    
    def notify(self, event_type: str, *args, **kwargs):
        """Notifica a todos los suscriptores de un evento"""
        with self._lock:
            if event_type not in self._callbacks:
                return
            
            # Ejecutar callbacks en threads separados para no bloquear
            for callback in self._callbacks[event_type]:
                try:
                    thread = threading.Thread(
                        target=callback,
                        args=args,
                        kwargs=kwargs,
                        daemon=True
                    )
                    thread.start()
                except Exception as e:
                    logger.error(f"Error al ejecutar callback para {event_type}: {e}")
    
    def get_event(self, event_type: str) -> threading.Event:
        """Obtiene o crea un threading.Event para un tipo de evento"""
        if event_type not in self._events:
            with self._lock:
                if event_type not in self._events:
                    self._events[event_type] = threading.Event()
        return self._events[event_type]


# Instancia global del sistema de notificaciones
_event_notification_system = EventNotificationSystem()


def get_notification_system() -> EventNotificationSystem:
    """Obtiene la instancia global del sistema de notificaciones"""
    return _event_notification_system

