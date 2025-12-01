# Credenciales para Iniciar Sesión

## 🔓 Estado Actual del Login

**IMPORTANTE**: El sistema de login actual es **básico** y acepta **cualquier usuario y contraseña** (mientras no estén vacíos).

Esto significa que puedes usar:
- **Usuario**: Cualquier cosa (ej: `admin`, `usuario`, `test`)
- **Contraseña**: Cualquier cosa (ej: `123`, `admin123`, `password`)

## 📝 Ejemplos de Credenciales que Funcionan

```
Usuario: admin
Contraseña: admin123
```

```
Usuario: test
Contraseña: test
```

```
Usuario: usuario
Contraseña: 123
```

**Cualquier combinación funciona mientras ambos campos tengan texto.**

---

## 🔐 Usuario en la Base de Datos

En el archivo `database/schema.sql` hay un usuario creado por defecto:

- **Username**: `admin`
- **Password Hash**: (hash de bcrypt)
- **Rol**: `admin`

**PERO**: El código actual de login **NO valida** contra la base de datos. Solo verifica que los campos no estén vacíos.

---

## ⚠️ Nota de Seguridad

Este es un sistema básico para desarrollo. En producción, deberías:

1. Validar credenciales contra la base de datos
2. Usar hash de contraseñas (bcrypt)
3. Implementar sesiones seguras
4. Agregar límite de intentos de login

---

## 🚀 Para Usar la Aplicación Ahora

Simplemente:
1. Abre la aplicación
2. Escribe **cualquier usuario** (ej: `admin`)
3. Escribe **cualquier contraseña** (ej: `123`)
4. Haz clic en "Entrar"

**¡Funcionará!**

---

## 💡 Si Quieres Implementar Login Real

Si quieres que el login valide contra la base de datos, necesitarías:

1. Crear un controlador de autenticación
2. Validar el hash de la contraseña con bcrypt
3. Verificar contra la tabla `users` en MySQL

¿Quieres que implemente el sistema de login completo con validación real?

