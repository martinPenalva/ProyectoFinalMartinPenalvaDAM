# Cómo Probar el Soporte de Múltiples Usuarios Simultáneos

## Requisitos Previos

1. ✅ MySQL Server ejecutándose
2. ✅ Base de datos `eventos_locales` creada y con datos
3. ✅ Al menos 2 usuarios creados en la base de datos (o usar el usuario ADMIN)

## Método 1: Probar en el Mismo Ordenador (Más Fácil)

### Paso 1: Abrir Primera Instancia

1. Abre una terminal/consola
2. Navega a la carpeta del proyecto:
   ```bash
   cd C:\Users\Martin\Downloads\prueba-PP-master\prueba-PP-master
   ```
3. Ejecuta la aplicación:
   ```bash
   python src/main.py
   ```
4. Inicia sesión con un usuario (ej: `ADMIN` / contraseña: `ADMINISTRADOR`)

### Paso 2: Abrir Segunda Instancia

1. Abre **otra terminal/consola nueva** (no cierres la primera)
2. Navega a la misma carpeta:
   ```bash
   cd C:\Users\Martin\Downloads\prueba-PP-master\prueba-PP-master
   ```
3. Ejecuta la aplicación nuevamente:
   ```bash
   python src/main.py
   ```
4. Inicia sesión con **otro usuario diferente** (o crea uno nuevo desde el registro)

### Paso 3: Verificar que Ambas Funcionan

- ✅ Ambas ventanas deben abrirse correctamente
- ✅ Ambas deben poder ver los mismos eventos y participantes
- ✅ No debe haber errores de conexión

## Método 2: Probar en Diferentes Ordenadores (Más Realista)

### Requisitos

- Ambos ordenadores en la misma red (o con acceso a la misma base de datos MySQL)
- MySQL configurado para aceptar conexiones remotas (si es necesario)

### Pasos

1. **En el ordenador 1**: Ejecuta la aplicación e inicia sesión
2. **En el ordenador 2**: Ejecuta la aplicación e inicia sesión con otro usuario
3. Ambos deben poder trabajar simultáneamente

## Escenarios de Prueba

### Escenario 1: Verificación Básica de Conexión Simultánea

**Objetivo**: Verificar que múltiples usuarios pueden conectarse al mismo tiempo

**Pasos**:
1. Abre 2-3 instancias de la aplicación
2. Inicia sesión con diferentes usuarios en cada una
3. Navega por las diferentes secciones (Eventos, Participantes, etc.)

**Resultado Esperado**:
- ✅ Todas las instancias funcionan correctamente
- ✅ No hay errores de conexión
- ✅ Los datos se muestran correctamente en todas las ventanas

---

### Escenario 2: Lectura Simultánea de Datos

**Objetivo**: Verificar que múltiples usuarios pueden leer los mismos datos sin conflictos

**Pasos**:
1. Usuario A: Ve a "Eventos" y observa la lista
2. Usuario B: Ve a "Eventos" y observa la lista
3. Usuario A: Ve a "Participantes" y observa la lista
4. Usuario B: Ve a "Participantes" y observa la lista

**Resultado Esperado**:
- ✅ Ambos usuarios ven los mismos datos
- ✅ No hay errores
- ✅ Las operaciones de lectura no interfieren entre sí

---

### Escenario 3: Creación Simultánea de Eventos

**Objetivo**: Verificar que múltiples usuarios pueden crear eventos al mismo tiempo

**Pasos**:
1. Usuario A: Crea un nuevo evento (ej: "Evento Usuario A")
2. Usuario B: Crea un nuevo evento (ej: "Evento Usuario B") **al mismo tiempo**
3. Ambos usuarios guardan sus eventos

**Resultado Esperado**:
- ✅ Ambos eventos se crean correctamente
- ✅ Ambos usuarios pueden ver ambos eventos después de recargar
- ✅ No hay conflictos ni errores

---

### Escenario 4: Edición Simultánea del Mismo Evento (Control de Versiones)

**Objetivo**: Verificar que el control de versiones optimista funciona

**Pasos**:
1. Usuario A: Abre un evento existente para editar (NO guarda todavía)
2. Usuario B: Abre el **mismo evento** para editar
3. Usuario A: Modifica el título y **guarda**
4. Usuario B: Modifica la descripción y **intenta guardar**

**Resultado Esperado**:
- ✅ Usuario A: Guarda exitosamente
- ✅ Usuario B: Recibe un error o mensaje indicando que el evento fue modificado
- ✅ Usuario B debe recargar el evento para ver los cambios de Usuario A

**Nota**: Si no aparece un mensaje de error explícito, verifica en la consola que el método `update()` retorne `False` cuando hay conflicto de versión.

---

### Escenario 5: Inscripción Simultánea (Condición de Carrera)

**Objetivo**: Verificar que el bloqueo transaccional previene sobre-inscripciones

**Preparación**:
1. Crea un evento con capacidad pequeña (ej: capacidad = 2)
2. Inscribe 1 participante (queda 1 plaza disponible)

**Pasos**:
1. Usuario A: Intenta inscribir un participante X en el evento
2. Usuario B: Intenta inscribir un participante Y en el **mismo evento** (al mismo tiempo)
3. Ambos intentan guardar simultáneamente

**Resultado Esperado**:
- ✅ Solo uno de los dos usuarios puede inscribir exitosamente
- ✅ El otro usuario recibe un mensaje de que el evento está lleno
- ✅ El evento no puede exceder su capacidad
- ✅ No hay errores de base de datos

**Cómo verificar**:
- Después de ambos intentos, verifica que el número de inscritos no exceda la capacidad
- Solo uno de los dos participantes (X o Y) debe estar inscrito

---

### Escenario 6: Múltiples Usuarios Inscribiendo en Diferentes Eventos

**Objetivo**: Verificar que las operaciones en diferentes eventos no interfieren

**Pasos**:
1. Usuario A: Inscribe participante 1 en Evento A
2. Usuario B: Inscribe participante 2 en Evento B (diferente)
3. Ambos lo hacen simultáneamente

**Resultado Esperado**:
- ✅ Ambas inscripciones se completan exitosamente
- ✅ No hay conflictos ni errores
- ✅ Cada evento tiene su participante correcto

---

### Escenario 7: Eliminación Simultánea

**Objetivo**: Verificar el comportamiento al eliminar datos simultáneamente

**Pasos**:
1. Usuario A: Intenta eliminar un evento
2. Usuario B: Intenta eliminar el **mismo evento** (al mismo tiempo)

**Resultado Esperado**:
- ✅ Solo uno de los dos puede eliminar el evento
- ✅ El otro usuario verá que el evento ya no existe al intentar acceder
- ✅ No hay errores críticos

---

## Verificación del Pool de Conexiones

### Ver Cuántas Conexiones Están Activas

1. Conecta a MySQL:
   ```bash
   mysql -u root -p -P 3309
   ```

2. Ejecuta:
   ```sql
   SHOW PROCESSLIST;
   ```

3. Deberías ver múltiples conexiones activas (una por cada instancia de la aplicación)

### Verificar el Tamaño del Pool

1. Abre `config/config.py`
2. Verifica que `pool_size` esté configurado (por defecto: 20)
3. Si abres más instancias que el tamaño del pool, algunas pueden esperar o fallar

## Pruebas de Carga (Opcional)

### Probar con Múltiples Instancias

1. Abre 5-10 instancias de la aplicación simultáneamente
2. Inicia sesión en todas con diferentes usuarios
3. Realiza operaciones en todas simultáneamente

**Resultado Esperado**:
- ✅ Todas las instancias funcionan
- ✅ No hay errores de "pool agotado" (a menos que excedas el tamaño del pool)
- ✅ El rendimiento puede ser más lento pero la aplicación sigue funcionando

## Solución de Problemas Durante las Pruebas

### Error: "No hay pool de conexiones disponible"

**Causa**: MySQL no está ejecutándose o las credenciales son incorrectas

**Solución**:
1. Verifica que MySQL esté ejecutándose
2. Verifica las credenciales en `config/config.py` o `.env`
3. Prueba la conexión manualmente

### Error: "Error al obtener conexión del pool"

**Causa**: El pool está saturado (demasiadas instancias abiertas)

**Solución**:
1. Cierra algunas instancias
2. O aumenta `pool_size` en `config/config.py`

### Los cambios no se ven en tiempo real

**Comportamiento Normal**: 
- Los cambios de un usuario no se reflejan automáticamente en otras ventanas
- Cada usuario debe recargar la vista (cambiar de sección y volver) para ver cambios

**Solución Futura**: Implementar sincronización en tiempo real (no está implementado actualmente)

### Conflictos de versión no se detectan

**Verificación**:
1. Abre la consola donde se ejecuta la aplicación
2. Intenta el Escenario 4 (edición simultánea)
3. Deberías ver mensajes en la consola si hay conflictos

## Checklist de Pruebas

Marca cada escenario cuando lo hayas probado:

- [ ] Escenario 1: Conexión simultánea básica
- [ ] Escenario 2: Lectura simultánea
- [ ] Escenario 3: Creación simultánea
- [ ] Escenario 4: Edición del mismo evento (control de versiones)
- [ ] Escenario 5: Inscripción simultánea (condición de carrera)
- [ ] Escenario 6: Operaciones en diferentes eventos
- [ ] Escenario 7: Eliminación simultánea
- [ ] Verificación del pool de conexiones
- [ ] Pruebas de carga (opcional)

## Resultado Final Esperado

Si todas las pruebas pasan correctamente, significa que:

✅ La aplicación soporta múltiples usuarios simultáneos  
✅ El control de concurrencia funciona correctamente  
✅ No hay condiciones de carrera en las inscripciones  
✅ El control de versiones previene conflictos  
✅ El pool de conexiones maneja múltiples usuarios eficientemente  

## Notas Importantes

1. **No hay sincronización en tiempo real**: Los cambios de un usuario no se ven automáticamente en otras ventanas hasta que recarguen
2. **Cada usuario necesita su propia instancia**: No es una aplicación web, cada usuario ejecuta su propia copia
3. **Base de datos compartida**: Todos los usuarios deben poder acceder a la misma base de datos MySQL

---

**Autor**: Martin Peñalva Artázcoz - 2º DAM

