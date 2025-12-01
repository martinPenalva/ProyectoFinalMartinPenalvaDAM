"""
Script de prueba para verificar que Tkinter funciona correctamente
"""

import tkinter as tk
from tkinter import ttk

def test_basic():
    """Prueba básica de Tkinter"""
    root = tk.Tk()
    root.title("Test Tkinter")
    root.geometry("400x300")
    root.configure(bg="#f4f6f9")
    
    # Label de prueba
    label = tk.Label(
        root,
        text="¡Tkinter funciona correctamente!",
        font=("Arial", 14, "bold"),
        bg="#f4f6f9",
        fg="#1f4e79"
    )
    label.pack(pady=50)
    
    # Botón
    btn = tk.Button(
        root,
        text="Cerrar",
        command=root.destroy,
        bg="#1f4e79",
        fg="white",
        padx=20,
        pady=10
    )
    btn.pack()
    
    root.mainloop()

if __name__ == "__main__":
    print("Iniciando prueba de Tkinter...")
    test_basic()
    print("Prueba completada.")

