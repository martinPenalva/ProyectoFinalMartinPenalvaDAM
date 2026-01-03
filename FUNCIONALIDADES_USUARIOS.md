# Funcionalidades y Casos de Uso - Gestor de Eventos Locales

## 📋 Resumen Ejecutivo

El **Gestor de Eventos Locales** es una aplicación que permite gestionar eventos, participantes e inscripciones. Los usuarios pueden inscribirse en eventos y los administradores pueden gestionar todo el sistema.

---

## 👥 Tipos de Usuarios

### 🔴 ADMINISTRADOR (ADMIN)
**Usuario por defecto:** `ADMIN` / `ADMINISTRADOR`

### 🔵 USUARIO NORMAL
**Cualquier usuario registrado con rol 'user'**

---

## 🔴 FUNCIONALIDADES DEL ADMINISTRADOR

### 1. GESTIÓN DE EVENTOS

#### Crear Evento
- **Acción**: Clic en "Nuevo evento" en la sección Eventos
- **Datos requeridos**:
  - Título del evento
  - Descripción
  - Ubicación
  - Fecha y hora de inicio
  - Fecha y hora de fin
  - Capacidad (número máximo de participantes)
  - Estado (Activo, Planificado, Finalizado, Cancelado)
- **Resultado**: Evento creado y disponible para inscripciones

#### Editar Evento
- **Acción**: Seleccionar evento y clic en "Editar"
- **Puede modificar**: Todos los datos del evento
- **Protección**: Si otro usuario está editando el mismo evento, se detecta el conflicto
- **Resultado**: Evento actualizado

#### Eliminar Evento
- **Acción**: Seleccionar evento y clic en "Eliminar"
- **Confirmación**: Se solicita confirmación antes de eliminar
- **Efecto**: Se eliminan también todas las inscripciones asociadas
- **Resultado**: Evento eliminado permanentemente

#### Buscar Eventos
- **Acción**: Escribir en el campo de búsqueda
- **Busca en**: Título, descripción y ubicación
- **Resultado**: Lista filtrada de eventos que coinciden

#### Ver Detalles de Evento
- **Acción**: Doble clic en un evento o clic en "Ver"
- **Muestra**: Toda la información del evento y lista de participantes inscritos

---

### 2. GESTIÓN DE PARTICIPANTES

#### Crear Participante
- **Acción**: Clic en "Nuevo participante" en la sección Participantes
- **Datos requeridos**:
  - Nombre
  - Apellidos
  - Email (único)
  - Teléfono (opcional)
  - DNI/NIE (único, obligatorio)
- **Validaciones**: Email válido, DNI/NIE con formato correcto
- **Resultado**: Participante creado y disponible para inscripciones

#### Editar Participante
- **Acción**: Seleccionar participante y clic en "Editar"
- **Puede modificar**: Todos los datos excepto DNI/NIE (único)
- **Resultado**: Participante actualizado

#### Eliminar Participante
- **Acción**: Seleccionar participante y clic en "Eliminar"
- **Confirmación**: Se solicita confirmación
- **Efecto**: Se eliminan también todas sus inscripciones
- **Resultado**: Participante eliminado permanentemente

#### Buscar Participantes
- **Acción**: Escribir en el campo de búsqueda
- **Busca en**: Nombre, apellidos, email y DNI/NIE
- **Resultado**: Lista filtrada de participantes

#### Ver Detalles de Participante
- **Acción**: Clic en "Ver" o doble clic en un participante
- **Muestra**: 
  - Información personal completa
  - Lista de eventos en los que está inscrito
  - Número total de inscripciones

#### Ver Inscripciones de un Participante
- **Acción**: Seleccionar participante y clic en "Inscripciones"
- **Muestra**: Lista de todos los eventos en los que está inscrito
- **Acciones adicionales**: Puede agregar el participante a más eventos

---

### 3. GESTIÓN DE INSCRIPCIONES

#### Crear Inscripción (Asignar Participante a Evento)
- **Acción**: Clic en "Nueva Inscripción" en la sección Inscripciones
- **Proceso**:
  1. Seleccionar un evento de la lista
  2. Seleccionar un participante de la lista
  3. Confirmar
- **Validaciones**:
  - El evento debe tener plazas disponibles
  - El participante no puede estar ya inscrito en ese evento
- **Resultado**: Participante inscrito en el evento

#### Ver Todas las Inscripciones
- **Acción**: Ir a la sección Inscripciones
- **Muestra**: Lista completa de todas las inscripciones del sistema
- **Información mostrada**:
  - Evento
  - Participante (nombre y email)
  - Teléfono del participante
  - Fecha de inscripción
  - Estado (confirmado, etc.)

#### Filtrar Inscripciones
- **Por Evento**: Seleccionar un evento del filtro → Muestra todos los participantes de ese evento
- **Por Participante**: Seleccionar un participante del filtro → Muestra todos los eventos de ese participante
- **Combinado**: Puede usar ambos filtros a la vez

#### Eliminar Inscripción
- **Acción**: Clic en el botón "🗑️" en la fila de la inscripción
- **Confirmación**: Se solicita confirmación
- **Resultado**: Inscripción eliminada (el participante ya no está inscrito en ese evento)

---

### 4. GESTIÓN DE USUARIOS

#### Crear Usuario
- **Acción**: Clic en "Nuevo usuario" en la sección Usuarios
- **Datos requeridos**:
  - Nombre de usuario (único)
  - Contraseña
  - Rol (admin o user)
- **Resultado**: Nuevo usuario creado con acceso al sistema

#### Editar Usuario
- **Acción**: Seleccionar usuario y clic en "Editar"
- **Puede modificar**:
  - Rol del usuario
  - Contraseña (opcional)
- **Resultado**: Usuario actualizado

#### Eliminar Usuario
- **Acción**: Seleccionar usuario y clic en "Eliminar"
- **Confirmación**: Se solicita confirmación
- **Resultado**: Usuario eliminado (ya no puede acceder al sistema)

#### Ver Usuarios
- **Acción**: Ir a la sección Usuarios
- **Muestra**: Lista de todos los usuarios del sistema con sus roles

---

### 5. REPORTES Y EXPORTACIÓN

#### Exportar a CSV
- **Acción**: Ir a la sección Reportes
- **Opciones**:
  - Exportar eventos
  - Exportar participantes
  - Exportar inscripciones
- **Resultado**: Archivo CSV generado en la carpeta `exports/`
- **Formato**: UTF-8 con BOM (compatible con Excel)

#### Exportar a PDF
- **Acción**: Ir a la sección Reportes
- **Opciones**: Mismas que CSV
- **Resultado**: Archivo PDF generado con formato profesional
- **Incluye**: Datos formateados y tablas organizadas

---

## 🔵 FUNCIONALIDADES DEL USUARIO NORMAL

### 1. VER EVENTOS

#### Consultar Eventos Disponibles
- **Acción**: Ir a la sección Eventos
- **Puede ver**: 
  - Lista de todos los eventos
  - Detalles de cada evento (título, fecha, ubicación, capacidad)
  - Número de inscritos en cada evento
- **Limitación**: Solo lectura, no puede crear/editar/eliminar

#### Buscar Eventos
- **Acción**: Usar el campo de búsqueda en la sección Eventos
- **Funciona igual que**: La búsqueda del administrador

---

### 2. VER PARTICIPANTES

#### Consultar Participantes
- **Acción**: Ir a la sección Participantes
- **Puede ver**: Lista de participantes registrados
- **Limitación**: Solo lectura, no puede crear/editar/eliminar

---

### 3. GESTIÓN DE PROPIAS INSCRIPCIONES

#### Inscribirse en un Evento
- **Acción**: Ir a la sección Inscripciones → Clic en "Inscribirme en un Evento"
- **Proceso**:
  1. Se muestra automáticamente su información de participante
  2. Selecciona un evento de la lista (solo eventos activos)
  3. Confirma la inscripción
- **Validaciones**:
  - El evento debe tener plazas disponibles
  - No puede estar ya inscrito en ese evento
  - Debe tener un perfil de participante asociado a su usuario
- **Resultado**: Queda inscrito en el evento seleccionado

#### Ver Sus Inscripciones
- **Acción**: Ir a la sección Inscripciones
- **Muestra**: Solo sus propias inscripciones (no las de otros usuarios)
- **Información**: Eventos en los que está inscrito, fechas, estados

#### Cancelar Inscripción
- **Acción**: En la lista de inscripciones, clic en "❌ Cancelar" en una de sus inscripciones
- **Confirmación**: Se solicita confirmación
- **Limitación**: Solo puede cancelar sus propias inscripciones
- **Resultado**: Ya no está inscrito en ese evento

---

### 4. REGISTRO DE NUEVO USUARIO

#### Crear Cuenta
- **Acción**: En la ventana de login, clic en "Registrarse"
- **Datos requeridos**:
  - **Datos de Participante**:
    - Nombre
    - Apellidos
    - Email (se usará para asociar usuario con participante)
    - Teléfono (opcional)
    - DNI/NIE
  - **Datos de Usuario**:
    - Nombre de usuario
    - Contraseña
    - Confirmar contraseña
- **Resultado**: 
  - Usuario creado con rol 'user'
  - Participante creado y asociado automáticamente
  - Puede iniciar sesión inmediatamente

---

## 🔄 FLUJOS DE TRABAJO TÍPICOS

### Flujo 1: Administrador crea un evento y gestiona inscripciones

1. **Admin inicia sesión** → Ve la pantalla principal
2. **Va a "Eventos"** → Clic en "Nuevo evento"
3. **Completa los datos** del evento (título, fecha, capacidad, etc.)
4. **Guarda el evento** → El evento queda disponible
5. **Va a "Inscripciones"** → Clic en "Nueva Inscripción"
6. **Selecciona el evento** y un participante
7. **Confirma** → El participante queda inscrito
8. **Puede ver** todas las inscripciones en la tabla
9. **Puede filtrar** por evento o por participante para encontrar inscripciones específicas

---

### Flujo 2: Usuario normal se inscribe en eventos

1. **Usuario inicia sesión** (o se registra primero)
2. **Va a "Eventos"** → Ve la lista de eventos disponibles
3. **Selecciona un evento** que le interesa
4. **Va a "Inscripciones"** → Clic en "Inscribirme en un Evento"
5. **Selecciona el evento** de la lista
6. **Confirma** → Queda inscrito automáticamente
7. **Ve sus inscripciones** en la tabla (solo las suyas)
8. **Si cambia de opinión**, puede cancelar su inscripción

---

### Flujo 3: Administrador gestiona participantes

1. **Admin va a "Participantes"**
2. **Crea nuevos participantes** o **edita existentes**
3. **Busca participantes** usando el campo de búsqueda
4. **Ve detalles** de un participante (doble clic)
5. **Ve los eventos** en los que está inscrito ese participante
6. **Puede agregarlo a más eventos** desde la vista de detalles

---

### Flujo 4: Usuario se registra por primera vez

1. **En la pantalla de login**, clic en "Registrarse"
2. **Completa el formulario**:
   - Datos personales (nombre, apellidos, email, DNI/NIE)
   - Datos de usuario (username, contraseña)
3. **Confirma el registro**
4. **Sistema crea**:
   - Un usuario con rol 'user'
   - Un participante asociado
5. **Puede iniciar sesión** inmediatamente con sus credenciales
6. **Ya puede inscribirse** en eventos

---

### Flujo 5: Administrador genera reportes

1. **Admin va a "Reportes"**
2. **Selecciona qué exportar**: Eventos, Participantes o Inscripciones
3. **Elige el formato**: CSV o PDF
4. **Confirma la exportación**
5. **Archivo generado** en la carpeta `exports/`
6. **Puede abrir** el archivo para análisis externo

---

## 🎯 CASOS DE USO ESPECÍFICOS

### Caso 1: Evento con capacidad limitada
- **Situación**: Un evento tiene capacidad de 50 personas
- **Comportamiento**: 
  - El sistema cuenta automáticamente las inscripciones confirmadas
  - Cuando se alcanza el límite, no permite más inscripciones
  - Muestra mensaje: "El evento está lleno"
- **Protección**: Incluso si dos usuarios intentan inscribirse simultáneamente, solo uno tendrá éxito

### Caso 2: Usuario quiere ver en qué eventos está inscrito
- **Acción**: Ir a "Inscripciones"
- **Resultado**: Ve solo sus propias inscripciones con toda la información

### Caso 3: Administrador quiere ver quién está inscrito en un evento específico
- **Acción**: Ir a "Inscripciones" → Filtrar por evento
- **Resultado**: Ve todos los participantes inscritos en ese evento

### Caso 4: Administrador quiere ver en qué eventos está inscrito un participante
- **Acción**: Ir a "Inscripciones" → Filtrar por participante
- **Resultado**: Ve todos los eventos en los que está inscrito ese participante

### Caso 5: Dos administradores editan el mismo evento simultáneamente
- **Situación**: Admin A y Admin B abren el mismo evento para editar
- **Comportamiento**:
  - El primero en guardar tiene éxito
  - El segundo recibe mensaje: "El evento fue modificado por otro usuario"
  - Debe recargar el evento para ver los cambios y volver a editar

### Caso 6: Usuario sin perfil de participante
- **Situación**: Usuario inicia sesión pero no tiene participante asociado
- **Comportamiento**: 
  - Ve mensaje: "No tienes un perfil de participante asociado"
  - No puede inscribirse en eventos
  - Debe contactar al administrador

---

## 📊 RESUMEN DE PERMISOS

| Funcionalidad | ADMIN | Usuario Normal |
|--------------|-------|----------------|
| **Ver eventos** | ✅ | ✅ |
| **Crear eventos** | ✅ | ❌ |
| **Editar eventos** | ✅ | ❌ |
| **Eliminar eventos** | ✅ | ❌ |
| **Ver participantes** | ✅ | ✅ |
| **Crear participantes** | ✅ | ❌ |
| **Editar participantes** | ✅ | ❌ |
| **Eliminar participantes** | ✅ | ❌ |
| **Ver todas las inscripciones** | ✅ | ❌ |
| **Ver solo mis inscripciones** | ✅ | ✅ |
| **Inscribir cualquier participante** | ✅ | ❌ |
| **Inscribirme a mí mismo** | ✅ | ✅ |
| **Cancelar cualquier inscripción** | ✅ | ❌ |
| **Cancelar mis inscripciones** | ✅ | ✅ |
| **Filtrar por evento** | ✅ | ✅ |
| **Filtrar por participante** | ✅ | ❌ |
| **Gestionar usuarios** | ✅ | ❌ |
| **Exportar reportes** | ✅ | ❌ |
| **Registrarse** | ✅ | ✅ |

---

## 🔐 SEGURIDAD Y VALIDACIONES

### Validaciones Automáticas
- **Email**: Debe tener formato válido (@)
- **DNI/NIE**: Formato correcto (validación básica)
- **Teléfono**: 9 dígitos
- **Capacidad**: Debe ser mayor que 0
- **Fechas**: La fecha de fin debe ser posterior a la de inicio
- **Unicidad**: Email y DNI/NIE únicos, username único

### Protecciones
- **Contraseñas**: Almacenadas con hash bcrypt (no se guardan en texto plano)
- **Control de acceso**: Solo usuarios autenticados pueden acceder
- **Permisos**: Funcionalidades restringidas según rol
- **Concurrencia**: Prevención de conflictos en ediciones simultáneas

---

**Autor**: Martin Peñalva Artázcoz - 2º DAM

