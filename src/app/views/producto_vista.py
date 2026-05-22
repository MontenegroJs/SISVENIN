"""
Módulo Producto - Vista
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from src.app.controllers.producto_controlador import ProductoControlador


class ProductoVista(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        titulo = QLabel(f"📦 Gestión de Productos")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        layout.addWidget(titulo)
        
        self.btn = QPushButton("🔄 Refrescar")
        self.btn.clicked.connect(self.cargar_datos)
        layout.addWidget(self.btn)
        
        self.label = QLabel("")
        layout.addWidget(self.label)
    
    def cargar_datos(self):
        datos = ProductoControlador.listar_ejemplo()
        self.label.setText(f"Cargados {len(datos)} productos")
