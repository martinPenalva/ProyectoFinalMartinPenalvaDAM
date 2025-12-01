@echo off
REM Script para ejecutar la aplicación y ver errores en consola
REM Los errores se mostrarán aquí y no se cerrará la ventana
REM Detecta automáticamente la ruta de Python

echo ========================================
echo Ejecutando Gestor de Eventos Locales...
echo ========================================
echo.
echo Revisa los mensajes de error abajo:
echo.

python src\main.py
if errorlevel 1 (
    echo Intentando con 'py'...
    py src\main.py
)

echo.
echo ========================================
echo La aplicación se cerró.
echo ========================================
pause

