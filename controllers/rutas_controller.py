from structures.listaAdyacencia import listaAdyacencia
from structures.datos_ruta import Ruta
import os
import heapq

class RutasController:
    def __init__(self):
        self.grafo = {}
       

    def cargar_rutas(self, file_path):
        """
        Carga las rutas desde un archivo TXT.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lineas = file.readlines()
                for linea in lineas:
                    if linea.strip():
                        origen, destino, distancia = linea.strip().split(' / ')
                        distancia = int(distancia.split(' ')[0])
                        self.agregar_ruta(origen, destino, distancia)
            print(f"Rutas cargadas desde {file_path}.")
        except Exception as e:
            print(f"Error al cargar rutas desde {file_path}: {e}")

    def agregar_ruta(self, origen, destino, distancia):
        if origen not in self.grafo:
            self.grafo[origen] = []
        if destino not in self.grafo:
            self.grafo[destino] = []
        self.grafo[origen].append((destino, distancia))
        self.grafo[destino].append((origen, distancia)) 

    def determinar_mejor_ruta(self, origen, destino):
        """
        Determina la mejor ruta (más corta) entre dos ciudades utilizando el algoritmo de Dijkstra.
        """
        if origen not in self.grafo or destino not in self.grafo:
            return None, float('inf')

        distancias = {ciudad: float('inf') for ciudad in self.grafo}
        distancias[origen] = 0
        prioridad = [(0, origen)]
        camino = {ciudad: None for ciudad in self.grafo}

        while prioridad:
            distancia_actual, ciudad_actual = heapq.heappop(prioridad)

            if ciudad_actual == destino:
                ruta = []
                while ciudad_actual:
                    ruta.append(ciudad_actual)
                    ciudad_actual = camino[ciudad_actual]
                ruta.reverse()
                return ruta, distancias[destino]

            for vecino, peso in self.grafo[ciudad_actual]:
                distancia = distancia_actual + peso
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    camino[vecino] = ciudad_actual
                    heapq.heappush(prioridad, (distancia, vecino))

        return None, float('inf')

    def imprimir_rutas(self):
        for origen in self.grafo:
            for destino, distancia in self.grafo[origen]:
                print(f"{origen} -> {destino}: {distancia} km")

    def limpiar_rutas(self):
        """Limpia la lista de rutas."""
        self.grafo = {}
        print("Lista de rutas limpiada.")

    def crear_ruta(self, origen, destino, distancia):
        self.agregar_ruta(origen, destino, distancia)
        print(f"Ruta creada: {origen} -> {destino} con distancia {distancia} km")

    def eliminar_ruta(self, origen, destino):
        if origen in self.grafo and destino in self.grafo:
            self.grafo[origen] = [ruta for ruta in self.grafo[origen] if ruta[0] != destino]
            self.grafo[destino] = [ruta for ruta in self.grafo[destino] if ruta[0] != origen]
            print(f"Ruta eliminada: {origen} -> {destino}")

    def obtener_rutas(self):
        return [(origen, destinos) for origen, destinos in self.grafo.items()]

    def generar_graphviz(self, filename="rutas.dot"):
        """Genera un archivo DOT para representar el grafo de rutas no dirigido."""
        rutas = self.obtener_rutas()
        aristas = set()  # Para almacenar aristas únicas
        with open(filename, 'w') as file:
            file.write("graph G {\n")
            file.write("    node [shape=circle, width=0.1, height=0.1, fontsize=10, label=\"\"];\n")
            for origen, vecinos in rutas:
                file.write(f'    "{origen}" [xlabel="{origen}", labelloc="t"];\n')
                for destino, tiempo in vecinos:
                    file.write(f'    "{destino}" [xlabel="{destino}", labelloc="t"];\n')
                    # Asegurarse de que cada arista se agregue solo una vez y no se crucen
                    if (origen, destino) not in aristas and (destino, origen) not in aristas:
                        file.write(f'    "{origen}" -- "{destino}" [label="{tiempo}", constraint=false];\n')
                        aristas.add((origen, destino))
            file.write("}\n")
        print(f"Archivo DOT generado: {filename}")
        
    def obtener_distancia(self, origen, destino):
            if origen in self.grafo and destino in self.grafo[origen]:
                return self.grafo[origen][destino]
            return None