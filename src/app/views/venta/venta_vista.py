"""
VentaVista - SISVENIN
POS rápido 3 clics (compatible con App.py + navegación)
"""

from functools import partial

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QListWidget, QListWidgetItem, QLabel, QDoubleSpinBox,
    QMessageBox, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QStackedWidget, QAbstractSpinBox
)
from PySide6.QtGui import QFont, QColor

from src.app.base_layout import BaseLayout
from src.app.controllers.producto_controlador import ProductoControlador
from src.app.controllers.venta_controlador import VentaControlador
from src.app.controllers.reporte_controlador import ReporteControlador

# ============================================================
# 🩹 PARCHE DE COMPATIBILIDAD (monkey patch — no toca producto_vista.py)
# ------------------------------------------------------------

try:
    from src.app.views.producto.components.tabla_productos import TablaProductos

    if not hasattr(TablaProductos, "set_items_per_page"):
        def _set_items_per_page_parche(self, items_per_page):
            """
            No-op de compatibilidad: TablaProductos ya recibe items_per_page
            por constructor: no hay una acción real que ejecutar aquí, solo
            evita el AttributeError que rompía resaltar_producto().
            """
            pass

        TablaProductos.set_items_per_page = _set_items_per_page_parche
except ImportError:
    # Si la ruta del componente cambia, no debe romper VentaVista.
    pass


class _SpinBoxPago(QDoubleSpinBox):
    """
    QDoubleSpinBox especializado para el campo "Pago con":
    - Selecciona todo el texto al recibir foco, para poder escribir el
      monto directamente sin tener que borrar el "0.00" a mano primero.
    - Si el campo queda vacío (por ejemplo, tras borrar todo) y se
      presionan las flechas o se pierde el foco, el valor pasa a 0.00
      en vez de "revivir" el monto que tenía antes de borrarlo.
    - Como ya no tiene borde propio (vive dentro de un contenedor junto
      a las flechas ▲▼ personalizadas), le avisa a ese contenedor cuándo
      pintarse de verde al enfocar, vía la propiedad dinámica "focused".
    """

    contenedor_focus = None

    def focusInEvent(self, event):
        super().focusInEvent(event)
        QTimer.singleShot(0, self.selectAll)
        self._marcar_foco(True)

    def focusOutEvent(self, event):
        if self.lineEdit().text().strip() == "":
            self.setValue(0.0)
        super().focusOutEvent(event)
        self._marcar_foco(False)

    def stepBy(self, steps):
        if self.lineEdit().text().strip() in ("", "-"):
            self.setValue(0.0)
            return
        super().stepBy(steps)

    def _marcar_foco(self, activo):
        if self.contenedor_focus is None:
            return
        self.contenedor_focus.setProperty("focused", activo)
        self.contenedor_focus.style().unpolish(self.contenedor_focus)
        self.contenedor_focus.style().polish(self.contenedor_focus)


class PanelBusqueda(QWidget):
    """
    Panel de búsqueda de productos para el POS.
    Formato: "Nombre – S/ precio (stock: X)"
    """

    # 🔧 TIPOGRAFÍA (mismo patrón de configuración explícita que TablaProductos)
    FUENTE_FAMILIA = "'Century Gothic', 'Trebuchet MS', 'Segoe UI', sans-serif"
    FUENTE_BASE_TAMANO = 14

    FUENTE_ETIQUETA_TAMANO = 14
    FUENTE_ETIQUETA_PESO = 700          # títulos de sección: BÚSQUEDA / CARRITO DE COMPRAS

    FUENTE_PRODUCTO_TAMANO = 15
    FUENTE_PRODUCTO_PESO = 500          # nombre del producto en la lista
    FUENTE_PRECIO_PESO = 700            # precio del producto en la lista (negrita)

    FUENTE_TOTAL_TAMANO = 24
    FUENTE_TOTAL_PESO = 700

    UMBRAL_STOCK_BAJO = 5   # mismo criterio que TablaProductos (stock < 5 = alerta)

    def __init__(self, on_navigate_to_report=None, on_navigate_to_products=None):
        super().__init__()

        # ================= NAVEGACIÓN (OBLIGATORIO POR APP.PY) =================
        self.on_navigate_to_report = on_navigate_to_report
        self.on_navigate_to_products = on_navigate_to_products

        # ================= CONTROLADOR =================
        self.controlador = VentaControlador()
        self.controlador_productos = ProductoControlador()
        self.resultados = []

        # ================= CONFIG VENTANA =================
        self.setWindowTitle("SISVENIN - POS VENTA")
        self.resize(1100, 650)

        # ================= ESTILO GENERAL SISVENIN =================
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BaseLayout.COLOR_FONDO_VENTANA};
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
                font-size: {self.FUENTE_BASE_TAMANO}px;
                font-family: {self.FUENTE_FAMILIA};
            }}

            QLineEdit {{
                background-color: {BaseLayout.COLOR_TARJETA};
                border: 1px solid {BaseLayout.COLOR_BORDE};
                padding: 8px;
                border-radius: {BaseLayout.BORDER_RADIUS_TARJETA}px;
            }}

            QListWidget {{
                background-color: {BaseLayout.COLOR_TARJETA};
                border: 1px solid {BaseLayout.COLOR_BORDE};
                border-radius: {BaseLayout.BORDER_RADIUS_TARJETA}px;
                outline: 0;
            }}

            QListWidget::item {{
                padding: 4px 8px;
                border-bottom: 1px solid {BaseLayout.COLOR_BORDE};
            }}

            QListWidget::item:hover {{
                background-color: #F1F8E9;
            }}

            QListWidget::item:selected {{
                background-color: #C8E6C9;
                border-left: 4px solid {BaseLayout.COLOR_PRIMARIO};
            }}

            QTableWidget {{
                background-color: {BaseLayout.COLOR_TARJETA};
                border: 1px solid {BaseLayout.COLOR_BORDE};
                border-radius: {BaseLayout.BORDER_RADIUS_TARJETA}px;
                gridline-color: {BaseLayout.COLOR_BORDE};
                outline: 0;
            }}

            QTableWidget::item {{
                padding: 10px 8px;
                border: none;
            }}

            QTableWidget::item:focus {{
                border: none;
                outline: none;
            }}

            QTableWidget::item:selected {{
                background-color: {BaseLayout.COLOR_FONDO_VENTANA};
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
            }}

            QHeaderView::section {{
                background-color: {BaseLayout.COLOR_FONDO_VENTANA};
                color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
                padding: 6px;
                border: none;
                border-bottom: 1px solid {BaseLayout.COLOR_BORDE};
                font-weight: bold;
            }}

            QPushButton#btnEliminarFila {{
                background-color: transparent;
                border: none;
                color: {BaseLayout.COLOR_PELIGRO};
                font-size: 15px;
                padding: 0px;
            }}

            QPushButton#btnEliminarFila:hover {{
                color: {BaseLayout.COLOR_PELIGRO_HOVER};
            }}

            QPushButton#btnCantidad {{
                background-color: {BaseLayout.COLOR_FONDO_VENTANA};
                border: 1px solid {BaseLayout.COLOR_BORDE};
                border-radius: 4px;
                font-weight: bold;
                color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
            }}

            QPushButton#btnCantidad:hover {{
                background-color: {BaseLayout.COLOR_TARJETA};
                color: {BaseLayout.COLOR_PRIMARIO};
            }}

            QPushButton#btnAlerta {{
                background-color: transparent;
                border: none;
                color: #E65100;
                text-align: left;
                padding: 2px 0px;
            }}

            QPushButton#btnAlerta:hover {{
                text-decoration: underline;
                color: #BF360C;
            }}
        """)

        # ================= LAYOUT PRINCIPAL =================
        self.layout_principal = QVBoxLayout()
        self.layout_principal.setContentsMargins(20, 16, 20, 20)
        self.layout_principal.setSpacing(14)
        self.setLayout(self.layout_principal)

        fila_paneles = QHBoxLayout()
        fila_paneles.setSpacing(16)
        self._construir_panel_productos(fila_paneles)
        self._construir_panel_carrito(fila_paneles)
        self.layout_principal.addLayout(fila_paneles)

        self._construir_barra_pago()
        self._construir_footer()

        # ================= EVENTOS =================
        self.input_busqueda.textChanged.connect(self.buscar_productos)
        self.lista_productos.itemClicked.connect(self._on_producto_clic)
        self.btn_cancelar.clicked.connect(self.cancelar_venta)
        self.btn_finalizar.clicked.connect(self.finalizar_venta)
        self.input_pago.valueChanged.connect(self.calcular_vuelto)
        self.input_pago.lineEdit().textChanged.connect(self.calcular_vuelto)

        # ================= ESTADO INICIAL =================
        self.buscar_productos()
        self.actualizar_tabla()
        self.actualizar_total()
        self._cargar_alertas()

        print("✅ VentaVista cargada correctamente")

    # ======================================================
    # 🧱 CONSTRUCCIÓN DE SECCIONES DE LA UI
    # ======================================================
    def _construir_panel_productos(self, contenedor_padre):
        """🟢 PANEL IZQUIERDO: búsqueda + resultados + alertas de stock."""
        self.panel_productos = QVBoxLayout()
        self.panel_productos.setSpacing(8)

        self.lbl_productos = QLabel("🔍  BÚSQUEDA")
        self.lbl_productos.setStyleSheet(f"""
            font-size: {self.FUENTE_ETIQUETA_TAMANO}px;
            font-weight: {self.FUENTE_ETIQUETA_PESO};
            color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
        """)

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText(" Buscar por nombre o código...")

        self.lbl_resultados = QLabel("RESULTADOS (clic para agregar)")
        self.lbl_resultados.setStyleSheet(f"color: {BaseLayout.COLOR_TEXTO_SECUNDARIO}; font-size: 12px;")

        self.lista_productos = QListWidget()

        self.panel_productos.addWidget(self.lbl_productos)
        self.panel_productos.addWidget(self.input_busqueda)
        self.panel_productos.addWidget(self.lbl_resultados)
        self.panel_productos.addWidget(self.lista_productos)

        self._construir_alertas_stock()
        self.panel_productos.addWidget(self.widget_alertas)

        contenedor_padre.addLayout(self.panel_productos, 2)

    def _construir_alertas_stock(self):
        """Caja amarilla de 'Alertas rápidas' de stock bajo (se oculta sola si no aplica)."""
        self.widget_alertas = QWidget()
        self.widget_alertas.setStyleSheet("""
            background-color: #FFF8E1;
            border: 1px solid #FFE082;
            border-radius: 8px;
        """)

        vbox = QVBoxLayout(self.widget_alertas)
        vbox.setContentsMargins(12, 10, 12, 10)
        vbox.setSpacing(4)

        lbl_titulo = QLabel("⚠️  Alertas rápidas")
        lbl_titulo.setStyleSheet("color: #F57C00; font-weight: 700;")
        vbox.addWidget(lbl_titulo)

        self.layout_alertas = QVBoxLayout()
        self.layout_alertas.setSpacing(2)
        vbox.addLayout(self.layout_alertas)

        self.widget_alertas.setVisible(False)

    def _construir_panel_carrito(self, contenedor_padre):
        """🟢 PANEL DERECHO: tabla del carrito + total."""
        self.panel_carrito = QVBoxLayout()
        self.panel_carrito.setSpacing(8)

        header_carrito = QHBoxLayout()
        self.lbl_carrito = QLabel("🛒  CARRITO DE COMPRAS")
        self.lbl_carrito.setStyleSheet(f"""
            font-size: {self.FUENTE_ETIQUETA_TAMANO}px;
            font-weight: {self.FUENTE_ETIQUETA_PESO};
            color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
        """)

        self.lbl_contador = QLabel("Productos: 0")
        self.lbl_contador.setStyleSheet(f"color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};")
        self.lbl_contador.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        header_carrito.addWidget(self.lbl_carrito)
        header_carrito.addWidget(self.lbl_contador)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            "Producto", "Cantidad", "Precio", "Subtotal", ""
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        anchos_columnas = {1: 110, 2: 90, 3: 100, 4: 48}
        for col, ancho in anchos_columnas.items():
            self.tabla.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
            self.tabla.setColumnWidth(col, ancho)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.verticalHeader().setDefaultSectionSize(52)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setFocusPolicy(Qt.NoFocus)

        # Estado vacío del carrito (se muestra cuando no hay productos)
        self.widget_carrito_vacio = QWidget()
        vbox_vacio = QVBoxLayout(self.widget_carrito_vacio)
        vbox_vacio.setAlignment(Qt.AlignCenter)
        lbl_icono_vacio = QLabel("🛒")
        lbl_icono_vacio.setAlignment(Qt.AlignCenter)
        lbl_icono_vacio.setStyleSheet("font-size: 40px;")
        lbl_texto_vacio = QLabel("El carrito está vacío.\nBusca productos para agregar.")
        lbl_texto_vacio.setAlignment(Qt.AlignCenter)
        lbl_texto_vacio.setStyleSheet(f"color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};")
        vbox_vacio.addWidget(lbl_icono_vacio)
        vbox_vacio.addWidget(lbl_texto_vacio)

        self.lbl_total = QLabel("TOTAL: S/ 0.00")
        self.lbl_total.setStyleSheet(f"""
            font-size: {self.FUENTE_TOTAL_TAMANO}px;
            font-weight: {self.FUENTE_TOTAL_PESO};
            color: {BaseLayout.COLOR_PRIMARIO};
        """)
        self.lbl_total.setAlignment(Qt.AlignRight)

        self.panel_carrito.addLayout(header_carrito)

        self.stack_carrito = QStackedWidget()
        self.stack_carrito.setMinimumHeight(320)
        self.stack_carrito.addWidget(self.tabla)
        self.stack_carrito.addWidget(self.widget_carrito_vacio)
        self.panel_carrito.addWidget(self.stack_carrito)

        self.panel_carrito.addWidget(self.lbl_total)

        contenedor_padre.addLayout(self.panel_carrito, 3)

    def _construir_barra_pago(self):
        """Tarjeta horizontal: PAGO CON | VUELTO, debajo de los dos paneles."""
        self.widget_pago = QWidget()
        self.widget_pago.setStyleSheet(f"""
            background-color: {BaseLayout.COLOR_TARJETA};
            border: 1px solid {BaseLayout.COLOR_BORDE};
            border-radius: {BaseLayout.BORDER_RADIUS_TARJETA}px;
        """)

        fila = QHBoxLayout(self.widget_pago)
        fila.setContentsMargins(16, 12, 16, 12)
        fila.setSpacing(10)

        self.lbl_pago = QLabel("💰  PAGO CON:  S/")
        self.lbl_pago.setStyleSheet(f"""
            font-weight: {self.FUENTE_ETIQUETA_PESO};
            color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
        """)
        self.lista_alertas.itemClicked.connect(self._on_alerta_clickeada)
        layout.addWidget(self.lista_alertas)
    
    def _cargar_alertas(self):
        """Carga los productos con stock bajo (<5)"""
        productos = self.controlador.obtener_productos_stock_bajo(limite=5)
        self.lista_alertas.clear()
        
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
        
        # Calcular total
        total = sum(p.precio_venta for p in self.carrito)
            
        # Verificar que el pago sea suficiente
        try:
            pago = float(self.pago_input.text() or "0")
        except ValueError:
            pago = 0
    
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
