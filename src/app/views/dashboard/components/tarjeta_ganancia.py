"""
Componente: Tarjeta de Ganancia Estimada del Día
"""

from datetime import date
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class TarjetaGanancia(QWidget):
    """
    Tarjeta que muestra la ganancia estimada del día.
    Diseño: Fondo blanco, borde redondeado, sombra suave.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.numero_ventas = 0

    def setup_ui(self):
        """Configura la interfaz de la tarjeta"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # Cabecera con ícono y título
        cabecera_layout = QHBoxLayout()
        
        icono_label = QLabel("💰")
        icono_label.setFont(QFont("DM Sans", 16))
        cabecera_layout.addWidget(icono_label)
        
        titulo_label = QLabel("GANANCIA ESTIMADA DEL DÍA")
        titulo_font = QFont("DM Sans", 14)
        titulo_font.setWeight(QFont.Bold)
        titulo_label.setFont(titulo_font)
        titulo_label.setStyleSheet("color: #757575;")
        cabecera_layout.addWidget(titulo_label)
        cabecera_layout.addStretch()
        
        layout.addLayout(cabecera_layout)

        # Monto de ganancia
        self.monto_label = QLabel("S/ 0.00")
        monto_font = QFont("DM Sans", 56)
        monto_font.setWeight(QFont.Bold)
        self.monto_label.setFont(monto_font)
        self.monto_label.setStyleSheet("color: #2E7D32;")
        layout.addWidget(self.monto_label)

        # Subtítulo con información de ventas
        self.subtitulo_label = QLabel("Basado en 0 ventas de hoy")
        subtitulo_font = QFont("DM Sans", 12)
        self.subtitulo_label.setFont(subtitulo_font)
        self.subtitulo_label.setStyleSheet("color: #757575;")
        layout.addWidget(self.subtitulo_label)

        # Estilos de la tarjeta
        self.setStyleSheet(
            """
            TarjetaGanancia {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
            """
        )

    def mostrar_ganancia(self, monto: float, numero_ventas: int = 0):
        """
        Actualiza el monto de ganancia mostrado.
        
        Args:
            monto: Monto de ganancia en float
            numero_ventas: Número de ventas realizadas hoy
        """
        self.numero_ventas = numero_ventas
        
        # Formatea el monto con 2 decimales
        monto_formateado = f"S/ {monto:.2f}"
        self.monto_label.setText(monto_formateado)
        
        # Actualiza subtítulo con pluralización
        if numero_ventas == 0:
            self.subtitulo_label.setText("Aún no hay ventas registradas hoy")
        elif numero_ventas == 1:
            self.subtitulo_label.setText("Basado en 1 venta de hoy")
        else:
            self.subtitulo_label.setText(f"Basado en {numero_ventas} ventas de hoy")
