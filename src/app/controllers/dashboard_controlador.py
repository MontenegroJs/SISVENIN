"""
Controlador del módulo Dashboard
"""
from src.app.models.dashboard_modelo import DashboardModelo


class DashboardControlador:
    
    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        return True

    @staticmethod
    def listar_ejemplo():
        return [
            DashboardModelo(id=1, nombre=f"Dashboard 1", descripcion="Descripción 1"),
            DashboardModelo(id=2, nombre=f"Dashboard 2", descripcion="Descripción 2"),
        ]
