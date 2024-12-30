import subprocess
from structures.datos_viajes import Viaje
from structures.lista_enlazada import LinkedList
from structures.BTree import BTree

class ViajesController:
    def __init__(self, rutas_controller, clientes_controller, vehiculos_controller):
        self.viajes = LinkedList()
        self.clientes_controller = clientes_controller
        self.vehiculos_controller = vehiculos_controller
        self.rutas_controller = rutas_controller
        print("ViajesController inicializado.")  # Depuración

    def crear_viaje(self, origen, destino, fecha_hora_inicio, cliente_dpi, vehiculo_placa):
        ruta, distancia = self.rutas_controller.determinar_mejor_ruta(origen, destino)
        cliente = self.clientes_controller.buscar_cliente(cliente_dpi)
        vehiculo = self.vehiculos_controller.buscar_vehiculo(vehiculo_placa)
        
        if not cliente:
            print(f"No se encontró el cliente con DPI {cliente_dpi}.")
            return False
        if not vehiculo:
            print(f"No se encontró el vehículo con placa {vehiculo_placa}.")
            return False
        if ruta is None:
            print(f"No se encontró una ruta entre {origen} y {destino}.")
            return False
        
        viaje = Viaje(origen, destino, fecha_hora_inicio, cliente, vehiculo, ruta, distancia)
        self.viajes.insertar_viaje_al_final(viaje)
        print(f"Viaje de {origen} a {destino} creado.")  # Depuración
        return True

    def generar_graphviz(self):
        if not self.viajes.head:
            return ""

        graphviz = "digraph G {\n"
        graphviz += "rankdir=LR;\n"
        graphviz += "node [shape=record];\n"

        current = self.viajes.head
        while current:
            viaje = current.data
            label_origen = f"{{<prev> | Origen: {viaje.origen} | <next>}}"
            label_destino = f"{{<prev> | Destino: {viaje.destino}\\nDistancia: {viaje.distancia} km | <next>}}"
            graphviz += f"\"{id(current)}_origen\" [label=\"{label_origen}\"];\n"
            graphviz += f"\"{id(current)}_destino\" [label=\"{label_destino}\"];\n"
            graphviz += f"\"{id(current)}_origen\":next -> \"{id(current)}_destino\":prev;\n"
            current = current.next

        current = self.viajes.head
        while current and current.next:
            graphviz += f"\"{id(current)}_destino\":next -> \"{id(current.next)}_origen\":prev;\n"
            graphviz += f"\"{id(current.next)}_origen\":prev -> \"{id(current)}_destino\":next;\n"
            current = current.next

        graphviz += "}\n"
        return graphviz

    def guardar_graphviz(self, filename="viajes.dot"):
        graphviz = self.generar_graphviz()
        with open(filename, "w") as file:
            file.write(graphviz)
        print(f"Archivo {filename} generado.")  # Depuración
        png_filename = filename.replace(".dot", ".png")
        subprocess.run(["dot", "-Tpng", filename, "-o", png_filename])
        print(f"Archivo {png_filename} generado.")  # Depuración

        # Abrir el archivo PNG
        subprocess.run(["start", png_filename], shell=True)

    def imprimir_clientes(self):
        for cliente in self.clientes_controller.obtener_clientes():
            print(f"DPI: {cliente.dpi}, Nombres: {cliente.nombres}, Apellidos: {cliente.apellidos}, Género: {cliente.genero}, Teléfono: {cliente.telefono}, Dirección: {cliente.direccion}")

    def imprimir_vehiculos(self):
        for vehiculo in self.vehiculos_controller.obtener_vehiculos():
            print(f"Placa: {vehiculo.placa}, Modelo: {vehiculo.modelo}, Año: {vehiculo.año}, Color: {vehiculo.color}")