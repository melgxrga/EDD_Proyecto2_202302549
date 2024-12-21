from lista_enlazada import LinkedList, Vertice, Node
from structures.datos_ruta import Ruta

class listaAdyacencia:
    def __init__(self):
        self.vertices = LinkedList()
    
    def insertar(self, ruta: Ruta):
        origen = self.vertices.buscar(Vertice(ruta.origen))
        destino = self.vertices.buscar(Vertice(ruta.destino))
        
        if origen is None:
            origen = Vertice(ruta.origen)
            self.vertices.insertar_al_final(origen, None)  # No asignar tiempo al vértice
            origen = self.vertices.buscar(origen)
        
        if destino is None:
            destino = Vertice(ruta.destino)
            self.vertices.insertar_al_final(destino, None)  # No asignar tiempo al vértice
            destino = self.vertices.buscar(destino)
        
        origen.data.vecinos.insertar_al_final(destino.data, ruta.tiempo)  # Asignar tiempo al nodo de la lista de vecinos