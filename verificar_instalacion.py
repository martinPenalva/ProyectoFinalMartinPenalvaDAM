"""
Script para verificar que Python y las dependencias estén instaladas correctamente
Ejecuta: python verificar_instalacion.py
"""

import sys
import subprocess

def verificar_python():
    """Verifica la versión de Python"""
    print("=" * 50)
    print("VERIFICACIÓN DE INSTALACIÓN DE PYTHON")
    print("=" * 50)
    
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} instalado")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠ ADVERTENCIA: Se recomienda Python 3.8 o superior")
        return False
    
    return True

def verificar_pip():
    """Verifica que pip esté instalado"""
    try:
        import pip
        print("✓ pip instalado")
        return True
    except ImportError:
        print("✗ pip NO está instalado")
        print("  Solución: Reinstala Python y marca 'Add pip'")
        return False

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    print("\n" + "=" * 50)
    print("VERIFICACIÓN DE DEPENDENCIAS")
    print("=" * 50)
    
    dependencias = {
        'mysql-connector-python': 'mysql.connector',
        'pandas': 'pandas',
        'reportlab': 'reportlab',
        'python-dotenv': 'dotenv',
    }
    
    faltantes = []
    
    for nombre, modulo in dependencias.items():
        try:
            __import__(modulo)
            print(f"✓ {nombre} instalado")
        except ImportError:
            print(f"✗ {nombre} NO instalado")
            faltantes.append(nombre)
    
    if faltantes:
        print(f"\n⚠ Faltan {len(faltantes)} dependencia(s)")
        print("  Solución: Ejecuta: pip install -r requirements.txt")
        return False
    
    return True

def verificar_mysql():
    """Intenta verificar la conexión a MySQL"""
    print("\n" + "=" * 50)
    print("VERIFICACIÓN DE MYSQL")
    print("=" * 50)
    
    try:
        import mysql.connector
        print("✓ mysql-connector-python disponible")
        
        # Intentar conectar (sin fallar si no hay servidor)
        try:
            from config.config import DB_CONFIG
            print(f"✓ Configuración encontrada")
            print(f"  Host: {DB_CONFIG.get('host', 'localhost')}")
            print(f"  Database: {DB_CONFIG.get('database', 'eventos_locales')}")
            
            # Intentar conexión
            conn = mysql.connector.connect(**DB_CONFIG)
            if conn.is_connected():
                print("✓ Conexión a MySQL exitosa")
                conn.close()
                return True
            else:
                print("✗ No se pudo conectar a MySQL")
                return False
        except FileNotFoundError:
            print("⚠ Archivo config/config.py no encontrado")
            print("  Crea el archivo .env o configura config.py")
            return False
        except Exception as e:
            print(f"⚠ Error al conectar: {str(e)}")
            print("  Verifica que MySQL esté corriendo y las credenciales sean correctas")
            return False
            
    except ImportError:
        print("✗ mysql-connector-python no instalado")
        return False

def verificar_estructura():
    """Verifica que la estructura del proyecto esté completa"""
    print("\n" + "=" * 50)
    print("VERIFICACIÓN DE ESTRUCTURA DEL PROYECTO")
    print("=" * 50)
    
    import os
    
    archivos_importantes = [
        'src/main.py',
        'src/views/main_window.py',
        'src/database/db_connection.py',
        'config/config.py',
        'database/schema.sql',
        'requirements.txt'
    ]
    
    todos_ok = True
    for archivo in archivos_importantes:
        if os.path.exists(archivo):
            print(f"✓ {archivo}")
        else:
            print(f"✗ {archivo} NO encontrado")
            todos_ok = False
    
    return todos_ok

def main():
    """Función principal"""
    resultados = []
    
    resultados.append(("Python", verificar_python()))
    resultados.append(("pip", verificar_pip()))
    resultados.append(("Estructura", verificar_estructura()))
    resultados.append(("Dependencias", verificar_dependencias()))
    resultados.append(("MySQL", verificar_mysql()))
    
    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN")
    print("=" * 50)
    
    ok = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    for nombre, resultado in resultados:
        estado = "✓ OK" if resultado else "✗ FALTA"
        print(f"{estado} - {nombre}")
    
    print(f"\n{ok}/{total} verificaciones pasadas")
    
    if ok == total:
        print("\n🎉 ¡Todo está listo! Puedes ejecutar: python src/main.py")
    else:
        print("\n⚠ Hay problemas que resolver. Revisa los mensajes arriba.")
        print("   Consulta INSTALACION_PYTHON.md para más ayuda.")

if __name__ == "__main__":
    main()

