from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

class Funciones():
    def __init__(self, ventana):
        self.ventana = ventana

class Administrador():
    def __init__(self,Cedula,Nombre,Apellido,Telefono,Email):
        self.Cedula = Cedula
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Telefono = Telefono
        self.Email = Email
class Empleado(Administrador):
    def __init__(self,Cedula,Nombre,Apellido,Telefono,Email):
        super().__init__(Cedula,Nombre,Apellido,Telefono,Email)

class Cliente(Empleado):
    def __init__(self,Cedula,Nombre,Apellido,Telefono,Email,LincenciaDeConducir):
        super().__init__(Cedula,Nombre,Apellido,Telefono,Email)
        self.LincenciaDeConduncir = LincenciaDeConducir
