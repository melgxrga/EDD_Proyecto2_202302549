from structures.listaAdyacencia import listaAdyacencia
from structures.datos_ruta import Ruta
import os

class RutasController:
    def __init__(self):
        # Inicializar la lista de adyacencia para almacenar las rutas
        self.lista_adyacencia = listaAdyacencia()

    def limpiar_rutas(self):
        """Limpia la lista de rutas."""
        self.lista_adyacencia = listaAdyacencia()
        print("Lista de rutas limpiada.")

    def crear_ruta(self, origen: str, destino: str, tiempo: int):
        """Crea y agrega una nueva ruta a la lista de adyacencia."""
        ruta = Ruta(origen, destino, tiempo)
        self.lista_adyacencia.insertar(ruta)
        print(f"Ruta de {origen} a {destino} con tiempo {tiempo} insertada en la lista de adyacencia.")

    def obtener_rutas(self):
        """Retorna la lista de rutas."""
        rutas = []
        current = self.lista_adyacencia.vertices.head
        while current:
            origen = current.data.valor
            vecinos = []
            vecino_actual = current.data.vecinos.head
            while vecino_actual:
                vecinos.append((vecino_actual.data.valor, vecino_actual.tiempo))
                vecino_actual = vecino_actual.next
            rutas.append((origen, vecinos))
            current = current.next
        return rutas

    def imprimir_rutas(self):
        """Imprime todas las rutas en la consola para depuración."""
        print("Lista de Rutas:")
        rutas = self.obtener_rutas()
        for origen, vecinos in rutas:
            for destino, tiempo in vecinos:
                print(f"{origen} -> {destino} : {tiempo} minutos")
                
    def generar_graphviz(self, filename="rutas.dot"):
        """Genera un archivo DOT para representar el grafo de rutas no dirigido."""
        rutas = self.obtener_rutas()
        with open(filename, 'w') as file:
            file.write("graph G {\n")
            file.write("    node [shape=circle, width=0.1, height=0.1, fontsize=10, label=\"\"];\n")
            for origen, vecinos in rutas:
                file.write(f'    "{origen}" [xlabel="{origen}", labelloc="t"];\n')
                for destino, tiempo in vecinos:
                    file.write(f'    "{destino}" [xlabel="{destino}", labelloc="t"];\n')
                    file.write(f'    "{origen}" -- "{destino}" [label="{tiempo}"];\n')
            file.write("}\n")
        print(f"Archivo DOT generado: {filename}")