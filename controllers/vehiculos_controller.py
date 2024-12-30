from structures.datos_vehiculo import DatosVehiculo
from structures.BTree import BTree

class VehiculosController:
    def __init__(self, arbol):
        # Inicializar una lista para almacenar los vehículos
        self.vehiculos = []
        self.arbol = arbol
        print("VehiculosController inicializado.")  # Depuración

    def limpiar_vehiculos(self):
        """Limpia la lista de vehículos."""
        self.vehiculos.clear()
        print("Lista de vehículos limpiada.")

    def crear_vehiculo(self, datos: DatosVehiculo):
        """Crea y agrega un nuevo vehículo a la lista y al árbol B."""
        self.vehiculos.append(datos)
        self.arbol.insertar_valor(datos)
        print(f"Vehículo con placa {datos.placa} insertado en el árbol B.")

    def obtener_vehiculos(self):
        """Retorna la lista de vehículos (objetos DatosVehiculo)."""
        return self.vehiculos

    def obtener_vehiculos_display(self):
        """Retorna una lista de cadenas de texto representando cada vehículo."""
        return [f"{vehiculo.placa} - {vehiculo.modelo}" for vehiculo in self.vehiculos]

    def imprimir_vehiculos(self):
        """Imprime todos los vehículos en la consola para depuración."""
        print("Lista de Vehículos:")
        for vehiculo in self.obtener_vehiculos():
            print(vehiculo)

    def buscar_vehiculo(self, placa: str):
        """Busca y retorna un vehículo por su placa."""
        for vehiculo in self.vehiculos:
            if vehiculo.placa == placa:
                return vehiculo
        print(f"Vehículo con placa {placa} no encontrado.")
        return None

    def modificar_vehiculo(self, datos: DatosVehiculo):
        """Modifica los datos de un vehículo existente."""
        vehiculo = self.buscar_vehiculo(datos.placa)
        if vehiculo:
            vehiculo.marca = datos.marca
            vehiculo.modelo = datos.modelo
            vehiculo.precio = datos.precio
            print(f"Vehículo con placa {datos.placa} modificado.")
            return True
        else:
            print(f"No se pudo modificar, vehículo con placa {datos.placa} no encontrado.")
            return False

    def eliminar_vehiculo(self, placa: str):
        """Elimina un vehículo por su placa."""
        vehiculo = self.buscar_vehiculo(placa)
        if vehiculo:
            self.vehiculos.remove(vehiculo)
            self.arbol.eliminar_valor(vehiculo)
            print(f"Vehículo con placa {placa} eliminado.")
            return True
        else:
            print(f"No se pudo eliminar, vehículo con placa {placa} no encontrado.")
            return False