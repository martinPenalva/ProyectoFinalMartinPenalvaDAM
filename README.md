# Gestor de Eventos Locales

Aplicación de escritorio desarrollada en Python para la gestión centralizada de eventos y participantes, con interfaz gráfica y base de datos MySQL.

## Características

- ✅ CRUD completo de eventos
- ✅ CRUD completo de participantes
- ✅ Asignación de participantes a eventos
- ✅ Búsqueda y filtrado avanzado
- ✅ Exportación a CSV y PDF
- ✅ **Soporte para múltiples usuarios simultáneos**: La aplicación permite que varios usuarios accedan y trabajen al mismo tiempo sin conflictos
- ✅ **Gestión avanzada de concurrencia**: 
  - Control de versiones optimista con locks de recursos
  - Bloqueos transaccionales (SELECT FOR UPDATE)
  - Sistema de locks por recurso (ResourceLockManager)
  - Procesamiento paralelo de suscripciones con worker threads
  - Reintentos automáticos con backoff exponencial
  - Sistema de notificaciones de eventos asíncronas
- ✅ Pool de conexiones configurable para optimizar el rendimiento con múltiples usuarios
- ✅ Interfaz gráfica intuitiva con Tkinter

## Requisitos

- Python 3.8 o superior
- MySQL Server 8.0 o superior
- Windows (desarrollado para Windows, compatible con otros SO)

## Instalación

1. Clonar el repositorio o descargar el proyecto
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configurar la base de datos:
   - Crear una base de datos MySQL
   - Ejecutar los scripts SQL en `database/schema.sql`
   - Configurar las credenciales en `config/config.py` o `.env`

## Uso

Ejecutar la aplicación:
```bash
python src/main.py
```

### Múltiples Usuarios Simultáneos

La aplicación está diseñada para soportar múltiples usuarios trabajando simultáneamente:

- **Cada usuario ejecuta su propia instancia** de la aplicación en su ordenador
- **Pool de conexiones compartido**: Todas las instancias comparten un pool de conexiones a la base de datos (configurable, por defecto 20 conexiones)
- **Control de concurrencia avanzado**: 
  - Control de versiones optimista con locks de recursos para evitar conflictos al editar eventos
  - Bloqueos transaccionales (`SELECT FOR UPDATE`) para prevenir condiciones de carrera en inscripciones
  - Sistema de locks por recurso (ResourceLockManager) para sincronización granular
  - Procesamiento paralelo de suscripciones usando worker threads y colas thread-safe
  - Reintentos automáticos con backoff exponencial para operaciones críticas
  - Sistema de notificaciones de eventos asíncronas (EventNotificationSystem)
  - Nivel de aislamiento `REPEATABLE READ` para garantizar consistencia de datos

**Nota**: Para un uso óptimo con muchos usuarios simultáneos, asegúrate de que MySQL Server tenga suficientes recursos y considera ajustar el tamaño del pool en `config/config.py` según tus necesidades.

## Estructura del Proyecto

```
PYTHON/
├── src/                    # Código fuente principal
│   ├── main.py            # Punto de entrada
│   ├── models/            # Modelos de datos
│   ├── views/             # Interfaz gráfica (Tkinter)
│   ├── controllers/       # Lógica de negocio
│   ├── database/          # Conexión y operaciones DB
│   └── utils/             # Utilidades (exportación, validación)
├── database/              # Scripts SQL
│   ├── schema.sql         # Esquema de la base de datos
│   └── seed.sql           # Datos de ejemplo (opcional)
├── tests/                 # Pruebas unitarias
├── config/                # Archivos de configuración
├── exports/               # Carpeta para archivos exportados
├── docs/                  # Documentación adicional
├── requirements.txt       # Dependencias Python
├── .gitignore
└── README.md
```

## Autor

Martin Peñalva Artázcoz - 2º DAM

## Licencia

Proyecto académico

