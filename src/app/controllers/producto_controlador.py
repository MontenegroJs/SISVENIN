"""
Controlador del módulo Producto
"""
from src.app.models.producto_modelo import ProductoModelo


class ProductoControlador:
    
    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        return True

    @staticmethod
    def listar_ejemplo():
        return [
            ProductoModelo(id=1, nombre=f"Producto 1", descripcion="Descripción 1"),
            ProductoModelo(id=2, nombre=f"Producto 2", descripcion="Descripción 2"),
        ]
