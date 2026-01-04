"""
Controlador para la gestión de eventos
Maneja la lógica de negocio relacionada con eventos
Incluye gestión avanzada de concurrencia para usuarios simultáneos
"""

from src.database.db_connection import DatabaseConnection
from src.models.event import Event
from mysql.connector import Error
from typing import List, Optional
from datetime import datetime
from src.utils.concurrency_manager import (
    retry_with_backoff,
    get_notification_system,
    ResourceLockManager
)
from config.config import CONCURRENCY_CONFIG

# Instancia global del gestor de locks
_lock_manager = ResourceLockManager()


class EventController:
    """Controlador para operaciones CRUD de eventos con gestión de concurrencia"""
    
    def __init__(self, db: DatabaseConnection, user_role: str = 'user'):
        """
        Inicializa el controlador de eventos
        
        Args:
            db: Conexión a la base de datos
            user_role: Rol del usuario ('admin' o 'user'). Solo admin puede modificar eventos.
        """
        self.db = db
        self.user_role = user_role
        self.is_admin = (user_role == 'admin')
    
    def _check_admin_permission(self) -> bool:
        """
        Verifica si el usuario actual tiene permisos de administrador
        
        Returns:
            True si es admin, False en caso contrario
        
        Raises:
            PermissionError: Si el usuario no es admin
        """
        if not self.is_admin:
            raise PermissionError("Solo los administradores pueden modificar eventos")
        return True
    
    def create(self, event: Event) -> Optional[int]:
        """
        Crea un nuevo evento
        Solo los administradores pueden crear eventos
        
        Raises:
            PermissionError: Si el usuario no es administrador
        """
        self._check_admin_permission()
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO events (title, description, location, start_datetime, 
                                  end_datetime, capacity, status, version)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
            """
            values = (
                event.title, event.description, event.location,
                event.start_datetime, event.end_datetime,
                event.capacity, event.status
            )
            
            cursor.execute(query, values)
            conn.commit()
            event_id = cursor.lastrowid
            cursor.close()
            return event_id
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al crear evento: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def get_all(self) -> List[Event]:
        """Obtiene todos los eventos"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM events ORDER BY start_datetime DESC"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            return [Event.from_dict(row) for row in results]
            
        except Error as e:
            print(f"Error al obtener eventos: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_by_id(self, event_id: int) -> Optional[Event]:
        """Obtiene un evento por su ID"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM events WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return Event.from_dict(result)
            return None
            
        except Error as e:
            print(f"Error al obtener evento: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    @retry_with_backoff(
        max_retries=CONCURRENCY_CONFIG.get('max_retries', 3),
        base_delay=CONCURRENCY_CONFIG.get('retry_base_delay', 0.1),
        max_delay=CONCURRENCY_CONFIG.get('retry_max_delay', 2.0),
        exceptions=(Error,)
    )
    def _update_internal(self, event: Event) -> bool:
        """
        Método interno para actualizar un evento con locks y control de versiones optimista.
        Solo los administradores pueden actualizar eventos.
        """
        self._check_admin_permission()
        # Usar lock de recurso para el evento específico
        resource_id = f"event_{event.event_id}"
        lock = _lock_manager.get_lock(resource_id)
        acquired = lock.acquire(timeout=CONCURRENCY_CONFIG.get('lock_timeout', 30))
        if not acquired:
            raise TimeoutError(f"No se pudo adquirir el lock para el evento {event.event_id} en {CONCURRENCY_CONFIG.get('lock_timeout', 30)}s")
        
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Verificar versión antes de actualizar (control de concurrencia optimista)
            query = """
                UPDATE events 
                SET title = %s, description = %s, location = %s,
                    start_datetime = %s, end_datetime = %s,
                    capacity = %s, status = %s, version = version + 1
                WHERE event_id = %s AND version = %s
            """
            values = (
                event.title, event.description, event.location,
                event.start_datetime, event.end_datetime,
                event.capacity, event.status, event.event_id, event.version
            )
            
            cursor.execute(query, values)
            affected_rows = cursor.rowcount
            conn.commit()
            cursor.close()
            
            if affected_rows == 0:
                # La versión cambió, conflicto de concurrencia
                return False
            
            # Notificar evento de actualización
            get_notification_system().notify(
                'event_updated',
                event_id=event.event_id,
                event=event
            )
            
            return True
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al actualizar evento: {e}")
            raise  # Re-lanzar para que el decorador de reintento lo maneje
        finally:
            if conn:
                conn.close()
            lock.release()
    
    def update(self, event: Event) -> bool:
        """
        Actualiza un evento (con control de concurrencia optimista y locks de recursos).
        Incluye reintentos automáticos y gestión de concurrencia mejorada.
        """
        try:
            return self._update_internal(event)
        except Exception as e:
            print(f"Error al actualizar evento después de reintentos: {e}")
            return False
    
    def delete(self, event_id: int) -> bool:
        """
        Elimina un evento
        Solo los administradores pueden eliminar eventos
        
        Raises:
            PermissionError: Si el usuario no es administrador
        """
        self._check_admin_permission()
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM events WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            return affected_rows > 0
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al eliminar evento: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def search(self, search_term: str) -> List[Event]:
        """Busca eventos por título, descripción o ubicación"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT * FROM events 
                WHERE title LIKE %s OR description LIKE %s OR location LIKE %s
                ORDER BY start_datetime DESC
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            results = cursor.fetchall()
            cursor.close()
            
            return [Event.from_dict(row) for row in results]
            
        except Error as e:
            print(f"Error al buscar eventos: {e}")
            return []
        finally:
            if conn:
                conn.close()

