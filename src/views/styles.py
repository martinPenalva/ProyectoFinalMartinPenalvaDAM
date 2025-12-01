"""
Estilos y colores para la aplicación
Basados en los diseños HTML
"""

import tkinter.ttk as ttk

# Colores principales del diseño
COLORS = {
    'primary': '#1f4e79',      # Azul oscuro (header, botones primarios)
    'sidebar': '#243447',      # Gris oscuro (sidebar)
    'sidebar_text': '#e0e6f0', # Texto sidebar
    'background': '#f4f6f9',   # Fondo principal
    'white': '#ffffff',
    'text_primary': '#1f2933',
    'text_secondary': '#6b7280',
    'border': '#d1d5db',
    'success': '#d1fae5',      # Tag success
    'success_text': '#065f46',
    'warning': '#fef3c7',      # Tag warning
    'warning_text': '#92400e',
    'danger': '#fee2e2',       # Tag danger
    'danger_text': '#991b1b',
    'badge': '#e0f2fe',        # Badge azul
    'badge_text': '#075985',
    'table_header': '#f9fafb',
    'table_row_even': '#f9fafb',
}


def configure_styles():
    """Configura los estilos de ttk"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Botón primario
    style.configure(
        'Primary.TButton',
        background=COLORS['primary'],
        foreground='white',
        borderwidth=0,
        focuscolor='none',
        padding=(8, 6)
    )
    style.map(
        'Primary.TButton',
        background=[('active', '#2563eb'), ('pressed', '#1e40af')]
    )
    
    # Botón outline
    style.configure(
        'Outline.TButton',
        background=COLORS['white'],
        foreground=COLORS['primary'],
        borderwidth=1,
        relief='solid',
        padding=(8, 6)
    )
    style.map(
        'Outline.TButton',
        background=[('active', COLORS['background'])]
    )
    
    # Botón secundario
    style.configure(
        'Secondary.TButton',
        background=COLORS['white'],
        foreground=COLORS['text_primary'],
        borderwidth=1,
        relief='solid',
        padding=(6, 4)
    )
    
    return style

