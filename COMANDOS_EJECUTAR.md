# Comandos para Ejecutar la Aplicación

## 🚀 OPCIÓN 1: Usar ejecutar.bat (MÁS FÁCIL)

Simplemente haz **doble clic** en el archivo:
```
ejecutar.bat
```

O desde PowerShell:
```powershell
.\ejecutar.bat
```

---

## 💻 OPCIÓN 2: Comando Completo en PowerShell

```powershell
C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe src\main.py
```

---

## 🔧 OPCIÓN 3: Deshabilitar el Alias de Windows Store

Si quieres que `python` funcione directamente:

### Paso 1: Abrir Configuración de Windows
1. Presiona `Win + I` (tecla Windows + I)
2. Ve a **"Aplicaciones"** → **"Ejecución de aplicaciones"**
3. O busca: **"Administrar alias de ejecución de aplicaciones"**

### Paso 2: Deshabilitar el alias
1. Busca **"python.exe"** o **"python"**
2. **Desactívalo** o **Elimínalo**

### Paso 3: Agregar Python al PATH
1. Presiona `Win + R`
2. Escribe: `sysdm.cpl` y presiona Enter
3. Ve a **"Opciones avanzadas"** → **"Variables de entorno"**
4. En **"Variables del sistema"**, busca **"Path"**
5. Haz clic en **"Editar"**
6. Haz clic en **"Nuevo"** y agrega:
   ```
   C:\Users\d508363\AppData\Local\Programs\Python\Python314\
   ```
7. Haz clic en **"Nuevo"** otra vez y agrega:
   ```
   C:\Users\d508363\AppData\Local\Programs\Python\Python314\Scripts\
   ```
8. Haz clic en **"Aceptar"** en todas las ventanas
9. **Cierra y vuelve a abrir PowerShell**

### Paso 4: Verificar
```powershell
python --version
```

Deberías ver: `Python 3.14.0`

---

## 📝 Crear un Alias en PowerShell (Temporal)

Abre PowerShell y ejecuta:

```powershell
function python { & "C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe" $args }
```

Esto solo funciona en esa sesión de PowerShell. Para hacerlo permanente:

```powershell
# Agregar al perfil de PowerShell
$profilePath = $PROFILE
if (-not (Test-Path $profilePath)) {
    New-Item -Path $profilePath -ItemType File -Force
}
Add-Content -Path $profilePath -Value "function python { & 'C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe' `$args }"
Add-Content -Path $profilePath -Value "function pip { & 'C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe' -m pip `$args }"
```

Después, reinicia PowerShell.

---

## ✅ RECOMENDACIÓN

**Usa `ejecutar.bat`** - Es lo más simple y siempre funciona.

---

## 🎯 Resumen Rápido

**Para ejecutar AHORA:**
```powershell
.\ejecutar.bat
```

**O:**
```powershell
C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe src\main.py
```

