"""
Módulo Dashboard - Vista
"""
from typing import Optional, Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from src.app.controllers.dashboard_controlador import DashboardControlador


class DashboardVista(QWidget):
    def __init__(
        self,
        on_navigate_to_products: Optional[Callable] = None,
        parent=None
    ):
        super().__init__(parent)
        
        self.on_navigate_to_products = on_navigate_to_products
        
        layout = QVBoxLayout(self)
        
        titulo = QLabel(f"📊 Dashboard")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        layout.addWidget(titulo)
        
        self.btn = QPushButton("🔄 Refrescar")
        self.btn.clicked.connect(self.cargar_datos)
        layout.addWidget(self.btn)
        
        self.label = QLabel("")
        layout.addWidget(self.label)
    
    def cargar_datos(self):
        datos = DashboardControlador.obtener_resumen_ejemplo()
        self.label.setText(f"Ganancia del día: S/ {datos.get('ganancia', 0):.2f}")