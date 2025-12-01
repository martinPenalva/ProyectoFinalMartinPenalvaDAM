# Guía de Instalación de Python en Windows

## Paso 1: Descargar Python

1. Visita el sitio oficial: **https://www.python.org/downloads/**
2. Haz clic en el botón grande **"Download Python 3.x.x"** (la versión más reciente)
3. Se descargará un archivo `.exe` (por ejemplo: `python-3.12.0-amd64.exe`)

## Paso 2: Instalar Python

1. **Ejecuta el instalador** que acabas de descargar
2. **MUY IMPORTANTE**: Marca la casilla **"Add Python to PATH"** (abajo en la primera pantalla)
   - Esto permite usar Python desde cualquier lugar
3. Haz clic en **"Install Now"**
4. Espera a que termine la instalación (puede tardar unos minutos)
5. Cuando termine, verás un mensaje "Setup was successful"
6. Haz clic en **"Close"**

## Paso 3: Verificar la Instalación

1. Abre **PowerShell** o **CMD** (Símbolo del sistema)
   - Presiona `Win + R`, escribe `powershell` y presiona Enter
   - O busca "PowerShell" en el menú de inicio

2. Ejecuta estos comandos para verificar:

```powershell
python --version
```

Deberías ver algo como: `Python 3.12.0`

```powershell
pip --version
```

Deberías ver la versión de pip (gestor de paquetes de Python)

## Paso 4: Instalar las Dependencias del Proyecto

Una vez instalado Python, necesitas instalar las librerías que usa este proyecto:

1. Abre PowerShell en la carpeta del proyecto:
   ```powershell
   cd C:\Users\d508363\Documents\Martin\PYTHON
   ```

2. Crea un entorno virtual (recomendado):
   ```powershell
   python -m venv venv
   ```

3. Activa el entorno virtual:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   Si te da error de política de ejecución, ejecuta primero:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. Instala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

## Paso 5: Configurar MySQL

Antes de ejecutar la aplicación, necesitas:

1. **Instalar MySQL Server** (si no lo tienes):
   - Descarga desde: https://dev.mysql.com/downloads/mysql/
   - O instala XAMPP que incluye MySQL: https://www.apachefriends.org/

2. **Crear la base de datos**:
   - Abre MySQL Workbench o la línea de comandos de MySQL
   - Ejecuta el script: `database/schema.sql`

3. **Configurar las credenciales**:
   - Copia `config/.env.example` a `config/.env`
   - Edita `config/.env` con tus credenciales de MySQL

## Paso 6: Ejecutar la Aplicación

```powershell
python src/main.py
```

## Solución de Problemas

### Error: "python no se reconoce como comando"
- **Solución**: Reinstala Python y asegúrate de marcar "Add Python to PATH"
- O agrega Python manualmente al PATH del sistema

### Error al activar el entorno virtual
- Ejecuta: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Luego intenta activar de nuevo

### Error de conexión a MySQL
- Verifica que MySQL esté corriendo
- Revisa las credenciales en `config/.env`
- Asegúrate de haber ejecutado `database/schema.sql`

## Versiones Recomendadas

- **Python**: 3.11 o 3.12 (las más estables)
- **MySQL**: 8.0 o superior

## Enlaces Útiles

- Python oficial: https://www.python.org/
- Documentación Python: https://docs.python.org/es/3/
- MySQL: https://dev.mysql.com/downloads/mysql/
- XAMPP (incluye MySQL): https://www.apachefriends.org/

