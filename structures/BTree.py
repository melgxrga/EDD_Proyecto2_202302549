from NodoArbolB import NodoArbolB
from graphviz import Digraph
from structures.datos_vehiculo import DatosVehiculo

class BTree:
    def __init__(self, orden: int):
        self.orden = orden
        self.raiz = NodoArbolB(True)
        print(f"BTree creado con orden {self.orden}")  # Depuración

    def insertar_valor(self, vehiculo: DatosVehiculo):
        print(f"Insertando vehículo: Placa={vehiculo.placa}, Modelo={vehiculo.modelo}")  # Depuración
        raiz: NodoArbolB = self.raiz
        self.insertar_valor_no_completo(raiz, vehiculo)
        if len(raiz.claves) > self.orden - 1:
            nodo: NodoArbolB = NodoArbolB(False)
            self.raiz = nodo
            nodo.hijos.insert(0, raiz)
            self.dividir_pagina(nodo, 0)
            print("Dividiendo página en BTree")  # Depuración

    def insertar_valor_no_completo(self, raiz: NodoArbolB, vehiculo: DatosVehiculo):
        posicion = len(raiz.claves) - 1
        if raiz.hoja:
            raiz.claves.append(None)  # Espacio para el nuevo vehículo
            # Mover las claves mayores hacia la derecha
            while posicion >= 0 and vehiculo.placa < raiz.claves[posicion].placa:
                raiz.claves[posicion + 1] = raiz.claves[posicion]
                posicion -= 1
            raiz.claves[posicion + 1] = vehiculo
            print(f"Vehículo insertado en hoja: {vehiculo}")  # Depuración
        else:
            # Encontrar el hijo adecuado para la inserción
            while posicion >= 0 and vehiculo.placa < raiz.claves[posicion].placa:
                posicion -= 1
            posicion += 1
            self.insertar_valor_no_completo(raiz.hijos[posicion], vehiculo)
            # Si el hijo está completo, dividirlo
            if len(raiz.hijos[posicion].claves) > self.orden - 1:
                self.dividir_pagina(raiz, posicion)
                print("Hijo completo, dividiendo página en BTree")  # Depuración

    def dividir_pagina(self, raiz: NodoArbolB, posicion: int):
        """
        Divide una página del árbol B cuando está lleno.
        """
        posicion_media: int = (self.orden - 1) // 2
        hijo: NodoArbolB = raiz.hijos[posicion]
        nodo: NodoArbolB = NodoArbolB(hijo.hoja)

        # Insertar el nuevo hijo en el árbol
        raiz.hijos.insert(posicion + 1, nodo)
        # Mover la clave del medio al nodo padre
        raiz.claves.insert(posicion, hijo.claves[posicion_media])
        # Dividir las claves entre los dos nodos
        nodo.claves = hijo.claves[posicion_media + 1:]
        hijo.claves = hijo.claves[:posicion_media]

        # Si el nodo no es una hoja, dividir también los hijos
        if not hijo.hoja:
            nodo.hijos = hijo.hijos[posicion_media + 1:]
            hijo.hijos = hijo.hijos[:posicion_media + 1]
        print(f"Página dividida en posición media {posicion_media}")  # Depuración

    def visualize(self, filename='btree_final'):
        dot = Digraph(comment='B-Tree')
        dot.attr(rankdir='TB', bgcolor="#1A1A1A", fontcolor="white")
        
        def add_nodes(node, node_id):
            # Crear etiqueta de nodo con las placas de los vehículos
            keys = [k.placa for k in node.claves]
            label = " | ".join(keys)
            dot.node(str(node_id), label, shape='record', style='filled', fillcolor="#313638", fontcolor="white")
            
            # Agregar hijos y aristas
            if not node.hoja:
                for i, child in enumerate(node.hijos):
                    child_id = f"{node_id}_{i}"
                    add_nodes(child, child_id)
                    dot.edge(str(node_id), str(child_id), color="#007CC9", fontcolor="white")
        
        add_nodes(self.raiz, "root")
        dot.render(filename, view=False, format='png')
        print(f"B-tree visualization saved as {filename}.png")
        
    def buscar_valor(self, placa: str):
        print(f"Buscando vehículo con placa: {placa}")  # Depuración
        return self.buscar_valor_en_nodo(self.raiz, placa)

    def buscar_valor_en_nodo(self, nodo: NodoArbolB, placa: str):
        i = 0
        while i < len(nodo.claves) and placa > nodo.claves[i].placa:
            i += 1
        if i < len(nodo.claves) and placa == nodo.claves[i].placa:
            print(f"Vehículo encontrado: {nodo.claves[i]}")  # Depuración
            return nodo.claves[i]
        elif nodo.hoja:
            print(f"Vehículo con placa {placa} no encontrado en hojas.")  # Depuración
            return None
        else:
            print(f"Descendiendo al hijo {i} para buscar placa {placa}")  # Depuración
            return self.buscar_valor_en_nodo(nodo.hijos[i], placa)
        
    def __iter__(self):
        return self.in_order_traversal()

    def in_order_traversal(self):
        # Implementación de una iteración en orden (in-order traversal)
        yield from self._in_order_traversal(self.raiz)

    def _in_order_traversal(self, nodo):
        if nodo is not None:
            for i in range(len(nodo.claves)):
                if not nodo.hoja:
                    yield from self._in_order_traversal(nodo.hijos[i])
                yield nodo.claves[i]
            if not nodo.hoja:
                yield from self._in_order_traversal(nodo.hijos[len(nodo.claves)])