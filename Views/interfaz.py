        
from tkinter import *
import tkinter as tk
from Controllers.funcionesGenerales import Funciones
from Views.Tooltip import Tooltip
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import Toplevel



class Interfaz():
    def abrir_pestanas(self):
#-------------------------------------pantalla principal--------------------------------------------------
        self.nueva_ventana = tk.Toplevel(self.ventana)
        self.nueva_ventana.title("Panel principal")
        self.nueva_ventana.geometry("1200x700")
        self.nueva_ventana.config(bg="#161616")

        self.frame_lateral = tk.Frame(self.nueva_ventana, bg="#222222", width=150)
        self.frame_lateral.place(x=0, y=0, relheight=1)

        self.btn_jcs = tk.Button(self.frame_lateral, text="MENÚ", command=self.mostrar_MENU, bg="#333", fg="white")
        self.btn_jcs.place(relx=0.5, rely=0.50, anchor="center", width=100, height=40)

        self.btn_empleado = tk.Button(self.frame_lateral, text="EMPLEADO", command=self.mostrar_empleado, bg="#333", fg="white")
        self.btn_empleado.place(relx=0.5, rely=0.43, anchor="center", width=100, height=40)

        self.btn_inventario = tk.Button(self.frame_lateral, text="INVENTARIO", command=self.mostrar_inventario, bg="#333", fg="white")
        self.btn_inventario.place(relx=0.5, rely=0.57, anchor="center", width=100, height=40)

        self.btn_administrador = tk.Button(self.frame_lateral, text="ADMINISTRADOR", command=self.mostrar_administrador, bg="#333", fg="white")
        self.btn_administrador.place(relx=0.5, rely=0.36, anchor="center", width=100, height=40)

        self.contenedor_frames = tk.Frame(self.nueva_ventana, bg="#161616", width=1050, height=700)
        self.contenedor_frames.place(x=150, y=0)

        self.frame_MENU = tk.Frame(self.contenedor_frames, bg="#161616", width=1050, height=700)
        self.frame_MENU.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_empleado = tk.Frame(self.contenedor_frames, bg="#161616", width=1050, height=700)
        self.frame_empleado.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_administrador = tk.Frame(self.contenedor_frames, bg="#161616", width=1050, height=700)
        self.frame_administrador.place(x=0, y=0,relwidth=1 ,relheight=1)

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
#----------------------------------segmento administrador--------------------------------------------------------------------
        self.label1 = tk.Label(self.frame_administrador, image=self.logo, bd=0)
        self.label1.place(x=385, y=70, width=330, height=220)

        tk.Label(self.frame_administrador, text=" Area de Administrador", fg="white", bg="#161616", font=("Arial", 16)).place(rely=0.45, relx=0.43)

        self.registrarse_empleado = tk.Button(self.frame_administrador, text="Registrarse", font=("Arial", 13), bg="#333", fg="white", command=self.resgistro_empleado)
        self.registrarse_empleado.place(rely=0.70, relx=0.55)

        lblId = tk.Label(self.frame_administrador, text="Id:", fg="white", bg="#161616", font=("Arial", 12))
        lblId.place(rely=0.55, relx=0.41)
        entryId = tk.Entry(self.frame_administrador, font=("Arial", 12))
        entryId.place(rely=0.55, relx=0.45)

        lblContraAdmin = tk.Label(self.frame_administrador, text="Contraseña:", fg="white", bg="#161616", font=("Arial", 12))
        lblContraAdmin.place(rely=0.60, relx=0.35)
        entryContraAdmin = tk.Entry(self.frame_administrador, show="*", font=("Arial", 12))
        entryContraAdmin.place(rely=0.60, relx=0.45)
        
        def login_admin():
            id = entryId.get()
            contraAdmin = entryContraAdmin.get()
            if self.funciones.iniciar_sesion_admin(id, contraAdmin):
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
                # Aquí puedes redirigir a la ventana principal del empleado
            else:
                messagebox.showerror("Error", "Cédula o contraseña incorrecta.")

        self.iniciar_sesion_empleado = tk.Button(self.frame_administrador, text="Iniciar Sesión", font=("Arial", 13), bg="#333", fg="white", command=login_admin)
        self.iniciar_sesion_empleado.place(rely=0.70, relx=0.42)
#----------------------------------segmento empleados------------------------------------------------------------------------
        self.label1 = tk.Label(self.frame_empleado, image=self.logo, bd=0)
        self.label1.place(x=385, y=70, width=330, height=220)

        tk.Label(self.frame_empleado, text="   Area de Empleados", fg="white", bg="#161616", font=("Arial", 16)).place(rely=0.45, relx=0.43)

        self.registrarse_empleado = tk.Button(self.frame_empleado, text="Registrarse", font=("Arial", 13), bg="#333", fg="white", command=self.resgistro_empleado)
        self.registrarse_empleado.place(rely=0.70, relx=0.55)

        lblCedula = tk.Label(self.frame_empleado, text="Cédula:", fg="white", bg="#161616", font=("Arial", 12))
        lblCedula.place(rely=0.55, relx=0.38)
        entryCedula = tk.Entry(self.frame_empleado, font=("Arial", 12))
        entryCedula.place(rely=0.55, relx=0.45)

        lblContra = tk.Label(self.frame_empleado, text="Contraseña:", fg="white", bg="#161616", font=("Arial", 12))
        lblContra.place(rely=0.60, relx=0.35)
        entryContra = tk.Entry(self.frame_empleado, show="*", font=("Arial", 12))
        entryContra.place(rely=0.60, relx=0.45)

        def intentar_login():
            cedula = entryCedula.get()
            contra = entryContra.get()
            if self.funciones.iniciar_sesion_empleado(cedula, contra):
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
                # Aquí puedes redirigir a la ventana principal del empleado
            else:
                messagebox.showerror("Error", "Cédula o contraseña incorrecta.")

        self.iniciar_sesion_empleado = tk.Button(self.frame_empleado, text="Iniciar Sesión", font=("Arial", 13), bg="#333", fg="white", command=intentar_login)
        self.iniciar_sesion_empleado.place(rely=0.70, relx=0.42)
    
    def resgistro_empleado(self):
        self.pestaña_registros_empleado = tk.Toplevel(self.frame_empleado)
        self.pestaña_registros_empleado.title("registrar empleado")
        self.pestaña_registros_empleado.geometry("600x600")
        self.pestaña_registros_empleado.config(bg="#161616")
        entrada_frame = tk.Frame(self.frame_empleado, bg="#161616")
        entrada_frame.pack(pady=10)

        tk.Label(self.pestaña_registros_empleado, text="Gestión de empleados", fg="white", bg="#161616", font=("Arial", 18)).pack(pady=30)

        lblCedula = tk.Label(self.pestaña_registros_empleado, text="Ingrese cédula*", fg="white", bg="#161616", font=("Arial", 14))
        lblCedula.pack(pady=5)
        entryCedula = tk.Entry(self.pestaña_registros_empleado, font=("Arial", 12))
        entryCedula.pack(pady=5)

        lblNombre = tk.Label(self.pestaña_registros_empleado, text="Ingrese su Nombre*", fg="white", bg="#161616", font=("arial", 14))
        lblNombre.pack(pady=5)
        entryNombre = tk.Entry(self.pestaña_registros_empleado, font=("arial", 12))
        entryNombre.pack(pady=5)

        lblApellido = tk.Label(self.pestaña_registros_empleado, text="Ingrese sus apellidos*", fg="white", bg="#161616", font=("Arial", 14))
        lblApellido.pack(pady=5)
        entryApellido = tk.Entry(self.pestaña_registros_empleado, font=("arial", 12))
        entryApellido.pack(pady=5)

        lbltelefono = tk.Label(self.pestaña_registros_empleado, text="Ingrese su telefono*", fg="white", bg="#161616", font=("Arial", 14))
        lbltelefono.pack(pady=5)
        entryTelefono = tk.Entry(self.pestaña_registros_empleado, font=("arial", 12))
        entryTelefono.pack(pady=5)

        lblContra = tk.Label(self.pestaña_registros_empleado, text="Agregue contraseña*", fg="white", bg="#161616", font=("Arial", 14))
        lblContra.pack(pady=5)
        entryContra = tk.Entry(self.pestaña_registros_empleado, show="*", font=("Arial", 12))
        entryContra.pack(pady=5)

        lblEmail = tk.Label(self.pestaña_registros_empleado, text="agregue su email*", fg="white", bg="#161616", font=("Arial", 14))
        lblEmail.pack(pady=5)
        entryEmail = tk.Entry(self.pestaña_registros_empleado, font=("Arial",12))
        entryEmail.pack(pady=5)

        def EmpleadoRegistrado():
            cedula = entryCedula.get()
            nombre = entryNombre.get()
            apellido = entryApellido.get()
            telefono = entryTelefono.get()
            email = entryEmail.get()
            contra = entryContra.get()
            self.funciones.registrar_empleado(cedula, nombre, apellido, telefono, email, contra)

        btn_registrarse = tk.Button(self.pestaña_registros_empleado, text="Registrarse", font=("Arial", 12), bg="#333", fg="white", command=EmpleadoRegistrado)
        btn_registrarse.pack(pady=15)
#--------------------------------------------funcion para las diferentes ventanas----------------------------------------------
        self.mostrar_MENU()

    def actualizar_estado_botones(self, activo):
        self.btn_jcs.config(bg="#333")
        self.btn_empleado.config(bg="#333")
        self.btn_inventario.config(bg="#333")
        self.btn_administrador.config(bg="#333")

        if activo == "MENU":
            self.btn_jcs.config(bg="#555")
        elif activo == "EMPLEADO":
            self.btn_empleado.config(bg="#555")
        elif activo == "INVENTARIO":
            self.btn_inventario.config(bg="#555")
        elif activo == "ADMINISTRADOR":
            self.btn_administrador.config(bg="#555")

    def mostrar_MENU(self):
        self.frame_MENU.tkraise()
        self.actualizar_estado_botones("MENU")

    def mostrar_empleado(self):
        self.frame_empleado.tkraise()
        self.actualizar_estado_botones("EMPLEADO")

    def mostrar_inventario(self):
        self.frame_inventario.tkraise()
        self.actualizar_estado_botones("INVENTARIO")
    
    def mostrar_administrador(self):
        self.frame_administrador.tkraise()
        self.actualizar_estado_botones("ADMINISTRADOR")
#---------------------------------------------------inventario----------------------------------------------------------------
    def construir_inventario(self):
        tk.Label(
            self.frame_inventario,
            text="INVENTARIO DE AUTOS",
            fg="white",
            bg="#161616",
            font=("Arial", 22)
        ).pack(pady=10)

        canvas = tk.Canvas(self.frame_inventario, bg="#161616", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.frame_inventario, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        frame_scroll = tk.Frame(canvas, bg="#161616")
        canvas.create_window((0, 0), window=frame_scroll, anchor='nw')

        def actualizar_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_scroll.bind("<Configure>", actualizar_scroll)

        autos = [
            {"nombre": "FERRARI 458 ITALIA", "estado": "Disponible", "precio": "$500/día", "imagen": "prueba-alquiler-de-vehiculos/icons/IMG-20250613-WA0041.jpg"},
            {"nombre": "LAMBORGHINI HURACAN", "estado": "Alquilado", "precio": "$723/día", "imagen": "prueba-alquiler-de-vehiculos/icons/IMG-20250613-WA0039.jpg"},
            {"nombre": "LAMBORGHINI CALLARDO", "estado": "Alquilado", "precio": "$630/día", "imagen": "prueba-alquiler-de-vehiculos/icons/IMG-20250613-WA0042.jpg"},
            {"nombre": "BMW M4", "estado": "Disponible", "precio": "$479/día", "imagen": "prueba-alquiler-de-vehiculos/icons/IMG-20250613-WA0043.jpg"},
            {"nombre": "BMW M8", "estado": "Alquilado", "precio": "$723/día", "imagen": "prueba-alquiler-de-vehiculos/icons/IMG-20250613-WA0044.jpg"},
            {"nombre": "PORSCHE 911GT3", "estado": "Alquilado", "precio": "$630/día", "imagen": "prueba-alquiler-de-vehiculos/icons/IMG-20250613-WA0045.jpg"},
            {"nombre": "PORSCHE 918 SPYDER", "estado": "Disponible", "precio": "$479/día", "imagen": "prueba-alquiler-de-vehiculos/icons/IMG-20250613-WA0046.jpg"},
            {"nombre": "FERRARI F40", "estado": "Alquilado", "precio": "$723/día", "imagen": "prueba-alquiler-de-vehiculos/icons/IMG-20250613-WA0048.jpg"},
            {"nombre": "BUGATTI VEYRON", "estado": "Disponible", "precio": "$630/día", "imagen": "prueba-alquiler-de-vehiculos/icons/IMG-20250613-WA0049.jpg"},
        ]

        columnas = 3
        for i, auto in enumerate(autos):
            frame_auto = tk.Frame(frame_scroll, bg="#2a2a2a", padx=10, pady=10)
            frame_auto.grid(row=i // columnas, column=i % columnas, padx=15, pady=15)

            try:
                img = Image.open(auto["imagen"]).resize((250, 130))
                foto = ImageTk.PhotoImage(img)
            except Exception as e:
                foto = None
                print(f"Error cargando imagen {auto['imagen']}: {e}")

            if foto:
                lbl_img = tk.Label(frame_auto, image=foto, bg="#2a2a2a")
                lbl_img.image = foto
                lbl_img.pack()

            tk.Label(frame_auto, text=auto["nombre"], bg="#2a2a2a", fg="white", font=("Arial", 12, "bold")).pack()
            tk.Label(frame_auto, text=f"Estado: {auto['estado']}", bg="#2a2a2a", fg="white").pack()
            tk.Label(frame_auto, text=f"Precio: {auto['precio']}", bg="#2a2a2a", fg="white").pack()
#-----------------------------------------ventana original----------------------------------------------------------------------
    def __init__(self, ventana):
        self.ventana = ventana 
        self.ventana.title("Alquiler de carros")
        self.ventana.config(width=700, height=500, bg="#161616")
        self.funciones = Funciones(self.ventana)

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

if __name__ == "__main__":
    Interfaz()