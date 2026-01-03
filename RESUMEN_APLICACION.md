# Resumen de la Aplicación - Gestor de Eventos Locales

## 📋 Descripción General

**Gestor de Eventos Locales** es una aplicación de escritorio desarrollada en Python con Tkinter para la gestión centralizada de eventos y participantes. Permite gestionar eventos locales, registrar participantes, manejar inscripciones y generar reportes, todo con soporte para múltiples usuarios simultáneos.

---

## 🎯 Funcionalidades Principales

### 1. Gestión de Eventos
- **Crear eventos**: Título, descripción, ubicación, fechas, capacidad
- **Editar eventos**: Modificar todos los datos del evento
- **Eliminar eventos**: Con confirmación y eliminación en cascada de inscripciones
- **Buscar eventos**: Por título, descripción o ubicación
- **Estados**: Activo, Planificado, Finalizado, Cancelado
- **Control de capacidad**: Verificación automática de plazas disponibles

### 2. Gestión de Participantes
- **Crear participantes**: Nombre, apellidos, email, teléfono, DNI/NIE
- **Editar participantes**: Modificar datos personales
- **Eliminar participantes**: Con eliminación en cascada de inscripciones
- **Buscar participantes**: Por nombre, apellidos, email o DNI/NIE
- **Ver detalles**: Información completa y eventos inscritos

### 3. Gestión de Inscripciones
- **Inscribir participantes en eventos**: Asignación de participantes a eventos
- **Cancelar inscripciones**: Eliminar inscripciones existentes
- **Ver inscripciones**: Listado completo con filtros
- **Control de capacidad**: Previene sobre-inscripciones
- **Filtros avanzados**:
  - Por evento (todos los usuarios)
  - Por participante (solo ADMIN)

### 4. Gestión de Usuarios (Solo ADMIN)
- **Crear usuarios**: Con rol (admin/user)
- **Editar usuarios**: Modificar roles y contraseñas
- **Eliminar usuarios**: Gestión completa del sistema
- **Ver usuarios**: Listado de todos los usuarios del sistema

### 5. Reportes y Exportación
- **Exportar a CSV**: Datos de eventos, participantes e inscripciones
- **Exportar a PDF**: Reportes formateados con ReportLab
- **Filtros**: Exportar datos específicos según criterios

### 6. Sistema de Autenticación
- **Login seguro**: Con hash bcrypt de contraseñas
- **Registro de usuarios**: Creación de cuenta con perfil de participante
- **Roles**: Admin y Usuario normal
- **Modo Demo**: Funciona sin base de datos (solo visualización)

---

## 👥 Roles de Usuario

### 🔴 Administrador (ADMIN)
**Credenciales por defecto:**
- Usuario: `ADMIN`
- Contraseña: `ADMINISTRADOR`

**Permisos:**
- ✅ Acceso completo a todas las funcionalidades
- ✅ Crear, editar y eliminar eventos
- ✅ Crear, editar y eliminar participantes
- ✅ Gestionar inscripciones (asignar cualquier participante a cualquier evento)
- ✅ Gestionar usuarios del sistema
- ✅ Ver todas las inscripciones
- ✅ Filtrar inscripciones por evento y por participante
- ✅ Exportar reportes

### 🔵 Usuario Normal
**Permisos:**
- ✅ Ver eventos y participantes
- ✅ Inscribirse en eventos (solo puede elegir el evento, se auto-asocia con su participante)
- ✅ Ver solo sus propias inscripciones
- ✅ Cancelar sus propias inscripciones
- ❌ No puede crear/editar/eliminar eventos
- ❌ No puede crear/editar/eliminar participantes
- ❌ No puede gestionar usuarios
- ❌ No puede ver inscripciones de otros usuarios

**Nota**: El usuario debe tener un perfil de participante asociado (buscado por email = username o email que contenga el username).

---

## 🏗️ Arquitectura y Estructura

### Patrón de Diseño: MVC (Model-View-Controller)

```
┌─────────────┐
│    Views    │  ← Interfaz gráfica (Tkinter)
│  (Tkinter)  │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Controllers │  ← Lógica de negocio
│  (CRUD)     │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Database   │  ← Pool de conexiones MySQL
│ Connection  │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   MySQL     │  ← Base de datos
│  Database   │
└─────────────┘
```

### Módulos Principales

#### 📁 Models (`src/models/`)
- **Event**: Modelo de datos para eventos
- **Participant**: Modelo de datos para participantes
- **User**: Modelo de datos para usuarios

#### 📁 Controllers (`src/controllers/`)
- **EventController**: CRUD completo de eventos + búsqueda
- **ParticipantController**: CRUD completo de participantes + búsqueda
- **RegistrationController**: Gestión de inscripciones (asignar/cancelar)
- **AuthController**: Autenticación y registro de usuarios
- **UserController**: Gestión de usuarios (solo admin)

#### 📁 Views (`src/views/`)
- **LoginWindow**: Ventana de inicio de sesión
- **RegisterWindow**: Ventana de registro de nuevos usuarios
- **MainWindow**: Ventana principal con menú lateral
- **EventView**: Vista completa de gestión de eventos
- **ParticipantView**: Vista completa de gestión de participantes
- **RegistrationView**: Vista de gestión de inscripciones
- **ReportsView**: Vista de reportes y exportación
- **UserView**: Vista de gestión de usuarios (solo admin)

#### 📁 Database (`src/database/`)
- **DatabaseConnection**: Singleton con pool de conexiones MySQL
  - Pool de 20 conexiones (configurable)
  - Thread-safe
  - Gestión automática de conexiones

#### 📁 Utils (`src/utils/`)
- **CSVExporter**: Exportación de datos a CSV
- **PDFExporter**: Exportación de datos a PDF
- **Validator**: Validaciones (email, DNI/NIE, teléfono)

---

## 🗄️ Base de Datos

### Esquema de Tablas

1. **users**
   - Almacena usuarios del sistema
   - Campos: user_id, username, password_hash, role, created_at
   - Roles: 'admin' o 'user'

2. **events**
   - Almacena eventos
   - Campos: event_id, title, description, location, start_datetime, end_datetime, capacity, status, version, created_at, updated_at
   - Estados: 'activo', 'planificado', 'finalizado', 'cancelado'
   - Control de versión para concurrencia

3. **participants**
   - Almacena participantes
   - Campos: participant_id, first_name, last_name, email, phone, identifier (DNI/NIE), created_at, updated_at
   - Email y DNI/NIE únicos

4. **event_registrations**
   - Relación N:M entre eventos y participantes (inscripciones)
   - Campos: registration_id, event_id, participant_id, registered_at, status
   - Restricción única: un participante solo puede inscribirse una vez por evento

5. **audit_logs**
   - Logs de auditoría (preparado para uso futuro)
   - Campos: log_id, user_id, action, entity, entity_id, details, timestamp

### Características de la Base de Datos
- ✅ Integridad referencial con FOREIGN KEYS
- ✅ Índices para optimizar búsquedas
- ✅ Control de concurrencia optimista (campo `version` en events)
- ✅ Eliminación en cascada de inscripciones al eliminar eventos/participantes
- ✅ Validaciones a nivel de base de datos (CHECK constraints)

---

## 🔒 Características de Seguridad y Concurrencia

### Soporte Multiusuario
- **Pool de conexiones**: 20 conexiones simultáneas (configurable)
- **Control de versión optimista**: Previene conflictos al editar eventos
- **Bloqueos transaccionales**: `SELECT FOR UPDATE` para inscripciones
- **Nivel de aislamiento**: `REPEATABLE READ` para transacciones críticas
- **Thread-safe**: Pool protegido con locks

### Seguridad
- **Contraseñas hasheadas**: bcrypt
- **Validación de datos**: Email, DNI/NIE, teléfono
- **Control de acceso**: Roles admin/user con permisos diferenciados

---

## 🎨 Interfaz de Usuario

### Diseño
- **Estilo moderno**: Basado en diseños HTML proporcionados
- **Colores**: Paleta azul oscuro (#1f4e79) y gris claro
- **Layout**: Menú lateral + área de contenido
- **Responsive**: Ventana redimensionable con tamaños mínimos

### Secciones Principales
1. **🏠 Inicio**: Resumen general con estadísticas y próximos eventos
2. **📅 Eventos**: Gestión completa de eventos (CRUD)
3. **👤 Participantes**: Gestión completa de participantes (CRUD)
4. **📝 Inscripciones**: Gestión de inscripciones con filtros
5. **📊 Reportes**: Exportación de datos a CSV/PDF
6. **⚙️ Usuarios**: Gestión de usuarios (solo admin)

---

## 🚀 Modo de Funcionamiento

### Modo Normal (con MySQL)
- Conexión a base de datos MySQL
- Todas las funcionalidades disponibles
- Datos persistentes
- Soporte multiusuario completo

### Modo Demo (sin MySQL)
- Funciona sin conexión a base de datos
- Interfaz completa visible
- No se guardan datos
- Útil para demostraciones o cuando MySQL no está disponible

---

## 📊 Flujo de Trabajo Típico

### Para un Administrador:
1. Iniciar sesión con credenciales de admin
2. Crear eventos con toda su información
3. Crear participantes o esperar a que se registren
4. Asignar participantes a eventos (inscripciones)
5. Ver reportes y exportar datos
6. Gestionar usuarios del sistema

### Para un Usuario Normal:
1. Registrarse o iniciar sesión
2. Ver eventos disponibles
3. Inscribirse en eventos de su interés
4. Ver sus inscripciones
5. Cancelar inscripciones si es necesario

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **Tkinter**: Interfaz gráfica
- **MySQL**: Base de datos relacional
- **mysql-connector-python**: Conector a MySQL
- **bcrypt**: Hash de contraseñas
- **ReportLab**: Generación de PDFs
- **pandas**: Procesamiento de datos (exportación CSV)

---

## 📝 Características Destacadas

1. ✅ **Soporte multiusuario real**: Múltiples usuarios pueden trabajar simultáneamente
2. ✅ **Control de concurrencia**: Previene conflictos y condiciones de carrera
3. ✅ **Interfaz intuitiva**: Diseño moderno y fácil de usar
4. ✅ **Validaciones robustas**: A nivel de aplicación y base de datos
5. ✅ **Exportación de datos**: CSV y PDF para análisis externos
6. ✅ **Modo Demo**: Funciona sin base de datos para demostraciones
7. ✅ **Seguridad**: Contraseñas hasheadas y control de acceso por roles
8. ✅ **Escalable**: Pool de conexiones configurable según necesidades

---

## 📌 Notas Importantes

- **Usuario por defecto**: ADMIN / ADMINISTRADOR
- **Base de datos**: `eventos_locales` (MySQL)
- **Puerto MySQL**: 3309 (configurable)
- **Pool de conexiones**: 20 conexiones por defecto
- **Formato de exportación**: CSV (UTF-8 con BOM) y PDF

---

**Autor**: Martin Peñalva Artázcoz - 2º DAM  
**Proyecto**: Gestor de Eventos Locales  
**Versión**: 1.0.0

