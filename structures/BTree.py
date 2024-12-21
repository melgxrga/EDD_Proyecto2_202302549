from NodoArbolB import NodoArbolB
from graphviz import Digraph
import os

class ArbolB:
    def __init__(self, orden: int):
        self.raiz: NodoArbolB = NodoArbolB(True)
        self.orden: int = orden

    def insertar_valor(self, valor: int):
        raiz: NodoArbolB = self.raiz
        self.insertar_valor_no_completo(raiz, valor)
        if len(raiz.claves) > self.orden - 1:
            nodo: NodoArbolB = NodoArbolB(False)
            self.raiz = nodo
            nodo.hijos.insert(0, raiz)
            self.dividir_pagina(nodo, 0)

    def insertar_valor_no_completo(self, raiz: NodoArbolB, valor: int):
        posicion = len(raiz.claves) - 1
        if raiz.hoja:
            raiz.claves.append(None)
            while posicion >= 0 and valor < raiz.claves[posicion]:
                raiz.claves[posicion + 1] = raiz.claves[posicion]
                posicion -= 1
            raiz.claves[posicion + 1] = valor
        else:
            while posicion >= 0 and valor < raiz.claves[posicion]:
                posicion -= 1
            posicion += 1
            self.insertar_valor_no_completo(raiz.hijos[posicion], valor)
            if len(raiz.hijos[posicion].claves) > self.orden - 1:
                self.dividir_pagina(raiz, posicion)

    def dividir_pagina(self, raiz: NodoArbolB, posicion: int):
        posicion_media: int = (self.orden - 1) // 2
        hijo: NodoArbolB = raiz.hijos[posicion]
        nodo: NodoArbolB = NodoArbolB(hijo.hoja)

        raiz.hijos.insert(posicion + 1, nodo)
        raiz.claves.insert(posicion, hijo.claves[posicion_media])
        nodo.claves = hijo.claves[posicion_media + 1:]
        hijo.claves = hijo.claves[:posicion_media]

        if not hijo.hoja:
            nodo.hijos = hijo.hijos[posicion_media + 1:]
            hijo.hijos = hijo.hijos[:posicion_media + 1]

    def imprimir_usuario(self) -> str:
        dot = 'digraph G {\n\tbgcolor="#1A1A1A";\n\t'
        dot += 'fontcolor=white;\n\tnodesep=0.5;\n\tsplines=false;\n\t'
        dot += 'node [shape=record width=1.2 style=filled fillcolor="#313638" '
        dot += 'fontcolor=white color=transparent];\n\t'
        dot += 'edge [fontcolor=white color="#007CC9"];\n\t'
        dot += self.imprimir(self.raiz)
        dot += "\n}"
        return dot

    def imprimir(self, nodo: NodoArbolB, id: list[int] = [0]) -> str:
        raiz = nodo
        arbol = f'n{id[0]}[label="'
        contador = 0

        for item in raiz.claves:
            if contador == len(raiz.claves) - 1:
                arbol += f"<f{contador}>|{item}|<f{contador + 1}>"
                break
            arbol += f"<f{contador}>|{item}|"
            contador += 1

        arbol += '"];\n\t'
        contador = 0
        id_padre = id[0]

        for item in raiz.hijos:
            # Add edge from parent to child
            arbol += f'n{id_padre}:f{contador}->n{id[0] + 1};\n\t'
            id[0] += 1
            arbol += self.imprimir(item, id)
            contador += 1

        return arbol

    def __str__(self):
        return f"{self.raiz}"

    def visualize(self, filename='btree_final'):
        dot = Digraph(comment='B-Tree')
        dot.attr(rankdir='TB')
        
        def add_nodes(node, node_id):
            # Crear etiqueta de nodo
            keys = [f"({k[0]},{k[1]})" for k in node.claves]
            label = " | ".join(keys)
            dot.node(str(node_id), label, shape='record')
            
            # Agregar hijos y aristas
            if not node.hoja:
                for i, child in enumerate(node.hijos):
                    child_id = f"{node_id}_{i}"
                    add_nodes(child, child_id)
                    dot.edge(str(node_id), child_id)
        
        add_nodes(self.raiz, "root")
        dot.render(filename, view=False, format='png')
        print(f"B-tree visualization saved as {filename}.png")

def main() -> None:
    arbolB = ArbolB(5)  # Crear árbol B de orden 5

    while True:
        try:
            valor: int = int(input("Ingrese un valor: "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue

        if valor == -1:
            print(arbolB.imprimir_usuario())
            continue

        if valor == -2:
            arbolB.visualize('btree_final')  # Generar visualización final
            break

        arbolB.insertar_valor(valor)
        # Opcional: Puedes imprimir el árbol después de cada inserción
        # arbolB.print_tree(arbolB.raiz)  # Asegúrate de tener este método

if __name__ == '__main__':
    main()