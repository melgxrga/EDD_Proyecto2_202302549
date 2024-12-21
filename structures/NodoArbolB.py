from datos_vehiculo import DatosVehiculo  

class NodoArbolB:
    def __init__(self, esHoja: bool):
        self.hoja: bool = esHoja
        self.claves: list[DatosVehiculo] = []
        self.hijos: list['NodoArbolB'] = []  
    
    def __str__(self):
        claves_str = ', '.join([vehiculo.placa for vehiculo in self.claves])
        return f"Hoja: {self.hoja}, Claves: [{claves_str}], Hijos: {len(self.hijos)}"