"""
Vista de usuarios
Basada en el diseño de otras vistas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.views.styles import COLORS
from src.models.user import User


class UserView:
    """Vista completa de gestión de usuarios"""
    
    def __init__(self, parent, user_controller, is_admin=False):
        self.parent = parent
        self.user_controller = user_controller
        self.is_admin = is_admin
        self.current_user = None
        self.create_widgets()
        self.load_users()
    
    def create_widgets(self):
        """Crea los widgets de la vista"""
        # Header con título y botones
        header_frame = tk.Frame(self.parent, bg=COLORS['background'])
        header_frame.pack(fill=tk.X, pady=(0, 16))
        
        title = tk.Label(
            header_frame,
            text="Usuarios",
            font=("Arial", 14, "bold"),
            bg=COLORS['background'],
            fg=COLORS['text_primary']
        )
        title.pack(side=tk.LEFT)
        
        actions_frame = tk.Frame(header_frame, bg=COLORS['background'])
        actions_frame.pack(side=tk.RIGHT)
        
        btn_new = tk.Button(
            actions_frame,
            text="+ Nuevo usuario",
            font=("Arial", 9),
            bg=COLORS['primary'],
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.show_new_user_modal,
            state=tk.NORMAL if self.is_admin else tk.DISABLED
        )
        btn_new.pack(side=tk.LEFT, padx=4)
        self.btn_new = btn_new
        
        # Filtros
        filters_frame = tk.Frame(self.parent, bg=COLORS['background'])
        filters_frame.pack(fill=tk.X, pady=(0, 12))
        
        self.search_entry = tk.Entry(
            filters_frame,
            font=("Arial", 9),
            relief=tk.SOLID,
            borderwidth=1,
            width=30
        )
        self.search_entry.pack(side=tk.LEFT, padx=(0, 8))
        self.search_entry.insert(0, "Buscar por nombre de usuario")
        self.search_entry.config(fg=COLORS['text_secondary'])
        self.search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in())
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_users())
        
        self.role_filter = ttk.Combobox(
            filters_frame,
            values=["Todos los roles", "Admin", "User"],
            state="readonly",
            width=20,
            font=("Arial", 9)
        )
        self.role_filter.current(0)
        self.role_filter.pack(side=tk.LEFT, padx=4)
        self.role_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_users())
        
        # Tabla de usuarios
        self.create_table()
    
    def create_table(self):
        """Crea la tabla de usuarios"""
        table_container = tk.Frame(self.parent, bg=COLORS['white'], relief=tk.FLAT)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Frame para scrollbar y tabla
        table_frame = tk.Frame(table_container, bg=COLORS['white'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (tabla)
        columns = ("Usuario", "Rol", "Fecha de creación")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading("Usuario", text="USUARIO")
        self.tree.heading("Rol", text="ROL")
        self.tree.heading("Fecha de creación", text="FECHA DE CREACIÓN")
        
        self.tree.column("Usuario", width=200)
        self.tree.column("Rol", width=150)
        self.tree.column("Fecha de creación", width=200)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind doble clic para editar
        self.tree.bind('<Double-1>', lambda e: self.edit_selected_user())
        
        # Botones de acción globales
        actions_frame = tk.Frame(table_container, bg=COLORS['table_header'])
        actions_frame.pack(fill=tk.X)
        
        btn_view = tk.Button(
            actions_frame,
            text="Ver",
            font=("Arial", 8),
            bg="#e5e7eb",
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self.view_selected_user
        )
        btn_view.pack(side=tk.LEFT, padx=4, pady=10)
        
        btn_edit = tk.Button(
            actions_frame,
            text="Editar",
            font=("Arial", 8),
            bg="#e5e7eb",
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self.edit_selected_user,
            state=tk.NORMAL if self.is_admin else tk.DISABLED
        )
        btn_edit.pack(side=tk.LEFT, padx=4)
        self.btn_edit = btn_edit
        
        btn_delete = tk.Button(
            actions_frame,
            text="Eliminar",
            font=("Arial", 8),
            bg="#e5e7eb",
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self.delete_selected_user,
            state=tk.NORMAL if self.is_admin else tk.DISABLED
        )
        btn_delete.pack(side=tk.LEFT, padx=4)
        self.btn_delete = btn_delete
    
    def load_users(self):
        """Carga los usuarios en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Verificar que hay controlador
        if not self.user_controller:
            messagebox.showinfo(
                "Modo Demo",
                "No hay conexión a la base de datos.\n\n"
                "La vista está disponible pero no se pueden cargar datos."
            )
            return
        
        try:
            # Obtener usuarios
            users = self.user_controller.get_all()
            
            if not users:
                return
            
            # Cargar usuarios en la tabla
            for user in users:
                created_at_str = ""
                if user.created_at:
                    if isinstance(user.created_at, datetime):
                        created_at_str = user.created_at.strftime("%d/%m/%Y %H:%M")
                    else:
                        try:
                            created_at_str = datetime.strptime(str(user.created_at), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
                        except:
                            created_at_str = str(user.created_at)
                
                role_display = "Administrador" if user.role == "admin" else "Usuario"
                
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        user.username,
                        role_display,
                        created_at_str
                    ),
                    tags=(user.role,)
                )
            
            # Configurar colores de tags
            self.tree.tag_configure("admin", foreground=COLORS['primary'])
            self.tree.tag_configure("user", foreground=COLORS['text_primary'])
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {str(e)}")
    
    def filter_users(self):
        """Filtra los usuarios según los criterios"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener usuarios
        if not self.user_controller:
            return
        
        try:
            users = self.user_controller.get_all()
            
            # Aplicar filtro de búsqueda
            search_text = self.search_entry.get().lower()
            if search_text and search_text != "buscar por nombre de usuario":
                users = [u for u in users if search_text in (u.username or "").lower()]
            
            # Aplicar filtro de rol
            role_filter = self.role_filter.get()
            if role_filter == "Admin":
                users = [u for u in users if u.role == "admin"]
            elif role_filter == "User":
                users = [u for u in users if u.role == "user"]
            
            # Mostrar usuarios filtrados
            for user in users:
                created_at_str = ""
                if user.created_at:
                    if isinstance(user.created_at, datetime):
                        created_at_str = user.created_at.strftime("%d/%m/%Y %H:%M")
                    else:
                        try:
                            created_at_str = datetime.strptime(str(user.created_at), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
                        except:
                            created_at_str = str(user.created_at)
                
                role_display = "Administrador" if user.role == "admin" else "Usuario"
                
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        user.username,
                        role_display,
                        created_at_str
                    ),
                    tags=(user.role,)
                )
            
            # Configurar colores de tags
            self.tree.tag_configure("admin", foreground=COLORS['primary'])
            self.tree.tag_configure("user", foreground=COLORS['text_primary'])
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar usuarios: {str(e)}")
    
    def on_search_focus_in(self):
        """Limpia el placeholder cuando se enfoca el campo de búsqueda"""
        if self.search_entry.get() == "Buscar por nombre de usuario":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=COLORS['text_primary'])
    
    def get_selected_user(self) -> User:
        """Obtiene el usuario seleccionado en la tabla"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario")
            return None
        
        item = self.tree.item(selection[0])
        username = item['values'][0]
        
        if not self.user_controller:
            return None
        
        return self.user_controller.get_by_username(username)
    
    def view_selected_user(self):
        """Ver detalles del usuario seleccionado"""
        user = self.get_selected_user()
        if not user:
            return
        
        self.show_user_details_modal(user)
    
    def edit_selected_user(self):
        """Editar el usuario seleccionado"""
        if not self.is_admin:
            messagebox.showwarning("Permiso denegado", "Solo los administradores pueden editar usuarios")
            return
        
        user = self.get_selected_user()
        if not user:
            return
        
        self.show_user_modal(user)
    
    def delete_selected_user(self):
        """Eliminar el usuario seleccionado"""
        if not self.is_admin:
            messagebox.showwarning("Permiso denegado", "Solo los administradores pueden eliminar usuarios")
            return
        
        user = self.get_selected_user()
        if not user:
            return
        
        result = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar al usuario '{user.username}'?\n\n"
            "Esta acción no se puede deshacer."
        )
        
        if result:
            if self.user_controller.delete(user.user_id):
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                self.load_users()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario")
    
    def show_new_user_modal(self):
        """Muestra el modal para nuevo usuario"""
        self.show_user_modal(None)
    
    def show_user_modal(self, user: User = None):
        """Muestra el modal de creación/edición de usuario"""
        modal = tk.Toplevel(self.parent)
        modal.title("Nuevo usuario" if not user else "Editar usuario")
        modal.geometry("450x400")
        modal.resizable(False, False)
        modal.configure(bg=COLORS['white'])
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (450 // 2)
        y = (modal.winfo_screenheight() // 2) - (400 // 2)
        modal.geometry(f'450x400+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg=COLORS['primary'], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="Nuevo usuario" if not user else "Editar usuario",
            font=("Arial", 10, "bold"),
            bg=COLORS['primary'],
            fg="white"
        )
        header_label.pack(pady=12)
        
        # Body
        body = tk.Frame(modal, bg=COLORS['white'])
        body.pack(fill=tk.BOTH, expand=True, padx=18, pady=14)
        
        # Campos del formulario
        self.modal_entries = {}
        
        # Usuario
        row1 = tk.Frame(body, bg=COLORS['white'])
        row1.pack(fill=tk.X, pady=8)
        tk.Label(row1, text="Usuario *", font=("Arial", 9), bg=COLORS['white'], fg="#4b5563", width=18, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 8))
        entry_username = tk.Entry(row1, font=("Arial", 9), relief=tk.SOLID, borderwidth=1)
        entry_username.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.modal_entries['username'] = entry_username
        
        # Contraseña
        row2 = tk.Frame(body, bg=COLORS['white'])
        row2.pack(fill=tk.X, pady=8)
        tk.Label(row2, text="Contraseña *" if not user else "Nueva contraseña", font=("Arial", 9), bg=COLORS['white'], fg="#4b5563", width=18, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 8))
        entry_password = tk.Entry(row2, font=("Arial", 9), relief=tk.SOLID, borderwidth=1, show="*")
        entry_password.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.modal_entries['password'] = entry_password
        
        # Confirmar contraseña
        row3 = tk.Frame(body, bg=COLORS['white'])
        row3.pack(fill=tk.X, pady=8)
        tk.Label(row3, text="Confirmar contraseña *" if not user else "Confirmar nueva contraseña", font=("Arial", 9), bg=COLORS['white'], fg="#4b5563", width=18, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 8))
        entry_confirm = tk.Entry(row3, font=("Arial", 9), relief=tk.SOLID, borderwidth=1, show="*")
        entry_confirm.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.modal_entries['confirm_password'] = entry_confirm
        
        # Rol
        row4 = tk.Frame(body, bg=COLORS['white'])
        row4.pack(fill=tk.X, pady=8)
        tk.Label(row4, text="Rol *", font=("Arial", 9), bg=COLORS['white'], fg="#4b5563", width=18, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 8))
        combo_role = ttk.Combobox(row4, values=["user", "admin"], state="readonly", font=("Arial", 9))
        combo_role.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.modal_entries['role'] = combo_role
        
        # Rellenar campos si es edición
        if user:
            entry_username.insert(0, user.username or "")
            entry_username.config(state=tk.DISABLED)  # No permitir cambiar el username
            if user.role == "admin":
                combo_role.current(1)
            else:
                combo_role.current(0)
        
        # Footer con botones
        footer = tk.Frame(modal, bg=COLORS['table_header'])
        footer.pack(fill=tk.X, padx=18, pady=(0, 14))
        
        btn_cancel = tk.Button(
            footer,
            text="Cancelar",
            font=("Arial", 9),
            bg=COLORS['white'],
            fg="#374151",
            relief=tk.SOLID,
            borderwidth=1,
            padx=14,
            pady=7,
            cursor="hand2",
            command=modal.destroy
        )
        btn_cancel.pack(side=tk.RIGHT, padx=6)
        
        btn_save = tk.Button(
            footer,
            text="Guardar",
            font=("Arial", 9),
            bg=COLORS['primary'],
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=7,
            cursor="hand2",
            command=lambda: self.save_user(user, modal)
        )
        btn_save.pack(side=tk.RIGHT)
    
    def save_user(self, user: User, modal):
        """Guarda el usuario"""
        try:
            # Obtener valores
            username = self.modal_entries['username'].get().strip()
            password = self.modal_entries['password'].get()
            confirm_password = self.modal_entries['confirm_password'].get()
            role = self.modal_entries['role'].get()
            
            # Validaciones
            if not username:
                messagebox.showerror("Error", "El nombre de usuario es obligatorio")
                return
            
            if not user:  # Nuevo usuario
                if not password:
                    messagebox.showerror("Error", "La contraseña es obligatoria")
                    return
                
                if password != confirm_password:
                    messagebox.showerror("Error", "Las contraseñas no coinciden")
                    return
                
                if len(password) < 6:
                    messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
                    return
            else:  # Editar usuario
                if password:  # Si se proporciona nueva contraseña
                    if password != confirm_password:
                        messagebox.showerror("Error", "Las contraseñas no coinciden")
                        return
                    
                    if len(password) < 6:
                        messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
                        return
            
            # Crear o actualizar usuario
            if user:
                user.role = role
                if password:
                    if self.user_controller.update(user, new_password=password):
                        messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                        modal.destroy()
                        self.load_users()
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar el usuario")
                else:
                    if self.user_controller.update(user):
                        messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                        modal.destroy()
                        self.load_users()
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar el usuario")
            else:
                new_user = User(
                    username=username,
                    role=role
                )
                
                user_id = self.user_controller.create(new_user, password)
                if user_id:
                    messagebox.showinfo("Éxito", "Usuario creado correctamente")
                    modal.destroy()
                    self.load_users()
                else:
                    messagebox.showerror("Error", "No se pudo crear el usuario (posiblemente el nombre de usuario ya existe)")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def show_user_details_modal(self, user: User):
        """Muestra los detalles del usuario en una ventana modal bonita"""
        modal = tk.Toplevel(self.parent)
        modal.title(f"Detalles del Usuario: {user.username}")
        modal.geometry("650x550")
        modal.resizable(True, True)
        modal.minsize(600, 500)
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (650 // 2)
        y = (modal.winfo_screenheight() // 2) - (550 // 2)
        modal.geometry(f"650x550+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(modal, bg=COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header con color
        header = tk.Frame(main_frame, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="👤 Detalles del Usuario",
            font=("Arial", 16, "bold"),
            bg=COLORS['primary'],
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Contenido
        content = tk.Frame(main_frame, bg=COLORS['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Nombre de usuario
        username_label = tk.Label(
            content,
            text=user.username,
            font=("Arial", 18, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary'],
            wraplength=580
        )
        username_label.pack(anchor=tk.W, pady=(0, 24))
        
        # Información en cards
        info_frame = tk.Frame(content, bg=COLORS['white'])
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos de información
        role_display = "Administrador" if user.role == "admin" else "Usuario"
        role_color = COLORS['primary'] if user.role == "admin" else COLORS['text_primary']
        
        created_at_str = ""
        if user.created_at:
            if isinstance(user.created_at, datetime):
                created_at_str = user.created_at.strftime("%d/%m/%Y %H:%M")
            else:
                try:
                    created_at_str = datetime.strptime(str(user.created_at), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
                except:
                    created_at_str = str(user.created_at)
        
        fields = [
            ("👤 Nombre de usuario", user.username, False),
            ("🔑 Rol", role_display, False, COLORS['primary'] if user.role == "admin" else COLORS['white'], role_color),
            ("📅 Fecha de creación", created_at_str or "No especificada", False)
        ]
        
        for field_data in fields:
            if len(field_data) == 5:  # Con colores personalizados
                label_text, value, is_multiline, bg_color, fg_color = field_data
            else:
                label_text, value, is_multiline = field_data
                bg_color = COLORS['white']
                fg_color = COLORS['text_primary']
            
            field_frame = tk.Frame(info_frame, bg=COLORS['white'])
            field_frame.pack(fill=tk.X, pady=(0, 16))
            
            label = tk.Label(
                field_frame,
                text=label_text,
                font=("Arial", 10, "bold"),
                bg=COLORS['white'],
                fg=COLORS['text_secondary'],
                anchor=tk.W
            )
            label.pack(anchor=tk.W, pady=(0, 4))
            
            value_label = tk.Label(
                field_frame,
                text=value,
                font=("Arial", 11),
                bg=bg_color,
                fg=fg_color,
                anchor=tk.W,
                padx=12,
                pady=8,
                relief=tk.FLAT if bg_color != COLORS['white'] else tk.SOLID,
                borderwidth=1 if bg_color == COLORS['white'] else 0
            )
            value_label.pack(anchor=tk.W, fill=tk.X)
        
        # Botón cerrar
        btn_close = tk.Button(
            content,
            text="Cerrar",
            font=("Arial", 10, "bold"),
            bg=COLORS['primary'],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=24,
            pady=10,
            command=modal.destroy
        )
        btn_close.pack(pady=(20, 0))
        
        modal.bind('<Escape>', lambda e: modal.destroy())

