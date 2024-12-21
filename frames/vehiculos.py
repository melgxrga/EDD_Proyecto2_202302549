import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from controllers.vehiculos_controller import VehiculosController

class VehiculosFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#2e2e2e')
        self.controller = controller
        
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
        # Limpiar la lista de vehículos antes de cargar nuevos
        self.controller.limpiar_vehiculos()
            
        # Abrir un cuadro de diálogo para seleccionar el archivo TXT
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                datos = file.read().strip()
                lineas = datos.split(';')
                    
                for linea in lineas:
                    if linea.strip():
                        campos = linea.split(',')
                        if len(campos) == 4:  # Ajustado a 4 campos: placa, marca, modelo, precio
                            placa, marca, modelo, precio = campos
                            # Crear e insertar el vehículo en el árbol B
                            self.controller.crear_vehiculo(
                                placa.strip(), 
                                marca.strip(), 
                                modelo.strip(), 
                                float(precio.strip())
                            )
                        
            self.actualizar_lista_vehiculos_visual()
            self.controller.arbol.visualize('btree_final')
            
            messagebox.showinfo("Éxito", "Vehículos cargados e insertados correctamente en el árbol B.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error al cargar los vehículos: {e}")

    def generar_graphviz(self):
        # Generar la visualización del árbol B
        self.controller.arbol.visualize('btree_final')
        messagebox.showinfo("Éxito", "Visualización del árbol B generada correctamente.")

    def crear_vehiculo_gui(self):
        self.mostrar_formulario(None, self.controller.crear_vehiculo)

    def mostrar_formulario_modificar(self):
        vehiculo_seleccionado = self.obtener_vehiculo_seleccionado()
        if vehiculo_seleccionado:
            self.mostrar_formulario(vehiculo_seleccionado, self.controller.modificar_vehiculo)

    def eliminar_vehiculo_gui(self):
        vehiculo_seleccionado = self.obtener_vehiculo_seleccionado()
        if vehiculo_seleccionado:
            self.controller.eliminar_vehiculo(vehiculo_seleccionado['placa'])
            self.actualizar_lista_vehiculos_visual()
            messagebox.showinfo("Éxito", "Vehículo eliminado correctamente.")
            
    def mostrar_informacion_gui(self):
        vehiculo_seleccionado = self.obtener_vehiculo_seleccionado()
        if vehiculo_seleccionado:
            # Changed from dictionary access to object attribute access
            info = f"Placa: {vehiculo_seleccionado.placa}\nMarca: {vehiculo_seleccionado.marca}\nModelo: {vehiculo_seleccionado.modelo}\nPrecio: {vehiculo_seleccionado.precio}"
            messagebox.showinfo("Información del Vehículo", info)

    def mostrar_formulario(self, vehiculo, accion):
        try:
            form = Toplevel(self)
            form.title("Formulario de Vehículo")
            form.geometry("300x400")
            form.config(bg='#2e2e2e')

            campos = ['placa', 'marca', 'modelo', 'precio']
            entradas = {}

            for campo in campos:
                label = tk.Label(form, text=campo.capitalize(), fg="white", bg='#2e2e2e')
                label.pack()
                entrada = tk.Entry(form, bg='#3e3e3e', fg="white")
                entrada.pack(ipady=2) 
                entradas[campo] = entrada

            if vehiculo:
                entradas['placa'].insert(0, vehiculo.placa)
                entradas['marca'].insert(0, vehiculo.marca)
                entradas['modelo'].insert(0, vehiculo.modelo)
                entradas['precio'].insert(0, vehiculo.precio)

            def on_submit():
                try:
                    # Get values from entries
                    placa = entradas['placa'].get().strip()
                    marca = entradas['marca'].get().strip()
                    modelo = entradas['modelo'].get().strip()
                    precio_str = entradas['precio'].get().strip()

                    # Validate fields
                    if not all([placa, marca, modelo, precio_str]):
                        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                        return

                    try:
                        precio = float(precio_str)
                    except ValueError:
                        messagebox.showwarning("Advertencia", "El precio debe ser un número válido.")
                        return

                    # Create DatosVehiculo object
                    datos = DatosVehiculo(placa, marca, modelo, precio)
                    
                    # Execute action (create or modify)
                    accion(datos)
                    
                    # Update UI
                    self.actualizar_lista_vehiculos_visual()
                    
                    # Close form
                    form.destroy()

                except Exception as e:
                    messagebox.showerror("Error", f"Error al procesar el formulario: {str(e)}")

            # Submit button
            submit_button = tk.Button(
                form, 
                text="Guardar",
                command=on_submit,
                bg='#4CAF50',
                fg="white"
            )
            submit_button.pack(pady=10)

            # Cancel button
            cancel_button = tk.Button(
                form,
                text="Cancelar",
                command=form.destroy,
                bg='#f44336',
                fg="white"
            )
            cancel_button.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el formulario: {str(e)}")
    def actualizar_lista_vehiculos_visual(self):
        """Actualiza la interfaz visual para mostrar los vehículos cargados."""
        self.vehiculo_list.delete(0, tk.END)
        vehiculos = self.controller.obtener_vehiculos()
        for vehiculo in vehiculos:
            # Changed from dictionary access to object attribute access
            vehiculo_str = f"Placa: {vehiculo.placa}, Marca: {vehiculo.marca}, Modelo: {vehiculo.modelo}, Precio: {vehiculo.precio}"
            self.vehiculo_list.insert(tk.END, vehiculo_str)


    def obtener_vehiculo_seleccionado(self):
        try:
            seleccion = self.vehiculo_list.curselection()
            if seleccion:
                index = seleccion[0]
                vehiculo_str = self.vehiculo_list.get(index)
                placa = vehiculo_str.split(",")[0].split(":")[1].strip()
                return self.controller.buscar_vehiculo(placa)
            else:
                messagebox.showwarning("Advertencia", "Seleccione un vehículo de la lista.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error al seleccionar el vehículo: {e}")
            return None