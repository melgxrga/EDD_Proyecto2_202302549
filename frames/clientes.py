import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk  # Necesario para manejar imágenes
from controllers.clientes_controller import ClientesController, Cliente
from structures.lista_circular_doble import ListaCircularDoble
from structures.datos_cliente import Cliente

class ClientesFrame(tk.Frame):
    def __init__(self, parent, clientes_controller):
        super().__init__(parent, bg='#2e2e2e')
        self.controller = clientes_controller  # Utilizar la instancia pasada

        tk.Label(self, text="Gestión de Clientes", font=("Helvetica", 18), fg="white", bg='#2e2e2e').pack(pady=20)
        
        # Botón para cargar clientes desde un archivo TXT
        cargar_txt_button = tk.Button(
            self, text="Cargar Clientes desde TXT", command=self.cargar_clientes_txt, bg='#4CAF50', fg="white"
        )
        cargar_txt_button.pack(pady=5)
                
        # Botón para generar Graphviz
        generar_graphviz_button = tk.Button(
            self, text="Generar Graphviz", command=self.generar_graphviz, bg='#4CAF50', fg="white"
        )
        generar_graphviz_button.pack(pady=5)

        # Botón para ver estructura
        ver_estructura_button = tk.Button(
            self, text="Ver Estructura", command=self.ver_estructura, bg='#4CAF50', fg="white"
        )
        ver_estructura_button.pack(pady=5)
        
        # Frame para agrupar los botones de acciones
        acciones_frame = tk.Frame(self, bg='#2e2e2e')
        acciones_frame.pack(pady=10)

        # Botón para Crear
        crear_button = tk.Button(
            acciones_frame, text="Crear Cliente", command=self.crear_cliente_gui, bg='#4CAF50', fg="white"
        )
        crear_button.grid(row=0, column=0, padx=5)

        # Botón para Modificar
        modificar_button = tk.Button(
            acciones_frame, text="Modificar Cliente", command=self.mostrar_formulario_modificar, bg='#4CAF50', fg="white"
        )
        modificar_button.grid(row=0, column=1, padx=5)

        # Botón para Eliminar
        eliminar_button = tk.Button(
            acciones_frame, text="Eliminar Cliente", command=self.eliminar_cliente_gui, bg='#4CAF50', fg="white"
        )
        eliminar_button.grid(row=0, column=2, padx=5)
        

        # Botón para Mostrar Información
        mostrar_info_button = tk.Button(
            acciones_frame, text="Mostrar Información", command=self.mostrar_informacion_gui, bg='#4CAF50', fg="white"
        )
        mostrar_info_button.grid(row=0, column=3, padx=5)
        
        # Lista para mostrar clientes
        self.client_list = tk.Listbox(
            self, bg='#3e3e3e', fg="white"
        )
        self.client_list.pack(pady=10, fill='both', expand=True)

        # Actualizar la lista visual al iniciar
        self.actualizar_lista_visual()

    def cargar_clientes_txt(self):
        # Abrir un cuadro de diálogo para seleccionar el archivo TXT
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de clientes",
            filetypes=[("Text files", "*.txt")]
        )
        if not file_path:
            return
        
        try:
            # Limpiar la lista de clientes antes de cargar nuevos
            self.controller.limpiar_clientes()

            with open(file_path, 'r', encoding='utf-8') as file:
                lineas = file.readlines()
                
                for linea in lineas:
                    if linea.strip():
                        campos = linea.strip().split(',')
                        if len(campos) == 6:
                            dpi, nombres, apellidos, genero, telefono, direccion = campos
                            self.controller.crear_cliente(
                                dpi.strip(), nombres.strip(), apellidos.strip(),
                                genero.strip(), telefono.strip(), direccion.strip()
                            )
                        else:
                            print(f"Línea inválida en el archivo: {linea.strip()}")  # Depuración

            # Actualizar la lista visual
            self.actualizar_lista_visual()
            # Imprimir clientes en consola para depuración
            self.controller.imprimir_clientes()

            messagebox.showinfo("Éxito", "Clientes cargados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")

    def actualizar_lista_visual(self):
        # Limpiar la lista visual
        self.client_list.delete(0, tk.END)
        # Obtener los clientes ordenados
        clientes_ordenados = self.controller.obtener_clientes()
        # Insertar los clientes en la lista visual
        for cliente in clientes_ordenados:
            self.client_list.insert(
                tk.END, f"DPI: {cliente.dpi}, Nombres: {cliente.nombres}, Apellidos: {cliente.apellidos}, Género: {cliente.genero}, Teléfono: {cliente.telefono}, Dirección: {cliente.direccion}"
            )

    def generar_graphviz(self):
        graphviz_code = self.controller.generar_graphviz()
        with open('clientes.dot', 'w', encoding='utf-8') as file:
            file.write(graphviz_code)
        import subprocess
        try:
            subprocess.run(['dot', '-Tpng', 'clientes.dot', '-o', 'clientes.png'], check=True)
            print("Archivo 'clientes.png' generado.")
        except FileNotFoundError:
            print("Error: Graphviz no está instalado o no está en el PATH del sistema.")

    def ver_estructura(self):
        try:
            image_path = "C:/Users/melga/OneDrive/Desktop/EDD_Proyecto2_202302549/clientes.png"
            image = Image.open(image_path)
            image.show()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    def crear_cliente_gui(self):
        form = Toplevel(self)
        form.title("Agregar Cliente")
        form.geometry("300x400")
        form.config(bg='#2e2e2e')

        campos = ['DPI', 'Nombres', 'Apellidos', 'Género', 'Teléfono', 'Dirección']
        entradas = {}

        for campo in campos:
            label = tk.Label(form, text=campo, fg="white", bg='#2e2e2e')
            label.pack(pady=(10, 0))
            entrada = tk.Entry(form, bg='#3e3e3e', fg="white")
            entrada.pack(ipady=2, padx=20, fill='x')
            entradas[campo.lower()] = entrada

        def on_submit():
            try:
                dpi = entradas['dpi'].get().strip()
                nombres = entradas['nombres'].get().strip()
                apellidos = entradas['apellidos'].get().strip()
                genero = entradas['género'].get().strip().upper()
                telefono = entradas['teléfono'].get().strip()
                direccion = entradas['dirección'].get().strip()

                if not all([dpi, nombres, apellidos, genero, telefono, direccion]):
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                    return

                # Validaciones adicionales
                if not dpi.isdigit():
                    messagebox.showwarning("Advertencia", "El DPI debe contener solo números.")
                    return
                if genero not in ['M', 'F']:
                    messagebox.showwarning("Advertencia", "El Género debe ser 'M' (Masculino) o 'F' (Femenino).")
                    return

                self.controller.crear_cliente(dpi, nombres, apellidos, genero, telefono, direccion)
                self.actualizar_lista_visual()
                form.destroy()
                messagebox.showinfo("Éxito", "Cliente agregado correctamente.")

            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar el formulario: {str(e)}")

        submit_button = tk.Button(
            form, 
            text="Guardar",
            command=on_submit,
            bg='#4CAF50',
            fg="white"
        )
        submit_button.pack(pady=10)

        cancel_button = tk.Button(
            form,
            text="Cancelar",
            command=form.destroy,
            bg='#f44336',
            fg="white"
        )
        cancel_button.pack(pady=5)

    def mostrar_formulario_modificar(self):
        seleccionado = self.client_list.curselection()
        if seleccionado:
            indice = seleccionado[0]
            cliente_seleccionado = self.controller.obtener_clientes()[indice]
            self.mostrar_formulario(cliente_seleccionado, self.modificar_cliente_gui)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para modificar.")

    def mostrar_formulario(self, cliente, accion):
        form = Toplevel(self)
        form.title("Formulario de Cliente")
        form.geometry("300x400")
        form.config(bg='#2e2e2e')

        campos = ['dpi', 'nombres', 'apellidos', 'genero', 'telefono', 'direccion']
        entradas = {}

        for campo in campos:
            label = tk.Label(form, text=campo.capitalize(), fg="white", bg='#2e2e2e')
            label.pack(pady=(10, 0))
            entrada = tk.Entry(form, bg='#3e3e3e', fg="white")
            entrada.pack(ipady=2, padx=20, fill='x')
            entradas[campo] = entrada

        if cliente:
            entradas['dpi'].insert(0, cliente.dpi)
            entradas['nombres'].insert(0, cliente.nombres)
            entradas['apellidos'].insert(0, cliente.apellidos)
            entradas['genero'].insert(0, cliente.genero)
            entradas['telefono'].insert(0, cliente.telefono)
            entradas['direccion'].insert(0, cliente.direccion)

        def on_submit():
            datos = {
                'dpi': entradas['dpi'].get().strip(),
                'nombres': entradas['nombres'].get().strip(),
                'apellidos': entradas['apellidos'].get().strip(),
                'genero': entradas['genero'].get().strip().upper(),
                'telefono': entradas['telefono'].get().strip(),
                'direccion': entradas['direccion'].get().strip(),
            }

            if not all(datos.values()):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return

            # Validaciones adicionales
            if not datos['dpi'].isdigit():
                messagebox.showwarning("Advertencia", "El DPI debe contener solo números.")
                return
            if datos['genero'] not in ['M', 'F']:
                messagebox.showwarning("Advertencia", "El Género debe ser 'M' (Masculino) o 'F' (Femenino).")
                return

            datos_cliente = Cliente(
                dpi=datos['dpi'],
                nombres=datos['nombres'],
                apellidos=datos['apellidos'],
                genero=datos['genero'],
                telefono=datos['telefono'],
                direccion=datos['direccion']
            )
            accion(datos_cliente)
            form.destroy()

        submit_button = tk.Button(form, text="Guardar", command=on_submit, bg='#4CAF50', fg="white")
        submit_button.pack(pady=10)

    def modificar_cliente_gui(self, datos):
        actualizado = self.controller.modificar_cliente(datos.dpi, datos)
        if actualizado:
            self.actualizar_lista_visual()
            messagebox.showinfo("Éxito", "Cliente modificado exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo modificar el cliente.")

    def eliminar_cliente_gui(self):
        seleccionado = self.client_list.curselection()
        if seleccionado:
            indice = seleccionado[0]
            cliente_seleccionado = self.controller.obtener_clientes()[indice]
            confirmar = messagebox.askyesno("Confirmar", f"¿Desea eliminar al cliente {cliente_seleccionado.nombres}?")
            if confirmar:
                eliminado = self.controller.eliminar_cliente(cliente_seleccionado.dpi)
                if eliminado:
                    self.actualizar_lista_visual()
                    messagebox.showinfo("Éxito", "Cliente eliminado exitosamente.")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el cliente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")

    def mostrar_informacion_gui(self):
        seleccionado = self.client_list.curselection()
        if seleccionado:
            indice = seleccionado[0]
            cliente = self.controller.obtener_clientes()[indice]
            info = (
                f"DPI: {cliente.dpi}\n"
                f"Nombres: {cliente.nombres}\n"
                f"Apellidos: {cliente.apellidos}\n"
                f"Género: {cliente.genero}\n"
                f"Teléfono: {cliente.telefono}\n"
                f"Dirección: {cliente.direccion}"
            )
            messagebox.showinfo("Información del Cliente", info)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para ver la información.")