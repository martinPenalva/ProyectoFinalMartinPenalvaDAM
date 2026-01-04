# Gestión de Concurrencia - Documentación Técnica

## Resumen

Se ha implementado un sistema completo de gestión de concurrencia para el Gestor de Eventos Locales, cumpliendo con los requisitos del módulo de Proyecto Intermodular. El sistema garantiza el manejo seguro de usuarios simultáneos, suscripciones en paralelo, y sincronización mediante múltiples mecanismos.

## Componentes Implementados

### 1. Módulo de Gestión de Concurrencia (`src/utils/concurrency_manager.py`)

#### ResourceLockManager
- **Propósito**: Gestión de locks por recurso individual
- **Características**:
  - Locks individuales por ID de recurso (ej: `event_1`, `event_2`)
  - Thread-safe usando `threading.RLock`
  - Timeouts configurables para evitar deadlocks
  - Permite paralelismo cuando los recursos son diferentes

#### ParallelSubscriptionProcessor
- **Propósito**: Procesamiento paralelo de suscripciones usando worker threads
- **Características**:
  - Worker threads configurables (por defecto 5)
  - Cola thread-safe para gestionar tareas
  - Procesamiento simultáneo de múltiples inscripciones
  - Espera de resultados con timeout opcional

#### EventNotificationSystem
- **Propósito**: Sistema de notificaciones asíncronas de eventos
- **Características**:
  - Suscripción/desuscripción de callbacks
  - Ejecución de callbacks en threads separados (no bloqueante)
  - Thread-safe usando locks

#### Decoradores de Utilidad
- **`retry_with_backoff`**: Reintentos automáticos con backoff exponencial
- **`with_resource_lock`**: Decorador para usar locks de recursos

### 2. Mejoras en RegistrationController

- ✅ **Locks de recursos**: Cada evento tiene su propio lock
- ✅ **Reintentos automáticos**: Hasta 3 reintentos con backoff exponencial
- ✅ **Procesamiento paralelo**: Método `register_multiple_participants_parallel()` para procesar múltiples inscripciones simultáneamente
- ✅ **Sistema de notificaciones**: Notifica cuando se crea una inscripción
- ✅ **Bloqueos transaccionales**: Mantiene `SELECT FOR UPDATE` a nivel de base de datos
- ✅ **Nivel de aislamiento**: `REPEATABLE READ` para garantizar consistencia

### 3. Mejoras en EventController

- ✅ **Locks de recursos**: Cada evento tiene su propio lock
- ✅ **Reintentos automáticos**: Hasta 3 reintentos con backoff exponencial
- ✅ **Control de versiones optimista**: Mantiene el sistema de versiones existente
- ✅ **Sistema de notificaciones**: Notifica cuando se actualiza un evento

### 4. Configuración (`config/config.py`)

Se han añadido nuevos parámetros de configuración:

```python
CONCURRENCY_CONFIG = {
    'lock_timeout': 30,  # segundos - tiempo máximo para adquirir un lock
    'max_retries': 3,  # número máximo de reintentos
    'pool_size': 20,  # Tamaño del pool de conexiones
    'subscription_workers': 5,  # Número de worker threads para procesamiento paralelo
    'max_queue_size': 100,  # Tamaño máximo de la cola de tareas
    'retry_base_delay': 0.1,  # Retraso base para reintentos (segundos)
    'retry_max_delay': 2.0  # Retraso máximo para reintentos (segundos)
}
```

## Características de Concurrencia Implementadas

### ✅ Usuarios Simultáneos
- **Pool de conexiones**: Múltiples usuarios pueden conectarse simultáneamente
- **Locks por recurso**: Cada recurso (evento) puede ser bloqueado independientemente
- **Thread-safe**: Todas las operaciones críticas son thread-safe

### ✅ Suscripción a Eventos en Paralelo
- **Worker threads**: 5 threads por defecto procesan suscripciones simultáneamente
- **Cola de tareas**: Sistema de colas thread-safe para gestionar múltiples tareas
- **Método dedicado**: `register_multiple_participants_parallel()` para procesar múltiples inscripciones en paralelo

### ✅ Gestión de Bloqueos y Sincronización
- **Locks de recursos**: Sincronización a nivel de aplicación usando `threading.RLock`
- **Bloqueos transaccionales**: Sincronización a nivel de base de datos usando `SELECT FOR UPDATE`
- **Control de versiones optimista**: Prevención de conflictos al editar eventos
- **Reintentos automáticos**: Manejo de errores temporales con reintentos

## Flujo de Ejecución

### Inscripción de Participante

1. Se adquiere el lock del evento específico (`event_{id}`)
2. Se inicia una transacción con nivel de aislamiento `REPEATABLE READ`
3. Se verifica la capacidad con `SELECT FOR UPDATE` (bloqueo a nivel de BD)
4. Se inserta el registro
5. Se confirma la transacción
6. Se notifica el evento de inscripción
7. Se libera el lock

### Actualización de Evento

1. Se adquiere el lock del evento específico
2. Se verifica la versión del evento (control optimista)
3. Se actualiza si la versión coincide
4. Se notifica el evento de actualización
5. Se libera el lock

### Suscripción Múltiple en Paralelo

1. Se envían todas las tareas a la cola de procesamiento
2. Los worker threads toman tareas de la cola
3. Cada worker adquiere el lock del evento cuando está disponible
4. Se procesan las inscripciones de forma concurrente pero segura
5. Se recopilan todos los resultados

## Casos de Uso

### Escenario 1: Dos usuarios inscriben simultáneamente en el mismo evento

- Usuario A adquiere lock del evento
- Usuario B espera (timeout configurable)
- Usuario A completa la inscripción y libera el lock
- Usuario B adquiere el lock, verifica capacidad y completa o falla según disponibilidad

### Escenario 2: Suscripción masiva

- Administrador llama a `register_multiple_participants_parallel()` con 20 participantes
- Las 20 tareas se encolan
- 5 worker threads procesan simultáneamente
- Cada worker adquiere el lock cuando está disponible
- Todas las inscripciones se procesan de forma eficiente y segura

### Escenario 3: Edición concurrente de eventos

- Usuario A y B abren el mismo evento para editar
- Usuario A guarda cambios → éxito (versión 0 → 1)
- Usuario B intenta guardar → falla (versión cambió, conflicto detectado)
- Usuario B debe recargar y volver a editar

## Ventajas de la Implementación

1. **Seguridad**: Múltiples capas de protección (locks + transacciones + versiones)
2. **Rendimiento**: Procesamiento paralelo donde es seguro
3. **Escalabilidad**: Configuración flexible para diferentes cargas de trabajo
4. **Robustez**: Reintentos automáticos para manejar errores temporales
5. **Observabilidad**: Sistema de notificaciones para tracking de cambios

## Requisitos Cumplidos

✅ **Usuarios simultáneos**: Soporte completo mediante pool de conexiones y locks
✅ **Suscripción a eventos en paralelo**: Implementado con worker threads y colas
✅ **Gestión de bloqueos**: Múltiples mecanismos (locks de recursos + bloqueos transaccionales)
✅ **Sincronización**: Thread-safe en todos los niveles

## Autor

Martin Peñalva Artázcoz - 2º DAM

