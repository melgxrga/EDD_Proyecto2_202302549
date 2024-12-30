import tkinter as tk
from PIL import Image, ImageTk
import sys
import os

# Agregar las carpetas 'frames', 'controllers' y 'structures' al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'frames'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'controllers'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'structures'))

from clientes import ClientesFrame
from vehiculos import VehiculosFrame
from viajes import ViajesFrame
from rutas import RutasFrame

from BTree import BTree
from controllers.vehiculos_controller import VehiculosController  # Importar VehiculosController directamente
from controllers.rutas_controller import RutasController  # Importar RutasController
from controllers.viajes_controller import ViajesController  # Importar ViajesController
from controllers.clientes_controller import ClientesController  # Importar ClientesController

def show_frame(frame):
    frame.tkraise()

def main():
    # Crear instancia del árbol B de orden 5
    orden_arbol = 5
    arbol = BTree(orden_arbol)

    # Crear instancias de controladores
    clientes_controller = ClientesController()
    vehiculos_controller = VehiculosController(arbol)
    rutas_controller = RutasController()

    # Crear instancia del controlador de viajes y pasarle los controladores necesarios
    viajes_controller = ViajesController(rutas_controller, clientes_controller, vehiculos_controller)

    # Imprimir datos para verificar
    viajes_controller.imprimir_clientes()
    viajes_controller.imprimir_vehiculos()

    root = tk.Tk()
    root.title("Gestión de Transporte")
    window_width = 1500
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")  
    root.resizable(False, False)

    # Cargar y redimensionar la imagen de fondo
    original_image = Image.open("C:/Users/melga/OneDrive/Desktop/EDD_Proyecto2_202302549/assets/fondo.jpg")
    resized_image = original_image.resize((window_width, window_height), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resized_image)
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    root.background_image = background_image  # Mantener referencia a la imagen

    # Crear contenedor para las diferentes páginas
    container = tk.Frame(root)
    container.place(relx=0.5, rely=0.5, anchor='center', width=window_width, height=window_height)

    # Crear frame inicial con la imagen de fondo
    inicio_frame = tk.Frame(container)
    inicio_frame.place(relwidth=1, relheight=1)
    inicio_background_label = tk.Label(inicio_frame, image=background_image)
    inicio_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Crear instancias de cada frame y pasar el controlador correspondiente
    clientes_frame = ClientesFrame(container, clientes_controller)
    vehiculos_frame = VehiculosFrame(container, vehiculos_controller)
    rutas_frame = RutasFrame(container, rutas_controller)
    viajes_frame = ViajesFrame(container, viajes_controller)

    for frame in (inicio_frame, clientes_frame, vehiculos_frame, rutas_frame, viajes_frame):
        frame.place(relwidth=1, relheight=1)

    # Crear la barra de menú
    menu_bar = tk.Menu(root)
    
    # Menú Inicio
    inicio_menu = tk.Menu(menu_bar, tearoff=0)
    inicio_menu.add_command(label="Inicio", command=lambda: show_frame(inicio_frame))
    menu_bar.add_cascade(label="Inicio", menu=inicio_menu)
    
    # Menú Clientes
    clientes_menu = tk.Menu(menu_bar, tearoff=0)
    clientes_menu.add_command(label="Ver Clientes", command=lambda: show_frame(clientes_frame))
    clientes_menu.add_command(label="Agregar Cliente", command=lambda: show_frame(clientes_frame))
    menu_bar.add_cascade(label="Clientes", menu=clientes_menu)
    
    # Menú Vehículos
    vehiculos_menu = tk.Menu(menu_bar, tearoff=0)
    vehiculos_menu.add_command(label="Ver Vehículos", command=lambda: show_frame(vehiculos_frame))
    vehiculos_menu.add_command(label="Agregar Vehículo", command=lambda: show_frame(vehiculos_frame))
    vehiculos_menu.add_command(label="Cargar Vehículos desde TXT", command=vehiculos_frame.cargar_vehiculos_txt)  # Añadir opción para cargar desde TXT
    menu_bar.add_cascade(label="Vehículos", menu=vehiculos_menu)
    
    # Menú Rutas
    rutas_menu = tk.Menu(menu_bar, tearoff=0)
    rutas_menu.add_command(label="Ver Rutas", command=lambda: show_frame(rutas_frame))
    rutas_menu.add_command(label="Agregar Ruta", command=lambda: show_frame(rutas_frame))
    rutas_menu.add_command(label="Cargar Rutas desde TXT", command=rutas_frame.cargar_rutas_txt)  # Añadir opción para cargar desde TXT
    menu_bar.add_cascade(label="Rutas", menu=rutas_menu)
    
    # Menú Viajes
    viajes_menu = tk.Menu(menu_bar, tearoff=0)
    viajes_menu.add_command(label="Ver Viajes", command=lambda: show_frame(viajes_frame))
    viajes_menu.add_command(label="Agregar Viaje", command=lambda: show_frame(viajes_frame))
    menu_bar.add_cascade(label="Viajes", menu=viajes_menu)
    
    root.config(menu=menu_bar)

    # Mostrar la primera pestaña por defecto
    show_frame(inicio_frame)

    root.mainloop()

if __name__ == "__main__":
    main()