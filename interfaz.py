from tkinter import *
import tkinter as tk
from funciones import Funciones
from Tooltip import Tooltip

class Interfaz():
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Alquiler de carros")
        self.ventana.config(width=700, height=500, bg="#161616")

        self.logo = tk.PhotoImage(file=r"prueba-alquiler-de-vehiculos\icons\logo.png")
        self.label1 = tk.Label(self.ventana, image=self.logo, bd=0)
        self.label1.place(x=190, y=60, width=300, height=200)

        # ✅ Crear instancia de Funciones
        self.funciones = Funciones(self.ventana)

        # ✅ El botón Entrar llama a abrir_pestanas de la clase Funciones
        self.btnEntrar = tk.Button(
            self.ventana,
            text="Entrar",
            bg="#161616",
            fg="white",
            font=(",20"),
            command=self.funciones.abrir_pestanas
        )
        self.btnEntrar.place(x=300, y=300, width=80, height=30)
        Tooltip(self.btnEntrar, "Entrar al menú principal...")

        self.ventana.mainloop()

# Ejecutar la interfaz
if __name__ == "__main__":
    Interfaz()