"""
Script de prueba para verificar el soporte de múltiples usuarios simultáneos
Ejecuta este script para verificar que el pool de conexiones funciona correctamente
"""

import sys
import os
import threading
import time

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database.db_connection import DatabaseConnection


def test_connection(thread_id, results):
    """Prueba una conexión desde un hilo"""
    try:
        db = DatabaseConnection()
        conn = db.get_connection()
        
        if conn and conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            results[thread_id] = "✅ Éxito"
            print(f"Hilo {thread_id}: Conexión exitosa")
        else:
            results[thread_id] = "❌ Fallo: No conectado"
            print(f"Hilo {thread_id}: No se pudo conectar")
    except Exception as e:
        results[thread_id] = f"❌ Error: {str(e)}"
        print(f"Hilo {thread_id}: Error - {str(e)}")


def main():
    """Prueba múltiples conexiones simultáneas"""
    print("=" * 60)
    print("PRUEBA DE MÚLTIPLES USUARIOS SIMULTÁNEOS")
    print("=" * 60)
    print()
    
    # Verificar que MySQL esté disponible
    try:
        db = DatabaseConnection()
        if not db.pool:
            print("❌ ERROR: No se pudo crear el pool de conexiones")
            print("   Verifica que MySQL esté ejecutándose y las credenciales sean correctas")
            return
        
        print(f"✅ Pool de conexiones creado (tamaño: {db.pool.pool_size})")
        print()
    except Exception as e:
        print(f"❌ ERROR: No se pudo conectar a la base de datos: {e}")
        return
    
    # Número de conexiones simultáneas a probar
    num_threads = 10
    print(f"Probando {num_threads} conexiones simultáneas...")
    print()
    
    results = {}
    threads = []
    
    # Crear y ejecutar hilos
    start_time = time.time()
    
    for i in range(num_threads):
        thread = threading.Thread(target=test_connection, args=(i, results))
        threads.append(thread)
        thread.start()
        time.sleep(0.1)  # Pequeño delay para simular usuarios reales
    
    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    # Mostrar resultados
    print()
    print("=" * 60)
    print("RESULTADOS")
    print("=" * 60)
    
    success_count = 0
    for i in range(num_threads):
        result = results.get(i, "❌ No completado")
        print(f"Conexión {i+1}: {result}")
        if "✅" in result:
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"Resumen: {success_count}/{num_threads} conexiones exitosas")
    print(f"Tiempo total: {elapsed:.2f} segundos")
    print("=" * 60)
    
    if success_count == num_threads:
        print()
        print("✅ ¡PRUEBA EXITOSA!")
        print("   El pool de conexiones puede manejar múltiples usuarios simultáneos")
    else:
        print()
        print("⚠️  ADVERTENCIA")
        print(f"   Solo {success_count} de {num_threads} conexiones fueron exitosas")
        print("   Puede que el pool esté saturado o haya problemas de conexión")
    
    print()
    print("Para probar con la aplicación real:")
    print("1. Abre múltiples terminales")
    print("2. En cada una, ejecuta: python src/main.py")
    print("3. Inicia sesión con diferentes usuarios")
    print("4. Realiza operaciones simultáneamente")
    print()
    print("Ver COMO_PROBAR_MULTIUSUARIO.md para más detalles")


if __name__ == "__main__":
    main()

