"""
Ventana de inicio de sesión
Basada en el diseño HTML diseno_login.html
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class LoginWindow:
    """Ventana de login con diseño moderno"""
    
    def __init__(self, root: tk.Tk, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Configura la ventana de login"""
        self.root.title("Gestor de Eventos Locales - Iniciar sesión")
        self.root.geometry("900x500")
        self.root.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores del diseño
        self.bg_gradient = "#1f4e79"  # Azul oscuro
        self.bg_light = "#f9fafb"     # Gris claro
        self.bg_white = "#ffffff"
        self.text_primary = "#1f4e79"
        self.text_secondary = "#6b7280"
        self.border_color = "#d1d5db"
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal con fondo
        main_frame = tk.Frame(self.root, bg=self.bg_light)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Container (simula el grid del HTML)
        container = tk.Frame(main_frame, bg=self.bg_light, relief=tk.FLAT)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo (info)
        info_panel = tk.Frame(container, bg=self.bg_gradient)
        info_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_info_panel(info_panel)
        
        # Panel derecho (login)
        login_panel = tk.Frame(container, bg=self.bg_white)
        login_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_login_panel(login_panel)
    
    def create_info_panel(self, parent):
        """Crea el panel de información izquierdo"""
        content_frame = tk.Frame(parent, bg=self.bg_gradient)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
        # Título
        title = tk.Label(
            content_frame,
            text="Gestor de Eventos Locales",
            font=("Arial", 18, "bold"),
            bg=self.bg_gradient,
            fg="white"
        )
        title.pack(anchor=tk.W, pady=(0, 12))
        
        # Descripción
        desc = tk.Label(
            content_frame,
            text="Accede a la aplicación para gestionar eventos, participantes e inscripciones en un entorno centralizado.",
            font=("Arial", 10),
            bg=self.bg_gradient,
            fg="white",
            wraplength=400,
            justify=tk.LEFT
        )
        desc.pack(anchor=tk.W, pady=(0, 10))
        
        # Lista de características
        features = [
            "Consulta y administra los eventos activos.",
            "Registra nuevos participantes y controla sus inscripciones.",
            "Genera informes en CSV y PDF para su distribución."
        ]
        
        for feature in features:
            label = tk.Label(
                content_frame,
                text=f"• {feature}",
                font=("Arial", 9),
                bg=self.bg_gradient,
                fg="white",
                anchor=tk.W,
                justify=tk.LEFT
            )
            label.pack(anchor=tk.W, pady=2)
        
        # Footer
        footer = tk.Label(
            content_frame,
            text="Solo personal autorizado. Si tienes problemas para acceder, contacta con el administrador.",
            font=("Arial", 8),
            bg=self.bg_gradient,
            fg="white",
            wraplength=400,
            justify=tk.LEFT
        )
        footer.pack(side=tk.BOTTOM, anchor=tk.W, pady=(18, 0))
    
    def create_login_panel(self, parent):
        """Crea el panel de login derecho"""
        content_frame = tk.Frame(parent, bg=self.bg_white)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=36, pady=32)
        
        # Título
        title = tk.Label(
            content_frame,
            text="Iniciar sesión",
            font=("Arial", 11, "bold"),
            bg=self.bg_white,
            fg=self.text_primary
        )
        title.pack(anchor=tk.W, pady=(0, 18))
        
        # Subtítulo
        subtitle = tk.Label(
            content_frame,
            text="Introduce tus credenciales para acceder al gestor.",
            font=("Arial", 9),
            bg=self.bg_white,
            fg=self.text_secondary
        )
        subtitle.pack(anchor=tk.W, pady=(0, 22))
        
        # Campo Usuario
        user_label = tk.Label(
            content_frame,
            text="Usuario",
            font=("Arial", 9),
            bg=self.bg_white,
            fg="#374151"
        )
        user_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.username_entry = tk.Entry(
            content_frame,
            font=("Arial", 9),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            bg="#f9fafb",
            insertbackground="#111827"  # Color del cursor
        )
        self.username_entry.pack(fill=tk.X, pady=(0, 16))
        self.username_entry.insert(0, "nombre.de.usuario")
        self.username_entry.config(fg=self.text_secondary)
        self.username_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(self.username_entry))
        self.username_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(self.username_entry))
        self.username_entry.bind('<Button-1>', lambda e: self.on_entry_click(self.username_entry))  # Al hacer clic
        
        # Campo Contraseña
        pass_label = tk.Label(
            content_frame,
            text="Contraseña",
            font=("Arial", 9),
            bg=self.bg_white,
            fg="#374151"
        )
        pass_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.password_entry = tk.Entry(
            content_frame,
            font=("Arial", 9),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            show="•",
            bg="#f9fafb",
            insertbackground="#111827"  # Color del cursor
        )
        self.password_entry.pack(fill=tk.X, pady=(0, 12))
        self.password_entry.insert(0, "••••••••")
        self.password_entry.config(fg=self.text_secondary)
        self.password_entry.bind('<FocusIn>', lambda e: self.on_password_focus_in())
        self.password_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(self.password_entry))
        self.password_entry.bind('<Button-1>', lambda e: self.on_password_click())  # Al hacer clic
        
        # Checkbox y link
        help_frame = tk.Frame(content_frame, bg=self.bg_white)
        help_frame.pack(fill=tk.X, pady=(0, 12))
        
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(
            help_frame,
            text="Recordar mi usuario",
            font=("Arial", 8),
            bg=self.bg_white,
            fg=self.text_secondary,
            variable=self.remember_var,
            selectcolor=self.bg_white
        )
        remember_check.pack(side=tk.LEFT)
        
        forgot_link = tk.Label(
            help_frame,
            text="¿Has olvidado la contraseña?",
            font=("Arial", 8),
            bg=self.bg_white,
            fg="#2563eb",
            cursor="hand2"
        )
        forgot_link.pack(side=tk.RIGHT)
        
        # Botón Entrar
        btn_enter = tk.Button(
            content_frame,
            text="Entrar",
            font=("Arial", 10, "bold"),
            bg=self.bg_gradient,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=10,
            command=self.handle_login
        )
        btn_enter.pack(fill=tk.X, pady=(4, 10))
        
        # Botón Registrarse
        btn_register = tk.Button(
            content_frame,
            text="Registrarse",
            font=("Arial", 10, "bold"),
            bg=self.bg_white,
            fg=self.text_primary,
            relief=tk.SOLID,
            borderwidth=1,
            cursor="hand2",
            padx=16,
            pady=10,
            command=self.handle_register
        )
        btn_register.pack(fill=tk.X, pady=(0, 18))
        
        # Separador
        separator = tk.Label(
            content_frame,
            text="o",
            font=("Arial", 8),
            bg=self.bg_white,
            fg="#9ca3af"
        )
        separator.pack(pady=(0, 8))
        
        # Footer
        footer = tk.Label(
            content_frame,
            text="Acceso restringido. Esta pantalla es un diseño de ejemplo para la memoria del proyecto.",
            font=("Arial", 8),
            bg=self.bg_white,
            fg="#9ca3af",
            wraplength=300
        )
        footer.pack()
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.handle_login())
    
    def on_entry_click(self, entry):
        """Maneja el clic en el campo de entrada"""
        if entry.get() in ["nombre.de.usuario"]:
            entry.delete(0, tk.END)
            entry.config(fg="#111827")
            entry.focus_set()
    
    def on_password_click(self):
        """Maneja el clic en el campo de contraseña"""
        if self.password_entry.get() == "••••••••":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(fg="#111827", show="•")
            self.password_entry.focus_set()
    
    def on_entry_focus_in(self, entry):
        """Maneja el foco en los campos de entrada"""
        if entry.get() in ["nombre.de.usuario", "••••••••"]:
            entry.delete(0, tk.END)
            entry.config(fg="#111827")
    
    def on_password_focus_in(self):
        """Maneja el foco en el campo de contraseña"""
        if self.password_entry.get() == "••••••••":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(fg="#111827", show="•")
    
    def on_entry_focus_out(self, entry):
        """Maneja la pérdida de foco"""
        if not entry.get():
            if entry == self.username_entry:
                entry.insert(0, "nombre.de.usuario")
                entry.config(fg=self.text_secondary)
            elif entry == self.password_entry:
                entry.insert(0, "••••••••")
                entry.config(fg=self.text_secondary, show="")
    
    def handle_login(self):
        """Maneja el intento de login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Validación básica
        if not username or username == "nombre.de.usuario":
            messagebox.showerror("Error", "Por favor, introduce tu nombre de usuario")
            return
        
        if not password or password == "••••••••":
            messagebox.showerror("Error", "Por favor, introduce tu contraseña")
            return
        
        # Intentar conectar a MySQL
        db = self.try_connect_database()
        
        if not db or not db.pool:
            # Modo demo: permitir login sin validación
            messagebox.showwarning(
                "Modo Demo",
                "No hay conexión a la base de datos.\n\n"
                "Se iniciará sesión en modo DEMO sin validación."
            )
            self.on_login_success(username, None, 'user')  # Modo demo: rol por defecto 'user'
            return
        
        # Validar credenciales contra la base de datos
        from src.controllers.auth_controller import AuthController
        
        auth_controller = AuthController(db)
        success, user_data, error_msg = auth_controller.login(username, password)
        
        if success:
            # Login exitoso - pasar también el rol
            self.on_login_success(username, db, user_data.get('role', 'user') if user_data else 'user')
        else:
            # Mostrar error de autenticación
            messagebox.showerror("Error de autenticación", error_msg or "Usuario o contraseña incorrectos")
    
    def try_connect_database(self):
        """Intenta conectar a la base de datos (no bloquea la interfaz)"""
        try:
            from src.database.db_connection import DatabaseConnection
            db = DatabaseConnection()
            if db and db.pool:
                if db.test_connection():
                    return db
            return None
        except Exception:
            # Si falla, retornar None (modo demo)
            return None
    
    def handle_register(self):
        """Abre la ventana de registro"""
        # Intentar conectar a la base de datos primero
        db = self.try_connect_database()
        
        if not db or not db.pool:
            messagebox.showerror(
                "Error",
                "No hay conexión a la base de datos.\n\n"
                "Por favor, asegúrate de que MySQL esté ejecutándose para poder registrarte."
            )
            return
        
        # Abrir ventana de registro
        from src.views.register_window import RegisterWindow
        
        def on_register_complete(username):
            # Después del registro, llenar el campo de usuario
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, username)
            self.username_entry.config(fg="#111827")
            self.password_entry.focus_set()
        
        RegisterWindow(self.root, db, on_register_complete)


