class DatosVehiculo:
    def __init__(self, placa: str, marca: str, modelo: str, precio: float):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.precio = precio

    def __lt__(self, other):
        return self.placa < other.placa

    def __eq__(self, other):
        return self.placa == other.placa

    def __str__(self):
        return f"{self.placa}, {self.marca}, {self.modelo}, {self.precio}"