"""
Modelo del módulo Producto
"""
class ProductoModelo:
    def __init__(self, id=None, nombre="", descripcion=""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.activo = True

    def __str__(self):
        return f"{self.nombre} (ID: {self.id})"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "activo": self.activo,
        }
