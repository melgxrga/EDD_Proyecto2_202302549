from structures.datos_vehiculo import DatosVehiculo
from structures.BTree import BTree

class VehiculosController:
    def __init__(self, arbol):
        # Inicializar una lista para almacenar los vehículos
        self.vehiculos = []
        self.arbol = arbol

    def limpiar_vehiculos(self):
        """Limpia la lista de vehículos."""
        self.vehiculos.clear()
        print("Lista de vehículos limpiada.")

    def crear_vehiculo(self, placa: str, marca: str, modelo: str, precio: float):
        """Crea y agrega un nuevo vehículo a la lista y al árbol B."""
        vehiculo = DatosVehiculo(placa, marca, modelo, precio)
        self.vehiculos.append(vehiculo)
        self.arbol.insertar_valor(vehiculo)
        print(f"Vehículo con placa {placa} insertado en el árbol B.")

    def obtener_vehiculos(self):
        """Retorna la lista de vehículos."""
        return self.vehiculos

    def imprimir_vehiculos(self):
        """Imprime todos los vehículos en la consola para depuración."""
        print("Lista de Vehículos:")
        for vehiculo in self.vehiculos:
            print(vehiculo)