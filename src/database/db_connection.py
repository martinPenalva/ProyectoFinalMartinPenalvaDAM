"""
Gestión de la conexión a la base de datos MySQL
"""

import mysql.connector
from mysql.connector import Error, pooling
import sys
import os
import threading

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config.config import DB_CONFIG, CONCURRENCY_CONFIG


class DatabaseConnection:
    """Clase para gestionar la conexión a MySQL con pool de conexiones"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.pool = None
        try:
            self._create_connection_pool()
        except Exception as e:
            # Si falla, pool queda en None (no imprimir error, se maneja en main.py)
            self.pool = None
        self._initialized = True
    
    def _create_connection_pool(self):
        """Crea un pool de conexiones a la base de datos para soportar múltiples usuarios simultáneos"""
        try:
            pool_size = CONCURRENCY_CONFIG.get('pool_size', 20)
            self.pool = pooling.MySQLConnectionPool(
                pool_name="eventos_pool",
                pool_size=pool_size,
                pool_reset_session=True,
                **DB_CONFIG
            )
            print(f"Pool de conexiones creado exitosamente (tamaño: {pool_size} conexiones)")
        except (Error, Exception) as e:
            # No crear pool si hay error
            self.pool = None
            # Re-lanzar la excepción para que main.py la capture
            raise
    
    def get_connection(self):
        """
        Obtiene una conexión del pool.
        Cada usuario puede tener su propia conexión simultáneamente.
        Las transacciones se manejan manualmente en los controladores.
        """
        if not self.pool:
            raise Error("No hay pool de conexiones disponible")
        try:
            conn = self.pool.get_connection()
            return conn
        except Error as e:
            print(f"Error al obtener conexión del pool: {e}")
            raise
    
    def test_connection(self):
        """Prueba la conexión a la base de datos"""
        try:
            conn = self.get_connection()
            if conn.is_connected():
                conn.close()
                return True
        except Error as e:
            print(f"Error de conexión: {e}")
            return False
        return False
    
    def close(self):
        """Cierra todas las conexiones del pool"""
        # El pool se cierra automáticamente cuando se destruye el objeto
        pass

