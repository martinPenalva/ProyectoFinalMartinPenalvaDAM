"""
Configuración de la aplicación Gestor de Eventos Locales
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la base de datos MySQL
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3309)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'eventos_locales'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': False  # Control manual de transacciones
}

# Configuración de la aplicación
APP_CONFIG = {
    'title': 'Gestor de Eventos Locales',
    'version': '1.0.0',
    'window_width': 1200,
    'window_height': 700,
    'min_window_width': 800,
    'min_window_height': 600
}

# Configuración de exportación
EXPORT_CONFIG = {
    'csv_encoding': 'utf-8-sig',  # UTF-8 con BOM para Excel
    'pdf_font': 'Helvetica',
    'pdf_font_size': 10,
    'exports_folder': 'exports'
}

# Configuración de concurrencia
CONCURRENCY_CONFIG = {
    'lock_timeout': 30,  # segundos - tiempo máximo para adquirir un lock
    'max_retries': 3,  # número máximo de reintentos en operaciones fallidas
    'pool_size': 20,  # Tamaño del pool de conexiones para soportar múltiples usuarios simultáneos
    'subscription_workers': 5,  # Número de worker threads para procesar suscripciones en paralelo
    'max_queue_size': 100,  # Tamaño máximo de la cola de tareas para procesamiento paralelo
    'retry_base_delay': 0.1,  # Retraso base para reintentos (segundos)
    'retry_max_delay': 2.0  # Retraso máximo para reintentos (segundos)
}

