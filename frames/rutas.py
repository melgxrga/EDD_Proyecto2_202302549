import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from controllers.rutas_controller import RutasController
import os
from PIL import Image

class RutasFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#2e2e2e')
        self.controller = controller
        
        tk.Label(self, text="Gestión de Rutas", font=("Helvetica", 18), fg="white", bg='#2e2e2e').pack(pady=20)
        
        # Botón para cargar rutas desde un archivo TXT
        cargar_txt_button = tk.Button(
            self, text="Cargar Rutas desde TXT", command=self.cargar_rutas_txt, bg='#4CAF50', fg="white"
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
            acciones_frame, text="Crear Ruta", command=self.crear_ruta_gui, bg='#4CAF50', fg="white"
        )
        crear_button.grid(row=0, column=0, padx=5)

        # Botón para Eliminar
        eliminar_button = tk.Button(
            acciones_frame, text="Eliminar Ruta", command=self.eliminar_ruta_gui, bg='#4CAF50', fg="white"
        )
        eliminar_button.grid(row=0, column=1, padx=5)

        # Botón para Mostrar Información
        mostrar_info_button = tk.Button(
            acciones_frame, text="Mostrar Información", command=self.mostrar_informacion_gui, bg='#4CAF50', fg="white"
        )
        mostrar_info_button.grid(row=0, column=2, padx=5)
        
        # Lista para mostrar rutas
        self.ruta_list = tk.Listbox(
            self, bg='#3e3e3e', fg="white"
        )
        self.ruta_list.pack(pady=10, fill='both', expand=True)

    def cargar_rutas_txt(self):
        # Limpiar la lista de rutas antes de cargar nuevas
        self.controller.limpiar_rutas()
            
        # Abrir un cuadro de diálogo para seleccionar el archivo TXT
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                datos = file.read().strip()
                print(f"Datos leídos del archivo: {datos}")  # Línea de depuración
                lineas = datos.split('%')
                    
                for linea in lineas:
                    if linea.strip():
                        print(f"Línea procesada: {linea}")  # Línea de depuración
                        campos = linea.split('/')
                        if len(campos) == 3:  # Ajustado a 3 campos: origen, destino, tiempo
                            origen, destino, tiempo = campos
                            print(f"Origen: {origen.strip()}, Destino: {destino.strip()}, Tiempo: {tiempo.strip()}")  # Línea de depuración
                            # Crear e insertar la ruta en la lista de adyacencia
                            self.controller.crear_ruta(
                                origen.strip(), 
                                destino.strip(),
                                int(tiempo.strip())
                            )
                        
            self.actualizar_lista_rutas_visual()
            
            messagebox.showinfo("Éxito", "Rutas cargadas e insertadas correctamente en la lista de adyacencia.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error al cargar las rutas: {e}")

    def generar_graphviz(self):
        """Genera el archivo DOT y lo convierte a una imagen usando neato."""
        self.controller.generar_graphviz()
        os.system("neato -Tpng rutas.dot -o rutas.png")
        messagebox.showinfo("Éxito", "Archivo Graphviz generado correctamente.")

    def ver_estructura(self):
        try:
            image_path = "C:/Users/melga/OneDrive/Desktop/EDD_Proyecto2_202302549/rutas.png"
            image = Image.open(image_path)
            image.show()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    def crear_ruta_gui(self):
        self.mostrar_formulario(None, self.controller.crear_ruta)

    def eliminar_ruta_gui(self):
        ruta_seleccionada = self.obtener_ruta_seleccionada()
        if ruta_seleccionada:
            origen, destino, tiempo = ruta_seleccionada
            self.controller.eliminar_ruta(origen, destino)
            self.actualizar_lista_rutas_visual()
            messagebox.showinfo("Éxito", "Ruta eliminada correctamente.")
            
    def mostrar_informacion_gui(self):
        ruta_seleccionada = self.obtener_ruta_seleccionada()
        if ruta_seleccionada:
            origen, destino, tiempo = ruta_seleccionada
            info = f"Origen: {origen}\nDestino: {destino}\nTiempo: {tiempo} minutos"
            messagebox.showinfo("Información de la Ruta", info)

    def mostrar_formulario(self, ruta, accion):
        try:
            form = Toplevel(self)
            form.title("Formulario de Ruta")
            form.geometry("300x200")
            form.config(bg='#2e2e2e')

            campos = ['origen', 'destino', 'tiempo']
            entradas = {}

            for campo in campos:
                label = tk.Label(form, text=campo.capitalize(), fg="white", bg='#2e2e2e')
                label.pack()
                entrada = tk.Entry(form, bg='#3e3e3e', fg="white")
                entrada.pack(ipady=2) 
                entradas[campo] = entrada

            if ruta:
                origen, destino, tiempo = ruta
                entradas['origen'].insert(0, origen)
                entradas['destino'].insert(0, destino)
                entradas['tiempo'].insert(0, tiempo)

            def on_submit():
                try:
                    # Get values from entries
                    origen = entradas['origen'].get().strip()
                    destino = entradas['destino'].get().strip()
                    tiempo_str = entradas['tiempo'].get().strip()

                    # Validate fields
                    if not all([origen, destino, tiempo_str]):
                        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                        return

                    try:
                        tiempo = int(tiempo_str)
                    except ValueError:
                        messagebox.showwarning("Advertencia", "El tiempo debe ser un número válido.")
                        return

                    # Execute action (create or modify)
                    accion(origen, destino, tiempo)
                    
                    # Update UI
                    self.actualizar_lista_rutas_visual()
                    
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

    def actualizar_lista_rutas_visual(self):
        """Actualiza la interfaz visual para mostrar las rutas cargadas."""
        self.ruta_list.delete(0, tk.END)
        rutas = self.controller.obtener_rutas()
        for origen, destinos in rutas:
            for destino, tiempo in destinos:
                ruta_str = f"Origen: {origen}, Destino: {destino}, Tiempo: {tiempo} minutos"
                self.ruta_list.insert(tk.END, ruta_str)

    def obtener_ruta_seleccionada(self):
        try:
            seleccion = self.ruta_list.curselection()
            if seleccion:
                index = seleccion[0]
                ruta_str = self.ruta_list.get(index)
                origen = ruta_str.split(",")[0].split(":")[1].strip()
                destino = ruta_str.split(",")[1].split(":")[1].strip()
                tiempo = ruta_str.split(",")[2].split(":")[1].strip().split()[0]
                return origen, destino, tiempo
            else:
                messagebox.showwarning("Advertencia", "Seleccione una ruta de la lista.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error al seleccionar la ruta: {e}")
            return None