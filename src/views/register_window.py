"""
Ventana de registro de nuevos usuarios
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class RegisterWindow:
    """Ventana de registro con diseño moderno"""
    
    def __init__(self, parent, db, on_register_success):
        self.parent = parent
        self.db = db
        self.on_register_success = on_register_success
        self.window = None
        self.create_window()
    
    def create_window(self):
        """Crea la ventana de registro"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Registrarse - Gestor de Eventos Locales")
        self.window.geometry("900x650")
        self.window.resizable(True, True)
        self.window.minsize(800, 550)
        
        # Centrar ventana
        self.center_window()
        
        # Colores del diseño
        self.bg_light = "#f9fafb"
        self.bg_white = "#ffffff"
        self.text_primary = "#1f4e79"
        self.text_secondary = "#6b7280"
        self.bg_gradient = "#1f4e79"
        
        self.create_widgets()
        
        # Hacer la ventana modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Actualizar scroll después de crear widgets
        self.window.after(100, self.update_scroll)
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def update_scroll(self):
        """Actualiza el área de scroll"""
        if hasattr(self, 'canvas'):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def create_widgets(self):
        """Crea los widgets de la interfaz con diseño de dos columnas"""
        # Frame principal
        main_frame = tk.Frame(self.window, bg=self.bg_light)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título principal
        title = tk.Label(
            main_frame,
            text="Crear nueva cuenta",
            font=("Arial", 18, "bold"),
            bg=self.bg_light,
            fg=self.text_primary
        )
        title.pack(pady=(0, 8))
        
        subtitle = tk.Label(
            main_frame,
            text="Completa los datos de participante y usuario para registrarte",
            font=("Arial", 10),
            bg=self.bg_light,
            fg=self.text_secondary
        )
        subtitle.pack(pady=(0, 24))
        
        # Frame para las dos columnas
        columns_frame = tk.Frame(main_frame, bg=self.bg_light)
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        # ========== COLUMNA IZQUIERDA: DATOS DE PARTICIPANTE ==========
        left_frame = tk.Frame(columns_frame, bg=self.bg_white, relief=tk.FLAT)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Título de la sección participante
        participant_title = tk.Label(
            left_frame,
            text="👤 Datos de Participante",
            font=("Arial", 14, "bold"),
            bg=self.bg_white,
            fg=self.text_primary
        )
        participant_title.pack(anchor=tk.W, padx=24, pady=(24, 8))
        
        participant_subtitle = tk.Label(
            left_frame,
            text="Información personal para tu perfil de participante",
            font=("Arial", 9),
            bg=self.bg_white,
            fg=self.text_secondary
        )
        participant_subtitle.pack(anchor=tk.W, padx=24, pady=(0, 24))
        
        # Container para campos de participante
        participant_container = tk.Frame(left_frame, bg=self.bg_white)
        participant_container.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))
        
        # Campo Nombre
        first_name_label = tk.Label(
            participant_container,
            text="Nombre *",
            font=("Arial", 9, "bold"),
            bg=self.bg_white,
            fg="#374151"
        )
        first_name_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.first_name_entry = tk.Entry(
            participant_container,
            font=("Arial", 10),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            bg="#f9fafb",
            insertbackground="#111827"
        )
        self.first_name_entry.pack(fill=tk.X, pady=(0, 16))
        self.first_name_entry.focus_set()
        
        # Campo Apellidos
        last_name_label = tk.Label(
            participant_container,
            text="Apellidos *",
            font=("Arial", 9, "bold"),
            bg=self.bg_white,
            fg="#374151"
        )
        last_name_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.last_name_entry = tk.Entry(
            participant_container,
            font=("Arial", 10),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            bg="#f9fafb",
            insertbackground="#111827"
        )
        self.last_name_entry.pack(fill=tk.X, pady=(0, 16))
        
        # Campo Email
        email_label = tk.Label(
            participant_container,
            text="Email *",
            font=("Arial", 9, "bold"),
            bg=self.bg_white,
            fg="#374151"
        )
        email_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.email_entry = tk.Entry(
            participant_container,
            font=("Arial", 10),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            bg="#f9fafb",
            insertbackground="#111827"
        )
        self.email_entry.pack(fill=tk.X, pady=(0, 16))
        
        # Campo Teléfono
        phone_label = tk.Label(
            participant_container,
            text="Teléfono (opcional)",
            font=("Arial", 9),
            bg=self.bg_white,
            fg="#374151"
        )
        phone_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.phone_entry = tk.Entry(
            participant_container,
            font=("Arial", 10),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            bg="#f9fafb",
            insertbackground="#111827"
        )
        self.phone_entry.pack(fill=tk.X, pady=(0, 16))
        
        # Campo DNI/NIE
        identifier_label = tk.Label(
            participant_container,
            text="DNI/NIE *",
            font=("Arial", 9, "bold"),
            bg=self.bg_white,
            fg="#374151"
        )
        identifier_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.identifier_entry = tk.Entry(
            participant_container,
            font=("Arial", 10),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            bg="#f9fafb",
            insertbackground="#111827"
        )
        self.identifier_entry.pack(fill=tk.X, pady=(0, 16))
        
        # ========== COLUMNA DERECHA: DATOS DE USUARIO ==========
        right_frame = tk.Frame(columns_frame, bg=self.bg_white, relief=tk.FLAT)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Título de la sección usuario
        user_title = tk.Label(
            right_frame,
            text="🔐 Datos de Usuario",
            font=("Arial", 14, "bold"),
            bg=self.bg_white,
            fg=self.text_primary
        )
        user_title.pack(anchor=tk.W, padx=24, pady=(24, 8))
        
        user_subtitle = tk.Label(
            right_frame,
            text="Credenciales para acceder al sistema",
            font=("Arial", 9),
            bg=self.bg_white,
            fg=self.text_secondary
        )
        user_subtitle.pack(anchor=tk.W, padx=24, pady=(0, 24))
        
        # Container para campos de usuario
        user_container = tk.Frame(right_frame, bg=self.bg_white)
        user_container.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))
        
        # Campo Usuario
        user_label = tk.Label(
            user_container,
            text="Nombre de usuario *",
            font=("Arial", 9, "bold"),
            bg=self.bg_white,
            fg="#374151"
        )
        user_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.username_entry = tk.Entry(
            user_container,
            font=("Arial", 10),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            bg="#f9fafb",
            insertbackground="#111827"
        )
        self.username_entry.pack(fill=tk.X, pady=(0, 16))
        
        # Campo Contraseña
        pass_label = tk.Label(
            user_container,
            text="Contraseña *",
            font=("Arial", 9, "bold"),
            bg=self.bg_white,
            fg="#374151"
        )
        pass_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.password_entry = tk.Entry(
            user_container,
            font=("Arial", 10),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            show="•",
            bg="#f9fafb",
            insertbackground="#111827"
        )
        self.password_entry.pack(fill=tk.X, pady=(0, 16))
        
        # Campo Confirmar Contraseña
        confirm_label = tk.Label(
            user_container,
            text="Confirmar contraseña *",
            font=("Arial", 9, "bold"),
            bg=self.bg_white,
            fg="#374151"
        )
        confirm_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.confirm_password_entry = tk.Entry(
            user_container,
            font=("Arial", 10),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            show="•",
            bg="#f9fafb",
            insertbackground="#111827"
        )
        self.confirm_password_entry.pack(fill=tk.X, pady=(0, 16))
        
        # Nota sobre campos obligatorios
        note_label = tk.Label(
            user_container,
            text="* Campos obligatorios",
            font=("Arial", 8),
            bg=self.bg_white,
            fg=self.text_secondary,
            anchor=tk.W
        )
        note_label.pack(anchor=tk.W, pady=(0, 16))
        
        # ========== BOTONES EN LA PARTE INFERIOR ==========
        buttons_frame = tk.Frame(main_frame, bg=self.bg_light)
        buttons_frame.pack(fill=tk.X, pady=(24, 0))
        
        # Botón Cancelar
        btn_cancel = tk.Button(
            buttons_frame,
            text="Cancelar",
            font=("Arial", 10),
            bg=self.bg_white,
            fg=self.text_primary,
            relief=tk.SOLID,
            borderwidth=1,
            cursor="hand2",
            padx=24,
            pady=12,
            command=self.window.destroy
        )
        btn_cancel.pack(side=tk.LEFT, padx=(0, 12))
        
        # Botón Aceptar/Registrarse
        btn_register = tk.Button(
            buttons_frame,
            text="✓ Aceptar y Registrarse",
            font=("Arial", 11, "bold"),
            bg=self.bg_gradient,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=32,
            pady=12,
            command=self.handle_register
        )
        btn_register.pack(side=tk.RIGHT)
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.handle_register())
        self.window.bind('<Escape>', lambda e: self.window.destroy())
    
    def handle_register(self):
        """Maneja el registro de usuario y participante"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Datos de participante
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        identifier = self.identifier_entry.get().strip()
        
        if not self.db or not self.db.pool:
            messagebox.showerror(
                "Error",
                "No hay conexión a la base de datos.\n\n"
                "Por favor, asegúrate de que MySQL esté ejecutándose."
            )
            return
        
        # Validar campos de participante
        if not first_name or not last_name or not email or not identifier:
            messagebox.showerror(
                "Error",
                "Por favor, completa todos los campos obligatorios:\n"
                "- Nombre\n"
                "- Apellidos\n"
                "- Email\n"
                "- DNI/NIE"
            )
            return
        
        # Validar email
        if '@' not in email:
            messagebox.showerror("Error", "Por favor, introduce un email válido")
            return
        
        # Validar teléfono si se proporciona
        phone_int = None
        if phone:
            try:
                phone_int = int(phone)
            except ValueError:
                messagebox.showerror("Error", "El teléfono debe ser un número válido")
                return
        
        # Importar controlador de autenticación
        from src.controllers.auth_controller import AuthController
        
        auth_controller = AuthController(self.db)
        success, error_msg = auth_controller.register(
            username, password, confirm_password,
            first_name, last_name, email, phone_int, identifier
        )
        
        if success:
            messagebox.showinfo(
                "Registro exitoso",
                f"Usuario '{username}' registrado correctamente.\n\n"
                "Tu perfil de participante también ha sido creado.\n"
                "Ahora puedes iniciar sesión con tus credenciales."
            )
            self.window.destroy()
            # Llamar callback si se proporcionó
            if self.on_register_success:
                self.on_register_success(username)
        else:
            messagebox.showerror("Error de registro", error_msg or "No se pudo registrar el usuario")
