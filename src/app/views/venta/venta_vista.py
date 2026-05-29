"""
Módulo Venta - Vista (POS)
"""
from typing import Optional, Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from src.app.controllers.venta_controlador import VentaControlador


class VentaVista(QWidget):
    def __init__(
        self,
        on_navigate_to_report: Optional[Callable] = None,
        on_navigate_to_products: Optional[Callable] = None,
        parent=None
    ):
        super().__init__(parent)
        
        self.on_navigate_to_report = on_navigate_to_report
        self.on_navigate_to_products = on_navigate_to_products
        
        layout = QVBoxLayout(self)
        
        titulo = QLabel(f"🛒 Punto de Venta (POS)")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        layout.addWidget(titulo)
        
        self.btn = QPushButton("🔄 Refrescar")
        self.btn.clicked.connect(self.cargar_datos)
        layout.addWidget(self.btn)
        
        self.label = QLabel("")
        layout.addWidget(self.label)
    
    def cargar_datos(self):
        datos = VentaControlador.listar_ejemplo()
        self.label.setText(f"Ventas del día: {len(datos)}")