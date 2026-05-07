"""
Controlador del módulo Cliente
"""
from .cliente_modelo import Cliente


class ClienteController:
    
    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        return True

    @staticmethod
    def listar_ejemplo():
        """Retorna lista de ejemplo para pruebas"""
        return [
            Cliente(id=1, nombre=f"Cliente 1", descripcion="Descripción 1"),
            Cliente(id=2, nombre=f"Cliente 2", descripcion="Descripción 2"),
            Cliente(id=3, nombre=f"Cliente 3", descripcion="Descripción 3"),
        ]
