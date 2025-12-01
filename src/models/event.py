"""
Modelo de datos para Eventos
"""

from datetime import datetime
from typing import Optional


class Event:
    """Clase que representa un evento"""
    
    def __init__(self, event_id: Optional[int] = None, title: str = "", 
                 description: str = "", location: str = "",
                 start_datetime: Optional[datetime] = None,
                 end_datetime: Optional[datetime] = None,
                 capacity: int = 0, status: str = "activo",
                 version: int = 0):
        self.event_id = event_id
        self.title = title
        self.description = description
        self.location = location
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.capacity = capacity
        self.status = status
        self.version = version  # Para control de concurrencia optimista
    
    def __str__(self):
        return f"Event({self.event_id}: {self.title})"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """Convierte el evento a diccionario"""
        return {
            'event_id': self.event_id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'capacity': self.capacity,
            'status': self.status,
            'version': self.version
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un evento desde un diccionario"""
        return cls(
            event_id=data.get('event_id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            location=data.get('location', ''),
            start_datetime=data.get('start_datetime'),
            end_datetime=data.get('end_datetime'),
            capacity=data.get('capacity', 0),
            status=data.get('status', 'activo'),
            version=data.get('version', 0)
        )

