from tkinter import *
import tkinter as tk
from tkinter import messagebox, simpledialog
from Models.ConexionBD import ConexionDB

class Funciones():
    def __init__(self, ventana):
        self.ventana = ventana
    

    def registrar_empleado(self, cedula, nombre, apellido, telefono, email, contra):
        try:
            conexion = ConexionDB()
            conexion.crearConexion()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "INSERT INTO empleados (Cedula, Nombre, Apellido, Telefono, Email, Contraseña) VALUES (%s, %s, %s, %s, %s, %s)"
            datos = (cedula, nombre, apellido, telefono, email, contra)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.cerrarConexion()
            messagebox.showinfo(print("exito","empleado registrado con éxito"))
        except Exception as e:
            messagebox.showerror(print("Error",f"al registrar empleado: {e}"))

    def solicitarClave(self):
        clave = simpledialog.askstring("clave de Administrador", "Ingrese la clave de Administrador: ")
        if clave != self.adminClave:
            messagebox.showerror("Error", "Clave Incorrecta!")
            return False
        return True
    pass

    def iniciar_sesion_empleado(self, cedula, contra):
        try:
            conexion = ConexionDB()
            conexion.crearConexion()
            db = conexion.getConnection()

            with db.cursor() as cursor:
                cursor.execute("SELECT Contraseña FROM empleados WHERE Cedula = %s", (cedula,))
                resultado = cursor.fetchone()

            conexion.cerrarConexion()

            if resultado is None:
                print("Cédula no registrada.")
                return False

            if resultado[0] == contra:
                return True
            else:
                print("Contraseña incorrecta.")
                return False

        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return False

    def iniciar_sesion_admin(self, id, contra):
        try:
            conexion = ConexionDB()
            conexion.crearConexion()
            db = conexion.getConnection()

            with db.cursor() as cursor:
                cursor.execute("SELECT Contraseña FROM administradores WHERE id = %s", (id,))
                resultado = cursor.fetchone()

            conexion.cerrarConexion()

            if resultado is None:
                print("id no registrado.")
                return False

            if resultado[0] == contra:
                return True
            else:
                print("Contraseña incorrecta.")
                return False

        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return False