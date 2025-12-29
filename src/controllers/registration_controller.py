"""
Controlador para la gestión de inscripciones
Maneja la asignación de participantes a eventos
"""

from src.database.db_connection import DatabaseConnection
from mysql.connector import Error
from typing import List, Optional, Dict
from datetime import datetime


class RegistrationController:
    """Controlador para operaciones de inscripciones"""
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def register_participant(self, event_id: int, participant_id: int, 
                           status: str = "confirmado") -> Optional[int]:
        """
        Registra un participante en un evento.
        Usa bloqueo SELECT FOR UPDATE para evitar condiciones de carrera
        cuando múltiples usuarios intentan inscribirse simultáneamente.
        """
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
            return registration_id
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al registrar participante: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
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
    
    def get_event_participants(self, event_id: int) -> List[Dict]:
        """Obtiene todos los participantes de un evento"""
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

