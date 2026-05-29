"""
Módulo Velocidad - Vista
"""
from typing import Optional, Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from src.app.controllers.velocidad_controlador import VelocidadControlador


class VelocidadVista(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        
        titulo = QLabel(f"⏱️ Prueba de Velocidad")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        layout.addWidget(titulo)
        
        self.btn = QPushButton("🔄 Iniciar prueba")
        self.btn.clicked.connect(self.iniciar_prueba)
        layout.addWidget(self.btn)
        
        self.label = QLabel("")
        layout.addWidget(self.label)
    
    def iniciar_prueba(self):
        resultado = VelocidadControlador.ejecutar_prueba_ejemplo()
        self.label.setText(f"Tiempo: {resultado.get('tiempo', 0)} segundos")