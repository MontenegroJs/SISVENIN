"""
Controlador del módulo Venta
"""
from src.app.models.venta_modelo import VentaModelo


class VentaControlador:
    
    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        return True

    @staticmethod
    def listar_ejemplo():
        return [
            VentaModelo(id=1, nombre=f"Venta 1", descripcion="Descripción 1"),
            VentaModelo(id=2, nombre=f"Venta 2", descripcion="Descripción 2"),
        ]
