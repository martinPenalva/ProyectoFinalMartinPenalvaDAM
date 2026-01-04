"""
Controlador para la gestión de participantes
Maneja la lógica de negocio relacionada con participantes
"""

from src.database.db_connection import DatabaseConnection
from src.models.participant import Participant
from mysql.connector import Error
from typing import List, Optional


class ParticipantController:
    """Controlador para operaciones CRUD de participantes"""
    
    def __init__(self, db: DatabaseConnection, user_role: str = 'user'):
        """
        Inicializa el controlador de participantes
        
        Args:
            db: Conexión a la base de datos
            user_role: Rol del usuario ('admin' o 'user'). Solo admin puede modificar participantes.
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
            raise PermissionError("Solo los administradores pueden modificar participantes")
        return True
    
    def create(self, participant: Participant) -> Optional[int]:
        """
        Crea un nuevo participante
        Solo los administradores pueden crear participantes
        
        Raises:
            PermissionError: Si el usuario no es administrador
        """
        self._check_admin_permission()
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO participants (first_name, last_name, email, phone, identifier)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                participant.first_name, participant.last_name,
                participant.email, participant.phone, participant.identifier
            )
            
            cursor.execute(query, values)
            conn.commit()
            participant_id = cursor.lastrowid
            cursor.close()
            return participant_id
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al crear participante: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def get_all(self) -> List[Participant]:
        """Obtiene todos los participantes"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM participants ORDER BY last_name, first_name"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            return [Participant.from_dict(row) for row in results]
            
        except Error as e:
            print(f"Error al obtener participantes: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_by_id(self, participant_id: int) -> Optional[Participant]:
        """Obtiene un participante por su ID"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM participants WHERE participant_id = %s"
            cursor.execute(query, (participant_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return Participant.from_dict(result)
            return None
            
        except Error as e:
            print(f"Error al obtener participante: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def update(self, participant: Participant) -> bool:
        """
        Actualiza un participante
        Solo los administradores pueden actualizar participantes
        
        Raises:
            PermissionError: Si el usuario no es administrador
        """
        self._check_admin_permission()
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE participants 
                SET first_name = %s, last_name = %s, email = %s, 
                    phone = %s, identifier = %s
                WHERE participant_id = %s
            """
            values = (
                participant.first_name, participant.last_name,
                participant.email, participant.phone, participant.identifier,
                participant.participant_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            return affected_rows > 0
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al actualizar participante: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def delete(self, participant_id: int) -> bool:
        """
        Elimina un participante
        Solo los administradores pueden eliminar participantes
        
        Raises:
            PermissionError: Si el usuario no es administrador
        """
        self._check_admin_permission()
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM participants WHERE participant_id = %s"
            cursor.execute(query, (participant_id,))
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            return affected_rows > 0
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al eliminar participante: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def search(self, search_term: str) -> List[Participant]:
        """Busca participantes por nombre, apellido, email o DNI"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT * FROM participants 
                WHERE first_name LIKE %s OR last_name LIKE %s 
                   OR email LIKE %s OR identifier LIKE %s
                ORDER BY last_name, first_name
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, 
                                  search_pattern, search_pattern))
            results = cursor.fetchall()
            cursor.close()
            
            return [Participant.from_dict(row) for row in results]
            
        except Error as e:
            print(f"Error al buscar participantes: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_by_email(self, email: str) -> Optional[Participant]:
        """Obtiene un participante por su email"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM participants WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return Participant.from_dict(result)
            return None
            
        except Error as e:
            print(f"Error al obtener participante por email: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def find_by_username(self, username: str) -> Optional[Participant]:
        """
        Busca un participante asociado a un username.
        Intenta múltiples estrategias:
        1. Email exacto = username
        2. Email que empiece con username@
        3. Email que contenga username (parte antes del @)
        """
        if not username:
            return None
        
        # Estrategia 1: Email exacto
        participant = self.get_by_email(username)
        if participant:
            return participant
        
        # Estrategia 2: Buscar por email que empiece con username@
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Buscar email que empiece con username@
            query = "SELECT * FROM participants WHERE email LIKE %s"
            cursor.execute(query, (f"{username}@%",))
            result = cursor.fetchone()
            
            if result:
                cursor.close()
                return Participant.from_dict(result)
            
            # Estrategia 3: Buscar email donde la parte antes del @ sea igual a username
            query = "SELECT * FROM participants WHERE SUBSTRING_INDEX(email, '@', 1) = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            
            cursor.close()
            
            if result:
                return Participant.from_dict(result)
            
            return None
            
        except Error as e:
            print(f"Error al buscar participante por username: {e}")
            return None
        finally:
            if conn:
                conn.close()

