"""
Vista de eventos
Basada en diseno_eventos.html
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.views.styles import COLORS
from src.models.event import Event
from src.utils.validators import Validator
from src.utils.exporters import CSVExporter, PDFExporter


class EventView:
    """Vista completa de gestión de eventos"""
    
    def __init__(self, parent, event_controller, registration_controller, is_admin=False):
        self.parent = parent
        self.event_controller = event_controller
        self.registration_controller = registration_controller
        self.is_admin = is_admin
        self.current_event = None
        self.create_widgets()
        self.load_events()
    
    def create_widgets(self):
        """Crea los widgets de la vista"""
        # Header con título y botones
        header_frame = tk.Frame(self.parent, bg=COLORS['background'])
        header_frame.pack(fill=tk.X, pady=(0, 16))
        
        title = tk.Label(
            header_frame,
            text="Eventos",
            font=("Arial", 14, "bold"),
            bg=COLORS['background'],
            fg=COLORS['text_primary']
        )
        title.pack(side=tk.LEFT)
        
        actions_frame = tk.Frame(header_frame, bg=COLORS['background'])
        actions_frame.pack(side=tk.RIGHT)
        
        btn_export_csv = tk.Button(
            actions_frame,
            text="Exportar CSV",
            font=("Arial", 9),
            bg=COLORS['white'],
            fg=COLORS['primary'],
            relief=tk.SOLID,
            borderwidth=1,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.export_csv
        )
        btn_export_csv.pack(side=tk.LEFT, padx=4)
        
        btn_export_pdf = tk.Button(
            actions_frame,
            text="Exportar PDF",
            font=("Arial", 9),
            bg=COLORS['white'],
            fg=COLORS['primary'],
            relief=tk.SOLID,
            borderwidth=1,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.export_pdf
        )
        btn_export_pdf.pack(side=tk.LEFT, padx=4)
        
        btn_new = tk.Button(
            actions_frame,
            text="+ Nuevo evento",
            font=("Arial", 9),
            bg=COLORS['primary'],
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.show_new_event_modal,
            state=tk.NORMAL if self.is_admin else tk.DISABLED
        )
        btn_new.pack(side=tk.LEFT, padx=4)
        self.btn_new = btn_new  # Guardar referencia
        
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
        self.search_entry.insert(0, "Buscar por título o ubicación")
        self.search_entry.config(fg=COLORS['text_secondary'])
        self.search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in())
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_events())
        
        self.status_filter = ttk.Combobox(
            filters_frame,
            values=["Todos los estados", "Activos", "Finalizados", "Cancelados"],
            state="readonly",
            width=20,
            font=("Arial", 9)
        )
        self.status_filter.current(0)
        self.status_filter.pack(side=tk.LEFT, padx=4)
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_events())
        
        self.sort_filter = ttk.Combobox(
            filters_frame,
            values=["Ordenar por fecha inicio", "Ordenar por título"],
            state="readonly",
            width=20,
            font=("Arial", 9)
        )
        self.sort_filter.current(0)
        self.sort_filter.pack(side=tk.LEFT, padx=4)
        self.sort_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_events())
        
        # Tabla de eventos
        self.create_table()
    
    def create_table(self):
        """Crea la tabla de eventos"""
        table_container = tk.Frame(self.parent, bg=COLORS['white'], relief=tk.FLAT)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Frame para scrollbar y tabla
        table_frame = tk.Frame(table_container, bg=COLORS['white'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (tabla)
        columns = ("Título", "Inicio", "Fin", "Localización", "Aforo", "Estado")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading("Título", text="TÍTULO")
        self.tree.heading("Inicio", text="INICIO")
        self.tree.heading("Fin", text="FIN")
        self.tree.heading("Localización", text="LOCALIZACIÓN")
        self.tree.heading("Aforo", text="AFORO")
        self.tree.heading("Estado", text="ESTADO")
        
        self.tree.column("Título", width=250)
        self.tree.column("Inicio", width=150)
        self.tree.column("Fin", width=150)
        self.tree.column("Localización", width=150)
        self.tree.column("Aforo", width=80)
        self.tree.column("Estado", width=120)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind doble clic para ver detalles
        self.tree.bind('<Double-1>', lambda e: self.view_selected_event())
        
        # Frame de acciones (botones en cada fila)
        # Nota: En Tkinter, los botones en cada fila requieren un enfoque diferente
        # Por ahora, usaremos menú contextual o botones globales
        
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
            command=self.view_selected_event
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
            command=self.edit_selected_event,
            state=tk.NORMAL if self.is_admin else tk.DISABLED
        )
        btn_edit.pack(side=tk.LEFT, padx=4)
        self.btn_edit = btn_edit  # Guardar referencia
        
        btn_delete = tk.Button(
            actions_frame,
            text="Eliminar",
            font=("Arial", 8),
            bg="#e5e7eb",
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self.delete_selected_event,
            state=tk.NORMAL if self.is_admin else tk.DISABLED
        )
        btn_delete.pack(side=tk.LEFT, padx=4)
        self.btn_delete = btn_delete  # Guardar referencia
    
    def load_events(self):
        """Carga los eventos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener eventos
        events = self.event_controller.get_all()
        
        # Ordenar por fecha inicio
        events.sort(key=lambda x: x.start_datetime if x.start_datetime else datetime.min, reverse=True)
        
        now = datetime.now()
        
        for event in events:
            start_str = event.start_datetime.strftime("%d/%m/%Y %H:%M") if event.start_datetime else ""
            end_str = event.end_datetime.strftime("%d/%m/%Y %H:%M") if event.end_datetime else ""
            
            # Respetar el estado establecido manualmente, o calcular basado en fechas si no está establecido
            if event.status and event.status.lower() in ['cancelado', 'activo', 'planificado', 'finalizado']:
                # Si hay un estado explícito, respetarlo
                status = event.status.lower()
            elif event.end_datetime and event.end_datetime < now:
                # Evento finalizado si la fecha de fin ya pasó
                status = "finalizado"
            elif event.start_datetime and event.start_datetime <= now <= (event.end_datetime or now):
                # Evento activo si está en curso
                status = "activo"
            elif event.start_datetime and event.start_datetime > now:
                # Evento planificado si aún no ha comenzado
                status = "planificado"
            else:
                # Por defecto
                status = event.status.lower() if event.status else "activo"
            
            status_display = status.capitalize()
            
            self.tree.insert(
                "",
                tk.END,
                values=(
                    event.title,
                    start_str,
                    end_str,
                    event.location or "",
                    event.capacity,
                    status_display
                ),
                tags=(status,)
            )
        
        # Configurar colores de tags
        self.tree.tag_configure("activo", foreground=COLORS['success_text'])
        self.tree.tag_configure("finalizado", foreground=COLORS['danger_text'])
        self.tree.tag_configure("cancelado", foreground=COLORS['danger_text'])
        self.tree.tag_configure("planificado", foreground=COLORS['badge_text'])
    
    def filter_events(self):
        """Filtra los eventos según los criterios"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener eventos
        events = self.event_controller.get_all()
        
        # Aplicar filtro de búsqueda
        search_text = self.search_entry.get().lower()
        if search_text and search_text != "buscar por título o ubicación":
            events = [e for e in events if 
                     search_text in (e.title or "").lower() or 
                     search_text in (e.location or "").lower()]
        
        # Aplicar filtro de estado
        status_filter = self.status_filter.get()
        if status_filter != "Todos los estados":
            now = datetime.now()
            filtered_events = []
            for event in events:
                # Calcular estado igual que en load_events
                if event.status and event.status.lower() in ['cancelado', 'activo', 'planificado', 'finalizado']:
                    # Si hay un estado explícito, respetarlo
                    status = event.status.lower()
                elif event.end_datetime and event.end_datetime < now:
                    status = "finalizado"
                elif event.start_datetime and event.start_datetime <= now <= (event.end_datetime or now):
                    status = "activo"
                elif event.start_datetime and event.start_datetime > now:
                    status = "planificado"
                else:
                    status = event.status.lower() if event.status else "activo"
                
                if status_filter == "Activos" and status == "activo":
                    filtered_events.append(event)
                elif status_filter == "Finalizados" and status == "finalizado":
                    filtered_events.append(event)
                elif status_filter == "Cancelados" and status == "cancelado":
                    filtered_events.append(event)
            
            events = filtered_events
        
        # Ordenar
        sort_option = self.sort_filter.get()
        if sort_option == "Ordenar por título":
            events.sort(key=lambda x: (x.title or "").lower())
        else:
            events.sort(key=lambda x: x.start_datetime if x.start_datetime else datetime.min, reverse=True)
        
        # Mostrar eventos filtrados
        now = datetime.now()
        for event in events:
            start_str = event.start_datetime.strftime("%d/%m/%Y %H:%M") if event.start_datetime else ""
            end_str = event.end_datetime.strftime("%d/%m/%Y %H:%M") if event.end_datetime else ""
            
            # Calcular estado (igual que en load_events)
            if event.status and event.status.lower() in ['cancelado', 'activo', 'planificado', 'finalizado']:
                # Si hay un estado explícito, respetarlo
                status = event.status.lower()
            elif event.end_datetime and event.end_datetime < now:
                status = "finalizado"
            elif event.start_datetime and event.start_datetime <= now <= (event.end_datetime or now):
                status = "activo"
            elif event.start_datetime and event.start_datetime > now:
                status = "planificado"
            else:
                status = event.status.lower() if event.status else "activo"
            
            status_display = status.capitalize()
            
            self.tree.insert(
                "",
                tk.END,
                values=(
                    event.title,
                    start_str,
                    end_str,
                    event.location or "",
                    event.capacity,
                    status_display
                ),
                tags=(status,)
            )
        
        # Configurar colores de tags
        self.tree.tag_configure("activo", foreground=COLORS['success_text'])
        self.tree.tag_configure("finalizado", foreground=COLORS['danger_text'])
        self.tree.tag_configure("cancelado", foreground=COLORS['danger_text'])
        self.tree.tag_configure("planificado", foreground=COLORS['badge_text'])
    
    def on_search_focus_in(self):
        """Maneja el foco en el campo de búsqueda"""
        if self.search_entry.get() == "Buscar por título o ubicación":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=COLORS['text_primary'])
    
    def view_selected_event(self):
        """Ver detalles del evento seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un evento para ver")
            return
        
        # Obtener datos del evento seleccionado
        item = self.tree.item(selection[0])
        title = item['values'][0]
        
        # Buscar el evento completo
        events = self.event_controller.get_all()
        event = next((e for e in events if e.title == title), None)
        
        if event:
            self.show_event_details(event)
    
    def edit_selected_event(self):
        """Editar el evento seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un evento para editar")
            return
        
        item = self.tree.item(selection[0])
        title = item['values'][0]
        
        events = self.event_controller.get_all()
        event = next((e for e in events if e.title == title), None)
        
        if event:
            self.show_event_modal(event)
    
    def delete_selected_event(self):
        """Eliminar el evento seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un evento para eliminar")
            return
        
        item = self.tree.item(selection[0])
        title = item['values'][0]
        
        events = self.event_controller.get_all()
        event = next((e for e in events if e.title == title), None)
        
        if event:
            if messagebox.askyesno("Confirmar", f"¿Eliminar el evento '{event.title}'?"):
                try:
                    if self.event_controller.delete(event.event_id):
                        messagebox.showinfo("Éxito", "Evento eliminado correctamente")
                        self.load_events()
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el evento")
                except PermissionError as e:
                    messagebox.showerror("Permiso denegado", str(e))
    
    def show_new_event_modal(self):
        """Muestra el modal para nuevo evento"""
        self.show_event_modal(None)
    
    def show_event_modal(self, event: Event = None):
        """Muestra el modal de creación/edición de evento"""
        modal = tk.Toplevel(self.parent)
        modal.title("Nuevo / Editar evento" if not event else "Editar evento")
        modal.geometry("550x600")
        modal.resizable(True, True)
        modal.minsize(520, 550)
        modal.configure(bg=COLORS['white'])
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (550 // 2)
        y = (modal.winfo_screenheight() // 2) - (600 // 2)
        modal.geometry(f'550x600+{x}+{y}')
        
        # Header
        header = tk.Frame(modal, bg=COLORS['primary'], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="Nuevo / Editar evento",
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
            ("Título *", "title", "entry"),
            ("Descripción", "description", "text"),
            ("Localización", "location", "entry"),
            ("Fecha y hora inicio *", "start_datetime", "entry"),
            ("Fecha y hora fin *", "end_datetime", "entry"),
            ("Aforo máximo", "capacity", "entry"),
            ("Estado", "status", "combo"),
        ]
        
        self.modal_entries = {}
        
        for i, (label_text, field_name, field_type) in enumerate(fields):
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
            
            if field_type == "entry":
                entry = tk.Entry(row, font=("Arial", 9), relief=tk.SOLID, borderwidth=1)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.modal_entries[field_name] = entry
            elif field_type == "text":
                text_widget = tk.Text(row, font=("Arial", 9), relief=tk.SOLID, borderwidth=1, height=3)
                text_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.modal_entries[field_name] = text_widget
            elif field_type == "combo":
                combo = ttk.Combobox(
                    row,
                    values=["Activo", "Planificado", "Finalizado", "Cancelado"],
                    state="readonly",
                    font=("Arial", 9)
                )
                combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.modal_entries[field_name] = combo
        
        # Rellenar campos si es edición
        if event:
            self.modal_entries['title'].insert(0, event.title or "")
            if event.description:
                self.modal_entries['description'].insert("1.0", event.description)
            self.modal_entries['location'].insert(0, event.location or "")
            if event.start_datetime:
                self.modal_entries['start_datetime'].insert(0, event.start_datetime.strftime("%d/%m/%Y %H:%M"))
            if event.end_datetime:
                self.modal_entries['end_datetime'].insert(0, event.end_datetime.strftime("%d/%m/%Y %H:%M"))
            self.modal_entries['capacity'].insert(0, str(event.capacity) if event.capacity else "")
            if event.status:
                # Mapear valores de la BD a los del combobox
                status_map = {
                    'activo': 'Activo',
                    'planificado': 'Planificado',
                    'finalizado': 'Finalizado',
                    'cancelado': 'Cancelado'
                }
                status_display = status_map.get(event.status.lower(), 'Activo')
                try:
                    idx = ["Activo", "Planificado", "Finalizado", "Cancelado"].index(status_display)
                    self.modal_entries['status'].current(idx)
                except:
                    self.modal_entries['status'].current(0)
            else:
                self.modal_entries['status'].current(0)
        
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
            command=lambda: self.save_event(event, modal)
        )
        btn_save.pack(side=tk.RIGHT)
    
    def save_event(self, event: Event, modal):
        """Guarda el evento"""
        try:
            # Obtener valores
            title = self.modal_entries['title'].get().strip()
            description = self.modal_entries['description'].get("1.0", tk.END).strip()
            location = self.modal_entries['location'].get().strip()
            start_str = self.modal_entries['start_datetime'].get().strip()
            end_str = self.modal_entries['end_datetime'].get().strip()
            capacity_str = self.modal_entries['capacity'].get().strip()
            status = self.modal_entries['status'].get()
            
            # Validaciones
            if not title:
                messagebox.showerror("Error", "El título es obligatorio")
                return
            
            # Parsear fechas
            try:
                start_datetime = datetime.strptime(start_str, "%d/%m/%Y %H:%M")
                end_datetime = datetime.strptime(end_str, "%d/%m/%Y %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Use: dd/mm/aaaa hh:mm")
                return
            
            # Validar rango de fechas
            if end_datetime <= start_datetime:
                messagebox.showerror("Error", "La fecha de fin debe ser posterior a la de inicio")
                return
            
            # Parsear capacidad
            try:
                capacity = int(capacity_str) if capacity_str else 0
            except ValueError:
                messagebox.showerror("Error", "La capacidad debe ser un número")
                return
            
            # Mapear el estado del combobox al valor de la BD
            status_map = {
                'Activo': 'activo',
                'Planificado': 'planificado',
                'Finalizado': 'finalizado',
                'Cancelado': 'cancelado'
            }
            status_db = status_map.get(status, 'activo')
            
            # Crear o actualizar evento
            if event:
                event.title = title
                event.description = description
                event.location = location
                event.start_datetime = start_datetime
                event.end_datetime = end_datetime
                event.capacity = capacity
                event.status = status_db
                
                try:
                    if self.event_controller.update(event):
                        messagebox.showinfo("Éxito", "Evento actualizado correctamente")
                        modal.destroy()
                        self.load_events()
                    else:
                        messagebox.showerror(
                            "Error de Concurrencia", 
                            "No se pudo actualizar el evento.\n\n"
                            "El evento fue modificado por otro usuario mientras lo editabas.\n"
                            "Por favor, recarga el evento y vuelve a intentar con los datos actualizados."
                        )
                except PermissionError as e:
                    messagebox.showerror("Permiso denegado", str(e))
                    modal.destroy()
            else:
                new_event = Event(
                    title=title,
                    description=description,
                    location=location,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                    capacity=capacity,
                    status=status_db
                )
                
                try:
                    event_id = self.event_controller.create(new_event)
                    if event_id:
                        messagebox.showinfo("Éxito", "Evento creado correctamente")
                        modal.destroy()
                        self.load_events()
                    else:
                        messagebox.showerror("Error", "No se pudo crear el evento")
                except PermissionError as e:
                    messagebox.showerror("Permiso denegado", str(e))
                    modal.destroy()
        
        except PermissionError as e:
            messagebox.showerror("Permiso denegado", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def show_event_details(self, event: Event):
        """Muestra los detalles del evento en una ventana modal bonita"""
        modal = tk.Toplevel(self.parent)
        modal.title(f"Detalles del Evento: {event.title}")
        modal.geometry("700x700")
        modal.resizable(True, True)
        modal.minsize(650, 600)
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (700 // 2)
        y = (modal.winfo_screenheight() // 2) - (700 // 2)
        modal.geometry(f"700x700+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(modal, bg=COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header con color
        header = tk.Frame(main_frame, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="📅 Detalles del Evento",
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
        
        # Título del evento
        event_title = tk.Label(
            content,
            text=event.title,
            font=("Arial", 18, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary'],
            wraplength=500,
            justify=tk.LEFT
        )
        event_title.pack(anchor=tk.W, pady=(0, 20))
        
        # Información en cards
        info_frame = tk.Frame(content, bg=COLORS['white'])
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Calcular estado (igual que en load_events)
        now = datetime.now()
        if event.status and event.status.lower() in ['cancelado', 'activo', 'planificado', 'finalizado']:
            # Si hay un estado explícito, respetarlo
            status = event.status.lower()
        elif event.end_datetime and event.end_datetime < now:
            status = "finalizado"
        elif event.start_datetime and event.start_datetime <= now <= (event.end_datetime or now):
            status = "activo"
        elif event.start_datetime and event.start_datetime > now:
            status = "planificado"
        else:
            status = event.status.lower() if event.status else "activo"
        
        # Asignar colores según el estado
        if status == "cancelado":
            status_color = COLORS['danger_text']
            status_bg = COLORS['danger']
        elif status == "finalizado":
            status_color = COLORS['danger_text']
            status_bg = COLORS['danger']
        elif status == "activo":
            status_color = COLORS['success_text']
            status_bg = COLORS['success']
        elif status == "planificado":
            status_color = COLORS['badge_text']
            status_bg = COLORS['badge']
        else:
            status_color = COLORS['success_text']
            status_bg = COLORS['success']
        
        # Obtener número de inscritos confirmados (las canceladas no cuentan)
        num_registered = 0
        if self.registration_controller:
            try:
                num_registered = self.registration_controller.count_confirmed_registrations(event.event_id)
            except:
                pass
        
        # Campos de información
        fields = [
            ("📝 Descripción", event.description or "Sin descripción", True),
            ("📍 Ubicación", event.location or "No especificada", False),
            ("🕐 Fecha de inicio", event.start_datetime.strftime("%d/%m/%Y %H:%M") if event.start_datetime else "No especificada", False),
            ("🕐 Fecha de fin", event.end_datetime.strftime("%d/%m/%Y %H:%M") if event.end_datetime else "No especificada", False),
            ("👥 Capacidad", f"{num_registered} / {event.capacity} inscritos", False),
            ("📊 Estado", status.capitalize(), False, status_bg, status_color)
        ]
        
        for i, field_data in enumerate(fields):
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
            
            if is_multiline:
                value_label = tk.Label(
                    field_frame,
                    text=value,
                    font=("Arial", 10),
                    bg=COLORS['white'],
                    fg=COLORS['text_primary'],
                    anchor=tk.W,
                    justify=tk.LEFT,
                    wraplength=600,
                    padx=12,
                    pady=8,
                    relief=tk.SOLID,
                    borderwidth=1
                )
            else:
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
        
        # Botones de acción
        buttons_frame = tk.Frame(content, bg=COLORS['white'])
        buttons_frame.pack(pady=(20, 0))
        
        # Botón Editar (solo para admin)
        if self.is_admin:
            def edit_and_close():
                modal.destroy()
                self.show_event_modal(event)
            
            btn_edit = tk.Button(
                buttons_frame,
                text="✏️ Editar",
                font=("Arial", 10, "bold"),
                bg=COLORS['primary'],
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                padx=24,
                pady=10,
                command=edit_and_close
            )
            btn_edit.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón cerrar
        btn_close = tk.Button(
            buttons_frame,
            text="Cerrar",
            font=("Arial", 10, "bold"),
            bg=COLORS['text_secondary'] if self.is_admin else COLORS['primary'],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=24,
            pady=10,
            command=modal.destroy
        )
        btn_close.pack(side=tk.LEFT)
        
        # Actualizar scroll después de crear widgets
        modal.after(100, lambda: canvas.configure(scrollregion=canvas.bbox("all")))
        
        modal.bind('<Escape>', lambda e: modal.destroy())
    
    def export_csv(self):
        """Exporta eventos a CSV"""
        events = self.event_controller.get_all()
        events_dict = [e.to_dict() for e in events]
        
        filepath = CSVExporter.export_events(events_dict)
        if filepath:
            messagebox.showinfo("Éxito", f"Eventos exportados a:\n{filepath}")
        else:
            messagebox.showerror("Error", "No se pudo exportar a CSV")
    
    def export_pdf(self):
        """Exporta eventos a PDF"""
        events = self.event_controller.get_all()
        events_dict = [e.to_dict() for e in events]
        
        filepath = PDFExporter.export_events(events_dict)
        if filepath:
            messagebox.showinfo("Éxito", f"Eventos exportados a:\n{filepath}")
        else:
            messagebox.showerror("Error", "No se pudo exportar a PDF")

