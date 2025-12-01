# Cómo Ejecutar la Aplicación

## ✅ Python está instalado correctamente

Tienes:
- Python 3.14.0 ✓
- pip 25.2 ✓

## 📋 Pasos para ejecutar la aplicación

### Paso 1: Ir al directorio del proyecto

```powershell
cd C:\Users\d508363\Documents\Martin\PYTHON
```

### Paso 2: Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

Esto instalará:
- mysql-connector-python
- pandas
- reportlab
- python-dotenv
- bcrypt

### Paso 3: Configurar la base de datos (si no lo has hecho)

1. Asegúrate de que MySQL esté instalado y corriendo
2. Ejecuta el script SQL: `database/schema.sql`
3. Configura las credenciales en `config/config.py` o crea un archivo `.env`

### Paso 4: Ejecutar la aplicación

```powershell
python src/main.py
```

---

## ⚠️ Si hay errores

### Error: "No module named 'mysql'"
```powershell
python -m pip install mysql-connector-python
```

### Error: "No module named 'pandas'"
```powershell
python -m pip install pandas
```

### Error: "No module named 'reportlab'"
```powershell
python -m pip install reportlab
```

### Error de conexión a MySQL
- Verifica que MySQL esté corriendo
- Revisa las credenciales en `config/config.py`
- Asegúrate de haber ejecutado `database/schema.sql`

---

## 🚀 Comandos rápidos

```powershell
# 1. Ir al proyecto
cd C:\Users\d508363\Documents\Martin\PYTHON

# 2. Instalar dependencias
python -m pip install -r requirements.txt

# 3. Ejecutar
python src/main.py
```

