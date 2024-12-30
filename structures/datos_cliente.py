
class Cliente:
    def __init__(self, dpi, nombres, apellidos, genero, telefono, direccion):
        self.dpi = int(dpi)  # Asegurarse de que el DPI sea un número
        self.nombres = nombres
        self.apellidos = apellidos
        self.genero = genero
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return (
            f"DPI: {self.dpi}, "
            f"Nombres: {self.nombres}, "
            f"Apellidos: {self.apellidos}, "
            f"Género: {self.genero}, "
            f"Teléfono: {self.telefono}, "
            f"Dirección: {self.direccion}"
        )
