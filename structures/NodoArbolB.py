class NodoArbolB:
    def __init__(self, esHoja: bool):
        self.hoja: bool = esHoja
        self.claves: list[int] = []
        self.hijos: list['NodoArbolB'] = []  # Usar comillas para referencias futuras
    
    def __str__(self):
        return f"Hola: {self.hoja}, Claves: {self.claves}, Hijos: {self.hijos}"