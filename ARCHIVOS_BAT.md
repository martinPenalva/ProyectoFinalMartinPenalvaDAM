# Archivos .bat - ¿Cuáles son necesarios?

## 📋 Archivos .bat en el proyecto

### 1. `crear_acceso_directo.bat` ⭐ **ESENCIAL**
- **Función**: Crea el acceso directo en el escritorio
- **Cuándo usarlo**: Cuando quieras crear o recrear el acceso directo
- **¿Necesario?**: SÍ, es el único realmente necesario si ya tienes el acceso directo

### 2. `crear_ejecutable.bat` 🔧 **OPCIONAL**
- **Función**: Crea un ejecutable .exe de la aplicación
- **Cuándo usarlo**: Si quieres crear un .exe para distribuir la aplicación
- **¿Necesario?**: NO, solo si quieres crear un ejecutable

### 3. `ejecutar.bat` ❌ **REDUNDANTE**
- **Función**: Ejecuta la aplicación mostrando la ventana de CMD
- **Cuándo usarlo**: Para desarrollo/debug (muestra errores en consola)
- **¿Necesario?**: NO, el acceso directo ya hace esto mejor (sin CMD)

### 4. `ejecutar_sin_cmd.bat` ❌ **REDUNDANTE**
- **Función**: Ejecuta la aplicación sin mostrar CMD
- **Cuándo usarlo**: Similar al acceso directo pero desde la carpeta
- **¿Necesario?**: NO, el acceso directo ya hace esto

## ✅ Recomendación

**Si ya tienes el acceso directo funcionando:**
- ✅ Mantener: `crear_acceso_directo.bat` (por si necesitas recrearlo)
- ✅ Mantener: `crear_ejecutable.bat` (opcional, solo si quieres crear .exe)
- ❌ Eliminar: `ejecutar.bat` (redundante)
- ❌ Eliminar: `ejecutar_sin_cmd.bat` (redundante)

**Resultado**: Solo necesitas 1-2 archivos .bat en lugar de 4.

