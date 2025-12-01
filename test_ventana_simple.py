"""
Test simple para verificar que Tkinter funciona
"""

import tkinter as tk
from tkinter import messagebox

def test():
    root = tk.Tk()
    root.title("Test")
    root.geometry("400x300")
    root.configure(bg="#f4f6f9")
    
    # Label de prueba
    label = tk.Label(
        root,
        text="¡Tkinter funciona!\n\nSi ves esto, el problema está en el código de la aplicación.",
        font=("Arial", 12),
        bg="#f4f6f9",
        fg="#1f4e79",
        justify=tk.CENTER
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
    test()

