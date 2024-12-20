import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel

class DatosVehiculo:
    def __init__(self, placa='', marca='', modelo='', anio='', color=''):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.color = color

class VehiculosFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#2e2e2e')
        tk.Label(self, text="Gestión de Vehículos", font=("Helvetica", 18), fg="white", bg='#2e2e2e').pack(pady=20)
        
        # Botón para cargar vehículos desde un archivo TXT
        cargar_txt_button = tk.Button(
            self, text="Cargar Vehículos desde TXT", command=self.cargar_vehiculos_txt, bg='#4CAF50', fg="white"
        )
        cargar_txt_button.pack(pady=5)
                
        # Botón para generar Graphviz
        generar_graphviz_button = tk.Button(
            self, text="Generar Graphviz", command=self.generar_graphviz, bg='#4CAF50', fg="white"
        )
        generar_graphviz_button.pack(pady=5)
        
        # Frame para agrupar los botones de acciones
        acciones_frame = tk.Frame(self, bg='#2e2e2e')
        acciones_frame.pack(pady=10)

        # Botón para Crear
        crear_button = tk.Button(
            acciones_frame, text="Crear Vehículo", command=self.crear_vehiculo_gui, bg='#4CAF50', fg="white"
        )
        crear_button.grid(row=0, column=0, padx=5)

        # Botón para Modificar
        modificar_button = tk.Button(
            acciones_frame, text="Modificar Vehículo", command=self.mostrar_formulario_modificar, bg='#4CAF50', fg="white"
        )
        modificar_button.grid(row=0, column=1, padx=5)

        # Botón para Eliminar
        eliminar_button = tk.Button(
            acciones_frame, text="Eliminar Vehículo", command=self.eliminar_vehiculo_gui, bg='#4CAF50', fg="white"
        )
        eliminar_button.grid(row=0, column=2, padx=5)

        # Botón para Mostrar Información
        mostrar_info_button = tk.Button(
            acciones_frame, text="Mostrar Información", command=self.mostrar_informacion_gui, bg='#4CAF50', fg="white"
        )
        mostrar_info_button.grid(row=0, column=3, padx=5)
        
        # Lista para mostrar vehículos
        self.vehiculo_list = tk.Listbox(
            self, bg='#3e3e3e', fg="white"
        )
        self.vehiculo_list.pack(pady=10, fill='both', expand=True)

    def cargar_vehiculos_txt(self):
        # Funcionalidad para cargar vehículos desde un archivo TXT
        pass

    def generar_graphviz(self):
        # Funcionalidad para generar Graphviz
        pass

    def crear_vehiculo_gui(self):
        # Funcionalidad para crear un nuevo vehículo
        pass

    def mostrar_formulario_modificar(self):
        # Funcionalidad para mostrar el formulario de modificación
        pass

    def eliminar_vehiculo_gui(self):
        # Funcionalidad para eliminar un vehículo
        pass

    def mostrar_informacion_gui(self):
        # Funcionalidad para mostrar la información de un vehículo
        pass

    def mostrar_formulario(self, vehiculo, accion):
        form = Toplevel(self)
        form.title("Formulario de Vehículo")
        form.geometry("300x400")
        form.config(bg='#2e2e2e')

        campos = ['placa', 'marca', 'modelo', 'anio', 'color']
        entradas = {}

        for campo in campos:
            label = tk.Label(form, text=campo.capitalize(), fg="white", bg='#2e2e2e')
            label.pack()
            entrada = tk.Entry(form, bg='#3e3e3e', fg="white")
            entrada.pack(ipady=2)  # Ajustar el padding interno vertical para hacer el cuadro más pequeño
            entradas[campo] = entrada

        if vehiculo:
            entradas['placa'].insert(0, vehiculo.placa)
            entradas['marca'].insert(0, vehiculo.marca)
            entradas['modelo'].insert(0, vehiculo.modelo)
            entradas['anio'].insert(0, vehiculo.anio)
            entradas['color'].insert(0, vehiculo.color)

        def on_submit():
            datos = DatosVehiculo(
                placa=entradas['placa'].get().strip(),
                marca=entradas['marca'].get().strip(),
                modelo=entradas['modelo'].get().strip(),
                anio=entradas['anio'].get().strip(),
                color=entradas['color'].get().strip()
            )
            if not datos.placa or not datos.marca or not datos.modelo or not datos.anio or not datos.color:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return
            accion(datos)
            form.destroy()

        submit_button = tk.Button(form, text="Guardar", command=on_submit, bg='#4CAF50', fg="white")
        submit_button.pack(pady=10)