@echo off
REM Script para crear un ejecutable .exe de la aplicación
REM Requiere PyInstaller instalado: pip install pyinstaller

echo ========================================
echo Crear Ejecutable de la Aplicacion
echo ========================================
echo.

REM Verificar si PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller no esta instalado.
    echo.
    echo Instalando PyInstaller...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo Error al instalar PyInstaller.
        pause
        exit /b 1
    )
)

echo.
echo Creando ejecutable...
echo Esto puede tardar unos minutos...
echo.

REM Obtener la ruta del script actual
set "SCRIPT_DIR=%~dp0"
set "ICONO=%SCRIPT_DIR%icono.ico"

REM Crear el ejecutable
pyinstaller --onefile --windowed --icon="%ICONO%" --name="GestorEventos" --add-data "config;config" --add-data "src;src" --hidden-import=mysql.connector --hidden-import=reportlab --hidden-import=bcrypt src\main.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Ejecutable creado exitosamente!
    echo ========================================
    echo.
    echo El ejecutable se encuentra en: dist\GestorEventos.exe
    echo.
    echo Puedes copiar este archivo a donde quieras y ejecutarlo directamente.
    echo.
) else (
    echo.
    echo ========================================
    echo Error al crear el ejecutable
    echo ========================================
    echo.
)

pause

