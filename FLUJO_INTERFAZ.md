# Flujo de Interfaces al Ejecutar main.py

## 🚀 Al ejecutar `src/main.py`

### Paso 1: Ventana de Login (PRIMERA)
- **Archivo**: `src/views/login_window.py`
- **Diseño**: Basado en `diseno_login.html`
- **Qué verás**:
  - Panel izquierdo azul con información
  - Panel derecho blanco con formulario de login
  - Campo "Usuario"
  - Campo "Contraseña"
  - Botón "Entrar"
  - Botón "Registrarse"

### Paso 2: Después de hacer login
- Escribe cualquier usuario y contraseña (ej: `admin` / `admin123`)
- Haz clic en "Entrar"

### Paso 3: Ventana Principal (SEGUNDA)
- **Archivo**: `src/views/main_window.py`
- **Diseño**: Basado en `diseno_inicio.html`
- **Qué verás**:
  - **Header azul** (barra superior) con:
    - "Gestor de Eventos Locales" (izquierda)
    - "Usuario: [tu nombre]" (derecha)
  
  - **Sidebar oscuro** (menú lateral izquierdo) con:
    - 🏠 Inicio
    - 📅 Eventos
    - 👤 Participantes
    - 📝 Inscripciones
    - 📊 Reportes
    - ⚙️ Usuarios
  
  - **Contenido principal** (área derecha) mostrando:
    - Vista de Inicio por defecto con:
      - Título "Resumen general"
      - 3 cards blancas con estadísticas
      - Panel con tabla de "Próximos eventos"

## 📋 Resumen del Flujo

```
Ejecutar main.py
    ↓
Ventana de LOGIN (login_window.py)
    ↓
[Escribes usuario/contraseña y haces clic en "Entrar"]
    ↓
Ventana PRINCIPAL (main_window.py)
    ├── Header azul
    ├── Sidebar con menú
    └── Contenido (vista de inicio por defecto)
```

## 🎯 Vistas Disponibles

Desde la ventana principal, puedes hacer clic en el menú lateral para ver:

1. **🏠 Inicio** → Vista de resumen (cards + tabla de eventos)
2. **📅 Eventos** → `event_view.py` → Tabla de eventos con CRUD
3. **👤 Participantes** → `participant_view.py` → Tabla de participantes con CRUD
4. **📝 Inscripciones** → (pendiente)
5. **📊 Reportes** → (pendiente)
6. **⚙️ Usuarios** → (pendiente)

## ⚠️ Nota sobre Modo Demo

Si no tienes MySQL instalado:
- Verás un mensaje de advertencia sobre "Modo Demo"
- Puedes cerrarlo y continuar
- La interfaz se mostrará completa
- No podrás guardar datos (pero puedes ver todo el diseño)

## 🎨 Diseños Implementados

- ✅ Login → `diseno_login.html`
- ✅ Inicio → `diseno_inicio.html`
- ✅ Eventos → `diseno_eventos.html`
- ✅ Participantes → `diseno_participantes.html`

