# Soporte de Múltiples Usuarios Simultáneos

## Descripción

La aplicación **Gestor de Eventos Locales** está diseñada para permitir que múltiples usuarios accedan y trabajen simultáneamente sin conflictos. Cada usuario ejecuta su propia instancia de la aplicación en su ordenador, y todas las instancias comparten la misma base de datos MySQL.

## Arquitectura

### Pool de Conexiones

- **Tamaño del pool**: 20 conexiones (configurable en `config/config.py`)
- **Patrón Singleton**: Todas las instancias de la aplicación comparten el mismo pool de conexiones
- **Thread-safe**: El pool está protegido con locks de threading para evitar condiciones de carrera

### Control de Concurrencia

La aplicación implementa técnicas avanzadas para manejar la concurrencia y garantizar un nivel técnico adecuado:

#### 1. Sistema de Locks por Recurso (ResourceLockManager)

- **Gestión de locks individuales**: Cada recurso (evento, participante) tiene su propio lock (RLock)
- **Sincronización granular**: Los locks se adquieren solo para recursos específicos, permitiendo paralelismo cuando es posible
- **Timeouts configurables**: Los locks tienen un timeout configurable para evitar deadlocks
- **Thread-safe**: Implementado usando threading.RLock para garantizar la seguridad en entornos multi-thread

**Ubicación**: `src/utils/concurrency_manager.py` - clase `ResourceLockManager`

#### 2. Control de Versiones Optimista con Locks (Eventos)

- Cada evento tiene un campo `version` que se incrementa en cada actualización
- Al actualizar un evento, se verifica que la versión no haya cambiado
- **Uso de locks de recursos**: Se adquiere un lock específico para el evento antes de actualizarlo
- **Reintentos automáticos**: En caso de fallo, se reintenta automáticamente con backoff exponencial
- Si la versión cambió, significa que otro usuario modificó el evento y se rechaza la actualización

**Ubicación**: `src/controllers/event_controller.py` - método `update()`

#### 3. Bloqueos Transaccionales con Locks (Inscripciones)

- Al inscribir un participante en un evento, se usa `SELECT FOR UPDATE` a nivel de base de datos
- **Locks de recursos a nivel de aplicación**: Se adquiere un lock específico para el evento antes de procesar la inscripción
- Esto bloquea el registro del evento mientras se verifica la capacidad
- Previene que dos usuarios inscriban simultáneamente cuando solo queda una plaza
- **Reintentos automáticos**: Las operaciones incluyen reintentos automáticos con backoff exponencial

**Ubicación**: `src/controllers/registration_controller.py` - método `register_participant()`

#### 4. Sistema de Suscripciones en Paralelo (ParallelSubscriptionProcessor)

- **Worker threads**: Procesa múltiples suscripciones simultáneamente usando worker threads
- **Cola de tareas**: Utiliza una cola thread-safe para gestionar las tareas pendientes
- **Procesamiento paralelo**: Permite procesar múltiples inscripciones en paralelo de forma segura
- **Configuración flexible**: Número de workers y tamaño de cola configurables

**Ubicación**: `src/utils/concurrency_manager.py` - clase `ParallelSubscriptionProcessor`
**Uso**: `src/controllers/registration_controller.py` - método `register_multiple_participants_parallel()`

#### 5. Sistema de Reintentos con Backoff Exponencial

- **Reintentos automáticos**: Las operaciones críticas se reintentan automáticamente en caso de fallo
- **Backoff exponencial**: El tiempo entre reintentos aumenta exponencialmente
- **Configuración flexible**: Número máximo de reintentos y tiempos de espera configurables
- **Manejo de excepciones**: Solo se reintentan excepciones específicas (por defecto, errores de base de datos)

**Ubicación**: `src/utils/concurrency_manager.py` - decorador `retry_with_backoff`
**Uso**: Decoradores aplicados a métodos críticos en controladores

#### 6. Sistema de Notificaciones de Eventos (EventNotificationSystem)

- **Notificaciones asíncronas**: Notifica a múltiples listeners cuando ocurren cambios
- **Ejecución en paralelo**: Los callbacks se ejecutan en threads separados para no bloquear
- **Suscripción/desuscripción**: Permite suscribirse y desuscribirse de diferentes tipos de eventos
- **Thread-safe**: Implementado usando locks para garantizar la seguridad

**Ubicación**: `src/utils/concurrency_manager.py` - clase `EventNotificationSystem`

#### 7. Nivel de Aislamiento de Transacciones

- Las transacciones críticas usan `REPEATABLE READ`
- Garantiza que los datos leídos durante una transacción no cambien
- Previene lecturas sucias y condiciones de carrera

## Configuración

### Ajustar el Tamaño del Pool

Edita `config/config.py`:

```python
CONCURRENCY_CONFIG = {
    'lock_timeout': 30,  # segundos - tiempo máximo para adquirir un lock
    'max_retries': 3,  # número máximo de reintentos en operaciones fallidas
    'pool_size': 20,  # Tamaño del pool de conexiones para soportar múltiples usuarios simultáneos
    'subscription_workers': 5,  # Número de worker threads para procesar suscripciones en paralelo
    'max_queue_size': 100,  # Tamaño máximo de la cola de tareas para procesamiento paralelo
    'retry_base_delay': 0.1,  # Retraso base para reintentos (segundos)
    'retry_max_delay': 2.0  # Retraso máximo para reintentos (segundos)
}
```

**Recomendaciones**:
- **5-10 usuarios**: pool_size = 10-15
- **10-20 usuarios**: pool_size = 20-30
- **20+ usuarios**: pool_size = 30-50

### Requisitos del Servidor MySQL

Para un rendimiento óptimo con múltiples usuarios:

1. **Conexiones máximas**: Asegúrate de que `max_connections` en MySQL sea mayor que el tamaño del pool
2. **Recursos**: El servidor debe tener suficiente RAM y CPU para manejar múltiples conexiones simultáneas
3. **Red**: Si los usuarios están en diferentes máquinas, asegúrate de que la red tenga suficiente ancho de banda

## Uso

### Ejecutar Múltiples Instancias

1. Cada usuario ejecuta la aplicación en su ordenador:
   ```bash
   python src/main.py
   ```

2. Todos los usuarios se conectan a la misma base de datos MySQL (configurada en `config/config.py` o `.env`)

3. Cada usuario puede:
   - Ver eventos y participantes en tiempo real
   - Crear, editar y eliminar eventos (con control de versiones y locks de recursos)
   - Inscribir participantes en eventos (con protección contra condiciones de carrera y locks)
   - Registrar múltiples participantes en paralelo (usando worker threads)
   - Exportar reportes

### Comportamiento Esperado

#### Escenario 1: Dos usuarios editan el mismo evento

1. Usuario A abre el evento para editar
2. Usuario B abre el mismo evento para editar
3. Usuario A guarda los cambios → ✅ Éxito
4. Usuario B intenta guardar → ❌ Error: "El evento fue modificado por otro usuario"

**Solución**: Usuario B debe recargar el evento y volver a hacer sus cambios.

#### Escenario 2: Dos usuarios inscriben en un evento con una plaza disponible

1. Evento tiene capacidad 10, ya hay 9 inscritos (1 plaza disponible)
2. Usuario A intenta inscribir participante X
   - Adquiere lock del evento (event_10)
   - Verifica capacidad con SELECT FOR UPDATE
   - Inscribe participante
   - Libera lock
3. Usuario B intenta inscribir participante Y (simultáneamente)
   - Intenta adquirir lock del evento (espera si está ocupado)
   - Una vez adquirido, verifica capacidad
   - Detecta que está lleno
   - Libera lock
4. Solo uno de los dos tendrá éxito → El primero en adquirir el lock
5. El otro recibirá un mensaje de que el evento está lleno

**Solución**: El sistema previene automáticamente la sobre-inscripción usando locks de recursos y bloqueos transaccionales.

#### Escenario 3: Suscripción múltiple en paralelo

1. Usuario administrador necesita inscribir 20 participantes en un evento
2. Usa el método `register_multiple_participants_parallel()`
3. Las 20 inscripciones se envían a la cola de tareas
4. 5 worker threads procesan las inscripciones en paralelo
5. Cada worker thread adquiere el lock del evento cuando está disponible
6. Las inscripciones se procesan de forma concurrente pero segura
7. Todos los resultados se recopilan al final

**Beneficio**: Procesamiento mucho más rápido que hacer las inscripciones de forma secuencial, manteniendo la seguridad.

## Limitaciones

1. **Aplicación de escritorio**: Cada usuario necesita tener la aplicación instalada en su ordenador
2. **Base de datos compartida**: Todos los usuarios deben poder acceder a la misma base de datos MySQL
3. **Sin sincronización en tiempo real**: Los cambios de un usuario no se reflejan automáticamente en las ventanas de otros usuarios hasta que recarguen la vista

## Solución de Problemas

### Error: "No hay pool de conexiones disponible"

- Verifica que MySQL Server esté ejecutándose
- Verifica las credenciales en `config/config.py` o `.env`
- Asegúrate de que la base de datos existe

### Error: "Error al obtener conexión del pool"

- El pool puede estar saturado (demasiados usuarios simultáneos)
- Solución: Aumenta `pool_size` en `config/config.py`
- O reduce el número de usuarios simultáneos

### Conflictos de concurrencia frecuentes

- Si los usuarios editan los mismos eventos frecuentemente, considera:
  - Implementar notificaciones cuando un evento es modificado
  - Añadir un sistema de "edición en curso" para evitar conflictos
  - Usar un sistema de colas para las actualizaciones

## Arquitectura de Concurrencia Implementada

### Módulo de Gestión de Concurrencia

El módulo `src/utils/concurrency_manager.py` proporciona:

1. **ResourceLockManager**: Gestión de locks por recurso con timeouts
2. **ParallelSubscriptionProcessor**: Procesador de tareas en paralelo con worker threads
3. **EventNotificationSystem**: Sistema de notificaciones asíncronas
4. **Decoradores de utilidad**: `retry_with_backoff`, `with_resource_lock`

### Integración en Controladores

Los controladores han sido mejorados para usar estos mecanismos:

- **EventController**: Locks de recursos + control de versiones optimista + reintentos
- **RegistrationController**: Locks de recursos + bloqueos transaccionales + procesamiento paralelo + reintentos

### Nivel de Concurrencia

La aplicación soporta:

- ✅ **Usuarios simultáneos**: Múltiples usuarios trabajando al mismo tiempo
- ✅ **Suscripción a eventos en paralelo**: Worker threads procesan múltiples inscripciones simultáneamente
- ✅ **Gestión de bloqueos**: Locks por recurso + bloqueos transaccionales de base de datos
- ✅ **Sincronización**: Múltiples mecanismos de sincronización (locks, transacciones, colas)

## Mejoras Futuras

Posibles mejoras para el soporte multiusuario:

1. **Sincronización en tiempo real**: Usar WebSockets o polling para actualizar las vistas automáticamente
2. **Historial de cambios**: Registrar quién y cuándo modificó cada registro
3. **Modo de solo lectura**: Permitir que algunos usuarios solo vean datos sin poder modificarlos
4. **Monitoreo de concurrencia**: Dashboard para ver el estado de locks y colas en tiempo real

## Autor

Martin Peñalva Artázcoz - 2º DAM

