class Nodo:
    def __init__(self, data):
        self.data = data
        self.next = self
        self.prev = self

class ListaCircularDoble:
    def __init__(self):
        self.head = None

    def agregar(self, data):
        new_node = Nodo(data)
        if not self.head:
            self.head = new_node
        else:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    def eliminar(self, nodo):
        if self.head == nodo and nodo.next == self.head:
            self.head = None
        else:
            nodo.prev.next = nodo.next
            nodo.next.prev = nodo.prev
            if self.head == nodo:
                self.head = nodo.next

    def imprimir(self):
        if not self.head:
            return
        current = self.head
        while True:
            print(current.data)
            current = current.next
            if current == self.head:
                break

    def esta_vacia(self):
        return self.head is None

    def generar_graphviz(self):
        if not self.head:
            return ""

        graphviz = "digraph G {\n"
        graphviz += "rankdir=LR;\n"
        graphviz += "node [shape=record];\n"

        # Crear los nodos con DPI y Nombres
        current = self.head
        while True:
            cliente = current.data
            label = f"{{<prev> | DPI: {cliente.dpi}\\nNombre: {cliente.nombres} | <next>}}"
            graphviz += f"\"{id(current)}\" [label=\"{label}\"];\n"
            current = current.next
            if current == self.head:
                break

        # Crear las conexiones entre los nodos
        current = self.head
        first_node_id = id(current)
        while True:
            next_node_id = id(current.next)
            if next_node_id == first_node_id:
                # Conexión curva entre el último y el primer nodo
                graphviz += f"\"{id(current)}\":next -> \"{next_node_id}\":prev [constraint=false];\n"
                graphviz += f"\"{next_node_id}\":prev -> \"{id(current)}\":next [constraint=false];\n"
            else:
                # Conexiones rectas entre los demás nodos
                graphviz += f"\"{id(current)}\":next -> \"{next_node_id}\":prev;\n"
                graphviz += f"\"{next_node_id}\":prev -> \"{id(current)}\":next;\n"
            current = current.next
            if current == self.head:
                break

        graphviz += "}\n"
        return graphviz

    def iterar(self):
        if not self.head:
            return
        current = self.head
        while True:
            yield current.data
            current = current.next
            if current == self.head:
                break

    def __iter__(self):
        return self.iterar()