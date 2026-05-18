# src/app/app.py
"""
Aplicación principal SISVENIN
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from .base_layout import BaseLayout          # ← importación relativa (misma carpeta)
from .views.producto_vista import ProductoVista


class App(BaseLayout):
    """Aplicación principal que extiende BaseLayout"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("SISVENIN - Minimarket Villa Carrion")
        self._registrar_modulos()
    
    def _registrar_modulos(self):
        """Registra todos los módulos de la aplicación"""
        
        # Módulo Producto
        self.vista_productos = ProductoVista()
        self.registrar_modulo("productos", self.vista_productos, habilitar_boton=True)
        
        # Placeholders para módulos futuros
        self.vista_clientes = QLabel("👥 Módulo de Clientes\n\nPróximamente disponible")
        self.vista_clientes.setAlignment(Qt.AlignCenter)
        self.vista_clientes.setStyleSheet("font-size: 18px; color: #555; padding: 50px;")
        self.registrar_modulo("clientes", self.vista_clientes)
        
        self.vista_ventas = QLabel("💰 Módulo de Ventas\n\nPróximamente disponible")
        self.vista_ventas.setAlignment(Qt.AlignCenter)
        self.vista_ventas.setStyleSheet("font-size: 18px; color: #555; padding: 50px;")
        self.registrar_modulo("ventas", self.vista_ventas)
        
        self.vista_reportes = QLabel("📊 Módulo de Reportes\n\nPróximamente disponible")
        self.vista_reportes.setAlignment(Qt.AlignCenter)
        self.vista_reportes.setStyleSheet("font-size: 18px; color: #555; padding: 50px;")
        self.registrar_modulo("reportes", self.vista_reportes)
        
        self.vista_config = QLabel("⚙️ Configuración\n\nPróximamente disponible")
        self.vista_config.setAlignment(Qt.AlignCenter)
        self.vista_config.setStyleSheet("font-size: 18px; color: #555; padding: 50px;")
        self.registrar_modulo("configuracion", self.vista_config)