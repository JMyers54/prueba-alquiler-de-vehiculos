from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import winsound
from Models.ConexionBD import ConexionDB

class Administrador():    
    def __init__(self,Cedula,Nombre,Apellido,Telefono,Email,Usuario,Contraseña):
        self.Cedula = Cedula
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Telefono = Telefono
        self.Email = Email
        self.Usuario = Usuario
        self.Contraseña = Contraseña

    def registrar(self):
        db = ConexionDB()
        try:
            db.cursor.execute("""
                INSERT INTO administradores
                (cedula, nombre, apellido, telefono, email, usuario, contraseña)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (self.Cedula, self.Nombre, self.Apellido, self.Telefono, self.Email, self.usuario, self.contraseña))
            db.conn.commit()
        finally:
            db.cerrar()

    def gestionarEmpleados(self):
        pass
    def informeUsoVehiculos(self):
        pass



class Empleado(Administrador):
    def __init__(self,Cedula,Nombre,Apellido,Telefono,Email):
        super().__init__(Cedula,Nombre,Apellido,Telefono,Email)

    def gestionarAlquiler(self):
        pass

    def gestionarDevolucion(self):
            pass

class Cliente(Empleado):
    def __init__(self,Cedula,Nombre,Apellido,Telefono,Email,LincenciaDeConducir):
        super().__init__(Cedula,Nombre,Apellido,Telefono,Email)