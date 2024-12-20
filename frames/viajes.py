import tkinter as tk

class ViajesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='lightyellow')
        tk.Label(self, text="Gestión de Viajes", font=("Helvetica", 18)).pack(pady=20)
        
        # Botón para agregar un nuevo viaje
        add_button = tk.Button(self, text="Agregar Viaje", command=self.agregar_viaje)
        add_button.pack(pady=10)
        
        # Lista para mostrar viajes
        self.viaje_list = tk.Listbox(self)
        self.viaje_list.pack(pady=10, fill='both', expand=True)
    
    def agregar_viaje(self):
        # Funcionalidad para agregar un nuevo viaje
        nuevo_viaje = "Viaje Nuevo"
        self.viaje_list.insert(tk.END, nuevo_viaje)