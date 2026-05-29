"""
Módulo Reporte - Vista
"""
from typing import Optional, Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from src.app.controllers.reporte_controlador import ReporteControlador


class ReporteVista(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        
        titulo = QLabel(f"📄 Reporte del Día")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        layout.addWidget(titulo)
        
        self.btn = QPushButton("🔄 Refrescar")
        self.btn.clicked.connect(self.cargar_datos)
        layout.addWidget(self.btn)
        
        self.label = QLabel("")
        layout.addWidget(self.label)
    
    def cargar_datos(self):
        datos = ReporteControlador.obtener_reporte_ejemplo()
        self.label.setText(f"Total ingresos: S/ {datos.get('total', 0):.2f}")