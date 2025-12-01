# Script de diagnóstico de Python
# Ejecuta: .\diagnostico_python.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DIAGNÓSTICO DE PYTHON" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar comando python
Write-Host "1. Verificando comando 'python'..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ 'python' no funciona" -ForegroundColor Red
}

# 2. Verificar comando py
Write-Host "2. Verificando comando 'py'..." -ForegroundColor Yellow
try {
    $pyVersion = py --version 2>&1
    Write-Host "   ✓ py encontrado: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ 'py' no funciona" -ForegroundColor Red
}

# 3. Buscar python.exe
Write-Host "3. Buscando python.exe..." -ForegroundColor Yellow
$pythonPaths = @(
    "$env:LOCALAPPDATA\Programs\Python",
    "C:\Python*",
    "$env:PROGRAMFILES\Python*",
    "$env:PROGRAMFILES(X86)\Python*"
)

$found = $false
foreach ($path in $pythonPaths) {
    $pythonExe = Get-ChildItem -Path $path -Filter python.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($pythonExe) {
        Write-Host "   ✓ Python encontrado en: $($pythonExe.FullName)" -ForegroundColor Green
        $found = $true
        break
    }
}

if (-not $found) {
    Write-Host "   ✗ No se encontró python.exe" -ForegroundColor Red
}

# 4. Verificar PATH
Write-Host "4. Verificando PATH..." -ForegroundColor Yellow
$pathEnv = $env:PATH -split ';'
$pythonInPath = $pathEnv | Where-Object { $_ -like '*Python*' }
if ($pythonInPath) {
    Write-Host "   ✓ Python encontrado en PATH:" -ForegroundColor Green
    foreach ($path in $pythonInPath) {
        Write-Host "     - $path" -ForegroundColor Gray
    }
} else {
    Write-Host "   ✗ Python NO está en PATH" -ForegroundColor Red
}

# 5. Verificar pip
Write-Host "5. Verificando pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "   ✓ pip encontrado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ pip no funciona" -ForegroundColor Red
}

# 6. Verificar where.exe
Write-Host "6. Buscando python con where.exe..." -ForegroundColor Yellow
try {
    $wherePython = where.exe python 2>&1
    if ($wherePython -and $wherePython -notlike '*no se encontró*') {
        Write-Host "   ✓ Python encontrado:" -ForegroundColor Green
        Write-Host "     $wherePython" -ForegroundColor Gray
    } else {
        Write-Host "   ✗ where.exe no encuentra python" -ForegroundColor Red
    }
} catch {
    Write-Host "   ✗ Error al buscar python" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RECOMENDACIONES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not $found) {
    Write-Host "⚠ Python no está instalado o no se encuentra" -ForegroundColor Yellow
    Write-Host "  Solución: Instala Python desde https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "  IMPORTANTE: Marca 'Add Python to PATH' durante la instalación" -ForegroundColor White
} elseif ($pythonInPath.Count -eq 0) {
    Write-Host "⚠ Python está instalado pero NO está en PATH" -ForegroundColor Yellow
    Write-Host "  Solución 1: Reinstala Python y marca 'Add Python to PATH'" -ForegroundColor White
    Write-Host "  Solución 2: Agrega Python manualmente al PATH (ver SOLUCION_ERROR_PYTHON.md)" -ForegroundColor White
} else {
    Write-Host "✓ Python parece estar instalado correctamente" -ForegroundColor Green
    Write-Host "  Si 'python' no funciona, prueba reiniciar PowerShell" -ForegroundColor White
}

Write-Host ""
Write-Host "Para más ayuda, consulta: SOLUCION_ERROR_PYTHON.md" -ForegroundColor Cyan

