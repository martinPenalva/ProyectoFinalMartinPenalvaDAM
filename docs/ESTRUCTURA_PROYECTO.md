# Estructura del Proyecto - Gestor de Eventos Locales

## 📁 Estructura de Carpetas

```
PYTHON/
│
├── 📂 config/                    # Configuración de la aplicación
│   ├── config.py                 # Configuración principal (DB, APP, EXPORT)
│   └── .env.example              # Plantilla de variables de entorno
│
├── 📂 database/                   # Scripts SQL
│   ├── schema.sql                # Esquema completo de la base de datos
│   └── seed.sql                  # Datos de ejemplo para desarrollo
│
├── 📂 src/                       # Código fuente principal
│   ├── main.py                   # Punto de entrada de la aplicación
│   │
│   ├── 📂 models/                # Modelos de datos (POJOs)
│   │   ├── __init__.py
│   │   ├── event.py              # Modelo Event
│   │   └── participant.py        # Modelo Participant
│   │
│   ├── 📂 controllers/           # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── event_controller.py   # CRUD de eventos
│   │   ├── participant_controller.py  # CRUD de participantes
│   │   └── registration_controller.py # Gestión de inscripciones
│   │
│   ├── 📂 database/              # Conexión y operaciones DB
│   │   ├── __init__.py
│   │   └── db_connection.py      # Pool de conexiones MySQL
│   │
│   ├── 📂 views/                 # Interfaz gráfica (Tkinter)
│   │   ├── __init__.py
│   │   └── main_window.py        # Ventana principal
│   │
│   └── 📂 utils/                 # Utilidades
│       ├── __init__.py
│       ├── exporters.py          # Exportación CSV/PDF
│       └── validators.py         # Validación de datos
│
├── 📂 tests/                     # Pruebas unitarias
│   ├── __init__.py
│   └── test_event_controller.py  # Ejemplo de pruebas
│
├── 📂 exports/                   # Archivos exportados (CSV/PDF)
│   └── (se genera automáticamente)
│
├── 📂 docs/                      # Documentación adicional
│   └── ESTRUCTURA_PROYECTO.md    # Este archivo
│
├── requirements.txt              # Dependencias Python
├── .gitignore                    # Archivos a ignorar en Git
├── README.md                     # Documentación principal
└── documentacion.txt             # Memoria del proyecto

```

## 🔄 Flujo de Datos

```
Usuario (GUI)
    ↓
Views (main_window.py, event_view.py, etc.)
    ↓
Controllers (event_controller.py, participant_controller.py)
    ↓
Database (db_connection.py)
    ↓
MySQL Database
```

## 📦 Módulos Principales

### Models (`src/models/`)
- **Event**: Representa un evento con todos sus atributos
- **Participant**: Representa un participante con datos personales

### Controllers (`src/controllers/`)
- **EventController**: Operaciones CRUD de eventos + búsqueda
- **ParticipantController**: Operaciones CRUD de participantes + búsqueda
- **RegistrationController**: Gestión de inscripciones (asignar participantes a eventos)

### Database (`src/database/`)
- **DatabaseConnection**: Singleton con pool de conexiones MySQL
- Maneja la concurrencia mediante pool de conexiones

### Views (`src/views/`)
- **MainWindow**: Ventana principal con menú lateral
- (Pendiente: EventView, ParticipantView, ReportView)

### Utils (`src/utils/`)
- **CSVExporter**: Exporta datos a CSV
- **PDFExporter**: Exporta datos a PDF con ReportLab
- **Validator**: Validaciones de email, DNI/NIE, teléfono, etc.

## 🗄️ Base de Datos

### Tablas:
1. **events**: Eventos locales
2. **participants**: Participantes
3. **event_registrations**: Relación N:M (inscripciones)
4. **users**: Usuarios del sistema
5. **audit_logs**: Logs de auditoría

### Características:
- Control de concurrencia optimista (campo `version` en events)
- Integridad referencial con FOREIGN KEYS
- Índices para optimizar búsquedas

## 🚀 Próximos Pasos

1. Implementar vistas completas (EventView, ParticipantView)
2. Implementar formularios de creación/edición
3. Implementar sistema de login (si se requiere)
4. Completar pruebas unitarias
5. Implementar exportación completa
6. Mejorar manejo de errores y mensajes al usuario

