"""
Modelo de datos para Participantes
"""

from typing import Optional


class Participant:
    """Clase que representa un participante"""
    
    def __init__(self, participant_id: Optional[int] = None,
                 first_name: str = "", last_name: str = "",
                 email: str = "", phone: Optional[int] = None,
                 identifier: str = ""):
        self.participant_id = participant_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.identifier = identifier  # DNI/NIE
    
    def __str__(self):
        return f"Participant({self.participant_id}: {self.full_name})"
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def full_name(self):
        """Retorna el nombre completo"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def to_dict(self):
        """Convierte el participante a diccionario"""
        return {
            'participant_id': self.participant_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'identifier': self.identifier
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un participante desde un diccionario"""
        return cls(
            participant_id=data.get('participant_id'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone'),
            identifier=data.get('identifier', '')
        )

