# Icono de la Aplicación

## ✅ Icono Configurado

La aplicación ahora tiene un icono personalizado que se muestra en:
- La barra de tareas de Windows
- La barra de título de las ventanas
- El acceso directo del escritorio (si se crea uno)

## 📁 Ubicación del Icono

El archivo `icono.ico` se encuentra en la raíz del proyecto:
```
prueba-PP-master/
  └── icono.ico
```

## 🎨 Características del Icono

- **Tamaño**: 256x256 píxeles (con múltiples resoluciones: 16, 32, 64, 128, 256)
- **Formato**: .ico (formato estándar de Windows)
- **Diseño**: Calendario/evento sobre fondo azul oscuro (#1f4e79)

## 🔧 Generar el Icono

Si necesitas regenerar el icono, ejecuta:

```bash
python crear_icono.py
```

**Requisitos**: Necesitas tener instalado Pillow:
```bash
pip install Pillow
```

## 📝 Notas

- El icono se carga automáticamente al iniciar la aplicación
- Si el icono no se encuentra, la aplicación funcionará normalmente sin él
- El icono se aplica a todas las ventanas de la aplicación (login, principal, etc.)

## 🖼️ Personalizar el Icono

Si quieres usar tu propio icono:

1. Crea o descarga una imagen de 256x256 píxeles
2. Conviértela a formato .ico usando:
   - Herramientas online: https://convertio.co/es/png-ico/
   - O usa el script `crear_icono.py` modificándolo
3. Reemplaza el archivo `icono.ico` en la raíz del proyecto

