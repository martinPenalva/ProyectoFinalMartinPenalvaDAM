# Debug: Ventana Vacía en Modo Demo

## 🔍 Problema
La ventana aparece vacía después del mensaje de advertencia sobre modo demo.

## ✅ Soluciones

### Paso 1: Verificar que Tkinter funciona

Ejecuta este script de prueba:

```powershell
C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe test_tkinter.py
```

Si ves una ventana con texto, Tkinter funciona correctamente.

### Paso 2: Ver errores en la consola

Cuando ejecutes la aplicación, revisa la consola de PowerShell. Deberías ver mensajes de error si hay algún problema.

### Paso 3: Verificar imports

Asegúrate de que todos los módulos se importen correctamente. El error puede estar en:

- `src/views/styles.py` - Colores
- `config/config.py` - Configuración
- Imports circulares

### Paso 4: Ejecutar con más información de debug

Modifica temporalmente `src/main.py` para ver más información:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Comando para ejecutar y ver errores

```powershell
C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe src\main.py 2>&1 | Tee-Object -FilePath error_log.txt
```

Esto guardará los errores en `error_log.txt`.

## 📝 Si la ventana sigue vacía

1. **Verifica la consola** - Debe haber mensajes de error
2. **Comparte los errores** - Cópialos y compártelos
3. **Prueba el test_tkinter.py** - Para verificar que Tkinter funciona

