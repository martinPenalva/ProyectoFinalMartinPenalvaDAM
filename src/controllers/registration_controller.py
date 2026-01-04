"""
Controlador para la gestión de inscripciones
Maneja la asignación de participantes a eventos
Incluye gestión avanzada de concurrencia para usuarios simultáneos
"""

from src.database.db_connection import DatabaseConnection
from mysql.connector import Error
from typing import List, Optional, Dict, Tuple
from datetime import datetime
from src.utils.concurrency_manager import (
    retry_with_backoff, 
    get_subscription_processor,
    get_notification_system,
    ResourceLockManager
)
from config.config import CONCURRENCY_CONFIG

# Instancia global del gestor de locks
_lock_manager = ResourceLockManager()


class RegistrationController:
    """Controlador para operaciones de inscripciones con gestión de concurrencia"""
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    @retry_with_backoff(
        max_retries=CONCURRENCY_CONFIG.get('max_retries', 3),
        base_delay=CONCURRENCY_CONFIG.get('retry_base_delay', 0.1),
        max_delay=CONCURRENCY_CONFIG.get('retry_max_delay', 2.0),
        exceptions=(Error,)
    )
    def _register_participant_internal(self, event_id: int, participant_id: int, 
                                      status: str = "confirmado") -> Optional[int]:
        """
        Método interno para registrar un participante con locks y transacciones.
        Usa bloqueo SELECT FOR UPDATE para evitar condiciones de carrera.
        """
        # Usar lock de recurso para el evento específico
        resource_id = f"event_{event_id}"
        lock = _lock_manager.get_lock(resource_id)
        acquired = lock.acquire(timeout=CONCURRENCY_CONFIG.get('lock_timeout', 30))
        if not acquired:
            raise TimeoutError(f"No se pudo adquirir el lock para el evento {event_id} en {CONCURRENCY_CONFIG.get('lock_timeout', 30)}s")
        
        conn = None
        try:
            conn = self.db.get_connection()
            # Configurar nivel de aislamiento REPEATABLE READ para evitar lecturas sucias y condiciones de carrera
            cursor = conn.cursor()
            cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
            conn.start_transaction()
            
            # Verificar capacidad del evento con bloqueo FOR UPDATE
            # Esto previene que otro usuario modifique el evento mientras verificamos
            capacity_query = """
                SELECT capacity, 
                       (SELECT COUNT(*) FROM event_registrations 
                        WHERE event_id = %s AND status = 'confirmado') as current
                FROM events WHERE event_id = %s
                FOR UPDATE
            """
            cursor.execute(capacity_query, (event_id, event_id))
            result = cursor.fetchone()
            
            if not result:
                conn.rollback()
                cursor.close()
                return None
            
            capacity, current = result
            if current >= capacity:
                conn.rollback()
                cursor.close()
                return None  # Evento lleno
            
            # Verificar si ya está registrado
            check_query = """
                SELECT registration_id FROM event_registrations 
                WHERE event_id = %s AND participant_id = %s
            """
            cursor.execute(check_query, (event_id, participant_id))
            if cursor.fetchone():
                conn.rollback()
                cursor.close()
                return None  # Ya está registrado
            
            # Insertar registro
            query = """
                INSERT INTO event_registrations (event_id, participant_id, status)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (event_id, participant_id, status))
            conn.commit()
            registration_id = cursor.lastrowid
            cursor.close()
            
            # Notificar evento de inscripción
            get_notification_system().notify(
                'registration_created',
                event_id=event_id,
                participant_id=participant_id,
                registration_id=registration_id
            )
            
            return registration_id
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al registrar participante: {e}")
            raise  # Re-lanzar para que el decorador de reintento lo maneje
        finally:
            if conn:
                conn.close()
            lock.release()
    
    def register_participant(self, event_id: int, participant_id: int, 
                           status: str = "confirmado") -> Optional[int]:
        """
        Registra un participante en un evento.
        Usa bloqueo SELECT FOR UPDATE y locks de recursos para evitar condiciones de carrera
        cuando múltiples usuarios intentan inscribirse simultáneamente.
        Incluye reintentos automáticos y gestión de concurrencia.
        """
        try:
            return self._register_participant_internal(event_id, participant_id, status)
        except Exception as e:
            print(f"Error al registrar participante después de reintentos: {e}")
            return None
    
    def unregister_participant(self, event_id: int, participant_id: int) -> bool:
        """Elimina el registro de un participante en un evento"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = """
                DELETE FROM event_registrations 
                WHERE event_id = %s AND participant_id = %s
            """
            cursor.execute(query, (event_id, participant_id))
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            return affected_rows > 0
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al desregistrar participante: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def update_status(self, event_id: int, participant_id: int, new_status: str) -> bool:
        """
        Actualiza el estado de una inscripción
        
        Args:
            event_id: ID del evento
            participant_id: ID del participante
            new_status: Nuevo estado ('confirmado', 'cancelado', 'pendiente')
        
        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        # Validar estado
        valid_statuses = ['confirmado', 'cancelado', 'pendiente']
        if new_status.lower() not in valid_statuses:
            raise ValueError(f"Estado inválido. Estados válidos: {', '.join(valid_statuses)}")
        
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Verificar que la inscripción existe
            check_query = """
                SELECT registration_id FROM event_registrations 
                WHERE event_id = %s AND participant_id = %s
            """
            cursor.execute(check_query, (event_id, participant_id))
            if not cursor.fetchone():
                cursor.close()
                return False
            
            # Actualizar estado
            update_query = """
                UPDATE event_registrations 
                SET status = %s
                WHERE event_id = %s AND participant_id = %s
            """
            cursor.execute(update_query, (new_status.lower(), event_id, participant_id))
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            # Notificar evento de cambio de estado
            if affected_rows > 0:
                get_notification_system().notify(
                    'registration_status_changed',
                    event_id=event_id,
                    participant_id=participant_id,
                    new_status=new_status.lower()
                )
            
            return affected_rows > 0
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al actualizar estado de inscripción: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def get_event_participants(self, event_id: int) -> List[Dict]:
        """
        Obtiene todos los participantes de un evento (incluyendo cancelados)
        Retorna todas las inscripciones independientemente del estado
        """
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT p.*, er.status as registration_status, er.registered_at
                FROM participants p
                INNER JOIN event_registrations er ON p.participant_id = er.participant_id
                WHERE er.event_id = %s
                ORDER BY er.registered_at DESC
            """
            cursor.execute(query, (event_id,))
            results = cursor.fetchall()
            cursor.close()
            
            return results
            
        except Error as e:
            print(f"Error al obtener participantes del evento: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def count_confirmed_registrations(self, event_id: int) -> int:
        """
        Cuenta solo las inscripciones confirmadas de un evento
        Las inscripciones canceladas no cuentan para la capacidad
        
        Returns:
            Número de inscripciones confirmadas
        """
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT COUNT(*) 
                FROM event_registrations 
                WHERE event_id = %s AND status = 'confirmado'
            """
            cursor.execute(query, (event_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return result[0] if result else 0
            
        except Error as e:
            print(f"Error al contar inscripciones confirmadas: {e}")
            return 0
        finally:
            if conn:
                conn.close()
    
    def get_participant_events(self, participant_id: int) -> List[Dict]:
        """Obtiene todos los eventos de un participante"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT e.*, er.status as registration_status, er.registered_at
                FROM events e
                INNER JOIN event_registrations er ON e.event_id = er.event_id
                WHERE er.participant_id = %s
                ORDER BY e.start_datetime DESC
            """
            cursor.execute(query, (participant_id,))
            results = cursor.fetchall()
            cursor.close()
            
            return results
            
        except Error as e:
            print(f"Error al obtener eventos del participante: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def register_multiple_participants_parallel(self, event_id: int, 
                                                participant_ids: List[int],
                                                status: str = "confirmado") -> List[Tuple[int, Optional[int]]]:
        """
        Registra múltiples participantes en un evento de forma paralela.
        Usa worker threads para procesar las inscripciones simultáneamente.
        
        Args:
            event_id: ID del evento
            participant_ids: Lista de IDs de participantes a inscribir
            status: Estado de la inscripción (por defecto "confirmado")
        
        Returns:
            Lista de tuplas (participant_id, registration_id o None)
        """
        processor = get_subscription_processor()
        results = []
        
        # Crear tareas para cada inscripción
        tasks = []
        for participant_id in participant_ids:
            tasks.append((
                self._register_participant_internal,
                (event_id, participant_id, status),
                {},
                None  # callback
            ))
        
        # Enviar todas las tareas a la cola de procesamiento paralelo
        submitted = processor.submit_batch(tasks)
        
        # Esperar a que se completen todas las tareas
        task_results = processor.wait_for_results(submitted, timeout=60.0)
        
        # Procesar resultados
        for i, (success, result, error) in enumerate(task_results):
            participant_id = participant_ids[i]
            if success and result:
                results.append((participant_id, result))
            else:
                print(f"Error al registrar participante {participant_id}: {error}")
                results.append((participant_id, None))
        
        return results

