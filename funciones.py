from tkinter import *
import tkinter as tk
from tkinter import ttk
class Funciones():
    def __init__(self, ventana, ):
        self.ventana = ventana
    def abrir_pestanas(self):
        self.nueva_ventana = tk.Toplevel(self.ventana)
        self.nueva_ventana.title("Panel principal")
        self.nueva_ventana.geometry("700x500")
        self.nueva_ventana.config(bg="#161616")
            # Crear el Notebook
        self.ventana1 = ttk.Notebook(self.nueva_ventana)
        self.ventana1.pack(fill="both", expand=True)
        self.frame1 = tk.Frame(self.ventana1, bg="#161616")  # Fondo de la pestaña
        self.ventana1.add(self.frame1, text="JCS")

        self.frame2 = tk.Frame(self.ventana1, bg="#161616")
        self.ventana1.add(self.frame2, text="empleado")