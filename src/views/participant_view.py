"""
Vista de participantes
Basada en diseno_participantes.html
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.views.styles import COLORS
from src.models.participant import Participant
from src.utils.validators import Validator
from src.utils.exporters import CSVExporter, PDFExporter


class ParticipantView:
    """Vista completa de gestión de participantes"""
    
    def __init__(self, parent, participant_controller, registration_controller, event_controller, is_admin=False):
        self.parent = parent
        self.participant_controller = participant_controller
        self.registration_controller = registration_controller
        self.event_controller = event_controller
        self.is_admin = is_admin  # Asignar is_admin ANTES de create_widgets()
        self.current_participant = None
        self.create_widgets()
        self.load_participants()
    
    def create_widgets(self):
        """Crea los widgets de la vista"""
        # Header con título y botones
        header_frame = tk.Frame(self.parent, bg=COLORS['background'])
        header_frame.pack(fill=tk.X, pady=(0, 16))
        
        title = tk.Label(
            header_frame,
            text="Participantes",
            font=("Arial", 14, "bold"),
            bg=COLORS['background'],
            fg=COLORS['text_primary']
        )
        title.pack(side=tk.LEFT)
        
        actions_frame = tk.Frame(header_frame, bg=COLORS['background'])
        actions_frame.pack(side=tk.RIGHT)
        
        btn_new = tk.Button(
            actions_frame,
            text="+ Nuevo participante",
            font=("Arial", 9),
            bg=COLORS['primary'],
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.show_new_participant_modal,
            state=tk.NORMAL if self.is_admin else tk.DISABLED
        )
        btn_new.pack(side=tk.LEFT, padx=4)
        
        # Filtros
        filters_frame = tk.Frame(self.parent, bg=COLORS['background'])
        filters_frame.pack(fill=tk.X, pady=(0, 12))
        
        self.search_entry = tk.Entry(
            filters_frame,
            font=("Arial", 9),
            relief=tk.SOLID,
            borderwidth=1,
            width=40
        )
        self.search_entry.pack(side=tk.LEFT, padx=(0, 8))
        self.search_entry.insert(0, "Buscar por nombre, apellidos o email")
        self.search_entry.config(fg=COLORS['text_secondary'])
        self.search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in())
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_participants())
        
        # Tabla de participantes
        self.create_table()
    
    def create_table(self):
        """Crea la tabla de participantes"""
        table_container = tk.Frame(self.parent, bg=COLORS['white'], relief=tk.FLAT)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Frame para scrollbar y tabla
        table_frame = tk.Frame(table_container, bg=COLORS['white'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (tabla)
        columns = ("Nombre", "Apellidos", "Email", "Teléfono", "DNI/NIE", "# Eventos")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading("Nombre", text="NOMBRE")
        self.tree.heading("Apellidos", text="APELLIDOS")
        self.tree.heading("Email", text="EMAIL")
        self.tree.heading("Teléfono", text="TELÉFONO")
        self.tree.heading("DNI/NIE", text="DNI / IDENTIFICADOR")
        self.tree.heading("# Eventos", text="# EVENTOS")
        
        self.tree.column("Nombre", width=120)
        self.tree.column("Apellidos", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Teléfono", width=120)
        self.tree.column("DNI/NIE", width=150)
        self.tree.column("# Eventos", width=100)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind doble clic para editar
        self.tree.bind('<Double-1>', lambda e: self.edit_selected_participant())
        
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
            command=self.view_selected_participant
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
            command=self.edit_selected_participant,
            state=tk.NORMAL if self.is_admin else tk.DISABLED
        )
        btn_edit.pack(side=tk.LEFT, padx=4)
        
        btn_delete = tk.Button(
            actions_frame,
            text="Eliminar",
            font=("Arial", 8),
            bg="#e5e7eb",
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self.delete_selected_participant,
            state=tk.NORMAL if self.is_admin else tk.DISABLED
        )
        btn_delete.pack(side=tk.LEFT, padx=4)
        
        btn_inscriptions = tk.Button(
            actions_frame,
            text="Inscripciones",
            font=("Arial", 8),
            bg="#e5e7eb",
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self.show_inscriptions_modal
        )
        btn_inscriptions.pack(side=tk.LEFT, padx=4)
    
    def load_participants(self):
        """Carga los participantes en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Verificar que hay controlador
        if not self.participant_controller:
            # Mostrar mensaje de modo demo
            messagebox.showinfo(
                "Modo Demo",
                "No hay conexión a la base de datos.\n\n"
                "La vista está disponible pero no se pueden cargar datos."
            )
            return
        
        try:
            # Obtener participantes
            participants = self.participant_controller.get_all()
            
            if not participants:
                # Mostrar mensaje si no hay participantes
                messagebox.showinfo(
                    "Sin datos",
                    "No hay participantes registrados en la base de datos.\n\n"
                    "Puedes crear nuevos participantes usando el botón 'Nuevo participante'."
                )
                return
            
            # Ordenar por apellidos
            participants.sort(key=lambda x: (x.last_name or "", x.first_name or ""))
            
            # Cargar participantes en la tabla
            for participant in participants:
                try:
                    # Obtener número de eventos
                    if self.registration_controller:
                        events = self.registration_controller.get_participant_events(participant.participant_id)
                        num_events = len(events) if events else 0
                    else:
                        num_events = 0
                    
                    phone_str = str(participant.phone) if participant.phone else ""
                    
                    self.tree.insert(
                        "",
                        tk.END,
                        values=(
                            participant.first_name or "",
                            participant.last_name or "",
                            participant.email or "",
                            phone_str,
                            participant.identifier or "",
                            num_events
                        ),
                        tags=(participant.participant_id,)
                    )
                except Exception as e:
                    print(f"Error al cargar participante {participant.participant_id}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
                    
        except Exception as e:
            error_msg = f"Error al cargar participantes: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", error_msg)
    
    def filter_participants(self):
        """Filtra los participantes según la búsqueda"""
        search_term = self.search_entry.get().lower()
        
        if search_term == "buscar por nombre, apellidos o email":
            self.load_participants()
            return
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar participantes
        if search_term:
            participants = self.participant_controller.search(search_term)
        else:
            participants = self.participant_controller.get_all()
        
        participants.sort(key=lambda x: (x.last_name or "", x.first_name or ""))
        
        for participant in participants:
            events = self.registration_controller.get_participant_events(participant.participant_id)
            num_events = len(events)
            
            phone_str = str(participant.phone) if participant.phone else ""
            
            self.tree.insert(
                "",
                tk.END,
                values=(
                    participant.first_name or "",
                    participant.last_name or "",
                    participant.email or "",
                    phone_str,
                    participant.identifier or "",
                    num_events
                ),
                tags=(participant.participant_id,)
            )
    
    def on_search_focus_in(self):
        """Maneja el foco en el campo de búsqueda"""
        if self.search_entry.get() == "Buscar por nombre, apellidos o email":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=COLORS['text_primary'])
    
    def view_selected_participant(self):
        """Ver detalles del participante seleccionado en una ventana modal bonita"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un participante para ver")
            return
        
        item = self.tree.item(selection[0])
        participant_id = item['tags'][0]
        
        participant = self.participant_controller.get_by_id(participant_id)
        
        if participant:
            self.show_participant_details_modal(participant)
    
    def show_participant_details_modal(self, participant):
        """Muestra los detalles del participante en una ventana modal bonita"""
        modal = tk.Toplevel(self.parent)
        modal.title(f"Detalles del Participante: {participant.full_name}")
        modal.geometry("650x650")
        modal.resizable(True, True)
        modal.minsize(600, 550)
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (650 // 2)
        y = (modal.winfo_screenheight() // 2) - (650 // 2)
        modal.geometry(f"650x650+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(modal, bg=COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header con color
        header = tk.Frame(main_frame, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="👤 Detalles del Participante",
            font=("Arial", 16, "bold"),
            bg=COLORS['primary'],
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Contenedor con scroll para el contenido
        canvas = tk.Canvas(main_frame, bg=COLORS['white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_content = tk.Frame(canvas, bg=COLORS['white'])
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def on_canvas_configure(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        scrollable_content.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido dentro del frame scrolleable
        content = scrollable_content
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Nombre completo del participante
        name_label = tk.Label(
            content,
            text=participant.full_name,
            font=("Arial", 18, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary'],
            wraplength=580
        )
        name_label.pack(anchor=tk.W, pady=(0, 24))
        
        # Información en cards
        info_frame = tk.Frame(content, bg=COLORS['white'])
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Obtener eventos del participante
        num_events = 0
        events_list = []
        if self.registration_controller:
            try:
                events = self.registration_controller.get_participant_events(participant.participant_id)
                num_events = len(events) if events else 0
                events_list = events[:15]  # Primeros 15 eventos
            except:
                pass
        
        # Campos de información
        fields = [
            ("📧 Email", participant.email or "No especificado", False),
            ("📱 Teléfono", str(participant.phone) if participant.phone else "No especificado", False),
            ("🆔 DNI/NIE", participant.identifier or "No especificado", False),
            ("📅 Eventos inscritos", f"{num_events} evento(s)", False)
        ]
        
        for label_text, value, is_multiline in fields:
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
                bg=COLORS['white'],
                fg=COLORS['text_primary'],
                anchor=tk.W,
                padx=12,
                pady=8,
                relief=tk.SOLID,
                borderwidth=1,
                wraplength=580 if is_multiline else None
            )
            value_label.pack(anchor=tk.W, fill=tk.X)
        
        # Lista de eventos si hay
        if events_list:
            events_label = tk.Label(
                info_frame,
                text="📋 Eventos:",
                font=("Arial", 10, "bold"),
                bg=COLORS['white'],
                fg=COLORS['text_secondary'],
                anchor=tk.W
            )
            events_label.pack(anchor=tk.W, pady=(8, 4))
            
            events_container = tk.Frame(info_frame, bg=COLORS['white'])
            events_container.pack(fill=tk.X, pady=(0, 8))
            
            for event in events_list[:15]:  # Mostrar hasta 15 eventos
                event_title = event.get('title', 'Sin título')
                event_date = event.get('start_datetime', '')
                if event_date:
                    if isinstance(event_date, datetime):
                        event_date = event_date.strftime("%d/%m/%Y")
                    else:
                        try:
                            event_date = datetime.strptime(str(event_date), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                        except:
                            event_date = str(event_date)
                
                event_text = f"  • {event_title}"
                if event_date:
                    event_text += f" ({event_date})"
                
                event_label = tk.Label(
                    events_container,
                    text=event_text,
                    font=("Arial", 9),
                    bg=COLORS['white'],
                    fg=COLORS['text_primary'],
                    anchor=tk.W,
                    padx=12,
                    pady=4
                )
                event_label.pack(anchor=tk.W)
            
            if num_events > 15:
                more_label = tk.Label(
                    events_container,
                    text=f"  ... y {num_events - 15} evento(s) más",
                    font=("Arial", 8),
                    bg=COLORS['white'],
                    fg=COLORS['text_secondary'],
                    anchor=tk.W,
                    padx=12,
                    pady=4
                )
                more_label.pack(anchor=tk.W)
        
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
        
        # Actualizar scroll después de crear widgets
        modal.after(100, lambda: canvas.configure(scrollregion=canvas.bbox("all")))
        
        modal.bind('<Escape>', lambda e: modal.destroy())
    
    def edit_selected_participant(self):
        """Editar el participante seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un participante para editar")
            return
        
        item = self.tree.item(selection[0])
        participant_id = item['tags'][0]
        
        participant = self.participant_controller.get_by_id(participant_id)
        
        if participant:
            self.show_participant_modal(participant)
    
    def delete_selected_participant(self):
        """Eliminar el participante seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un participante para eliminar")
            return
        
        item = self.tree.item(selection[0])
        participant_id = item['tags'][0]
        
        participant = self.participant_controller.get_by_id(participant_id)
        
        if participant:
            if messagebox.askyesno("Confirmar", f"¿Eliminar el participante '{participant.full_name}'?"):
                if self.participant_controller.delete(participant_id):
                    messagebox.showinfo("Éxito", "Participante eliminado correctamente")
                    self.load_participants()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el participante")
    
    def show_new_participant_modal(self):
        """Muestra el modal para nuevo participante"""
        self.show_participant_modal(None)
    
    def show_participant_modal(self, participant: Participant = None):
        """Muestra el modal de creación/edición de participante"""
        modal = tk.Toplevel(self.parent)
        modal.title("Nuevo / Editar participante" if not participant else "Editar participante")
        modal.geometry("520x350")
        modal.resizable(False, False)
        modal.configure(bg=COLORS['white'])
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (520 // 2)
        y = (modal.winfo_screenheight() // 2) - (350 // 2)
        modal.geometry(f'520x350+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg=COLORS['primary'], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="Nuevo / Editar participante",
            font=("Arial", 10, "bold"),
            bg=COLORS['primary'],
            fg="white"
        )
        header_label.pack(pady=12)
        
        # Body
        body = tk.Frame(modal, bg=COLORS['white'])
        body.pack(fill=tk.BOTH, expand=True, padx=18, pady=14)
        
        # Campos del formulario
        fields = [
            ("Nombre *", "first_name"),
            ("Apellidos *", "last_name"),
            ("Email *", "email"),
            ("Teléfono", "phone"),
            ("DNI / Identificador", "identifier"),
        ]
        
        self.modal_entries = {}
        
        for label_text, field_name in fields:
            row = tk.Frame(body, bg=COLORS['white'])
            row.pack(fill=tk.X, pady=8)
            
            label = tk.Label(
                row,
                text=label_text,
                font=("Arial", 9),
                bg=COLORS['white'],
                fg="#4b5563",
                width=18,
                anchor=tk.W
            )
            label.pack(side=tk.LEFT, padx=(0, 8))
            
            entry = tk.Entry(row, font=("Arial", 9), relief=tk.SOLID, borderwidth=1)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.modal_entries[field_name] = entry
        
        # Rellenar campos si es edición
        if participant:
            self.modal_entries['first_name'].insert(0, participant.first_name or "")
            self.modal_entries['last_name'].insert(0, participant.last_name or "")
            self.modal_entries['email'].insert(0, participant.email or "")
            self.modal_entries['phone'].insert(0, str(participant.phone) if participant.phone else "")
            self.modal_entries['identifier'].insert(0, participant.identifier or "")
        
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
            command=lambda: self.save_participant(participant, modal)
        )
        btn_save.pack(side=tk.RIGHT)
    
    def save_participant(self, participant: Participant, modal):
        """Guarda el participante"""
        try:
            # Obtener valores
            first_name = self.modal_entries['first_name'].get().strip()
            last_name = self.modal_entries['last_name'].get().strip()
            email = self.modal_entries['email'].get().strip()
            phone_str = self.modal_entries['phone'].get().strip()
            identifier = self.modal_entries['identifier'].get().strip()
            
            # Validaciones
            if not first_name:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            if not last_name:
                messagebox.showerror("Error", "Los apellidos son obligatorios")
                return
            
            if not email:
                messagebox.showerror("Error", "El email es obligatorio")
                return
            
            if email and not Validator.validate_email(email):
                messagebox.showerror("Error", "El formato del email no es válido")
                return
            
            # Parsear teléfono
            phone = None
            if phone_str:
                try:
                    phone = int(phone_str.replace(" ", "").replace("-", ""))
                    if not Validator.validate_phone(str(phone)):
                        messagebox.showerror("Error", "El teléfono debe tener 9 dígitos")
                        return
                except ValueError:
                    messagebox.showerror("Error", "El teléfono debe ser un número")
                    return
            
            # Validar DNI/NIE si se proporciona
            if identifier and not Validator.validate_dni_nie(identifier):
                messagebox.showwarning("Advertencia", "El formato del DNI/NIE puede no ser válido")
            
            # Crear o actualizar participante
            if participant:
                participant.first_name = first_name
                participant.last_name = last_name
                participant.email = email
                participant.phone = phone
                participant.identifier = identifier
                
                if self.participant_controller.update(participant):
                    messagebox.showinfo("Éxito", "Participante actualizado correctamente")
                    modal.destroy()
                    self.load_participants()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el participante")
            else:
                new_participant = Participant(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    identifier=identifier
                )
                
                participant_id = self.participant_controller.create(new_participant)
                if participant_id:
                    messagebox.showinfo("Éxito", "Participante creado correctamente")
                    modal.destroy()
                    self.load_participants()
                else:
                    messagebox.showerror("Error", "No se pudo crear el participante")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def show_inscriptions_modal(self):
        """Muestra el modal de inscripciones del participante"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un participante para ver sus inscripciones")
            return
        
        item = self.tree.item(selection[0])
        participant_id = item['tags'][0]
        
        participant = self.participant_controller.get_by_id(participant_id)
        
        if not participant:
            return
        
        # Crear modal
        modal = tk.Toplevel(self.parent)
        modal.title(f"Inscripciones de {participant.full_name}")
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
            text=f"Inscripciones de {participant.full_name}",
            font=("Arial", 10, "bold"),
            bg=COLORS['primary'],
            fg="white"
        )
        header_label.pack(pady=12)
        
        # Body con tabla
        body = tk.Frame(modal, bg=COLORS['white'])
        body.pack(fill=tk.BOTH, expand=True, padx=18, pady=14)
        
        # Obtener eventos del participante
        events = self.registration_controller.get_participant_events(participant_id)
        
        if events:
            # Crear tabla
            table_frame = tk.Frame(body, bg=COLORS['white'])
            table_frame.pack(fill=tk.BOTH, expand=True)
            
            # Headers
            headers = ["Evento", "Fecha", "Estado"]
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
            
            # Filas
            for i, event_data in enumerate(events):
                row_frame = tk.Frame(
                    table_frame,
                    bg=COLORS['white'] if i % 2 == 0 else COLORS['table_row_even']
                )
                row_frame.pack(fill=tk.X)
                
                start_date = event_data.get('start_datetime', '')
                if start_date:
                    if isinstance(start_date, datetime):
                        start_date = start_date.strftime('%d/%m/%Y %H:%M')
                    else:
                        start_date = str(start_date)
                
                data = [
                    event_data.get('title', '')[:40],
                    start_date,
                    event_data.get('registration_status', 'confirmado')
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
        else:
            no_data = tk.Label(
                body,
                text="No hay inscripciones registradas",
                font=("Arial", 10),
                bg=COLORS['white'],
                fg=COLORS['text_secondary']
            )
            no_data.pack(pady=50)
        
        # Footer
        footer = tk.Frame(modal, bg=COLORS['table_header'])
        footer.pack(fill=tk.X, padx=18, pady=(0, 14))
        
        btn_add = tk.Button(
            footer,
            text="Agregar a evento",
            font=("Arial", 9),
            bg=COLORS['white'],
            fg="#374151",
            relief=tk.SOLID,
            borderwidth=1,
            padx=14,
            pady=7,
            cursor="hand2",
            command=lambda: self.add_to_event(participant_id, modal)
        )
        btn_add.pack(side=tk.LEFT)
        
        btn_close = tk.Button(
            footer,
            text="Cerrar",
            font=("Arial", 9),
            bg=COLORS['primary'],
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=7,
            cursor="hand2",
            command=modal.destroy
        )
        btn_close.pack(side=tk.RIGHT)
    
    def add_to_event(self, participant_id, parent_modal):
        """Agrega el participante a un evento"""
        # Obtener lista de eventos
        events = self.event_controller.get_all()
        
        if not events:
            messagebox.showwarning("Advertencia", "No hay eventos disponibles")
            return
        
        # Crear diálogo de selección
        event_titles = [f"{e.title} ({e.start_datetime.strftime('%d/%m/%Y') if e.start_datetime else 'Sin fecha'})" for e in events]
        
        selection_modal = tk.Toplevel(parent_modal)
        selection_modal.title("Seleccionar evento")
        selection_modal.geometry("400x200")
        selection_modal.transient(parent_modal)
        selection_modal.grab_set()
        
        label = tk.Label(
            selection_modal,
            text="Selecciona un evento:",
            font=("Arial", 10),
            pady=20
        )
        label.pack()
        
        event_var = tk.StringVar()
        event_combo = ttk.Combobox(
            selection_modal,
            textvariable=event_var,
            values=event_titles,
            state="readonly",
            width=40
        )
        event_combo.pack(pady=10)
        event_combo.current(0)
        
        def on_confirm():
            selected_index = event_combo.current()
            if selected_index >= 0:
                selected_event = events[selected_index]
                
                # Registrar participante
                registration_id = self.registration_controller.register_participant(
                    selected_event.event_id,
                    participant_id
                )
                
                if registration_id:
                    messagebox.showinfo("Éxito", f"Participante inscrito en '{selected_event.title}'")
                    selection_modal.destroy()
                    parent_modal.destroy()
                    self.show_inscriptions_modal()  # Recargar
                else:
                    messagebox.showerror("Error", "No se pudo inscribir al participante (evento lleno o ya inscrito)")
        
        btn_confirm = tk.Button(
            selection_modal,
            text="Confirmar",
            command=on_confirm,
            bg=COLORS['primary'],
            fg="white",
            padx=20,
            pady=5
        )
        btn_confirm.pack(pady=10)

