"""
Controlador de autenticación de usuarios
Maneja login, registro y validación de credenciales
"""

import bcrypt
from mysql.connector import Error
from typing import Optional, Tuple
from src.database.db_connection import DatabaseConnection


class AuthController:
    """Controlador para autenticación de usuarios"""
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def hash_password(self, password: str) -> str:
        """Genera un hash bcrypt de la contraseña"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                password_hash.encode('utf-8')
            )
        except Exception:
            return False
    
    def login(self, username: str, password: str) -> Tuple[bool, Optional[dict], Optional[str]]:
        """
        Intenta autenticar un usuario
        
        Returns:
            Tuple[bool, Optional[dict], Optional[str]]: 
            (éxito, datos_usuario, mensaje_error)
        """
        if not self.db or not self.db.pool:
            return False, None, "No hay conexión a la base de datos"
        
        if not username or not password:
            return False, None, "Usuario y contraseña son requeridos"
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Buscar usuario por username
            query = "SELECT user_id, username, password_hash, role FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not user:
                return False, None, "Usuario o contraseña incorrectos"
            
            # Verificar contraseña
            if self.verify_password(password, user['password_hash']):
                # Retornar datos del usuario (sin la contraseña)
                user_data = {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'role': user['role']
                }
                return True, user_data, None
            else:
                return False, None, "Usuario o contraseña incorrectos"
                
        except Error as e:
            return False, None, f"Error de base de datos: {str(e)}"
        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"
    
    def register(self, username: str, password: str, confirm_password: str,
                 first_name: str = None, last_name: str = None, email: str = None,
                 phone: int = None, identifier: str = None) -> Tuple[bool, Optional[str]]:
        """
        Registra un nuevo usuario y opcionalmente crea su perfil de participante
        
        Returns:
            Tuple[bool, Optional[str]]: (éxito, mensaje_error)
        """
        if not self.db or not self.db.pool:
            return False, "No hay conexión a la base de datos"
        
        # Validaciones básicas de usuario
        if not username or not password or not confirm_password:
            return False, "Todos los campos de usuario son requeridos"
        
        if len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"
        
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        if password != confirm_password:
            return False, "Las contraseñas no coinciden"
        
        # Validaciones de participante (si se proporcionan)
        create_participant = first_name and last_name and email and identifier
        if create_participant:
            if '@' not in email:
                return False, "El email no es válido"
        
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Verificar si el usuario ya existe
            check_query = "SELECT user_id FROM users WHERE username = %s"
            cursor.execute(check_query, (username,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return False, "El nombre de usuario ya está en uso"
            
            # Verificar si el DNI/NIE ya existe (si se proporciona)
            if create_participant and identifier:
                check_dni_query = "SELECT participant_id FROM participants WHERE identifier = %s"
                cursor.execute(check_dni_query, (identifier,))
                if cursor.fetchone():
                    cursor.close()
                    conn.close()
                    return False, "El DNI/NIE ya está registrado"
            
            # Verificar si el email ya existe (si se proporciona)
            if create_participant and email:
                check_email_query = "SELECT participant_id FROM participants WHERE email = %s"
                cursor.execute(check_email_query, (email,))
                if cursor.fetchone():
                    cursor.close()
                    conn.close()
                    return False, "El email ya está registrado"
            
            # Crear hash de la contraseña
            password_hash = self.hash_password(password)
            
            # Insertar nuevo usuario
            insert_user_query = """
                INSERT INTO users (username, password_hash, role)
                VALUES (%s, %s, 'user')
            """
            cursor.execute(insert_user_query, (username, password_hash))
            user_id = cursor.lastrowid
            
            # Si se proporcionaron datos de participante, crear el participante
            if create_participant:
                insert_participant_query = """
                    INSERT INTO participants (first_name, last_name, email, phone, identifier)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_participant_query, (
                    first_name, last_name, email, phone, identifier
                ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True, None
            
        except Error as e:
            if conn:
                conn.rollback()
                conn.close()
            return False, f"Error de base de datos: {str(e)}"
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            return False, f"Error inesperado: {str(e)}"
    
    def user_exists(self, username: str) -> bool:
        """Verifica si un usuario existe"""
        if not self.db or not self.db.pool:
            return False
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = "SELECT user_id FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            exists = cursor.fetchone() is not None
            
            cursor.close()
            conn.close()
            
            return exists
        except Exception:
            return False

