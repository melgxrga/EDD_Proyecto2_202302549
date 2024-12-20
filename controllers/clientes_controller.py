from structures.lista_circular_doble import ListaCircularDoble

class Cliente:
    def __init__(self, dpi, nombres, apellidos, genero, telefono, direccion):
        self.dpi = int(dpi)  # Asegurarse de que el DPI sea un número
        self.nombres = nombres
        self.apellidos = apellidos
        self.genero = genero
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return (
            f"DPI: {self.dpi}, "
            f"Nombres: {self.nombres}, "
            f"Apellidos: {self.apellidos}, "
            f"Género: {self.genero}, "
            f"Teléfono: {self.telefono}, "
            f"Dirección: {self.direccion}"
        )

class ClientesController:
    def __init__(self):
        self.clientes = ListaCircularDoble()

    def agregar_cliente(self, cliente):
        self.clientes.agregar(cliente)
        self.ordenar_clientes_por_dpi()

    def obtener_clientes(self):
        return sorted(list(self.clientes), key=lambda cliente: cliente.dpi)

    def ordenar_clientes_por_dpi(self):
        clientes_ordenados = self.obtener_clientes()
        self.clientes = ListaCircularDoble()
        for cliente in clientes_ordenados:
            self.clientes.agregar(cliente)

    def imprimir_clientes(self):
        print("Lista de Clientes:")
        for cliente in self.obtener_clientes():
            print(cliente)
            
    def generar_graphviz(self):
        return self.clientes.generar_graphviz()
    
    def limpiar_clientes(self):
        self.clientes = ListaCircularDoble()

    def crear_cliente(self, dpi, nombres, apellidos, genero, telefono, direccion):
        nuevo_cliente = Cliente(dpi, nombres, apellidos, genero, telefono, direccion)
        self.agregar_cliente(nuevo_cliente)

    def modificar_cliente(self, dpi, nuevos_datos):
        encontrado = False
        for cliente in self.clientes:
            if cliente.dpi == int(dpi):
                cliente.nombres = nuevos_datos.nombres
                cliente.apellidos = nuevos_datos.apellidos
                cliente.genero = nuevos_datos.genero
                cliente.telefono = nuevos_datos.telefono
                cliente.direccion = nuevos_datos.direccion
                encontrado = True
                break
        return encontrado

    def eliminar_cliente(self, dpi):
        nodo_actual = self.clientes.head
        if not nodo_actual:
            return False
        while True:
            if nodo_actual.data.dpi == int(dpi):
                self.clientes.eliminar(nodo_actual)
                return True
            nodo_actual = nodo_actual.next
            if nodo_actual == self.clientes.head:
                break
        return False

    def obtener_cliente_por_dpi(self, dpi):
        for cliente in self.clientes:
            if cliente.dpi == int(dpi):
                return cliente
        return None