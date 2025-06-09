from tkinter import *
import tkinter as tk
from tkinter import ttk
from funciones import Funciones
class Interfaz():

    def __init__(self):

        self.ventana = tk.Tk()
        self.ventana.title("alquiler de carros")
        self.ventana.config(width=700, height=500, bg="#161616")

        self.logo= tk.PhotoImage(file=r"icons\logo.png")
        self.label1= tk.Label(self.ventana, image=self.logo,bd=0)
        self.label1.place(x=190,y=60,width=300,height=200)
        self.funciones = Funciones(self.ventana)
        self.btnEntrar = tk.Button(self.ventana,text="Entrar", bd=0,bg="#161616",fg="white", font=(",20"), command=self.funciones.abrir_pestanas)
        self.btnEntrar.place(x=300,y=300, width=90, height=60)

        self.ventana.mainloop()