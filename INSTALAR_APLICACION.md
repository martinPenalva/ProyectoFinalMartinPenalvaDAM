# Instalar la Aplicación en el Escritorio

## 🖥️ Opción 1: Crear Acceso Directo (Recomendado)

### Método A: Usando el script .bat

1. **Haz doble clic** en `crear_acceso_directo.bat`
2. El script creará automáticamente un acceso directo en tu escritorio
3. **Haz doble clic** en el acceso directo del escritorio para ejecutar la aplicación

### Método B: Usando PowerShell

1. **Abre PowerShell** (clic derecho → Ejecutar como administrador)
2. Navega a la carpeta del proyecto:
   ```powershell
   cd "C:\Users\Martin\Downloads\prueba-PP-master\prueba-PP-master"
   ```
3. Ejecuta el script:
   ```powershell
   .\crear_acceso_directo.ps1
   ```

### Método C: Manualmente

1. **Clic derecho** en el escritorio → **Nuevo** → **Acceso directo**
2. En "Ubicación del elemento", escribe:
   ```
   python "C:\Users\Martin\Downloads\prueba-PP-master\prueba-PP-master\src\main.py"
   ```
   (Ajusta la ruta según tu ubicación)
3. Haz clic en **Siguiente**
4. Nombre: `Gestor de Eventos Locales`
5. Haz clic en **Finalizar**
6. **Clic derecho** en el acceso directo → **Propiedades** → **Cambiar icono**
7. Selecciona el archivo `icono.ico` del proyecto

---

## 📦 Opción 2: Crear Ejecutable (.exe) con PyInstaller

Para crear un ejecutable independiente que no requiera Python instalado:

### Paso 1: Instalar PyInstaller

```bash
pip install pyinstaller
```

### Paso 2: Crear el ejecutable

```bash
cd "C:\Users\Martin\Downloads\prueba-PP-master\prueba-PP-master"
pyinstaller --onefile --windowed --icon=icono.ico --name="GestorEventos" src\main.py
```

### Paso 3: Encontrar el ejecutable

El ejecutable se creará en la carpeta `dist`:
```
dist\GestorEventos.exe
```

### Paso 4: Crear acceso directo

1. Copia `GestorEventos.exe` a donde quieras (por ejemplo, `C:\Program Files\GestorEventos\`)
2. Crea un acceso directo en el escritorio apuntando a ese .exe

---

## 🎯 Opción 3: Instalador Completo (Avanzado)

Para crear un instalador profesional con Inno Setup o NSIS:

### Con Inno Setup (Recomendado)

1. Descarga Inno Setup: https://jrsoftware.org/isdl.php
2. Crea un script de instalación que:
   - Copie los archivos necesarios
   - Cree un acceso directo en el escritorio
   - Agregue entrada en el menú Inicio
   - Configure el icono

### Con NSIS

1. Descarga NSIS: https://nsis.sourceforge.io/Download
2. Crea un script .nsi para generar el instalador

---

## ✅ Verificación

Después de crear el acceso directo:

1. ✅ Debe aparecer en tu escritorio
2. ✅ Debe tener el icono de la aplicación
3. ✅ Al hacer doble clic, debe abrir la aplicación
4. ✅ El icono debe aparecer en la barra de tareas cuando la aplicación está ejecutándose

---

## 🔧 Solución de Problemas

### El acceso directo no funciona

- Verifica que Python esté instalado y en el PATH
- Verifica que la ruta al script sea correcta
- Intenta ejecutar el script directamente: `python src\main.py`

### El icono no aparece

- Verifica que el archivo `icono.ico` exista en la raíz del proyecto
- En las propiedades del acceso directo, verifica que el icono esté configurado

### Error de permisos

- Ejecuta el script como Administrador
- Verifica que tengas permisos para escribir en el escritorio

---

## 📝 Notas

- El acceso directo es la forma más simple y rápida
- El ejecutable (.exe) es mejor si quieres distribuir la aplicación sin requerir Python
- El instalador es la mejor opción para distribución profesional

