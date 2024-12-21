from lista_enlazada import LinkedList, Vertice, Node

class listaAdyacencia:
    def __init__(self):
        self.vertices = LinkedList()
    
    def insertar(self, origen_valor, destino_valor):
        origen = self.vertices.buscar(Vertice(origen_valor))
        destino = self.vertices.buscar(Vertice(destino_valor))
        
        if origen is None:
            origen = Vertice(origen_valor)
            self.vertices.insertar_al_final(origen)
            origen = self.vertices.buscar(origen)
        
        if destino is None:
            destino = Vertice(destino_valor)
            self.vertices.insertar_al_final(destino)
            destino = self.vertices.buscar(destino)
        
        origen.data.vecinos.insertar_al_final(destino.data)