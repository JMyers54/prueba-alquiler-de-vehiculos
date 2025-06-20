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

    def agregar_vehiculos(self, id, marca, modelo, año, tipo, precio_diario, estado, imagen):
        try:
            conexion = ConexionDB()
            conexion.crearConexion()
            db = conexion.getConnection()
            with db.cursor() as cursor:
                cursor.execute("INSERT INTO vehiculos (ID, MARCA, MODELO, AÑO, TIPO, PRECIO_DIARIO, ESTADO, IMAGEN) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(id, marca, modelo, año, tipo, precio_diario, estado, imagen))
                db.commit()
            conexion.cerrarConexion()
            return True
        except Exception as e:
            print(f"Error al agregar vehiculo {e}")
            return False

    
    def eliminar_vehiculos(self,id):
        try:
            conexion = ConexionDB()
            conexion.crearConexion()
            db = conexion.getConnection()
            with db.cursor() as cursor:
                cursor.execute("DELETE FROM vehiculos WHERE ID = %s", (id,))
                db.commit()
            conexion.cerrarConexion()
            return True
        except Exception as e:
            print(f"Error al eliminar vehiculo: {e}")
            return False
    


class Empleado(Administrador):
    def __init__(self,Cedula,Nombre,Apellido,Telefono,Email):
        self.Cedula = Cedula
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Telefono = Telefono
        self.Email = Email

    def registrar(self):
        db = ConexionDB()
        try:
            db.cursor.execute("INSERT INTO administradores(cedula, nombre, apellido, telefono, email, usuario, contraseña)VALUES (%s, %s, %s, %s, %s, %s, %s)",(self.Cedula, self.Nombre, self.Apellido, self.Telefono, self.Email, self.usuario, self.contraseña))
            db.conn.commit()
        finally:
            db.cerrar()

class Cliente(Empleado):
    def __init__(self,Cedula,Nombre,Apellido,Telefono,Email,LicenciaDeConducir):
        self.Cedula = Cedula
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Telefono = Telefono
        self.Email = Email
        self.LicenciaDeConducir = LicenciaDeConducir