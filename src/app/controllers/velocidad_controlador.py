"""
Controlador del módulo Velocidad
"""
from src.app.models.velocidad_modelo import VelocidadModelo


class VelocidadControlador:
    
    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        return True

    @staticmethod
    def listar_ejemplo():
        return [
            VelocidadModelo(id=1, nombre=f"Velocidad 1", descripcion="Descripción 1"),
            VelocidadModelo(id=2, nombre=f"Velocidad 2", descripcion="Descripción 2"),
        ]
