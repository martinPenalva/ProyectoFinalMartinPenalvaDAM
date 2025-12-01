"""
Controlador para la gestión de usuarios
Maneja la lógica de negocio relacionada con usuarios
"""

from src.database.db_connection import DatabaseConnection
from src.models.user import User
from mysql.connector import Error
from typing import List, Optional
from datetime import datetime
import bcrypt


class UserController:
    """Controlador para operaciones CRUD de usuarios"""
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def get_all(self) -> List[User]:
        """Obtiene todos los usuarios"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT user_id, username, password_hash, role, created_at
                FROM users
                ORDER BY created_at DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            users = []
            for row in rows:
                user = User(
                    user_id=row['user_id'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    role=row['role'],
                    created_at=row['created_at']
                )
                users.append(user)
            
            return users
            
        except Error as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por ID"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT user_id, username, password_hash, role, created_at
                FROM users
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return User(
                    user_id=row['user_id'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    role=row['role'],
                    created_at=row['created_at']
                )
            return None
            
        except Error as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por nombre de usuario"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT user_id, username, password_hash, role, created_at
                FROM users
                WHERE username = %s
            """
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return User(
                    user_id=row['user_id'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    role=row['role'],
                    created_at=row['created_at']
                )
            return None
            
        except Error as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def create(self, user: User, password: str) -> Optional[int]:
        """Crea un nuevo usuario"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Verificar si el usuario ya existe
            check_query = "SELECT user_id FROM users WHERE username = %s"
            cursor.execute(check_query, (user.username,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return None
            
            # Crear hash de la contraseña
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            query = """
                INSERT INTO users (username, password_hash, role)
                VALUES (%s, %s, %s)
            """
            values = (user.username, password_hash, user.role)
            
            cursor.execute(query, values)
            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
            return user_id
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al crear usuario: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def update(self, user: User, new_password: Optional[str] = None) -> bool:
        """Actualiza un usuario"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            if new_password:
                # Actualizar contraseña
                password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                query = """
                    UPDATE users 
                    SET username = %s, password_hash = %s, role = %s
                    WHERE user_id = %s
                """
                values = (user.username, password_hash, user.role, user.user_id)
            else:
                # No actualizar contraseña
                query = """
                    UPDATE users 
                    SET username = %s, role = %s
                    WHERE user_id = %s
                """
                values = (user.username, user.role, user.user_id)
            
            cursor.execute(query, values)
            affected_rows = cursor.rowcount
            conn.commit()
            cursor.close()
            
            return affected_rows > 0
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al actualizar usuario: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def delete(self, user_id: int) -> bool:
        """Elimina un usuario"""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            affected_rows = cursor.rowcount
            conn.commit()
            cursor.close()
            
            return affected_rows > 0
            
        except Error as e:
            if conn:
                conn.rollback()
            print(f"Error al eliminar usuario: {e}")
            return False
        finally:
            if conn:
                conn.close()

