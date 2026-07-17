"""
Módulo Dashboard - Vista
Muestra la ganancia estimada del día y alertas visuales.
"""

from datetime import date
from typing import Optional, Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from src.app.controllers.dashboard_controlador import DashboardControlador
from src.app.views.dashboard.components.tarjeta_ganancia import TarjetaGanancia


class DashboardVista(QWidget):
    """
    Vista del Dashboard - Pantalla principal de SISVENIN.
    Muestra la ganancia estimada del día como elemento principal.
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        on_navigate_to_products: Optional[Callable] = None,
        parent=None
    ):
        super().__init__(parent)
        
        self.db_path = db_path or "sisvenin.db"
        self.on_navigate_to_products = on_navigate_to_products
        self.controlador = DashboardControlador(vista=self, db_path=self.db_path)
        
        self.setup_ui()
        self.cargar_datos()

    def setup_ui(self):
        """Configura la interfaz del dashboard"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(24)

        # Cabecera: Título + Fecha
        cabecera_layout = QHBoxLayout()
        
        titulo = QLabel("Dashboard")
        titulo_font = QFont("DM Sans", 24)
        titulo_font.setWeight(QFont.Bold)
        titulo.setFont(titulo_font)
        titulo.setStyleSheet("color: #212121;")
        cabecera_layout.addWidget(titulo)
        
        cabecera_layout.addStretch()
        
        fecha_actual = date.today().strftime("%d/%m/%Y")
        fecha_label = QLabel(f"Hoy: {fecha_actual}")
        fecha_font = QFont("DM Sans", 12)
        fecha_label.setFont(fecha_font)
        fecha_label.setStyleSheet("color: #757575;")
        cabecera_layout.addWidget(fecha_label)
        
        main_layout.addLayout(cabecera_layout)

        # Tarjeta de Ganancia (elemento principal)
        self.tarjeta_ganancia = TarjetaGanancia()
        main_layout.addWidget(self.tarjeta_ganancia)

        # Botón para refrescar (opcional)
        btn_refrescar = QPushButton("🔄 Refrescar")
        btn_refrescar.setStyleSheet(
            """
            QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1B5E20;
            }
            """
        )
        btn_refrescar.clicked.connect(self.cargar_datos)
        main_layout.addWidget(btn_refrescar)

        main_layout.addStretch()

        # Fondo del widget
        self.setStyleSheet("background-color: #F5F5F5;")

    def showEvent(self, event):
        """Se llama cuando la vista se muestra - refrescar datos"""
        super().showEvent(event)
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos de ganancia del controlador"""
        try:
            # Obtiene la ganancia del controlador
            self.controlador.actualizar_indicador_ganancia()
        except Exception as e:
            import sys
            print(f"[DashboardVista] Error al cargar datos: {e}", file=sys.stderr)
            self.mostrar_ganancia(0.0, 0)

    def mostrar_ganancia(self, monto: float, numero_ventas: int = 0):
        """
        Muestra la ganancia en la tarjeta.
        Llamado por el controlador.
        
        Args:
            monto: Monto de ganancia en float
            numero_ventas: Número de ventas del día (opcional)
        """
        self.tarjeta_ganancia.mostrar_ganancia(monto, numero_ventas)