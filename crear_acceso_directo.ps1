# Script PowerShell para crear un acceso directo en el escritorio
# Autor: Martin Peñalva Artázcoz

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Crear Acceso Directo en el Escritorio" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Obtener la ruta del script actual
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $scriptDir "src\main.py"
$iconoPath = Join-Path $scriptDir "icono.ico"

# Obtener la ruta del escritorio
$desktop = [Environment]::GetFolderPath("Desktop")
$nombre = "Gestor de Eventos Locales"
$rutaAccesoDirecto = Join-Path $desktop "$nombre.lnk"

Write-Host "Creando acceso directo..." -ForegroundColor Yellow
Write-Host ""

try {
    # Crear script VBS que ejecuta Python sin mostrar CMD
    $vbsScript = Join-Path $scriptDir "ejecutar_app.vbs"
    $vbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "python `"$scriptPath`"", 0, False
Set WshShell = Nothing
"@
    $vbsContent | Out-File -FilePath $vbsScript -Encoding ASCII
    
    # Crear el acceso directo que ejecuta el VBS
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($rutaAccesoDirecto)
    $Shortcut.TargetPath = "wscript.exe"
    $Shortcut.Arguments = "//B `"$vbsScript`""
    $Shortcut.WorkingDirectory = $scriptDir
    $Shortcut.Description = "Gestor de Eventos Locales - Aplicación de escritorio"
    
    # Agregar icono si existe
    if (Test-Path $iconoPath) {
        $Shortcut.IconLocation = $iconoPath
    }
    
    $Shortcut.Save()
    
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Acceso directo creado exitosamente!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "El acceso directo '$nombre' ha sido creado en tu escritorio." -ForegroundColor White
    Write-Host "Puedes hacer doble clic en él para ejecutar la aplicación." -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Error al crear el acceso directo" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Intenta ejecutar este script como Administrador." -ForegroundColor Yellow
    Write-Host ""
}

Read-Host "Presiona Enter para salir"

