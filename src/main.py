"""
Gestor de Eventos Locales
Punto de entrada principal de la aplicación
Autor: Martin Peñalva Artázcoz
"""

import sys
import os

# Agregar el directorio raíz y src al path para imports
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.views.login_window import LoginWindow
from src.views.main_window import MainWindow
from src.database.db_connection import DatabaseConnection
import tkinter as tk
from tkinter import messagebox


class App:
    """Clase principal de la aplicación"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.db = None
        self.username = None
        self.main_window = None
        self.setup_icon()
    
    def setup_icon(self):
        """Configura el icono de la aplicación"""
        try:
            # Buscar el icono en diferentes ubicaciones posibles
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_paths = [
                os.path.join(root_dir, 'icono.ico'),
                os.path.join(root_dir, 'assets', 'icono.ico'),
                os.path.join(root_dir, 'src', 'assets', 'icono.ico'),
            ]
            
            icon_path = None
            for path in icon_paths:
                if os.path.exists(path):
                    icon_path = path
                    break
            
            if icon_path:
                # Windows
                try:
                    self.root.iconbitmap(icon_path)
                except:
                    # Si iconbitmap falla, intentar con PhotoImage (para algunos sistemas)
                    try:
                        icon = tk.PhotoImage(file=icon_path)
                        self.root.iconphoto(False, icon)
                    except:
                        pass
        except Exception as e:
            # Si no se puede cargar el icono, continuar sin él
            print(f"No se pudo cargar el icono: {e}")
    
    def start(self):
        """Inicia la aplicación mostrando el login"""
        try:
            # NO intentar conectar a MySQL aquí - mostrar la ventana primero
            self.db = None
            
            # Mostrar ventana de login INMEDIATAMENTE (sin esperar MySQL)
            login = LoginWindow(self.root, self.on_login_success)
            self.root.mainloop()
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al iniciar la aplicación:\n{str(e)}"
            )
            import traceback
            traceback.print_exc()
        finally:
            # Cerrar conexión a la base de datos si existe
            if self.db:
                try:
                    self.db.close()
                except:
                    pass
    
    def on_logout(self):
        """Callback cuando se cierra sesión"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Cerrar conexión a la base de datos
        if self.db:
            try:
                self.db.close()
            except:
                pass
        self.db = None
        self.username = None
        self.main_window = None
        
        # Mostrar login nuevamente
        login = LoginWindow(self.root, self.on_login_success)
    
    def on_login_success(self, username: str, db=None, role: str = 'user'):
        """Callback cuando el login es exitoso"""
        try:
            self.username = username
            self.user_role = role  # Guardar el rol del usuario
            self.db = db  # Base de datos (puede ser None)
            
            # Mostrar advertencia si no hay BD (después de login, no bloqueante)
            if not self.db:
                self.root.after(100, lambda: messagebox.showwarning(
                    "Modo Demo",
                    "No se pudo conectar a MySQL.\n\n"
                    "La aplicación se ejecutará en modo DEMO.\n"
                    "Podrás ver la interfaz completa pero no se guardarán datos.\n\n"
                    "Para funcionalidad completa, instala MySQL Server."
                ))
            
            # Limpiar ventana de login
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Crear y mostrar ventana principal
            print(f"Creando MainWindow con db={self.db}, username={username}, role={role}")
            self.main_window = MainWindow(self.root, self.db, username, self.on_logout, role)
            self.root.title("Gestor de Eventos Locales")
            
            # Asegurar que la ventana se muestre
            self.root.update()
            self.root.update_idletasks()
            print("MainWindow creada exitosamente")
        except Exception as e:
            error_msg = f"Error al crear la ventana principal:\n{str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            
            # Mostrar error en la ventana
            error_label = tk.Label(
                self.root,
                text=error_msg + "\n\nRevisa la consola para más detalles.",
                font=("Arial", 10),
                bg="#f4f6f9",
                fg="red",
                justify=tk.LEFT,
                wraplength=600
            )
            error_label.pack(pady=50, padx=50)
            
            messagebox.showerror("Error", error_msg)


def main():
    """Función principal que inicia la aplicación"""
    app = App()
    app.start()


if __name__ == "__main__":
    main()

