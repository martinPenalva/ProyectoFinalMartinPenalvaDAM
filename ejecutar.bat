@echo off
REM Script para ejecutar la aplicación usando Python del sistema
REM Detecta automáticamente la ruta de Python

echo Ejecutando Gestor de Eventos Locales...
echo.

REM Intentar usar 'python' primero, si no funciona usar 'py'
python src\main.py
if errorlevel 1 (
    echo Intentando con 'py'...
    py src\main.py
)

pause

