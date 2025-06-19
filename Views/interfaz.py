from tkinter import * 
import tkinter as tk
from Controllers.funcionesGenerales import Funciones
from Controllers.clases import Administrador, Cliente, Empleado
from Views.Tooltip import Tooltip
from PIL import Image, ImageTk 
from tkinter import messagebox, Toplevel, filedialog
import os , shutil
from Models.ConexionBD import ConexionDB
from tkinter import ttk

class Interfaz():
    def gestionar_empleados(self):
        ventana = Toplevel(self.ventana)
        ventana.title("Gestión de Empleados")
        ventana.geometry("750x400")
        ventana.configure(bg="#161616")

        tk.Label(ventana, text="EMPLEADOS REGISTRADOS", font=("Arial", 18), fg="white", bg="#161616").pack(pady=10)

        # Contenedor de la tabla
        frame_tabla = tk.Frame(ventana, bg="#161616")
        frame_tabla.pack(fill="both", expand=True, padx=20)

        columnas = ("Cédula", "Nombre", "Apellido", "Teléfono", "Email")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=140)

        tabla.pack()

        # Cargar datos desde la base
        conexion = ConexionDB()
        conexion.crearConexion()
        db = conexion.getConnection()

        try:
            with db.cursor() as cursor:
                cursor.execute("SELECT CEDULA, NOMBRE, APELLIDO, TELEFONO, EMAIL FROM empleados")
                empleados = cursor.fetchall()
                for emp in empleados:
                    tabla.insert("", "end", values=emp)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la lista de empleados.\n{e}")
        finally:
            conexion.cerrarConexion()

        # Botón para eliminar empleado
        def eliminar_empleado():
            seleccion = tabla.selection()
            if not seleccion:
                messagebox.showwarning("Aviso", "Seleccione un empleado para eliminar.")
                return
            
            datos = tabla.item(seleccion)["values"]
            cedula = datos[0]

            confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar al empleado con cédula {cedula}?")
            if not confirmar:
                return

            conexion.crearConexion()
            db = conexion.getConnection()
            try:
                with db.cursor() as cursor:
                    cursor.execute("DELETE FROM empleados WHERE CEDULA = %s", (cedula,))
                db.commit()
                messagebox.showinfo("Éxito", f"Empleado {cedula} eliminado.")
                tabla.delete(seleccion)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el empleado.\n{e}")
            finally:
                conexion.cerrarConexion()

        tk.Button(ventana, text="Eliminar Empleado", command=eliminar_empleado, bg="#c0392b", fg="white").pack(pady=10)

    def abrir_informe(self):
        ventana_informe = Toplevel(self.ventana)
        ventana_informe.title("Informe de Alquileres")
        ventana_informe.geometry("900x500")
        ventana_informe.configure(bg="#161616")

        tk.Label(ventana_informe, text="INFORME DE ALQUILERES", bg="#161616", fg="white", font=("Arial", 18)).pack(pady=10)

        frame_tabla = tk.Frame(ventana_informe, bg="#161616")
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("ID Vehículo", "Cliente", "Teléfono", "Fecha Inicio", "Fecha Fin", "Estado")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=120)

        tabla.pack(fill="both", expand=True)

        # Cargar datos desde la base de datos
        conexion = ConexionDB()
        conexion.crearConexion()
        db = conexion.getConnection()

        try:
            with db.cursor() as cursor:
                cursor.execute("SELECT a.ID_VEHICULO, a.NOMBRE_CLIENTE, a.TELEFONO_CLIENTE, a.FECHA_INICIAL, a.FECHA_FINAL, v.ESTADO FROM alquilados a JOIN vehiculos v ON a.ID_VEHICULO = v.ID")
                resultados = cursor.fetchall()
                for fila in resultados:
                    devuelto = "si" if fila[:6] else "No"
                    tabla.insert("", "end", values=fila[:6] + (devuelto,))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el informe.\n{e}")
        finally:
            conexion.cerrarConexion()

    def devolver_vehiculo(self, id_vehiculo):
        confirmado = messagebox.askyesno("Confirmar", f"¿Está seguro de que desea devolver el vehículo ID {id_vehiculo}?")
        if not confirmado:
            return

        conexion = ConexionDB()
        conexion.crearConexion()
        db = conexion.getConnection()

        try:
            with db.cursor() as cursor:
                # Actualizar el estado del vehículo
                cursor.execute("UPDATE vehiculos SET ESTADO = 'disponible' WHERE ID = %s", (id_vehiculo,))
                cursor.execute("UPDATE alquilados SET DEVUELTOS = TRUE WHERE ID_VEHICULO = %s AND DEVUELTOS = FALSE ORDER BY FECHA_INICIAL DESC LIMIT 1",(id_vehiculo,))
            db.commit()
            messagebox.showinfo("Éxito", f"Vehículo {id_vehiculo} devuelto correctamente.")
            self.construir_inventario()  # Recargar inventario
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo devolver el vehículo.\n{e}")
        finally:
            conexion.cerrarConexion()

    def formulario_alquiler(self, id_vehiculo):
        def mostrar():
            conexion = ConexionDB()
            conexion.crearConexion()
            db = conexion.getConnection()

            with db.cursor() as cursor:
                cursor.execute("SELECT ESTADO FROM vehiculos WHERE ID = %s", (id_vehiculo,))
                resultado = cursor.fetchone()

            conexion.cerrarConexion()

            if not resultado or resultado[0].lower() != "disponible":
                messagebox.showerror("Error", "Este vehículo ya no está disponible")
                return

            self.ventana_alquilar = Toplevel(self.ventana)
            self.ventana_alquilar.title("Registrar Alquiler")
            self.ventana_alquilar.geometry("400x400")
            self.ventana_alquilar.configure(bg="#161616")

            campos = {
                "Cédula": tk.StringVar(),
                "Nombre": tk.StringVar(),
                "Telefono": tk.StringVar(),
                "Email": tk.StringVar(),
                "Licencia de conducir": tk.StringVar(),
                "fecha Inicio (año/mes/dia)": tk.StringVar(),
                "fecha Fin (año/mes/dia)": tk.StringVar()
            }

            row = 0
            for label_text, var in campos.items():
                tk.Label(self.ventana_alquilar, text=label_text, bg="#161616", fg="white").grid(row=row, column=0, pady=10, padx=10, sticky="w")
                tk.Entry(self.ventana_alquilar, textvariable=var).grid(row=row, column=1, padx=10)
                row += 1

            def registrar():
                datos = {clave: var.get().strip() for clave, var in campos.items()}
                if "" in datos.values():
                    messagebox.showwarning("Campos vacíos", "Por favor complete la información")
                    return

                conexion = ConexionDB()
                conexion.crearConexion()
                db = conexion.getConnection()

                try:
                    with db.cursor() as cursor:
                        # Verificar si el cliente ya está registrado
                        cursor.execute("SELECT * FROM cliente WHERE Cedula = %s", (datos["Cédula"],))
                        existe = cursor.fetchone()
                        # Insertar cliente si no existe
                        if not existe:
                            cursor.execute("INSERT INTO cliente (Cedula, Nombre, Apellido, Telefono, Email, LicenciaDeConducir)VALUES (%s, %s, %s, %s, %s, %s)", (datos["Cédula"], datos["Nombre"], "", datos["Telefono"], datos["Email"], datos["Licencia de conducir"]))
                        # Registrar el alquiler
                        cursor.execute("INSERT INTO alquilados (ID_VEHICULO, NOMBRE_CLIENTE, TELEFONO_CLIENTE,FECHA_INICIAL, FECHA_FINAL, EMAIL, LICENCIADECONDUCIR, DEVUELTOS)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (id_vehiculo, datos["Nombre"], datos["Telefono"],datos["fecha Inicio (año/mes/dia)"], datos["fecha Fin (año/mes/dia)"],datos["Email"], datos["Licencia de conducir"], False))
                        # Actualizar estado del vehículo
                        cursor.execute("UPDATE vehiculos SET ESTADO = 'alquilado' WHERE ID = %s", (id_vehiculo,))
                    db.commit()
                    messagebox.showinfo("Éxito", "Alquiler registrado correctamente.")
                    self.ventana_alquilar.destroy()
                    self.construir_inventario()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo registrar el alquiler.\n{e}")
                finally:
                    conexion.cerrarConexion()
            tk.Button(self.ventana_alquilar, text="Registrar Alquiler", command=registrar, bg="blue", fg="white").grid(row=row, column=0, columnspan=2, pady=20)
        return mostrar

    def resgistrar_vehiculos(self):
        self.ventana_vehiculo = tk.Toplevel(self.frame_administrador)
        self.ventana_vehiculo.title("registrar empleado")
        self.ventana_vehiculo.geometry("900x800")
        self.ventana_vehiculo.config(bg="#161616")
        entrada_frame = tk.Frame(self.ventana_vehiculo, bg="#161616")
        entrada_frame.pack(pady=10)

        tk.Label(self.ventana_vehiculo, text="Agregar Vehiculo", fg="white", bg="#161616", font=("Arial", 18)).place(relx=0.40,rely=0.25)

        lblId = tk.Label(self.ventana_vehiculo, text="Ingrese el Id*", fg="white", bg="#161616", font=("Arial", 12))
        lblId.place(relx=0.16, rely=0.40)
        entryId = tk.Entry(self.ventana_vehiculo, font=("Arial", 12))
        entryId.place(relx=0.28,rely=0.40)

        lblMarca = tk.Label(self.ventana_vehiculo, text="Ingrese la Marca*", fg="white", bg="#161616", font=("arial", 12))
        lblMarca.place(relx=0.13, rely=0.50)
        entryMarca = tk.Entry(self.ventana_vehiculo, font=("arial", 12))
        entryMarca.place(relx=0.28, rely=0.50)

        lblModelo = tk.Label(self.ventana_vehiculo, text="Ingrese el Modelo*", fg="white", bg="#161616", font=("Arial", 12))
        lblModelo.place(relx=0.12, rely=0.60)
        entryModelo = tk.Entry(self.ventana_vehiculo, font=("arial", 12))
        entryModelo.place(relx=0.28, rely=0.60)

        lblAño = tk.Label(self.ventana_vehiculo, text="Ingrese el año*", fg="white", bg="#161616", font=("Arial", 12))
        lblAño.place(relx=0.15, rely=0.70)
        entryAño = tk.Entry(self.ventana_vehiculo, font=("arial", 12))
        entryAño.place(relx=0.28, rely=0.70)

        lblTipo = tk.Label(self.ventana_vehiculo, text="Agregue el tipo*", fg="white", bg="#161616", font=("Arial", 12))
        lblTipo.place(relx=0.55, rely=0.40)
        entryTipo = tk.Entry(self.ventana_vehiculo, font=("Arial", 12))
        entryTipo.place(relx=0.70, rely=0.40)
        
        lblPrecioDia = tk.Label(self.ventana_vehiculo, text="valor diario*", fg="white", bg="#161616", font=("Arial", 12))
        lblPrecioDia.place(relx=0.58, rely=0.50)
        entryPrecioDia = tk.Entry(self.ventana_vehiculo, font=("Arial",12))
        entryPrecioDia.place(relx=0.70, rely=0.50)

        lblEstado = tk.Label(self.ventana_vehiculo, text="Estado Inicial*", fg="white", bg="#161616", font=("Arial", 12))
        lblEstado.place(relx=0.56, rely=0.60)
        entryEstado = tk.Entry(self.ventana_vehiculo, font=("Arial",12))
        entryEstado.place(relx=0.70, rely=0.60)

        self.ruta_imagen = tk.StringVar()

        def  Imagen():
            archivo = filedialog.askopenfilename(title="seleccione imagen del vehiculo", filetypes=[("imágenes", "*.jpg *.png *.jpeg *.gif")])
            if archivo:
                nombre = os.path.basename(archivo)
                destino = os.path.join("prueba_alquiler_de_vehiculos", "icons", "autos", nombre)
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                if not os.path.exists(destino):
                    shutil.copy(archivo, destino)
                self.ruta_imagen.set(destino)
        self.btnSelecionImagen = tk.Button(self.ventana_vehiculo, text="seleccionar Imagen", command=Imagen, bg="#444", fg="white")
        self.btnSelecionImagen.place()
        self.ubicacion = tk.Entry(self.ventana_vehiculo, textvariable=self.ruta_imagen, font=("Arial", 10), state="readonly")
        self.ubicacion.place()
        def VehiculoRegistrado():
            Id = entryId.get()
            Marca = entryMarca.get()
            Modelo = entryModelo.get()
            Año = entryAño.get()
            Tipo = entryTipo.get()
            PrecioDia = entryPrecioDia.get()
            Estado = entryEstado.get()
            Imagen = self.ruta_imagen.get()

            if "" in [Id, Marca,Modelo, Año, Tipo, PrecioDia, Estado, Imagen]:
                messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
                return            
            exito = self.administrador.agregar_vehiculos(Id, Marca, Modelo, Año, Tipo, PrecioDia, Estado, Imagen)
            if exito:
                messagebox.showinfo("Éxito", "Vehículo agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo agregar el vehículo.")
                return self.resgistrar_vehiculos
            
        self.btn_imagen = tk.Button(self.ventana_vehiculo, text="foto", command=Imagen, bg="#444", fg="white")
        self.btn_imagen.place(relx=0.10, rely=0.50)

        self.btn_vehiculoRegistrado = tk.Button(self.ventana_vehiculo, text="guardar", command=VehiculoRegistrado, bg="#444", fg="white")
        self.btn_vehiculoRegistrado.place(relx=0.5, rely=0.50)

    def abrir_pestanas(self):
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
                self.ventana_admin = tk.Toplevel(self.nueva_ventana)
                self.ventana_admin.title("MENU ADMINISTRADOR")
                self.ventana_admin.geometry("700x600")
                self.ventana_admin.configure(bg="#161616")
                self.logo_admin = tk.Label(self.ventana_admin,image=self.logo, bd=0)
                self.logo_admin.place(x=220, y=70, width=330, height=220)
                self.btnRegistro = tk.Button(self.ventana_admin, text="agregar vehiculo", font=("Arial", 13), bg="#333", fg="white",command=self.resgistrar_vehiculos)
                self.btnRegistro.place(rely=0.70, relx=0.38)
                self.lblEliminarVehiculo = tk.Label(self.ventana_admin, text="Id del vehiculo a eliminar:",fg="white", bg="#161616", font=("Arial", 12))
                self.lblEliminarVehiculo.place(rely=0.50, relx=0.40)
                self.entryEliminar = tk.Entry(self.ventana_admin, font=("Arial",12))
                self.entryEliminar.place(rely=0.60, relx=0.40)
                self.btn_eliminar = tk.Button(self.ventana_admin, text="Eliminar", font=("Arial", 13), bg="#444", fg="white",  command=eliminar_vehiculo)
                self.btn_eliminar.place(rely=0.70, relx=0.25)
                self.btn_registro_clientes = tk.Button(self.ventana_admin, text="informe", font=("Arial", 13), bg="#444", fg="white", command=self.abrir_informe)
                self.btn_registro_clientes.place(rely=0.70, relx=0.60)
                self.btn_registro_empleados = tk.Button(self.ventana_admin, text="Gestionar empleados",font=("Arial", 13),bg="#444", fg="white", command=self.gestionar_empleados )
                self.btn_registro_empleados.place(rely=0.80, relx=0.40)

            else:
                messagebox.showerror("Error", "Cédula o contraseña incorrecta.")
        self.iniciar_sesion_empleado = tk.Button(self.frame_administrador, text="Iniciar Sesión", font=("Arial", 13), bg="#333", fg="white", command=login_admin)
        self.iniciar_sesion_empleado.place(rely=0.70, relx=0.42)

        def eliminar_vehiculo():
            id = self.entryEliminar.get()
            if id.strip() == "":
                messagebox.showwarning("Campo vacío","Por favor ingresar un Id valido")
                return
            confirmado = messagebox.askyesno("confirmar", f"¿seguro que desea eliminar este vehiculo con ID: {id}?")
            if confirmado:
                exito = self.administrador.eliminar_vehiculos(id)
                if exito:
                    messagebox.showinfo("Éxito", "Vehículo eliminado correctamente")
                    self.construir_inventario()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el vehículo.")


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
                self.ventana_empleado = tk.Toplevel(self.nueva_ventana)
                self.ventana_empleado.title("MENU ADMINISTRADOR")
                self.ventana_empleado.geometry("700x600")
                self.ventana_empleado.configure(bg="#161616")
                self.logo_empleado = tk.Label(self.ventana_empleado,image=self.logo, bd=0)
                self.logo_empleado.place(x=280, y=70, width=330, height=220)
                self.btnRegistro = tk.Button(self.ventana_empleado, text="Generar Registro", font=("Arial", 13), bg="#333", fg="white", command=self.abrir_informe)
                self.btnRegistro.place(rely=0.70, relx=0.42)
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
        for widget in self.frame_inventario.winfo_children():
            widget.destroy()
        # Crear canvas con scroll vertical
        canvas = tk.Canvas(self.frame_inventario, bg="#161616", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame_inventario, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        scrollable_frame = tk.Frame(canvas, bg="#161616")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
    
        conexion = ConexionDB()
        conexion.crearConexion()
        db = conexion.getConnection()

        with db.cursor() as cursor:
            cursor.execute("SELECT ID, MARCA, MODELO, PRECIO_DIARIO, ESTADO, IMAGEN FROM vehiculos")
            autos = cursor.fetchall()
        
        conexion.cerrarConexion()

        fila = 0
        columna = 0

        for auto in autos:
            Id, Marca, Modelo, PrecioDiario, Estado, ruta_imagen = auto
            frame_auto = tk.Frame(scrollable_frame, bg="#2a2a2a", padx=10, pady=10)
            frame_auto.grid(row=fila, column=columna, padx=20, pady=20)

            try:
                img = Image.open(ruta_imagen).resize((250, 130))
                foto = ImageTk.PhotoImage(img)
                lbl_img = tk.Label(frame_auto, image=foto, bg="#2a2a2a")
                lbl_img.image = foto
                lbl_img.pack()
            except Exception as e:
                print(f"Error cargando imagen: {e}")

            tk.Label(frame_auto, text=f"{Marca} {Modelo}", bg="#2a2a2a", fg="white").pack()
            tk.Label(frame_auto, text=f"Estado: {Estado}", bg="#2a2a2a", fg="white").pack()
            tk.Label(frame_auto, text=f"Precio: {PrecioDiario}", bg="#2a2a2a", fg="white").pack()
            
            def alquiler_vehiculo(id_vehiculo = Id):
                self.formulario_alquiler(Id)()
            
            if Estado.lower() == "disponible":
                            self.btnAlquilar = tk.Button(frame_auto, text="alquilar", bg="#444", fg="white", command=alquiler_vehiculo).pack(pady=5)
            elif Estado.lower() =="alquilado":
                def devolver_vehiculo(id_vehiculo = Id):
                    self.devolver_vehiculo(id_vehiculo)
                tk.Button(frame_auto,text="devolver", bg="#444", fg="white", command=devolver_vehiculo).pack(pady=5)
            columna += 1
            if columna >= 3:
                columna = 0
                fila += 1

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
        self.administrador = Administrador("Cedula","Nombre","Apellido","Telefono","Email","Usuario","Contraseña")

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