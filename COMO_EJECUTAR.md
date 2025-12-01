# ¿Qué Archivo Ejecutar?

## ❌ NO ejecutes archivos de views directamente

Los archivos en `src/views/` son módulos que se importan, NO se ejecutan directamente.

## ✅ Archivo a ejecutar: `src/main.py`

Este es el **punto de entrada** de la aplicación. Es el único archivo que debes ejecutar.

## 🚀 Comandos para Ejecutar

### Opción 1: Usar ejecutar.bat (MÁS FÁCIL)
```powershell
.\ejecutar.bat
```

O simplemente haz **doble clic** en `ejecutar.bat`

### Opción 2: Comando completo
```powershell
C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe src\main.py
```

## 📁 Estructura de Archivos

```
src/
├── main.py              ← ⭐ ESTE ES EL QUE EJECUTAS
├── views/               ← Estos son módulos (NO se ejecutan)
│   ├── login_window.py
│   ├── main_window.py
│   ├── event_view.py
│   └── participant_view.py
├── controllers/        ← Módulos (NO se ejecutan)
├── models/             ← Módulos (NO se ejecutan)
└── database/           ← Módulos (NO se ejecutan)
```

## 🔄 Flujo de Ejecución

1. Ejecutas: `src/main.py`
2. `main.py` importa y usa:
   - `login_window.py` → Muestra la ventana de login
   - `main_window.py` → Muestra la ventana principal
   - `event_view.py` → Muestra la vista de eventos
   - `participant_view.py` → Muestra la vista de participantes

## ⚠️ Importante

- **NO ejecutes**: `python src/views/login_window.py` ❌
- **NO ejecutes**: `python src/views/main_window.py` ❌
- **SÍ ejecuta**: `python src/main.py` ✅

## 📝 Resumen

**Solo ejecuta:**
```powershell
.\ejecutar.bat
```

O:
```powershell
C:\Users\d508363\AppData\Local\Programs\Python\Python314\python.exe src\main.py
```

**Eso es todo. No necesitas ejecutar ningún otro archivo.**

