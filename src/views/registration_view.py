"""
Vista de gestión de inscripciones
Permite ver, crear y eliminar inscripciones de participantes a eventos
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime
from typing import List, Dict

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.views.styles import COLORS
from src.controllers.registration_controller import RegistrationController
from src.controllers.event_controller import EventController
from src.controllers.participant_controller import ParticipantController


class RegistrationView:
    """Vista completa de gestión de inscripciones"""
    
    def __init__(self, parent, registration_controller, event_controller, participant_controller, is_admin=False):
        self.parent = parent
        self.registration_controller = registration_controller
        self.event_controller = event_controller
        self.participant_controller = participant_controller
        self.is_admin = is_admin
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Título y subtítulo
        title_frame = tk.Frame(self.parent, bg=COLORS['background'])
        title_frame.pack(fill=tk.X, pady=(0, 16))
        
        title = tk.Label(
            title_frame,
            text="Gestión de Inscripciones",
            font=("Arial", 16, "bold"),
            bg=COLORS['background'],
            fg=COLORS['primary']
        )
        title.pack(anchor=tk.W)
        
        subtitle = tk.Label(
            title_frame,
            text="Asigna participantes a eventos y gestiona sus inscripciones.",
            font=("Arial", 10),
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        )
        subtitle.pack(anchor=tk.W, pady=(4, 0))
        
        # Barra de herramientas
        toolbar = tk.Frame(self.parent, bg=COLORS['background'])
        toolbar.pack(fill=tk.X, pady=(0, 16))
        
        btn_new = tk.Button(
            toolbar,
            text="➕ Nueva Inscripción",
            font=("Arial", 10, "bold"),
            bg=COLORS['primary'],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=8,
            command=self.show_new_registration_modal,
            state=tk.NORMAL if self.is_admin else tk.DISABLED
        )
        btn_new.pack(side=tk.LEFT)
        if not self.is_admin:
            info_label = tk.Label(
                toolbar,
                text="(Solo administradores pueden crear/editar inscripciones)",
                font=("Arial", 8),
                bg=COLORS['background'],
                fg=COLORS['text_secondary']
            )
            info_label.pack(side=tk.LEFT, padx=(12, 0))
        
        btn_refresh = tk.Button(
            toolbar,
            text="🔄 Actualizar",
            font=("Arial", 10),
            bg=COLORS['white'],
            fg=COLORS['text_primary'],
            relief=tk.SOLID,
            borderwidth=1,
            cursor="hand2",
            padx=16,
            pady=8,
            command=self.load_data
        )
        btn_refresh.pack(side=tk.LEFT, padx=(8, 0))
        
        # Filtros
        filter_frame = tk.Frame(self.parent, bg=COLORS['background'])
        filter_frame.pack(fill=tk.X, pady=(0, 16))
        
        tk.Label(
            filter_frame,
            text="Filtrar por evento:",
            font=("Arial", 9),
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        ).pack(side=tk.LEFT, padx=(0, 8))
        
        self.filter_event_var = tk.StringVar(value="Todos")
        self.filter_event_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_event_var,
            state="readonly",
            width=30,
            font=("Arial", 9)
        )
        self.filter_event_combo.pack(side=tk.LEFT)
        self.filter_event_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Tabla de inscripciones
        table_container = tk.Frame(self.parent, bg=COLORS['white'], relief=tk.FLAT)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Headers
        headers_frame = tk.Frame(table_container, bg=COLORS['table_header'])
        headers_frame.pack(fill=tk.X)
        
        headers = ["Evento", "Participante", "Email", "Teléfono", "Fecha Inscripción", "Estado", "Acciones"]
        header_widths = [200, 150, 180, 100, 140, 100, 120]
        
        for header, width in zip(headers, header_widths):
            label = tk.Label(
                headers_frame,
                text=header.upper(),
                font=("Arial", 9, "bold"),
                bg=COLORS['table_header'],
                fg=COLORS['text_secondary'],
                padx=8,
                pady=10,
                anchor=tk.W,
                width=width // 8
            )
            label.pack(side=tk.LEFT, padx=2)
        
        # Scrollable frame para las filas
        canvas_frame = tk.Frame(table_container, bg=COLORS['white'])
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg=COLORS['white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=COLORS['white'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.table_canvas = canvas
        self.table_frame = self.scrollable_frame
    
    def load_data(self):
        """Carga los datos de inscripciones"""
        # Limpiar tabla
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        if not self.registration_controller:
            no_data_label = tk.Label(
                self.table_frame,
                text="Modo Demo - Sin base de datos",
                font=("Arial", 10),
                bg=COLORS['white'],
                fg=COLORS['text_secondary'],
                pady=20
            )
            no_data_label.pack()
            return
        
        try:
            # Obtener todos los eventos para el filtro
            events = self.event_controller.get_all() if self.event_controller else []
            event_dict = {e.event_id: e for e in events}
            
            # Actualizar combo de filtros
            event_names = ["Todos"] + [e.title for e in events]
            self.filter_event_combo['values'] = event_names
            
            # Obtener todas las inscripciones
            all_registrations = []
            for event in events:
                participants = self.registration_controller.get_event_participants(event.event_id)
                for participant in participants:
                    all_registrations.append({
                        'event_id': event.event_id,
                        'event_title': event.title,
                        'participant_id': participant['participant_id'],
                        'participant_name': f"{participant['first_name']} {participant['last_name']}",
                        'email': participant['email'],
                        'phone': participant.get('phone', ''),
                        'registered_at': participant.get('registered_at', ''),
                        'status': participant.get('registration_status', 'confirmado')
                    })
            
            # Aplicar filtro
            filtered = self.filter_registrations(all_registrations)
            
            if not filtered:
                no_data_label = tk.Label(
                    self.table_frame,
                    text="No hay inscripciones registradas",
                    font=("Arial", 10),
                    bg=COLORS['white'],
                    fg=COLORS['text_secondary'],
                    pady=20
                )
                no_data_label.pack()
                return
            
            # Mostrar inscripciones
            for i, reg in enumerate(filtered):
                self.create_registration_row(reg, i)
            
            # Actualizar scroll
            self.table_canvas.update_idletasks()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar inscripciones:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def filter_registrations(self, registrations: List[Dict]) -> List[Dict]:
        """Filtra las inscripciones según el filtro seleccionado"""
        filter_value = self.filter_event_var.get()
        if filter_value == "Todos":
            return registrations
        
        # Buscar el evento seleccionado
        events = self.event_controller.get_all() if self.event_controller else []
        selected_event = None
        for event in events:
            if event.title == filter_value:
                selected_event = event
                break
        
        if selected_event:
            return [r for r in registrations if r['event_id'] == selected_event.event_id]
        
        return registrations
    
    def apply_filters(self):
        """Aplica los filtros y recarga la tabla"""
        self.load_data()
    
    def create_registration_row(self, registration: Dict, index: int):
        """Crea una fila en la tabla de inscripciones"""
        row_frame = tk.Frame(
            self.table_frame,
            bg=COLORS['white'] if index % 2 == 0 else COLORS['table_row_even']
        )
        row_frame.pack(fill=tk.X)
        
        # Formatear fecha
        registered_at = registration.get('registered_at', '')
        if registered_at:
            if isinstance(registered_at, datetime):
                date_str = registered_at.strftime("%d/%m/%Y %H:%M")
            else:
                try:
                    date_str = datetime.strptime(str(registered_at), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
                except:
                    date_str = str(registered_at)
        else:
            date_str = ""
        
        # Formatear teléfono
        phone = registration.get('phone', '')
        phone_str = str(phone) if phone else "-"
        
        # Estado con color
        status = registration.get('status', 'confirmado')
        status_bg = COLORS['success'] if status == 'confirmado' else COLORS['warning']
        status_text_color = COLORS['success_text'] if status == 'confirmado' else COLORS['warning_text']
        
        data = [
            registration['event_title'][:30],
            registration['participant_name'][:25],
            registration['email'][:30],
            phone_str,
            date_str,
            status
        ]
        
        widths = [200, 150, 180, 100, 140, 100]
        
        for data_item, width in zip(data, widths):
            if data_item == status:
                # Estado con color
                status_label = tk.Label(
                    row_frame,
                    text=status.upper(),
                    font=("Arial", 8),
                    bg=status_bg,
                    fg=status_text_color,
                    padx=8,
                    pady=6,
                    anchor=tk.W
                )
                status_label.pack(side=tk.LEFT, padx=2, fill=tk.Y)
            else:
                label = tk.Label(
                    row_frame,
                    text=str(data_item),
                    font=("Arial", 9),
                    bg=row_frame.cget('bg'),
                    fg=COLORS['text_primary'],
                    padx=8,
                    pady=8,
                    anchor=tk.W,
                    width=width // 8
                )
                label.pack(side=tk.LEFT, padx=2)
        
        # Botón eliminar (solo admin)
        if self.is_admin:
            btn_delete = tk.Button(
                row_frame,
                text="🗑️",
                font=("Arial", 10),
                bg=row_frame.cget('bg'),
                fg=COLORS['danger_text'],
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda: self.delete_registration(
                    registration['event_id'],
                    registration['participant_id']
                )
            )
            btn_delete.pack(side=tk.LEFT, padx=4)
    
    def show_new_registration_modal(self):
        """Muestra el modal para crear una nueva inscripción"""
        if not self.registration_controller:
            messagebox.showwarning("Advertencia", "Modo Demo - No se pueden crear inscripciones")
            return
        
        modal = tk.Toplevel(self.parent)
        modal.title("Nueva Inscripción")
        modal.geometry("500x300")
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (300 // 2)
        modal.geometry(f"500x300+{x}+{y}")
        
        content = tk.Frame(modal, bg=COLORS['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        # Título
        title = tk.Label(
            content,
            text="Nueva Inscripción",
            font=("Arial", 14, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        )
        title.pack(anchor=tk.W, pady=(0, 20))
        
        # Seleccionar evento
        tk.Label(
            content,
            text="Evento:",
            font=("Arial", 10),
            bg=COLORS['white'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 4))
        
        events = self.event_controller.get_all() if self.event_controller else []
        event_names = [e.title for e in events]
        
        if not event_names:
            tk.Label(
                content,
                text="No hay eventos disponibles",
                font=("Arial", 9),
                bg=COLORS['white'],
                fg=COLORS['text_secondary']
            ).pack(anchor=tk.W, pady=(0, 20))
            tk.Button(
                content,
                text="Cerrar",
                command=modal.destroy,
                bg=COLORS['primary'],
                fg="white",
                padx=20,
                pady=8
            ).pack(pady=10)
            return
        
        event_combo = ttk.Combobox(
            content,
            values=event_names,
            state="readonly",
            font=("Arial", 10),
            width=40
        )
        event_combo.pack(fill=tk.X, pady=(0, 16))
        event_combo.current(0)
        
        # Seleccionar participante
        tk.Label(
            content,
            text="Participante:",
            font=("Arial", 10),
            bg=COLORS['white'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 4))
        
        participants = self.participant_controller.get_all() if self.participant_controller else []
        participant_names = [f"{p.first_name} {p.last_name} ({p.email})" for p in participants]
        
        if not participant_names:
            tk.Label(
                content,
                text="No hay participantes disponibles",
                font=("Arial", 9),
                bg=COLORS['white'],
                fg=COLORS['text_secondary']
            ).pack(anchor=tk.W, pady=(0, 20))
            tk.Button(
                content,
                text="Cerrar",
                command=modal.destroy,
                bg=COLORS['primary'],
                fg="white",
                padx=20,
                pady=8
            ).pack(pady=10)
            return
        
        participant_combo = ttk.Combobox(
            content,
            values=participant_names,
            state="readonly",
            font=("Arial", 10),
            width=40
        )
        participant_combo.pack(fill=tk.X, pady=(0, 24))
        participant_combo.current(0)
        
        def on_confirm():
            event_idx = event_combo.current()
            participant_idx = participant_combo.current()
            
            if event_idx < 0 or participant_idx < 0:
                messagebox.showerror("Error", "Selecciona un evento y un participante")
                return
            
            selected_event = events[event_idx]
            selected_participant = participants[participant_idx]
            
            # Registrar
            registration_id = self.registration_controller.register_participant(
                selected_event.event_id,
                selected_participant.participant_id
            )
            
            if registration_id:
                messagebox.showinfo("Éxito", "Inscripción creada correctamente")
                modal.destroy()
                self.load_data()
            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo crear la inscripción.\n\n"
                    "El participante ya está inscrito o el evento está lleno."
                )
        
        # Botones
        btn_frame = tk.Frame(content, bg=COLORS['white'])
        btn_frame.pack(fill=tk.X)
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            command=modal.destroy,
            bg=COLORS['white'],
            fg=COLORS['text_primary'],
            relief=tk.SOLID,
            borderwidth=1,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=(0, 8))
        
        tk.Button(
            btn_frame,
            text="Crear Inscripción",
            command=on_confirm,
            bg=COLORS['primary'],
            fg="white",
            padx=20,
            pady=8
        ).pack(side=tk.LEFT)
    
    def delete_registration(self, event_id: int, participant_id: int):
        """Elimina una inscripción"""
        if not self.registration_controller:
            messagebox.showwarning("Advertencia", "Modo Demo - No se pueden eliminar inscripciones")
            return
        
        result = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Estás seguro de que deseas eliminar esta inscripción?"
        )
        
        if result:
            success = self.registration_controller.unregister_participant(event_id, participant_id)
            if success:
                messagebox.showinfo("Éxito", "Inscripción eliminada correctamente")
                self.load_data()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la inscripción")

