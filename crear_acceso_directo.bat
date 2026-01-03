@echo off
REM Script para crear un acceso directo en el escritorio
REM Autor: Martin Peñalva Artázcoz

echo ========================================
echo Crear Acceso Directo en el Escritorio
echo ========================================
echo.

REM Obtener la ruta del script actual
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_PATH=%SCRIPT_DIR%src\main.py"
set "ICONO_PATH=%SCRIPT_DIR%icono.ico"
set "VBS_SCRIPT=%TEMP%\ejecutar_app.vbs"

REM Obtener la ruta del escritorio del usuario
for /f "tokens=2*" %%a in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop') do set DESKTOP=%%b

REM Nombre del acceso directo
set "NOMBRE=Gestor de Eventos Locales"

REM Crear el acceso directo usando PowerShell con ejecución silenciosa
echo Creando acceso directo en el escritorio...
echo.

REM Crear un script VBS temporal que se ejecutará
set "VBS_SCRIPT=%SCRIPT_DIR%ejecutar_app.vbs"
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo WshShell.Run "python ""%SCRIPT_PATH%""", 0, False
echo Set WshShell = Nothing
) > "%VBS_SCRIPT%"

REM Crear el acceso directo que ejecuta el VBS
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\%NOMBRE%.lnk'); $Shortcut.TargetPath = 'wscript.exe'; $Shortcut.Arguments = '//B \"%VBS_SCRIPT%\"'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'Gestor de Eventos Locales - Aplicacion de escritorio'; if (Test-Path '%ICONO_PATH%') { $Shortcut.IconLocation = '%ICONO_PATH%'; }; $Shortcut.Save(); Write-Host 'Acceso directo creado exitosamente!'"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Acceso directo creado exitosamente!
    echo ========================================
    echo.
    echo El acceso directo "%NOMBRE%" ha sido creado en tu escritorio.
    echo Puedes hacer doble clic en el para ejecutar la aplicacion.
    echo.
) else (
    echo.
    echo ========================================
    echo Error al crear el acceso directo
    echo ========================================
    echo.
    echo Intenta ejecutar este script como Administrador.
    echo.
)

pause

