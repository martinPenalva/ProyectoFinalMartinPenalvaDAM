# Solución: Problema con el alias de Python

## 🔍 Problema Detectado

Windows tiene un alias en `C:\Users\d508363\AppData\Local\Microsoft\WindowsApps\python.exe` que redirige a Microsoft Store, y esto tiene prioridad sobre tu Python real.

## ✅ Soluciones

### Solución 1: Usar el script ejecutar.bat (MÁS FÁCIL)

He creado un archivo `ejecutar.bat` que usa la ruta completa de Python.

**Simplemente haz doble clic en `ejecutar.bat`** o ejecuta:
```powershell
.\ejecutar.bat
```

---

### Solución 2: Usar la ruta completa en PowerShell

```powershell
C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe src\main.py
```

---

### Solución 3: Crear un alias en PowerShell (RECOMENDADO)

Abre PowerShell y ejecuta:

```powershell
# Crear un alias permanente
function python { & "C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe" $args }
function pip { & "C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe" -m pip $args }

# Hacer permanente (agregar al perfil)
$profilePath = $PROFILE
if (-not (Test-Path $profilePath)) {
    New-Item -Path $profilePath -ItemType File -Force
}
Add-Content -Path $profilePath -Value "function python { & 'C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe' `$args }"
Add-Content -Path $profilePath -Value "function pip { & 'C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe' -m pip `$args }"
```

Después de esto, reinicia PowerShell y `python` funcionará correctamente.

---

### Solución 4: Arreglar el PATH (DEFINITIVO)

1. **Presiona `Win + R`**
2. **Escribe**: `sysdm.cpl` y presiona Enter
3. **Ve a la pestaña "Opciones avanzadas"**
4. **Haz clic en "Variables de entorno"**
5. **En "Variables del sistema", busca "Path"**
6. **Haz clic en "Editar"**
7. **Busca esta línea y elimínala:**
   ```
   C:\Users\d508363\AppData\Local\Microsoft\WindowsApps
   ```
   (O muévela al final de la lista)
8. **Asegúrate de que estas líneas estén al INICIO:**
   ```
   C:\Users\d508363\AppData\Local\Programs\Python\Python314\
   C:\Users\d508363\AppData\Local\Programs\Python\Python314\Scripts\
   ```
   (Si no están, agrégalas)
9. **Haz clic en "Aceptar" en todas las ventanas**
10. **Cierra y vuelve a abrir PowerShell**

---

## 🚀 Ejecutar la Aplicación Ahora

### Opción A: Usar el script (MÁS FÁCIL)
```powershell
.\ejecutar.bat
```

### Opción B: Usar la ruta completa
```powershell
C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe src\main.py
```

### Opción C: Después de arreglar el PATH
```powershell
python src\main.py
```

---

## 📝 Nota

Las dependencias ya están instaladas correctamente. Solo necesitas ejecutar la aplicación usando una de las opciones arriba.

