"""
Script para crear el icono de la aplicación
Genera un icono .ico a partir de una imagen o crea uno simple
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def crear_icono_simple():
        """Crea un icono simple con un calendario/evento"""
        # Crear imagen de 256x256 (tamaño estándar para iconos)
        size = 256
        img = Image.new('RGBA', (size, size), (31, 78, 121, 255))  # Color azul oscuro #1f4e79
        draw = ImageDraw.Draw(img)
        
        # Dibujar un círculo blanco (representando un evento)
        margin = 40
        draw.ellipse([margin, margin, size - margin, size - margin], 
                    fill=(255, 255, 255, 255), outline=(255, 255, 255, 255), width=5)
        
        # Dibujar un calendario simple
        # Marco del calendario
        cal_x = size // 2 - 60
        cal_y = size // 2 - 40
        cal_w = 120
        cal_h = 100
        
        # Parte superior del calendario (mes)
        draw.rectangle([cal_x, cal_y, cal_x + cal_w, cal_y + 30], 
                      fill=(220, 38, 38, 255))  # Rojo para el mes
        
        # Parte principal del calendario
        draw.rectangle([cal_x, cal_y + 30, cal_x + cal_w, cal_y + cal_h], 
                      fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
        
        # Líneas del calendario
        for i in range(1, 3):
            y = cal_y + 30 + (cal_h - 30) // 3 * i
            draw.line([cal_x, y, cal_x + cal_w, y], fill=(200, 200, 200, 255), width=1)
        
        for i in range(1, 3):
            x = cal_x + cal_w // 3 * i
            draw.line([x, cal_y + 30, x, cal_y + cal_h], fill=(200, 200, 200, 255), width=1)
        
        # Guardar como ICO
        icon_path = os.path.join(os.path.dirname(__file__), 'icono.ico')
        img.save(icon_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        print(f"Icono creado exitosamente en: {icon_path}")
        return icon_path
    
    if __name__ == "__main__":
        crear_icono_simple()
        
except ImportError:
    print("PIL/Pillow no está instalado.")
    print("Instálalo con: pip install Pillow")
    print("\nO puedes crear el icono manualmente:")
    print("1. Crea una imagen de 256x256 píxeles")
    print("2. Guárdala como 'icono.ico' en la raíz del proyecto")
    print("3. Puedes usar herramientas online como:")
    print("   - https://convertio.co/es/png-ico/")
    print("   - https://www.icoconverter.com/")

