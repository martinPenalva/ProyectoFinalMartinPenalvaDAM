"""
Ventana principal de la aplicación
Interfaz gráfica principal con menú lateral
Basada en los diseños HTML
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.database.db_connection import DatabaseConnection
from src.controllers.event_controller import EventController
from src.controllers.participant_controller import ParticipantController
from src.controllers.registration_controller import RegistrationController
from src.controllers.user_controller import UserController
from config.config import APP_CONFIG
from src.views.styles import COLORS

# Importar vistas
try:
    from src.views.event_view import EventView
    from src.views.participant_view import ParticipantView
    from src.views.user_view import UserView
except ImportError:
    EventView = None
    ParticipantView = None
    UserView = None


class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self, root: tk.Tk, db=None, username: str = "Admin", on_logout=None, user_role: str = 'user'):
        self.root = root
        self.db = db
        self.username = username
        self.user_role = user_role  # 'admin' o 'user'
        self.is_admin = (user_role == 'admin')  # Flag para verificar si es admin
        self.current_view = None
        self.active_menu_item = None
        self.on_logout = on_logout  # Callback para logout
        
        # Controladores (solo si hay base de datos)
        if db is not None and hasattr(db, 'pool') and db.pool:  # Verificar que el pool existe
            try:
                self.event_controller = EventController(db)
                self.participant_controller = ParticipantController(db)
                self.registration_controller = RegistrationController(db)
                self.user_controller = UserController(db)
            except Exception as e:
                # Si hay error al crear controladores, usar None
                print(f"Advertencia: No se pudieron crear controladores: {e}")
                self.event_controller = None
                self.participant_controller = None
                self.registration_controller = None
                self.user_controller = None
        else:
            # Modo demo sin base de datos
            self.event_controller = None
            self.participant_controller = None
            self.registration_controller = None
            self.user_controller = None
        
        try:
            print("Configurando ventana...")
            self.setup_window()
            print("Creando widgets...")
            self.create_widgets()
            print("Widgets creados exitosamente")
        except Exception as e:
            error_msg = f"Error al crear widgets: {e}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            # Mostrar mensaje de error en la ventana
            try:
                error_label = tk.Label(
                    self.root,
                    text=f"Error al crear la interfaz:\n{str(e)}\n\nRevisa la consola.",
                    font=("Arial", 10),
                    bg="#f4f6f9",
                    fg="red",
                    justify=tk.LEFT,
                    wraplength=600
                )
                error_label.pack(pady=50, padx=50)
            except:
                # Si ni siquiera podemos mostrar el error, al menos imprimirlo
                print("No se pudo mostrar el error en la ventana")
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title(APP_CONFIG['title'])
        self.root.geometry(f"{APP_CONFIG['window_width']}x{APP_CONFIG['window_height']}")
        self.root.minsize(APP_CONFIG['min_window_width'], APP_CONFIG['min_window_height'])
        self.root.configure(bg=COLORS['background'])
        
        # Centrar ventana
        self.center_window()
    
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
        try:
            print("Creando header...")
            # Header
            self.create_header()
            print("Header creado")
            
            # Layout principal (sidebar + content)
            print("Creando layout_frame...")
            layout_frame = tk.Frame(self.root, bg=COLORS['background'])
            layout_frame.pack(fill=tk.BOTH, expand=True)
            print("Layout frame creado")
            
            # Sidebar
            print("Creando sidebar...")
            try:
                self.create_sidebar(layout_frame)
                print("Sidebar creado")
            except Exception as e:
                print(f"Error al crear sidebar: {e}")
                import traceback
                traceback.print_exc()
                raise
            
            # Content area
            print("Creando content_frame...")
            self.content_frame = tk.Frame(layout_frame, bg=COLORS['background'])
            self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=32, pady=24)
            print("Content frame creado")
            
            # Mostrar vista de inicio por defecto
            print("Mostrando vista de inicio...")
            try:
                self.show_home()
                print("Vista de inicio mostrada")
            except Exception as e:
                print(f"Error al mostrar inicio: {e}")
                import traceback
                traceback.print_exc()
                # Mostrar mensaje de error en lugar de contenido
                error_label = tk.Label(
                    self.content_frame,
                    text=f"Error al cargar contenido:\n{str(e)}",
                    font=("Arial", 10),
                    bg=COLORS['background'],
                    fg="red"
                )
                error_label.pack(pady=50)
            
            # Forzar actualización de la ventana
            print("Actualizando ventana...")
            self.root.update_idletasks()
            self.root.update()
            print("Ventana actualizada")
        except Exception as e:
            error_msg = f"Error en create_widgets: {e}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            # Mostrar error visible
            try:
                error_frame = tk.Frame(self.root, bg="#f4f6f9")
                error_frame.pack(fill=tk.BOTH, expand=True)
                error_label = tk.Label(
                    error_frame,
                    text=f"Error al crear la interfaz:\n{str(e)}\n\nRevisa la consola para más detalles.",
                    font=("Arial", 10),
                    bg="#f4f6f9",
                    fg="red",
                    justify=tk.LEFT,
                    wraplength=600
                )
                error_label.pack(pady=50, padx=50)
            except:
                print("No se pudo mostrar el error en la ventana")
    
    def create_header(self):
        """Crea el header superior"""
        header = tk.Frame(self.root, bg=COLORS['primary'], height=56)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="Gestor de Eventos Locales",
            font=("Arial", 12, "bold"),
            bg=COLORS['primary'],
            fg="white"
        )
        title.pack(side=tk.LEFT, padx=28, pady=14)
        
        # Frame para usuario y botón cerrar sesión
        user_frame = tk.Frame(header, bg=COLORS['primary'])
        user_frame.pack(side=tk.RIGHT, padx=28, pady=14)
        
        user_info = tk.Label(
            user_frame,
            text=f"Usuario: {self.username}",
            font=("Arial", 10),
            bg=COLORS['primary'],
            fg="white"
        )
        user_info.pack(side=tk.LEFT, padx=(0, 12))
        
        btn_logout = tk.Button(
            user_frame,
            text="🚪 Cerrar Sesión",
            font=("Arial", 9),
            bg="#dc2626",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=6,
            command=self.logout
        )
        btn_logout.pack(side=tk.LEFT)
    
    def create_sidebar(self, parent):
        """Crea el menú lateral"""
        sidebar = tk.Frame(parent, bg=COLORS['sidebar'], width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Título del menú
        menu_title = tk.Label(
            sidebar,
            text="MENÚ PRINCIPAL",
            font=("Arial", 9),
            bg=COLORS['sidebar'],
            fg="#9fb3d1"
        )
        menu_title.pack(anchor=tk.W, padx=12, pady=(16, 12))
        
        # Items del menú
        menu_items = [
            ("🏠", "Inicio", self.show_home),
            ("📅", "Eventos", self.show_events),
            ("👤", "Participantes", self.show_participants),
            ("📝", "Inscripciones", self.show_inscriptions),
            ("📊", "Reportes", self.show_reports),
            ("⚙️", "Usuarios", self.show_users),
        ]
        
        self.menu_buttons = []
        for icon, text, command in menu_items:
            btn_frame = tk.Frame(sidebar, bg=COLORS['sidebar'])
            btn_frame.pack(fill=tk.X, padx=12, pady=3)
            
            btn = tk.Label(
                btn_frame,
                text=f"{icon} {text}",
                font=("Arial", 10),
                bg=COLORS['sidebar'],
                fg=COLORS['sidebar_text'],
                anchor=tk.W,
                padx=12,
                pady=10,
                cursor="hand2"
            )
            btn.pack(fill=tk.X)
            btn.bind('<Button-1>', lambda e, cmd=command, b=btn: self.on_menu_click(cmd, b))
            
            self.menu_buttons.append(btn)
    
    def on_menu_click(self, command, button):
        """Maneja el clic en un item del menú"""
        # Resetear todos los botones
        for btn in self.menu_buttons:
            btn.config(bg=COLORS['sidebar'], fg=COLORS['sidebar_text'], font=("Arial", 10))
        
        # Activar el botón seleccionado
        button.config(bg=COLORS['primary'], fg="white", font=("Arial", 10, "bold"))
        self.active_menu_item = button
        
        # Ejecutar comando
        command()
    
    def clear_content(self):
        """Limpia el contenido del panel principal"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_view = None
    
    def show_home(self):
        """Muestra la vista de inicio (basada en diseno_inicio.html)"""
        try:
            self.clear_content()
            
            # Verificar que content_frame existe
            if not hasattr(self, 'content_frame') or not self.content_frame:
                print("Error: content_frame no existe")
                return
            
            # Título
            title = tk.Label(
                self.content_frame,
                text="Resumen general",
                font=("Arial", 16, "bold"),
                bg=COLORS['background'],
                fg=COLORS['primary']
            )
            title.pack(anchor=tk.W, pady=(0, 8))
            
            subtitle = tk.Label(
                self.content_frame,
                text="Visión rápida del estado de los eventos y participantes.",
                font=("Arial", 10),
                bg=COLORS['background'],
                fg=COLORS['text_secondary']
            )
            subtitle.pack(anchor=tk.W, pady=(0, 24))
        
            # Cards de estadísticas
            cards_frame = tk.Frame(self.content_frame, bg=COLORS['background'])
            cards_frame.pack(fill=tk.X, pady=(0, 24))
            
            # Obtener datos reales (o datos de ejemplo si no hay BD)
            try:
                if self.event_controller:
                    events = self.event_controller.get_all()
                    participants = self.participant_controller.get_all()
                    today_events = [e for e in events if e.start_datetime and e.start_datetime.date() == datetime.now().date()]
                else:
                    # Modo demo - datos de ejemplo
                    events = []
                    participants = []
                    today_events = []
            except Exception as e:
                print(f"Error al obtener datos: {e}")
                import traceback
                traceback.print_exc()
                events = []
                participants = []
                today_events = []
            
            stats = [
                ("Total de eventos", len(events), "Próximos 30 días"),
                ("Participantes registrados", len(participants), "En todos los eventos"),
                ("Eventos hoy", len(today_events), "Requieren seguimiento"),
            ]
            
            for i, (title_text, value, subtitle_text) in enumerate(stats):
                card = tk.Frame(cards_frame, bg=COLORS['white'], relief=tk.FLAT)
                card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 16) if i < len(stats)-1 else 0)
                card.configure(width=220)
                
                # Contenido del card
                card_title = tk.Label(
                    card,
                    text=title_text.upper(),
                    font=("Arial", 9),
                    bg=COLORS['white'],
                    fg=COLORS['text_secondary']
                )
                card_title.pack(anchor=tk.W, padx=18, pady=(16, 6))
                
                card_value = tk.Label(
                    card,
                    text=str(value),
                    font=("Arial", 16, "bold"),
                    bg=COLORS['white'],
                    fg=COLORS['text_primary']
                )
                card_value.pack(anchor=tk.W, padx=18)
                
                card_subtitle = tk.Label(
                    card,
                    text=subtitle_text,
                    font=("Arial", 9),
                    bg=COLORS['white'],
                    fg="#9ca3af"
                )
                card_subtitle.pack(anchor=tk.W, padx=18, pady=(4, 16))
        
            # Panel de próximos eventos
            panel = tk.Frame(self.content_frame, bg=COLORS['white'], relief=tk.FLAT)
            panel.pack(fill=tk.BOTH, expand=True)
        
            panel_header = tk.Frame(panel, bg=COLORS['white'])
            panel_header.pack(fill=tk.X, padx=18, pady=16)
            
            panel_title = tk.Label(
                panel_header,
                text="Próximos eventos",
                font=("Arial", 11, "bold"),
                bg=COLORS['white'],
                fg=COLORS['text_primary']
            )
            panel_title.pack(side=tk.LEFT)
            
            badge = tk.Label(
                panel_header,
                text="Próximos 7 días",
                font=("Arial", 8),
                bg=COLORS['success'],
                fg=COLORS['success_text'],
                padx=8,
                pady=2
            )
            badge.pack(side=tk.RIGHT)
            
            # Tabla de eventos
            table_frame = tk.Frame(panel, bg=COLORS['white'])
            table_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 16))
            
            # Headers
            headers = ["Evento", "Fecha", "Ubicación", "Aforo", "Inscritos"]
            header_frame = tk.Frame(table_frame, bg=COLORS['table_header'])
            header_frame.pack(fill=tk.X)
            
            for header in headers:
                label = tk.Label(
                    header_frame,
                    text=header.upper(),
                    font=("Arial", 8),
                    bg=COLORS['table_header'],
                    fg=COLORS['text_secondary'],
                    padx=6,
                    pady=8,
                    anchor=tk.W
                )
                label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Filas de eventos (próximos 7 días)
            try:
                from datetime import timedelta
                next_week = datetime.now() + timedelta(days=7)
                upcoming_events = [e for e in events if e.start_datetime and e.start_datetime <= next_week][:5]
            except:
                upcoming_events = []
            
            # Si no hay eventos, mostrar mensaje
            if not upcoming_events:
                row_frame = tk.Frame(table_frame, bg=COLORS['white'])
                row_frame.pack(fill=tk.X)
                no_data = tk.Label(
                    row_frame,
                    text="No hay eventos próximos (Modo Demo - Sin base de datos)",
                    font=("Arial", 9),
                    bg=COLORS['white'],
                    fg=COLORS['text_secondary'],
                    padx=6,
                    pady=8
                )
                no_data.pack(fill=tk.X)
            else:
                for i, event in enumerate(upcoming_events):
                    row_frame = tk.Frame(table_frame, bg=COLORS['white'] if i % 2 == 0 else COLORS['table_row_even'])
                    row_frame.pack(fill=tk.X)
                    
                    # Obtener número de inscritos
                    try:
                        if self.registration_controller:
                            registrations = self.registration_controller.get_event_participants(event.event_id)
                            num_registered = len(registrations)
                        else:
                            num_registered = 0
                    except:
                        num_registered = 0
                    
                    data = [
                        event.title[:40],
                        event.start_datetime.strftime("%d/%m/%Y %H:%M") if event.start_datetime else "",
                        event.location or "",
                        str(event.capacity),
                        str(num_registered)
                    ]
                    
                    for data_item in data:
                        label = tk.Label(
                            row_frame,
                            text=data_item,
                            font=("Arial", 9),
                            bg=row_frame.cget('bg'),
                            fg=COLORS['text_primary'],
                            padx=6,
                            pady=8,
                            anchor=tk.W
                        )
                        label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"Error en show_home: {e}")
            import traceback
            traceback.print_exc()
            # Mostrar mensaje de error en la ventana
            error_label = tk.Label(
                self.content_frame,
                text=f"Error al mostrar inicio:\n{str(e)}",
                font=("Arial", 10),
                bg=COLORS['background'],
                fg="red"
            )
            error_label.pack(pady=50)
    
    def show_events(self):
        """Muestra la vista de eventos"""
        self.clear_content()
        
        if not self.db:
            # Modo demo sin base de datos
            label = tk.Label(
                self.content_frame,
                text="Vista de Eventos\n\n(Modo Demo - Sin base de datos)\n\nLa interfaz está disponible pero no se pueden guardar datos.",
                font=("Arial", 12),
                bg=COLORS['background'],
                fg=COLORS['text_secondary'],
                justify=tk.CENTER
            )
            label.pack(pady=50)
            return
        
        if EventView:
            self.current_view = EventView(
                self.content_frame,
                self.event_controller,
                self.registration_controller,
                self.is_admin
            )
        else:
            # Fallback si no está disponible
            label = tk.Label(
                self.content_frame,
                text="Vista de Eventos - Cargando...",
                font=("Arial", 14),
                bg=COLORS['background']
            )
            label.pack(pady=50)
    
    def show_participants(self):
        """Muestra la vista de participantes"""
        self.clear_content()
        
        if not self.db:
            # Modo demo sin base de datos
            label = tk.Label(
                self.content_frame,
                text="Vista de Participantes\n\n(Modo Demo - Sin base de datos)\n\nLa interfaz está disponible pero no se pueden guardar datos.",
                font=("Arial", 12),
                bg=COLORS['background'],
                fg=COLORS['text_secondary'],
                justify=tk.CENTER
            )
            label.pack(pady=50)
            return
        
        if ParticipantView:
            self.current_view = ParticipantView(
                self.content_frame,
                self.participant_controller,
                self.registration_controller,
                self.event_controller,
                self.is_admin
            )
        else:
            # Fallback si no está disponible
            label = tk.Label(
                self.content_frame,
                text="Vista de Participantes - Cargando...",
                font=("Arial", 14),
                bg=COLORS['background']
            )
            label.pack(pady=50)
    
    def show_inscriptions(self):
        """Muestra la vista de inscripciones"""
        self.clear_content()
        
        if not self.db:
            # Modo demo sin base de datos
            label = tk.Label(
                self.content_frame,
                text="Vista de Inscripciones\n\n(Modo Demo - Sin base de datos)\n\nLa interfaz está disponible pero no se pueden guardar datos.",
                font=("Arial", 12),
                bg=COLORS['background'],
                fg=COLORS['text_secondary'],
                justify=tk.CENTER
            )
            label.pack(pady=50)
            return
        
        try:
            from src.views.registration_view import RegistrationView
            self.current_view = RegistrationView(
                self.content_frame,
                self.registration_controller,
                self.event_controller,
                self.participant_controller,
                self.is_admin,
                self.username  # Pasar el username del usuario actual
            )
        except Exception as e:
            label = tk.Label(
                self.content_frame,
                text=f"Error al cargar inscripciones:\n{str(e)}",
                font=("Arial", 12),
                bg=COLORS['background'],
                fg="red"
            )
            label.pack(pady=50)
            import traceback
            traceback.print_exc()
    
    def show_reports(self):
        """Muestra la vista de reportes"""
        self.clear_content()
        
        if not self.db:
            # Modo demo sin base de datos
            label = tk.Label(
                self.content_frame,
                text="Vista de Reportes\n\n(Modo Demo - Sin base de datos)\n\nLa interfaz está disponible pero no se pueden exportar datos.",
                font=("Arial", 12),
                bg=COLORS['background'],
                fg=COLORS['text_secondary'],
                justify=tk.CENTER
            )
            label.pack(pady=50)
            return
        
        try:
            from src.views.reports_view import ReportsView
            self.current_view = ReportsView(
                self.content_frame,
                self.event_controller,
                self.participant_controller,
                self.registration_controller
            )
        except Exception as e:
            label = tk.Label(
                self.content_frame,
                text=f"Error al cargar reportes:\n{str(e)}",
                font=("Arial", 12),
                bg=COLORS['background'],
                fg="red"
            )
            label.pack(pady=50)
            import traceback
            traceback.print_exc()
    
    def logout(self):
        """Cierra la sesión y vuelve al login"""
        result = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Estás seguro de que deseas cerrar sesión?"
        )
        
        if result:
            # Cerrar conexión a la base de datos
            if self.db:
                try:
                    self.db.close()
                except:
                    pass
            
            # Si hay callback de logout, usarlo
            if self.on_logout:
                self.on_logout()
            else:
                # Fallback: limpiar y mostrar login
                for widget in self.root.winfo_children():
                    widget.destroy()
                
                from src.views.login_window import LoginWindow
                
                def on_login_success(username, db=None):
                    # Recrear la ventana principal
                    for widget in self.root.winfo_children():
                        widget.destroy()
                    MainWindow(self.root, db, username, self.on_logout)
                
                login = LoginWindow(self.root, on_login_success)
    
    def show_users(self):
        """Muestra la vista de usuarios"""
        self.clear_content()
        
        if not UserView:
            label = tk.Label(
                self.content_frame,
                text="Vista de Usuarios no disponible",
                font=("Arial", 14),
                bg=COLORS['background']
            )
            label.pack(pady=50)
            return
        
        try:
            self.current_view = UserView(
                self.content_frame,
                self.user_controller,
                is_admin=self.is_admin
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la vista de usuarios: {str(e)}")
            import traceback
            traceback.print_exc()

