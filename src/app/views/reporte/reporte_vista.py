"""
Módulo Reporte - Vista
Implementación de la vista del reporte del día con tarjetas, tabla y preview.
"""
from typing import Optional
import os
import tempfile
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QMessageBox,
    QFileDialog,
    QFrame,
    QTextBrowser,
    QSizePolicy,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt, QTimer

from src.app.controllers.reporte_controlador import ReporteControlador
from src.app.shared.components.sis_button import SisButton
from src.app.views.reporte.components.resumen_dia import ResumenDia
from src.app.views.reporte.components.tabla_productos_vendidos import TablaProductosVendidos


class ReporteVista(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ReporteVista")
        self.controlador = ReporteControlador()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet(
            "QLabel#SectionTitle { font-size: 18px; font-weight: 700; color: #1A237E; }"
            "QLabel#SectionSubtitle { font-size: 14px; color: #757575; }"
            "QScrollBar:vertical { width: 10px; }"
            "QFrame#SectionCard { background: white; border: 1px solid #E0E0E0; border-radius: 18px; }"
        )

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)

        self._setup_resumen(content_layout)
        self._setup_detalle(content_layout)
        self._setup_acciones(content_layout)
        self._setup_preview(content_layout)

        self.scroll_area.setWidget(content_widget)
        main_layout.addWidget(self.scroll_area)

        self.cargar_datos()


    def _setup_resumen(self, parent_layout):
        contenedor = QFrame()
        contenedor.setObjectName("SectionCard")
        contenedor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        contenedor.setStyleSheet(
            "QFrame#SectionCard { background: white; border: 1px solid #E0E0E0; border-radius: 18px; }"
        )
        contenedor_layout = QVBoxLayout(contenedor)
        contenedor_layout.setContentsMargins(24, 24, 24, 24)
        contenedor_layout.setSpacing(18)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        section_title = QLabel("📊 RESUMEN DEL DÍA")
        section_title.setObjectName("SectionTitle")
        section_title.setStyleSheet("font-size: 18px; font-weight: 700; color: #1A237E;")

        section_description = QLabel("Datos clave del reporte diario.")
        section_description.setObjectName("SectionSubtitle")
        section_description.setStyleSheet("font-size: 14px; color: #5C6BC0;")

        header_layout.addWidget(section_title)
        header_layout.addStretch()
        contenedor_layout.addLayout(header_layout)
        contenedor_layout.addWidget(section_description)
        self.resumen_widget = ResumenDia()
        contenedor_layout.addWidget(self.resumen_widget)

        parent_layout.addWidget(contenedor)

    def _setup_detalle(self, parent_layout):
        contenedor = QFrame()
        contenedor.setObjectName("SectionCard")
        contenedor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contenedor.setStyleSheet(
            "QFrame#SectionCard { background: white; border: 1px solid #E0E0E0; border-radius: 18px; }"
        )
        contenedor_layout = QVBoxLayout(contenedor)
        contenedor_layout.setContentsMargins(24, 24, 24, 24)
        contenedor_layout.setSpacing(20)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        seccion_title = QLabel("🛒 PRODUCTOS VENDIDOS HOY")
        seccion_title.setObjectName("SectionTitle")
        seccion_title.setStyleSheet("font-size: 18px; font-weight: 700; color: #212121;")

        header_layout.addWidget(seccion_title)
        header_layout.addStretch()

        seccion_subtitle = QLabel("Lista de productos vendidos con cantidad, precio unitario y subtotal.")
        seccion_subtitle.setObjectName("SectionSubtitle")
        seccion_subtitle.setStyleSheet("font-size: 14px; color: #5C6BC0;")

        contenedor_layout.addLayout(header_layout)
        contenedor_layout.addWidget(seccion_subtitle)
        self.tabla_productos = TablaProductosVendidos()
        contenedor_layout.addWidget(self.tabla_productos)

        self.label_totales = QLabel("")
        self.label_totales.setStyleSheet("font-size: 14px; color: #455A64; margin-top: 14px;")
        self.label_totales.setAlignment(Qt.AlignLeft)
        self.label_totales.setWordWrap(True)
        contenedor_layout.addWidget(self.label_totales)

        parent_layout.addWidget(contenedor)

    def _setup_acciones(self, parent_layout):
        contenedor = QFrame()
        contenedor.setObjectName("SectionCard")
        contenedor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contenedor.setStyleSheet(
            "QFrame#SectionCard { background: white; border: 1px solid #E0E0E0; border-radius: 16px; }"
        )
        contenedor_layout = QVBoxLayout(contenedor)
        contenedor_layout.setContentsMargins(24, 24, 24, 24)
        contenedor_layout.setSpacing(16)

        # Sección de acciones: botones solamente (sin título ni subtítulo)

        # Sección de acciones: mostrar únicamente los dos botones (sin tabla)
        self.btn_imprimir = SisButton("🖨️ IMPRIMIR REPORTE", variant="primary")
        self.btn_imprimir.clicked.connect(self.imprimir_reporte)
        self.btn_export_pdf = SisButton("💾 GUARDAR PDF", variant="secondary")
        self.btn_export_pdf.clicked.connect(self.exportar_pdf)
        self.btn_imprimir.setMinimumWidth(220)
        self.btn_export_pdf.setMinimumWidth(220)

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(16)
        botones_layout.addStretch()
        botones_layout.addWidget(self.btn_export_pdf)
        botones_layout.addWidget(self.btn_imprimir)

        contenedor_layout.addLayout(botones_layout)
        parent_layout.addWidget(contenedor)

    def _setup_preview(self, parent_layout):
        preview_box = QFrame()
        preview_box.setStyleSheet(
            "QFrame { background: white; border: 1px solid #E0E0E0; border-radius: 16px; }"
        )
        preview_layout = QVBoxLayout(preview_box)
        preview_layout.setContentsMargins(18, 18, 18, 18)
        preview_layout.setSpacing(10)

        preview_title = QLabel("Vista previa de reporte")
        preview_title.setObjectName("SectionTitle")
        preview_title.setStyleSheet("font-size: 18px; margin-bottom: 0px; color: #212121;")

        preview_info = QLabel("Revisa el contenido antes de generar el archivo PDF.")
        preview_info.setObjectName("SectionSubtitle")
        preview_info.setStyleSheet("font-size: 14px; color: #757575;")

        preview_layout.addWidget(preview_title)
        preview_layout.addWidget(preview_info)

        try:
            from PySide6.QtWebEngineWidgets import QWebEngineView
            self.preview = QWebEngineView()
            self._use_webengine = True
        except Exception:
            self.preview = QTextBrowser()
            self._use_webengine = False

        self.preview.setStyleSheet("border: 1px solid #E0E0E0; border-radius: 12px; background: #F5F5F5;")
        preview_layout.addWidget(self.preview)

        parent_layout.addWidget(preview_box)

    def cargar_datos(self, fecha: Optional[str] = None):

        datos = self.controlador.obtener_datos_para_reporte_dia(fecha)

        if datos.get("error"):
            QMessageBox.warning(self, "Error", datos.get("mensaje_error", "Error al cargar reporte"))
            return

        resumen = datos.get("resumen", {})
        productos = datos.get("productos", [])

        self.resumen_widget.actualizar(
            total_ingresos=resumen.get("total_ingresos", 0.0),
            total_ventas=resumen.get("total_ventas", 0),
            ganancia=resumen.get("ganancia_estimada", 0.0),
            margen=resumen.get("margen_promedio", 0.0),
        )

        self.tabla_productos.actualizar(productos)

        total_cant = sum(p.get("cantidad", 0) for p in productos)
        total_sub = sum(p.get("subtotal", 0.0) for p in productos)
        total_productos = len(productos)
        self.label_totales.setText(
            f"Mostrando {total_productos} productos vendidos · Total: S/ {total_sub:.2f}"
        )

        try:
            html = self.controlador._armar_html_reporte(datos)
            self.preview.setHtml(html)
        except Exception:
            self.preview.setText("No se puede mostrar la vista previa en este momento.")

    def exportar_pdf(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar reporte PDF", "reporte_del_dia.pdf", "PDF Files (*.pdf)")
        if not ruta:
            return

        resultado = self.controlador.exportar_reporte_pdf(None, ruta)
        if resultado.get("error"):
            self.show_toast(resultado.get("mensaje", "Error al exportar PDF"), error=True)
            return

        self.show_toast(f"PDF guardado en {resultado.get('ruta_pdf')}")

    def imprimir_reporte(self):
        fd, temp_path = tempfile.mkstemp(suffix='.pdf')
        os.close(fd)
        resultado = self.controlador.exportar_reporte_pdf(None, temp_path)
        if resultado.get('error'):
            self.show_toast(resultado.get('mensaje', 'Error al generar PDF'), error=True)
            return

        ruta_pdf = resultado.get('ruta_pdf')
        try:
            if os.name == 'nt':
                os.startfile(ruta_pdf, 'print')
                self.show_toast("Enviando a impresora...")
            else:
                os.startfile(ruta_pdf)
                self.show_toast("PDF generado en el visor por defecto.")
        except Exception:
            self.show_toast(f"PDF generado en {ruta_pdf}")

    def show_toast(self, mensaje: str, duration: int = 2200, error: bool = False):
        toast = QLabel(mensaje, self)
        toast.setAttribute(Qt.WA_TransparentForMouseEvents)
        toast.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        toast.setStyleSheet(
            "background: #2E7D32; color: white; padding: 10px 16px; border-radius: 12px; font-weight: 700;"
            if not error
            else "background: #D32F2F; color: white; padding: 10px 16px; border-radius: 12px; font-weight: 700;"
        )
        toast.adjustSize()
        x = max(20, (self.width() - toast.width()) // 2)
        toast.move(x, 20)
        toast.show()
        toast.raise_()
        QTimer.singleShot(duration, toast.deleteLater)
