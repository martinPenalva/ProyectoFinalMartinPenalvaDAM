# Solución: Python no funciona

## 🔍 Problema Detectado

El comando `python` no se reconoce. Esto significa que:
- Python no está instalado, O
- Python no está en el PATH del sistema

## ✅ Soluciones

### Solución 1: Verificar si Python está instalado

1. **Busca Python en el menú de inicio:**
   - Presiona `Win` (tecla Windows)
   - Escribe: `Python`
   - ¿Aparece "Python 3.x" o "IDLE"?

2. **Si aparece:**
   - Python está instalado pero no está en el PATH
   - Ve a la **Solución 2**

3. **Si NO aparece:**
   - Python no está instalado
   - Ve a la **Solución 3**

---

### Solución 2: Agregar Python al PATH (si está instalado)

1. **Encuentra dónde está Python:**
   - Busca en: `C:\Users\d508363\AppData\Local\Programs\Python\`
   - O en: `C:\Python3x\`
   - O busca "python.exe" en el explorador de archivos

2. **Agregar al PATH:**
   - Presiona `Win + R`
   - Escribe: `sysdm.cpl`
   - Presiona Enter
   - Ve a la pestaña **"Opciones avanzadas"**
   - Haz clic en **"Variables de entorno"**
   - En "Variables del sistema", busca **"Path"**
   - Haz clic en **"Editar"**
   - Haz clic en **"Nuevo"**
   - Agrega la ruta donde está Python (ej: `C:\Users\d508363\AppData\Local\Programs\Python\Python312\`)
   - También agrega la carpeta `Scripts` (ej: `C:\Users\d508363\AppData\Local\Programs\Python\Python312\Scripts\`)
   - Haz clic en **"Aceptar"** en todas las ventanas
   - **Cierra y vuelve a abrir PowerShell**

3. **Verificar:**
   ```powershell
   python --version
   ```

---

### Solución 3: Reinstalar Python correctamente

1. **Desinstala Python** (si está instalado):
   - Panel de Control → Programas → Desinstalar
   - Busca "Python" y desinstálalo

2. **Descarga Python nuevamente:**
   - Ve a: https://www.python.org/downloads/
   - Descarga Python 3.12.x (Windows installer 64-bit)

3. **Instala CORRECTAMENTE:**
   - Ejecuta el instalador
   - **MUY IMPORTANTE**: Marca la casilla **"Add Python to PATH"** ✅
   - Haz clic en "Install Now"
   - Espera a que termine

4. **Verificar:**
   - Cierra y vuelve a abrir PowerShell
   - Ejecuta: `python --version`

---

### Solución 4: Usar la ruta completa de Python

Si Python está instalado pero no funciona el comando, puedes usar la ruta completa:

1. **Encuentra python.exe:**
   - Busca "python.exe" en el explorador de archivos
   - La ruta típica es: `C:\Users\d508363\AppData\Local\Programs\Python\Python312\python.exe`

2. **Ejecuta con la ruta completa:**
   ```powershell
   C:\Users\d508363\AppData\Local\Programs\Python\Python312\python.exe src/main.py
   ```

   (Ajusta la ruta según donde esté tu Python)

---

### Solución 5: Usar Python desde Microsoft Store

1. Abre **Microsoft Store**
2. Busca: **"Python 3.12"**
3. Haz clic en **"Instalar"**
4. Una vez instalado, cierra y vuelve a abrir PowerShell
5. Ejecuta: `python --version`

---

## 🔧 Verificación Rápida

Ejecuta estos comandos en PowerShell para diagnosticar:

```powershell
# Verificar si python está en alguna ubicación
where.exe python

# Verificar variables de entorno
$env:PATH

# Buscar python.exe
Get-ChildItem -Path C:\Users\d508363\AppData\Local\Programs\ -Filter python.exe -Recurse -ErrorAction SilentlyContinue
```

---

## 📝 Comandos Alternativos

Si `python` no funciona, prueba:

```powershell
# En Windows, a veces funciona:
py src/main.py

# O con la ruta completa:
& "C:\Users\d508363\AppData\Local\Programs\Python\Python312\python.exe" src/main.py
```

---

## ✅ Una vez que funcione Python

Después de solucionar el problema, ejecuta:

```powershell
# Verificar versión
python --version

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python src/main.py
```

---

## 🆘 Si nada funciona

1. **Reinstala Python** desde cero
2. **Asegúrate de marcar "Add Python to PATH"** durante la instalación
3. **Reinicia el ordenador** después de instalar
4. **Abre PowerShell como administrador** y prueba de nuevo

