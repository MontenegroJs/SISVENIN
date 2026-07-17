"""
Controlador del módulo Dashboard
"""
import sqlite3
from datetime import date
import sys
from src.app.models.dashboard_modelo import (
    calcular_ganancia_estimada_dia,
    obtener_numero_ventas_dia
)


class DashboardControlador:
    """Controlador para el módulo Dashboard - HU-03"""
    
    def __init__(self, vista=None, db_path=None):
        """
        Inicializa el controlador.
        
        Args:
            vista: Objeto de vista (PySide6)
            db_path: Ruta a la base de datos SQLite
        """
        self.vista = vista
        self.db_path = db_path
    
    def obtener_ganancia_estimada_dia(self, fecha: str = None) -> float:
        """
        Obtiene la ganancia estimada para un día específico.
        
        Args:
            fecha: Fecha en formato YYYY-MM-DD. Si es None, usa el día actual.
        
        Returns:
            float: Ganancia estimada
        """
        if fecha is None:
            fecha = date.today().isoformat()
        
        if self.db_path is None:
            print(f"[Dashboard] db_path es None", file=sys.stderr)
            return 0.0
        
        try:
            conn = sqlite3.connect(self.db_path)
            ganancia = calcular_ganancia_estimada_dia(conn, fecha)
            conn.close()
            return ganancia
        except Exception as e:
            print(f"[Dashboard] Error al obtener ganancia: {e}", file=sys.stderr)
            return 0.0
    
    def obtener_numero_ventas_dia(self, fecha: str = None) -> int:
        """
        Obtiene el número de ventas realizadas en un día específico.
        
        Args:
            fecha: Fecha en formato YYYY-MM-DD. Si es None, usa el día actual.
        
        Returns:
            int: Número de ventas del día
        """
        if fecha is None:
            fecha = date.today().isoformat()
        
        if self.db_path is None:
            print(f"[Dashboard] db_path es None", file=sys.stderr)
            return 0
        
        try:
            conn = sqlite3.connect(self.db_path)
            numero_ventas = obtener_numero_ventas_dia(conn, fecha)
            conn.close()
            return numero_ventas
        except Exception as e:
            print(f"[Dashboard] Error al obtener número de ventas: {e}", file=sys.stderr)
            return 0
    
    def actualizar_indicador_ganancia(self, fecha: str = None):
        """
        Obtiene la ganancia y número de ventas, y actualiza el indicador en la vista.
        
        Args:
            fecha: Fecha en formato YYYY-MM-DD. Si es None, usa el día actual.
        """
        if self.vista is None:
            return
        
        ganancia = self.obtener_ganancia_estimada_dia(fecha)
        numero_ventas = self.obtener_numero_ventas_dia(fecha)
        self.vista.mostrar_ganancia(ganancia, numero_ventas)
