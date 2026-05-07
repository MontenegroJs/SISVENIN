"""
Componente compartido: Botón principal del sistema
"""
from PySide6.QtWidgets import QPushButton

class BotonPrimario(QPushButton):
    def __init__(self, texto):
        super().__init__(texto)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)