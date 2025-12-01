@echo off
REM Script para ejecutar sin mostrar errores de MySQL
REM Detecta automáticamente la ruta de Python

echo Ejecutando aplicación...
echo.

REM Redirigir stderr para ocultar errores de MySQL
python src\main.py 2>nul
if errorlevel 1 (
    echo Intentando con 'py'...
    py src\main.py 2>nul
)

pause

