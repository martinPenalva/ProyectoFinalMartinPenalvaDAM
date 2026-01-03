"""
Vista de reportes y exportación de datos
Permite exportar eventos, participantes e inscripciones a CSV y PDF
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import csv
from datetime import datetime
from typing import List, Dict

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.views.styles import COLORS
from src.utils.exporters import CSVExporter, PDFExporter
from src.controllers.event_controller import EventController
from src.controllers.participant_controller import ParticipantController
from src.controllers.registration_controller import RegistrationController


class ReportsView:
    """Vista completa de reportes y exportación"""
    
    def __init__(self, parent, event_controller, participant_controller, registration_controller):
        self.parent = parent
        self.event_controller = event_controller
        self.participant_controller = participant_controller
        self.registration_controller = registration_controller
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Título y subtítulo
        title_frame = tk.Frame(self.parent, bg=COLORS['background'])
        title_frame.pack(fill=tk.X, pady=(0, 24))
        
        title = tk.Label(
            title_frame,
            text="Reportes y Exportación",
            font=("Arial", 16, "bold"),
            bg=COLORS['background'],
            fg=COLORS['primary']
        )
        title.pack(anchor=tk.W)
        
        subtitle = tk.Label(
            title_frame,
            text="Exporta datos de eventos, participantes e inscripciones en formato CSV o PDF.",
            font=("Arial", 10),
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        )
        subtitle.pack(anchor=tk.W, pady=(4, 0))
        
        # Cards de exportación
        cards_frame = tk.Frame(self.parent, bg=COLORS['background'])
        cards_frame.pack(fill=tk.BOTH, expand=True)
        
        # Card: Exportar Eventos
        self.create_export_card(
            cards_frame,
            "📅 Eventos",
            "Exporta la lista completa de eventos con sus detalles",
            [
                ("CSV", self.export_events_csv),
                ("PDF", self.export_events_pdf)
            ]
        )
        
        # Card: Exportar Participantes
        self.create_export_card(
            cards_frame,
            "👤 Participantes",
            "Exporta el listado de todos los participantes registrados",
            [
                ("CSV", self.export_participants_csv),
                ("PDF", self.export_participants_pdf)
            ]
        )
        
        # Card: Exportar Inscripciones
        self.create_export_card(
            cards_frame,
            "📝 Inscripciones",
            "Exporta las inscripciones de participantes a eventos",
            [
                ("CSV", self.export_registrations_csv),
                ("PDF", self.export_registrations_pdf)
            ]
        )
        
        # Card: Reporte Completo
        self.create_export_card(
            cards_frame,
            "📊 Reporte Completo",
            "Genera un reporte completo con todos los datos del sistema",
            [
                ("PDF Completo", self.export_full_report)
            ]
        )
    
    def create_export_card(self, parent, title, description, buttons):
        """Crea una tarjeta de exportación"""
        card = tk.Frame(parent, bg=COLORS['white'], relief=tk.FLAT)
        card.pack(fill=tk.X, pady=(0, 16))
        
        # Contenido del card
        content = tk.Frame(card, bg=COLORS['white'])
        content.pack(fill=tk.X, padx=24, pady=20)
        
        # Título
        card_title = tk.Label(
            content,
            text=title,
            font=("Arial", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        )
        card_title.pack(anchor=tk.W, pady=(0, 8))
        
        # Descripción
        card_desc = tk.Label(
            content,
            text=description,
            font=("Arial", 9),
            bg=COLORS['white'],
            fg=COLORS['text_secondary'],
            wraplength=600,
            justify=tk.LEFT
        )
        card_desc.pack(anchor=tk.W, pady=(0, 16))
        
        # Botones
        btn_frame = tk.Frame(content, bg=COLORS['white'])
        btn_frame.pack(fill=tk.X)
        
        for btn_text, btn_command in buttons:
            btn = tk.Button(
                btn_frame,
                text=btn_text,
                font=("Arial", 10, "bold"),
                bg=COLORS['primary'],
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                padx=20,
                pady=10,
                command=btn_command
            )
            btn.pack(side=tk.LEFT, padx=(0, 8))
    
    def export_events_csv(self):
        """Exporta eventos a CSV"""
        if not self.event_controller:
            messagebox.showwarning("Advertencia", "Modo Demo - No se pueden exportar datos")
            return
        
        try:
            events = self.event_controller.get_all()
            if not events:
                messagebox.showinfo("Información", "No hay eventos para exportar")
                return
            
            # Convertir a diccionarios
            events_data = []
            for event in events:
                events_data.append({
                    'ID': event.event_id,
                    'Título': event.title,
                    'Descripción': event.description or '',
                    'Ubicación': event.location or '',
                    'Fecha Inicio': event.start_datetime.strftime("%d/%m/%Y %H:%M") if event.start_datetime else '',
                    'Fecha Fin': event.end_datetime.strftime("%d/%m/%Y %H:%M") if event.end_datetime else '',
                    'Capacidad': event.capacity,
                    'Estado': event.status
                })
            
            filepath = CSVExporter.export_events(events_data)
            if filepath:
                messagebox.showinfo(
                    "Éxito",
                    f"Eventos exportados correctamente a:\n{filepath}\n\n"
                    "El archivo se ha guardado en tu ordenador."
                )
                # Abrir la carpeta donde se guardó el archivo
                try:
                    import subprocess
                    import platform
                    if platform.system() == "Windows":
                        os.startfile(os.path.dirname(filepath))
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.Popen(["open", os.path.dirname(filepath)])
                    else:  # Linux
                        subprocess.Popen(["xdg-open", os.path.dirname(filepath)])
                except:
                    pass
            elif filepath is None:
                # Usuario canceló el diálogo
                pass
            else:
                messagebox.showerror("Error", "No se pudo exportar los eventos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar eventos:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def export_events_pdf(self):
        """Exporta eventos a PDF"""
        if not self.event_controller:
            messagebox.showwarning("Advertencia", "Modo Demo - No se pueden exportar datos")
            return
        
        try:
            events = self.event_controller.get_all()
            if not events:
                messagebox.showinfo("Información", "No hay eventos para exportar")
                return
            
            # Convertir a diccionarios
            events_data = []
            for event in events:
                events_data.append({
                    'event_id': event.event_id,
                    'title': event.title,
                    'description': event.description or '',
                    'location': event.location or '',
                    'start_datetime': event.start_datetime,
                    'end_datetime': event.end_datetime,
                    'capacity': event.capacity,
                    'status': event.status
                })
            
            filepath = PDFExporter.export_events(events_data)
            if filepath:
                messagebox.showinfo(
                    "Éxito",
                    f"Eventos exportados correctamente a:\n{filepath}\n\n"
                    "El archivo se ha guardado en tu ordenador."
                )
                # Abrir la carpeta donde se guardó el archivo
                try:
                    import subprocess
                    import platform
                    if platform.system() == "Windows":
                        os.startfile(os.path.dirname(filepath))
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.Popen(["open", os.path.dirname(filepath)])
                    else:  # Linux
                        subprocess.Popen(["xdg-open", os.path.dirname(filepath)])
                except:
                    pass
            elif filepath is None:
                # Usuario canceló el diálogo
                pass
            else:
                messagebox.showerror("Error", "No se pudo exportar los eventos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar eventos:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def export_participants_csv(self):
        """Exporta participantes a CSV"""
        if not self.participant_controller:
            messagebox.showwarning("Advertencia", "Modo Demo - No se pueden exportar datos")
            return
        
        try:
            participants = self.participant_controller.get_all()
            if not participants:
                messagebox.showinfo("Información", "No hay participantes para exportar")
                return
            
            # Convertir a diccionarios
            participants_data = []
            for participant in participants:
                participants_data.append({
                    'ID': participant.participant_id,
                    'Nombre': participant.first_name,
                    'Apellidos': participant.last_name,
                    'Email': participant.email,
                    'Teléfono': participant.phone or '',
                    'DNI/NIE': participant.identifier
                })
            
            filepath = CSVExporter.export_participants(participants_data)
            if filepath:
                messagebox.showinfo(
                    "Éxito",
                    f"Participantes exportados correctamente a:\n{filepath}\n\n"
                    "El archivo se ha guardado en tu ordenador."
                )
                # Abrir la carpeta donde se guardó el archivo
                try:
                    import subprocess
                    import platform
                    if platform.system() == "Windows":
                        os.startfile(os.path.dirname(filepath))
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.Popen(["open", os.path.dirname(filepath)])
                    else:  # Linux
                        subprocess.Popen(["xdg-open", os.path.dirname(filepath)])
                except:
                    pass
            elif filepath is None:
                # Usuario canceló el diálogo
                pass
            else:
                messagebox.showerror("Error", "No se pudo exportar los participantes")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar participantes:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def export_participants_pdf(self):
        """Exporta participantes a PDF"""
        if not self.participant_controller:
            messagebox.showwarning("Advertencia", "Modo Demo - No se pueden exportar datos")
            return
        
        try:
            participants = self.participant_controller.get_all()
            if not participants:
                messagebox.showinfo("Información", "No hay participantes para exportar")
                return
            
            # Convertir a diccionarios
            participants_data = []
            for participant in participants:
                participants_data.append({
                    'participant_id': participant.participant_id,
                    'first_name': participant.first_name,
                    'last_name': participant.last_name,
                    'email': participant.email,
                    'phone': participant.phone or '',
                    'identifier': participant.identifier
                })
            
            filepath = PDFExporter.export_participants(participants_data)
            if filepath:
                messagebox.showinfo(
                    "Éxito",
                    f"Participantes exportados correctamente a:\n{filepath}\n\n"
                    "El archivo se ha guardado en tu ordenador."
                )
                # Abrir la carpeta donde se guardó el archivo
                try:
                    import subprocess
                    import platform
                    if platform.system() == "Windows":
                        os.startfile(os.path.dirname(filepath))
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.Popen(["open", os.path.dirname(filepath)])
                    else:  # Linux
                        subprocess.Popen(["xdg-open", os.path.dirname(filepath)])
                except:
                    pass
            elif filepath is None:
                # Usuario canceló el diálogo
                pass
            else:
                messagebox.showerror("Error", "No se pudo exportar los participantes")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar participantes:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def export_registrations_csv(self):
        """Exporta inscripciones a CSV"""
        if not self.registration_controller or not self.event_controller:
            messagebox.showwarning("Advertencia", "Modo Demo - No se pueden exportar datos")
            return
        
        try:
            # Obtener todas las inscripciones
            all_registrations = []
            events = self.event_controller.get_all() if self.event_controller else []
            
            for event in events:
                participants = self.registration_controller.get_event_participants(event.event_id)
                for participant in participants:
                    all_registrations.append({
                        'ID Evento': event.event_id,
                        'Evento': event.title,
                        'ID Participante': participant['participant_id'],
                        'Participante': f"{participant['first_name']} {participant['last_name']}",
                        'Email': participant['email'],
                        'Teléfono': participant.get('phone', '') or '',
                        'Fecha Inscripción': participant.get('registered_at', ''),
                        'Estado': participant.get('registration_status', 'confirmado')
                    })
            
            if not all_registrations:
                messagebox.showinfo("Información", "No hay inscripciones para exportar")
                return
            
            # Usar diálogo de guardado
            default_filename = f"inscripciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
                initialfile=default_filename,
                title="Guardar inscripciones como CSV"
            )
            
            if not filepath:  # Usuario canceló
                return
            
            # Exportar usando CSVExporter
            from config.config import EXPORT_CONFIG
            
            try:
                with open(filepath, 'w', newline='', encoding=EXPORT_CONFIG['csv_encoding']) as f:
                    if all_registrations:
                        fieldnames = all_registrations[0].keys()
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(all_registrations)
                
                messagebox.showinfo(
                    "Éxito",
                    f"Inscripciones exportadas correctamente a:\n{filepath}\n\n"
                    "El archivo se ha guardado en tu ordenador."
                )
                # Abrir la carpeta donde se guardó el archivo
                try:
                    import subprocess
                    import platform
                    if platform.system() == "Windows":
                        os.startfile(os.path.dirname(filepath))
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.Popen(["open", os.path.dirname(filepath)])
                    else:  # Linux
                        subprocess.Popen(["xdg-open", os.path.dirname(filepath)])
                except:
                    pass
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el archivo:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar inscripciones:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def export_registrations_pdf(self):
        """Exporta inscripciones a PDF"""
        if not self.registration_controller or not self.event_controller:
            messagebox.showwarning("Advertencia", "Modo Demo - No se pueden exportar datos")
            return
        
        try:
            # Obtener todas las inscripciones
            all_registrations = []
            events = self.event_controller.get_all() if self.event_controller else []
            
            for event in events:
                participants = self.registration_controller.get_event_participants(event.event_id)
                for participant in participants:
                    all_registrations.append({
                        'ID Evento': event.event_id,
                        'Evento': event.title,
                        'ID Participante': participant['participant_id'],
                        'Participante': f"{participant['first_name']} {participant['last_name']}",
                        'Email': participant['email'],
                        'Teléfono': participant.get('phone', '') or '',
                        'Fecha Inscripción': participant.get('registered_at', ''),
                        'Estado': participant.get('registration_status', 'confirmado')
                    })
            
            if not all_registrations:
                messagebox.showinfo("Información", "No hay inscripciones para exportar")
                return
            
            filepath = PDFExporter.export_registrations(all_registrations)
            if filepath:
                messagebox.showinfo(
                    "Éxito",
                    f"Inscripciones exportadas correctamente a:\n{filepath}\n\n"
                    "El archivo se ha guardado en tu ordenador."
                )
                # Abrir la carpeta donde se guardó el archivo
                try:
                    import subprocess
                    import platform
                    if platform.system() == "Windows":
                        os.startfile(os.path.dirname(filepath))
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.Popen(["open", os.path.dirname(filepath)])
                    else:  # Linux
                        subprocess.Popen(["xdg-open", os.path.dirname(filepath)])
                except:
                    pass
            elif filepath is None:
                # Usuario canceló el diálogo
                pass
            else:
                messagebox.showerror("Error", "No se pudo exportar las inscripciones")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar inscripciones:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def export_full_report(self):
        """Exporta un reporte completo en PDF"""
        messagebox.showinfo(
            "Información",
            "El reporte completo está en desarrollo.\n\n"
            "Por ahora, puedes exportar eventos y participantes por separado."
        )

