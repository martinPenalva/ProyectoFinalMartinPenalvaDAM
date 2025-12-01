# Instalación Rápida de Python - Guía Visual

## 📥 Paso 1: Descargar

En la página de Python que estás viendo:

1. **Busca la sección "Files"** (más abajo en la página)
2. **Encuentra "Windows installer (64-bit)"** - dice "Recommended"
3. **Haz clic** en ese enlace
4. Se descargará un archivo como: `python-3.14.0-amd64.exe`

## 🔧 Paso 2: Instalar

1. **Abre el archivo** que acabas de descargar (estará en tu carpeta de Descargas)
2. **IMPORTANTE**: En la primera pantalla, marca la casilla:
   ```
   ☑ Add Python to PATH
   ```
   (Está abajo, en la parte inferior de la ventana)
3. Haz clic en **"Install Now"**
4. Espera a que termine (puede tardar 2-5 minutos)
5. Cuando termine, verás "Setup was successful"
6. Haz clic en **"Close"**

## ✅ Paso 3: Verificar

1. Abre **PowerShell**:
   - Presiona `Win + R`
   - Escribe: `powershell`
   - Presiona Enter

2. Escribe y presiona Enter:
   ```powershell
   python --version
   ```

3. Deberías ver:
   ```
   Python 3.14.0
   ```

## 🎯 Paso 4: Instalar Dependencias del Proyecto

1. En PowerShell, ve a tu carpeta del proyecto:
   ```powershell
   cd C:\Users\d508363\Documents\Martin\PYTHON
   ```

2. Instala las librerías necesarias:
   ```powershell
   pip install -r requirements.txt
   ```

3. Esto instalará:
   - mysql-connector-python
   - pandas
   - reportlab
   - python-dotenv
   - Y otras dependencias

## 🚀 Paso 5: Ejecutar la Aplicación

```powershell
python src/main.py
```

## ⚠️ Si Prefieres una Versión Más Estable

Python 3.14 es muy nuevo. Si prefieres algo más probado:

1. Ve a: https://www.python.org/downloads/
2. Haz scroll hacia abajo
3. Busca "Looking for a specific release?"
4. Haz clic en **"Python 3.12.x"** o **"Python 3.13.x"**
5. Descarga el instalador de Windows (64-bit)
6. Sigue los mismos pasos de instalación

## ❓ Problemas Comunes

### "python no se reconoce como comando"
- **Solución**: Reinstala Python y asegúrate de marcar "Add Python to PATH"
- O reinicia PowerShell después de instalar

### Error al ejecutar pip
- Ejecuta: `python -m pip install -r requirements.txt`

### Necesitas permisos de administrador
- Haz clic derecho en el instalador → "Ejecutar como administrador"

