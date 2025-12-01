# Gestor de Eventos Locales

Aplicación de escritorio desarrollada en Python para la gestión centralizada de eventos y participantes, con interfaz gráfica y base de datos MySQL.

## Características

- ✅ CRUD completo de eventos
- ✅ CRUD completo de participantes
- ✅ Asignación de participantes a eventos
- ✅ Búsqueda y filtrado avanzado
- ✅ Exportación a CSV y PDF
- ✅ Gestión de concurrencia multiusuario
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

