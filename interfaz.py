from tkinter import *
import tkinter as tk
from tkinter import ttk
from funciones import Funciones
from Tooltip import Tooltip
class Interfaz():
    def abrir_pestanas(self):
        self.nueva_ventana = tk.Toplevel(self.ventana)
        self.nueva_ventana.title("Pagina Principal")
        self.nueva_ventana.geometry("700x500")
        self.nueva_ventana.config(bg="#161616")

        self.ventana1 = ttk.Notebook(self.nueva_ventana)
        self.ventana1.pack(fill="both", expand=True)

        self.frame1 = tk.Frame(self.ventana1, bg="#161616") 
        self.ventana1.add(self.frame1, text="JCS")

        self.frame2 = tk.Frame(self.ventana1, bg="#161616")
        self.ventana1.add(self.frame2, text="empleado")

        self.frame3 = tk.Frame(self.ventana1, bg="#161616")
        self.ventana1.add(self.frame3, text="administrador")

        self.btnInventario = tk.Button(self.frame1, text="Inventario",bd=0,fg="white",bg="#161616")
        self.btnInventario.place(x=140,y=350, width=80, height=30)
        Tooltip(self.btnInventario, "carros disponibles y precios")

        self.btnAlquiler = tk.Button(self.frame1, text="Alquilar", bd=0,fg="white", bg="#161616")
        self.btnAlquiler.place(x=460, y=350, width=80, height=30)
        Tooltip(self.btnAlquiler, "alquile su vehiculo y mire sus especificaciones")

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("alquiler de carros")
        self.ventana.config(width=700, height=500, bg="#161616")

        self.logo= tk.PhotoImage(file=r"icons\logo.png")
        self.label1= tk.Label(self.ventana, image=self.logo,bd=0)
        self.label1.place(x=190,y=60,width=300,height=200)
        self.funciones = Funciones(self.ventana)
        self.btnEntrar = tk.Button(self.ventana,text="Entrar", bd=0,bg="#161616",fg="white", font=(",20"), command=self.abrir_pestanas)
        self.btnEntrar.place(x=300,y=300, width=80, height=30)
        Tooltip(self.btnEntrar, "entrar al menu principal.." )

        self.ventana.mainloop()