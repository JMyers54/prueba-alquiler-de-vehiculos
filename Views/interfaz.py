from tkinter import *
import tkinter as tk
from Controllers.funciones import Funciones
from Views.Tooltip import Tooltip
from PIL import Image, ImageTk

class Interfaz():
    def abrir_pestanas(self):
        self.nueva_ventana = tk.Toplevel(self.ventana)
        self.nueva_ventana.title("Panel principal")
        self.nueva_ventana.geometry("1200x700")
        self.nueva_ventana.config(bg="#161616")

        self.frame_lateral = tk.Frame(self.nueva_ventana, bg="#161616", width=150)
        self.frame_lateral.place(x=0, y=0, relheight=1)

        self.btn_jcs = tk.Button(self.frame_lateral, text="MENÚ", command=self.mostrar_MENU, bg="#333", fg="white")
        self.btn_jcs.place(relx=0.5, rely=0.50, anchor="center", width=100, height=40)

        self.btn_empleado = tk.Button(self.frame_lateral, text="EMPLEADO", command=self.mostrar_empleado, bg="#333", fg="white")
        self.btn_empleado.place(relx=0.5, rely=0.43, anchor="center", width=100, height=40)

        self.btn_inventario = tk.Button(self.frame_lateral, text="INVENTARIO", command=self.mostrar_inventario, bg="#333", fg="white")
        self.btn_inventario.place(relx=0.5, rely=0.57, anchor="center", width=100, height=40)

        self.contenedor_frames = tk.Frame(self.nueva_ventana, bg="#161616", width=1050, height=700)
        self.contenedor_frames.place(x=150, y=0)

        self.frame_MENU = tk.Frame(self.contenedor_frames, bg="#161616", width=1050, height=700)
        self.frame_MENU.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_empleado = tk.Frame(self.contenedor_frames, bg="#161616", width=1050, height=700)
        self.frame_empleado.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_inventario = tk.Frame(self.contenedor_frames, bg="#161616", width=1050, height=700)
        self.frame_inventario.place(x=0, y=0, relwidth=1, relheight=1)

        self.construir_inventario()

        ruta_img1 = "prueba-alquiler-de-vehiculos/icons/logo.png"
        ruta_img2 = "prueba-alquiler-de-vehiculos/icons/lamborghini-veneno-1.png"

        imagen1 = Image.open(ruta_img1).resize((300, 300))
        self.img_MENU1 = ImageTk.PhotoImage(imagen1)
        label1 = tk.Label(self.frame_MENU, image=self.img_MENU1, bg="#161616", bd=0)
        label1.place(relx=0.5, y=-70, anchor="n")

        imagen2 = Image.open(ruta_img2).resize((800, 400))
        self.img_MENU2 = ImageTk.PhotoImage(imagen2)
        label2 = tk.Label(self.frame_MENU, image=self.img_MENU2, bg="#161616", bd=0)
        label2.place(relx=0.5, rely=0.2, anchor="n")

        label3 = tk.Label(self.frame_MENU, text="NUEVA ADQUISICIÓN", fg="white", bg="#161616", font=("Arial", 18, "bold"))
        label3.place(relx=0.5, rely=0.78, anchor="n")

        label4 = tk.Label(self.frame_MENU, text="Precio: $1000", fg="white", bg="#161616", font=("Arial", 16))
        label4.place(relx=0.5, rely=0.92, anchor="n")

        label5 = tk.Label(self.frame_MENU, text="LAMBORGHINI VENENO", fg="white", bg="#161616", font=("Arial", 16))
        label5.place(relx=0.5, rely=0.85, anchor="n")

        # Sección EMPLEADO
        tk.Label(self.frame_empleado, text="Gestión de empleados", fg="white", bg="#161616", font=("Arial", 18)).pack(pady=30)

        entrada_frame = tk.Frame(self.frame_empleado, bg="#161616")
        entrada_frame.pack(pady=10)

        lbl_cedula = tk.Label(entrada_frame, text="Ingrese cédula", fg="white", bg="#161616", font=("Arial", 14))
        lbl_cedula.pack(pady=5)
        entry_cedula = tk.Entry(entrada_frame, font=("Arial", 12))
        entry_cedula.pack(pady=5)

        lbl_contra = tk.Label(entrada_frame, text="Agregue contraseña", fg="white", bg="#161616", font=("Arial", 14))
        lbl_contra.pack(pady=5)
        entry_contra = tk.Entry(entrada_frame, show="*", font=("Arial", 12))
        entry_contra.pack(pady=5)

        btn_ingresar = tk.Button(entrada_frame, text="Ingresar", font=("Arial", 12), bg="#333", fg="white")
        btn_ingresar.pack(pady=10)

        self.mostrar_MENU()

    def actualizar_estado_botones(self, activo):
        self.btn_jcs.config(bg="#333")
        self.btn_empleado.config(bg="#333")
        self.btn_inventario.config(bg="#333")

        if activo == "MENU":
            self.btn_jcs.config(bg="#555")
        elif activo == "EMPLEADO":
            self.btn_empleado.config(bg="#555")
        elif activo == "INVENTARIO":
            self.btn_inventario.config(bg="#555")

    def mostrar_MENU(self):
        self.frame_MENU.tkraise()
        self.actualizar_estado_botones("MENU")

    def mostrar_empleado(self):
        self.frame_empleado.tkraise()
        self.actualizar_estado_botones("EMPLEADO")

    def mostrar_inventario(self):
        self.frame_inventario.tkraise()
        self.actualizar_estado_botones("INVENTARIO")

    def construir_inventario(self):
        # (Contenido sin cambios)
        pass

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Alquiler de carros")
        self.ventana.config(width=700, height=500, bg="#161616")

        self.logo = tk.PhotoImage(file=r"prueba-alquiler-de-vehiculos\icons\logo.png")
        self.label1 = tk.Label(self.ventana, image=self.logo, bd=0)
        self.label1.place(x=190, y=60, width=300, height=200)

        self.funciones = Funciones(self.ventana)

        self.btnEntrar = tk.Button(
            self.ventana,
            text="Entrar",
            bg="#161616",
            fg="white",
            font=(",20"),
            command=self.abrir_pestanas
        )
        self.btnEntrar.place(x=300, y=300, width=80, height=30)
        Tooltip(self.btnEntrar, "Entrar al menú principal...")

        self.ventana.mainloop()


if __name__ == "__main__":
    Interfaz()
