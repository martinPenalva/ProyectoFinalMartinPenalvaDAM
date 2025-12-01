"""
Modelo de datos para Usuarios
"""

from datetime import datetime
from typing import Optional


class User:
    """Clase que representa un usuario"""
    
    def __init__(self, user_id: Optional[int] = None, username: str = "", 
                 password_hash: str = "", role: str = "user",
                 created_at: Optional[datetime] = None):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at
    
    def __str__(self):
        return f"User({self.user_id}: {self.username})"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """Convierte el usuario a diccionario"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password_hash': self.password_hash,
            'role': self.role,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un usuario desde un diccionario"""
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username', ''),
            password_hash=data.get('password_hash', ''),
            role=data.get('role', 'user'),
            created_at=data.get('created_at')
        )

