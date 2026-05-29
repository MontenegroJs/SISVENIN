"""
Controlador del módulo Reporte
"""
from src.app.models.reporte_modelo import ReporteModelo


class ReporteControlador:
    
    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        return True

    @staticmethod
    def listar_ejemplo():
        return [
            ReporteModelo(id=1, nombre=f"Reporte 1", descripcion="Descripción 1"),
            ReporteModelo(id=2, nombre=f"Reporte 2", descripcion="Descripción 2"),
        ]
