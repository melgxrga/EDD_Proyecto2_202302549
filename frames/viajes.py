import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from controllers.viajes_controller import ViajesController
from structures.datos_viajes import Viaje  # Asegúrate de tener esta importación si es necesario
from PIL import Image

class ViajesFrame(tk.Frame):
    def __init__(self, parent, controller: ViajesController):
        super().__init__(parent, bg='#2e2e2e')
        self.controller = controller
    
        tk.Label(self, text="Gestión de Viajes", font=("Helvetica", 18), fg="white", bg='#2e2e2e').pack(pady=20)
        
        crear_viaje_button = tk.Button(
            self, text="Crear Viaje", command=self.crear_viaje_gui, bg='#4CAF50', fg="white"
        )
        crear_viaje_button.pack(pady=5)
        
        generar_graphviz_button = tk.Button(
            self, text="Generar Graphviz", command=self.generar_graphviz, bg='#2196F3', fg="white"
        )
        generar_graphviz_button.pack(pady=5)

        # Botón para ver estructura
        ver_estructura_button = tk.Button(
            self, text="Ver Estructura", command=self.ver_estructura, bg='#4CAF50', fg="white"
        )
        ver_estructura_button.pack(pady=5)
        
        self.viaje_list = tk.Listbox(
            self, bg='#3e3e3e', fg="white"
        )
        self.viaje_list.pack(pady=10, fill='both', expand=True)
        
        self.actualizar_lista_viajes_visual()

    def crear_viaje_gui(self):
        vehiculos = self.obtener_vehiculos()
        if not vehiculos:
            messagebox.showwarning("Advertencia", "No hay vehículos disponibles para crear un viaje.")
            return

        form = Toplevel(self)
        form.title("Formulario de Viaje")
        form.geometry("400x400")
        form.config(bg='#2e2e2e')

        campos = ['origen', 'destino', 'fecha_hora_inicio', 'cliente_dpi']
        entradas = {}

        for campo in campos:
            label = tk.Label(form, text=campo.capitalize(), fg="white", bg='#2e2e2e')
            label.pack()
            entrada = tk.Entry(form, bg='#3e3e3e', fg="white")
            entrada.pack(ipady=2)
            entradas[campo] = entrada

        # Combobox para seleccionar vehículo
        tk.Label(form, text="Vehículo", fg="white", bg='#2e2e2e').pack()
        vehiculo_combobox = ttk.Combobox(form, values=vehiculos, state="readonly")
        vehiculo_combobox.pack(ipady=2)

        def on_submit():
            try:
                origen = entradas['origen'].get().strip()
                destino = entradas['destino'].get().strip()
                fecha_hora_inicio = entradas['fecha_hora_inicio'].get().strip()
                cliente_dpi = entradas['cliente_dpi'].get().strip()
                vehiculo = vehiculo_combobox.get().strip()

                if not all([origen, destino, fecha_hora_inicio, cliente_dpi, vehiculo]):
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                    return

                # Verificar si el cliente existe
                cliente = self.controller.clientes_controller.buscar_cliente(cliente_dpi)
                if not cliente:
                    messagebox.showerror("Error", f"No se encontró el cliente con DPI {cliente_dpi}.")
                    return

                # Extraer placa del vehículo
                vehiculo_placa = vehiculo.split(" - ")[0]

                éxito = self.controller.crear_viaje(origen, destino, fecha_hora_inicio, cliente_dpi, vehiculo_placa)
                if éxito:
                    self.actualizar_lista_viajes_visual()
                    form.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo crear el viaje. Verifica los datos ingresados.")

            except Exception as e:
                print(f"Error al procesar el formulario: {str(e)}")
               
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

    def obtener_vehiculos(self):
        try:
            vehiculos = [f"{vehiculo.placa} - {vehiculo.modelo}" for vehiculo in self.controller.vehiculos_controller.obtener_vehiculos()]
            print(f"Obteniendo vehículos: {vehiculos}")  # Mensaje de depuración
            return vehiculos
        except AttributeError:
            messagebox.showerror("Error", "No se pudo acceder a los vehículos.")
            return []

    def actualizar_lista_viajes_visual(self):
        self.viaje_list.delete(0, tk.END)
        for viaje in self.controller.viajes:
            viaje_str = f"Origen: {viaje.origen}, Destino: {viaje.destino}, Fecha y Hora: {viaje.fecha_hora_inicio}"
            self.viaje_list.insert(tk.END, viaje_str)

    def generar_graphviz(self):
        self.controller.guardar_graphviz()
        messagebox.showinfo("Éxito", "Archivo Graphviz generado exitosamente.")

    def ver_estructura(self):
        try:
            image_path = "C:/Users/melga/OneDrive/Desktop/EDD_Proyecto2_202302549/viajes.png"
            image = Image.open(image_path)
            image.show()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")