"""
Controlador para la gestión de eventos
Maneja la lógica de negocio relacionada con eventos
"""

from src.database.db_connection import DatabaseConnection
from src.models.event import Event
from mysql.connector import Error
from typing import List, Optional
from datetime import datetime


class EventController:
    """Controlador para operaciones CRUD de eventos"""
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, event: Event) -> Optional[int]:
        """Crea un nuevo evento"""
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
    
    def update(self, event: Event) -> bool:
        """Actualiza un evento (con control de concurrencia optimista)"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Verificar versión antes de actualizar
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
            
            return True
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al actualizar evento: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def delete(self, event_id: int) -> bool:
        """Elimina un evento"""
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

