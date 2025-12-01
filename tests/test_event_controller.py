"""
Pruebas unitarias para EventController
"""

import unittest
from datetime import datetime
from src.controllers.event_controller import EventController
from src.models.event import Event
from src.database.db_connection import DatabaseConnection


class TestEventController(unittest.TestCase):
    """Clase de pruebas para EventController"""
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todas las pruebas"""
        cls.db = DatabaseConnection()
        cls.controller = EventController(cls.db)
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        # Limpiar datos de prueba si es necesario
        pass
    
    def test_create_event(self):
        """Prueba la creación de un evento"""
        event = Event(
            title="Evento de Prueba",
            description="Descripción de prueba",
            location="Ubicación de prueba",
            start_datetime=datetime(2024, 12, 25, 10, 0),
            end_datetime=datetime(2024, 12, 25, 12, 0),
            capacity=50,
            status="activo"
        )
        
        event_id = self.controller.create(event)
        self.assertIsNotNone(event_id)
        self.assertIsInstance(event_id, int)
    
    def test_get_all_events(self):
        """Prueba obtener todos los eventos"""
        events = self.controller.get_all()
        self.assertIsInstance(events, list)
    
    # Agregar más pruebas según sea necesario


if __name__ == '__main__':
    unittest.main()

