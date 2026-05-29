"""
Aplicación principal SISVENIN
"""

import os
from src.app.base_layout import BaseLayout
from src.app.views.producto.producto_vista import ProductoVista
from src.app.views.dashboard.dashboard_vista import DashboardVista
from src.app.views.venta.venta_vista import VentaVista
from src.app.views.reporte.reporte_vista import ReporteVista
from src.app.views.velocidad.velocidad_vista import VelocidadVista


class App(BaseLayout):
    """Aplicación principal que extiende BaseLayout con menú lateral"""
    
    def __init__(self):
        super().__init__()
        self._registrar_modulos()
        # Mostrar Dashboard por defecto
        self._mostrar_modulo_por_nombre("dashboard")
    
    def _obtener_ruta_icono(self, nombre_icono: str) -> str:
        """
        Obtiene la ruta absoluta de un icono SVG.
        
        Args:
            nombre_icono: Nombre del archivo (ej: 'menu_dashboard.svg')
        
        Returns:
            str: Ruta absoluta al icono
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(base_dir, "src", "assets", "icons", nombre_icono)
    
    def _registrar_modulos(self):
        """Registra todos los módulos de la aplicación"""
        
        # Módulo Dashboard
        self.vista_dashboard = DashboardVista(
            on_navigate_to_products=self._ir_a_productos
        )
        self.registrar_modulo(
            nombre="dashboard",
            widget=self.vista_dashboard,
            texto_menu="Dashboard",
            icono=self._obtener_ruta_icono("menu_dashboard.svg"),
            icono_es_svg=True,
            titulo_pantalla="Dashboard"
        )
        
        # Módulo POS
        self.vista_pos = VentaVista(
            on_navigate_to_report=self._ir_a_reportes,
            on_navigate_to_products=self._ir_a_productos
        )
        self.registrar_modulo(
            nombre="pos",
            widget=self.vista_pos,
            texto_menu="POS",
            icono=self._obtener_ruta_icono("menu_venta.svg"),
            icono_es_svg=True,
            titulo_pantalla="Punto de Venta"
        )
        
        # Módulo Productos
        self.vista_productos = ProductoVista()
        self.registrar_modulo(
            nombre="productos",
            widget=self.vista_productos,
            texto_menu="Productos",
            icono=self._obtener_ruta_icono("menu_producto.svg"),
            icono_es_svg=True,
            titulo_pantalla="Gestión de Productos"
        )
        
        # Módulo Reporte
        self.vista_reporte = ReporteVista()
        self.registrar_modulo(
            nombre="reporte",
            widget=self.vista_reporte,
            texto_menu="Reporte del día",
            icono=self._obtener_ruta_icono("menu_reporte.svg"),
            icono_es_svg=True,
            titulo_pantalla="Reporte del Día"
        )
        
        # Módulo Prueba velocidad
        self.vista_velocidad = VelocidadVista()
        self.registrar_modulo(
            nombre="velocidad",
            widget=self.vista_velocidad,
            texto_menu="Prueba velocidad",
            icono=self._obtener_ruta_icono("menu_velocidad.svg"),
            icono_es_svg=True,
            titulo_pantalla="Prueba de Velocidad"
        )
    
    # ==================== MÉTODOS DE NAVEGACIÓN ====================
    
    def _ir_a_productos(self, highlight_id=None):
        """Navega al módulo de productos"""
        self._mostrar_modulo_por_nombre("productos")
        if highlight_id and hasattr(self, 'vista_productos'):
            self.vista_productos.resaltar_producto(highlight_id)
    
    def _ir_a_reportes(self):
        """Navega al módulo de reportes"""
        self._mostrar_modulo_por_nombre("reporte")
    
    def _mostrar_modulo_por_nombre(self, nombre):
        """Muestra un módulo específico por su nombre"""
        if nombre in self.modulos:
            info = self.modulos[nombre]
            self._mostrar_modulo(info["indice"], info["titulo_pantalla"])