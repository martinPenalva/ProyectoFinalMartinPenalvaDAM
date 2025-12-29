# Soporte de Múltiples Usuarios Simultáneos

## Descripción

La aplicación **Gestor de Eventos Locales** está diseñada para permitir que múltiples usuarios accedan y trabajen simultáneamente sin conflictos. Cada usuario ejecuta su propia instancia de la aplicación en su ordenador, y todas las instancias comparten la misma base de datos MySQL.

## Arquitectura

### Pool de Conexiones

- **Tamaño del pool**: 20 conexiones (configurable en `config/config.py`)
- **Patrón Singleton**: Todas las instancias de la aplicación comparten el mismo pool de conexiones
- **Thread-safe**: El pool está protegido con locks de threading para evitar condiciones de carrera

### Control de Concurrencia

La aplicación implementa varias técnicas para manejar la concurrencia:

#### 1. Control de Versiones Optimista (Eventos)

- Cada evento tiene un campo `version` que se incrementa en cada actualización
- Al actualizar un evento, se verifica que la versión no haya cambiado
- Si la versión cambió, significa que otro usuario modificó el evento y se rechaza la actualización

**Ubicación**: `src/controllers/event_controller.py` - método `update()`

#### 2. Bloqueos Transaccionales (Inscripciones)

- Al inscribir un participante en un evento, se usa `SELECT FOR UPDATE`
- Esto bloquea el registro del evento mientras se verifica la capacidad
- Previene que dos usuarios inscriban simultáneamente cuando solo queda una plaza

**Ubicación**: `src/controllers/registration_controller.py` - método `register_participant()`

#### 3. Nivel de Aislamiento de Transacciones

- Las transacciones críticas usan `REPEATABLE READ`
- Garantiza que los datos leídos durante una transacción no cambien
- Previene lecturas sucias y condiciones de carrera

## Configuración

### Ajustar el Tamaño del Pool

Edita `config/config.py`:

```python
CONCURRENCY_CONFIG = {
    'lock_timeout': 30,
    'max_retries': 3,
    'pool_size': 20  # Ajusta según el número de usuarios simultáneos esperados
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
   - Crear, editar y eliminar eventos (con control de versiones)
   - Inscribir participantes en eventos (con protección contra condiciones de carrera)
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
3. Usuario B intenta inscribir participante Y (simultáneamente)
4. Solo uno de los dos tendrá éxito → El primero en completar la transacción
5. El otro recibirá un mensaje de que el evento está lleno

**Solución**: El sistema previene automáticamente la sobre-inscripción.

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

## Mejoras Futuras

Posibles mejoras para el soporte multiusuario:

1. **Sincronización en tiempo real**: Usar WebSockets o polling para actualizar las vistas automáticamente
2. **Sistema de notificaciones**: Alertar a los usuarios cuando otros usuarios modifican datos
3. **Historial de cambios**: Registrar quién y cuándo modificó cada registro
4. **Modo de solo lectura**: Permitir que algunos usuarios solo vean datos sin poder modificarlos

## Autor

Martin Peñalva Artázcoz - 2º DAM

