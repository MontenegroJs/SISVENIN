"""
Módulo Venta - Vista (POS)
"""
from typing import Optional, Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from src.app.controllers.venta_controlador import VentaControlador
from src.app.controllers.reporte_controlador import ReporteControlador


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
                # Botón para Cerrar Caja (HU-10)
        self.btn_cerrar_caja = QPushButton("🔒 Cerrar Caja")
        self.btn_cerrar_caja.clicked.connect(self.cerrar_caja)
        layout.addWidget(self.btn_cerrar_caja)
        
        self.label = QLabel("")
        layout.addWidget(self.label)
    
    def cargar_datos(self):
        datos = VentaControlador.listar_ejemplo()
        self.label.setText(f"Ventas del día: {len(datos)}")
    def cerrar_caja(self):
        """Cierra la caja y genera el reporte del día (HU-10)"""
        from PySide6.QtWidgets import QMessageBox
        
        respuesta = QMessageBox.question(
            self,
            "Cerrar Caja",
            "¿Estás segura de que quieres cerrar la caja del día?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            try:
                controlador = ReporteControlador()
                reporte_texto = controlador.generar_reporte_dia()
                QMessageBox.information(
                    self,
                    "Reporte del Día",
                    reporte_texto,
                    QMessageBox.Ok
                )
                print("✅ Cierre de caja ejecutado correctamente")
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"No se pudo generar el reporte: {e}"
                )
                print(f"❌ Error al cerrar caja: {e}")