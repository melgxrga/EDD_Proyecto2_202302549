from structures.lista_circular_doble import ListaCircularDoble
from structures.datos_cliente import Cliente
import os

class ClientesController:
    def __init__(self, file_path="data/clientes.txt"):
        self.clientes = ListaCircularDoble()
        self.cargar_clientes(file_path)
        print("ClientesController inicializado.")  # Depuración

    def cargar_clientes(self, file_path="data/clientes.txt"):
        """
        Carga clientes desde un archivo TXT.
        """
        if not os.path.exists(file_path):
            print(f"Archivo {file_path} no encontrado. No se pueden cargar clientes.")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lineas = file.readlines()
                for linea in lineas:
                    if linea.strip():  # Ignorar líneas vacías
                        partes = linea.strip().split(',')
                        if len(partes) != 6:
                            print(f"Línea inválida en {file_path}: {linea.strip()}")
                            continue
                        dpi, nombres, apellidos, genero, telefono, direccion = partes
                        self.crear_cliente(
                            dpi.strip(), nombres.strip(), apellidos.strip(),
                            genero.strip(), telefono.strip(), direccion.strip()
                        )
            print(f"Clientes cargados desde {file_path}: {self.clientes.tamaño()}")  # Depuración
        except Exception as e:
            print(f"Ha ocurrido un error al cargar los clientes: {e}")

    def agregar_cliente(self, cliente):
        self.clientes.agregar(cliente)
        print(f"Cliente agregado: DPI: {cliente.dpi}, Nombres: {cliente.nombres}, Apellidos: {cliente.apellidos}")  # Depuración
        self.ordenar_clientes_por_dpi()

    def obtener_clientes(self):
        # Retorna una lista de objetos Cliente ordenados por dpi
        clientes = sorted(list(self.clientes), key=lambda cliente: cliente.dpi)
        # Imprimir el contenido de la lista circular doble
        print("Contenido de la lista circular doble:")
        for cliente in self.clientes:
            print(f"DPI: {cliente.dpi}, Nombres: {cliente.nombres}, Apellidos: {cliente.apellidos}")
        return clientes

    def ordenar_clientes_por_dpi(self):
        clientes_ordenados = self.obtener_clientes()
        self.clientes = ListaCircularDoble()
        for cliente in clientes_ordenados:
            self.clientes.agregar(cliente)
        print("Clientes ordenados por DPI.")  # Depuración

    def imprimir_clientes(self):
        print("Lista de Clientes:")
        for cliente in self.obtener_clientes():
            print(f"{cliente.dpi} - {cliente.nombres} {cliente.apellidos}")

    def generar_graphviz(self):
        return self.clientes.generar_graphviz()
    
    def limpiar_clientes(self):
        self.clientes = ListaCircularDoble()
        print("Lista de clientes limpiada.")  # Depuración

    def crear_cliente(self, dpi, nombres, apellidos, genero, telefono, direccion):
        nuevo_cliente = Cliente(dpi, nombres, apellidos, genero, telefono, direccion)
        self.agregar_cliente(nuevo_cliente)

    def modificar_cliente(self, dpi, nuevos_datos):
        encontrado = False
        for cliente in self.clientes:
            if cliente.dpi == dpi:
                cliente.nombres = nuevos_datos.nombres
                cliente.apellidos = nuevos_datos.apellidos
                cliente.genero = nuevos_datos.genero
                cliente.telefono = nuevos_datos.telefono
                cliente.direccion = nuevos_datos.direccion
                encontrado = True
                print(f"Cliente con DPI {dpi} modificado.")  # Depuración
                break
        if not encontrado:
            print(f"Cliente con DPI {dpi} no encontrado.")  # Depuración
        return encontrado

    def eliminar_cliente(self, dpi):
        nodo_actual = self.clientes.head
        if not nodo_actual:
            print("La lista de clientes está vacía.")  # Depuración
            return False

        while True:
            if nodo_actual.dato.dpi == dpi:
                if nodo_actual == self.clientes.head and nodo_actual.siguiente == self.clientes.head:
                    self.clientes.head = None
                else:
                    nodo_actual.anterior.siguiente = nodo_actual.siguiente
                    nodo_actual.siguiente.anterior = nodo_actual.anterior
                    if nodo_actual == self.clientes.head:
                        self.clientes.head = nodo_actual.siguiente
                print(f"Cliente con DPI {dpi} eliminado.")  # Depuración
                return True
            nodo_actual = nodo_actual.siguiente
            if nodo_actual == self.clientes.head:
                break
        print(f"Cliente con DPI {dpi} no encontrado para eliminar.")  # Depuración
        return False

    def buscar_cliente(self, dpi):
        """
        Busca un cliente por su DPI en la lista circular doble.
        """
        return self.clientes.buscar(dpi)