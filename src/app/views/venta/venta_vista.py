"""
VentaVista - SISVENIN
POS rápido 3 clics (compatible con App.py + navegación)
"""

from functools import partial

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView
)

from src.app.base_layout import BaseLayout
from src.app.controllers.venta_controlador import VentaControlador
from src.app.shared.components.sis_button import SisButton


class VentaVista(QWidget):
    """
    Vista POS de ventas - SISVENIN
    Compatible con sistema modular (App.py)
    """

    # 🔧 TIPOGRAFÍA (mismo patrón de configuración explícita que TablaProductos)
    FUENTE_FAMILIA = "'Century Gothic', 'Trebuchet MS', 'Segoe UI', sans-serif"
    FUENTE_BASE_TAMANO = 14

    FUENTE_ETIQUETA_TAMANO = 14
    FUENTE_ETIQUETA_PESO = 700          # títulos de sección: PRODUCTOS / CARRITO DE VENTA

    FUENTE_PRODUCTO_TAMANO = 15
    FUENTE_PRODUCTO_PESO = 500          # nombre del producto en la lista
    FUENTE_PRECIO_PESO = 700            # precio del producto en la lista (negrita)

    FUENTE_TOTAL_TAMANO = 24
    FUENTE_TOTAL_PESO = 700

    def __init__(self, on_navigate_to_report=None, on_navigate_to_products=None):
        super().__init__()

        # ================= NAVEGACIÓN (OBLIGATORIO POR APP.PY) =================
        self.on_navigate_to_report = on_navigate_to_report
        self.on_navigate_to_products = on_navigate_to_products

        # ================= CONTROLADOR =================
        self.controlador = VentaControlador()
        self.resultados = []

        # ================= CONFIG VENTANA =================
        self.setWindowTitle("SISVENIN - POS VENTA")
        self.resize(1000, 600)

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
        """)

        # ================= LAYOUT PRINCIPAL =================
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(16)

        # ======================================================
        # 🟢 PANEL IZQUIERDO: PRODUCTOS
        # ======================================================
        self.panel_productos = QVBoxLayout()
        self.panel_productos.setSpacing(8)

        self.lbl_productos = QLabel("PRODUCTOS")
        self.lbl_productos.setStyleSheet(f"""
            font-size: {self.FUENTE_ETIQUETA_TAMANO}px;
            font-weight: {self.FUENTE_ETIQUETA_PESO};
            color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
        """)

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("🔍  Buscar producto...")

        self.lista_productos = QListWidget()

        self.btn_agregar = SisButton(
            "Agregar al carrito",
            variant="primary"
        )

        self.panel_productos.addWidget(self.lbl_productos)
        self.panel_productos.addWidget(self.input_busqueda)
        self.panel_productos.addWidget(self.lista_productos)
        self.panel_productos.addWidget(self.btn_agregar)

        # ======================================================
        # 🟢 PANEL DERECHO: CARRITO
        # ======================================================
        self.panel_carrito = QVBoxLayout()
        self.panel_carrito.setSpacing(8)

        header_carrito = QHBoxLayout()
        self.lbl_carrito = QLabel("CARRITO DE VENTA")
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
            "Producto", "Precio", "Cantidad", "Subtotal", ""
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)

        self.lbl_total = QLabel("TOTAL: S/ 0.00")
        self.lbl_total.setStyleSheet(f"""
            font-size: {self.FUENTE_TOTAL_TAMANO}px;
            font-weight: {self.FUENTE_TOTAL_PESO};
            color: {BaseLayout.COLOR_PRIMARIO};
        """)
        self.lbl_total.setAlignment(Qt.AlignRight)

        # ================= PAGO CON =================
        self.lbl_pago = QLabel("PAGO CON:")
        self.lbl_pago.setStyleSheet(f"""
            font-weight: {self.FUENTE_ETIQUETA_PESO};
            color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
        """)

        self.input_pago = QLineEdit()
        self.input_pago.setPlaceholderText("Ingrese monto pagado...")
        self.input_pago.setStyleSheet("font-size: 16px; padding: 8px;")

        # ================= VUELTO =================
        self.lbl_vuelto = QLabel("VUELTO: S/ 0.00")
        self.lbl_vuelto.setStyleSheet(f"""
            font-size: 26px;
            font-weight: {self.FUENTE_TOTAL_PESO};
            color: {BaseLayout.COLOR_PRIMARIO};
        """)
        self.lbl_vuelto.setAlignment(Qt.AlignRight)

        self.lbl_error_pago = QLabel("")
        self.lbl_error_pago.setStyleSheet(f"color: {BaseLayout.COLOR_PELIGRO}; font-weight: bold;")

        botones_carrito = QHBoxLayout()
        self.btn_cancelar = SisButton(
            "Cancelar",
            variant="secondary"
        )
        self.btn_finalizar = SisButton(
            "Finalizar venta",
            variant="primary"
        )
        botones_carrito.addWidget(self.btn_cancelar)
        botones_carrito.addWidget(self.btn_finalizar)

        self.panel_carrito.addLayout(header_carrito)
        self.panel_carrito.addWidget(self.tabla)
        self.panel_carrito.addWidget(self.lbl_total)
        self.panel_carrito.addWidget(self.lbl_pago)
        self.panel_carrito.addWidget(self.input_pago)
        self.panel_carrito.addWidget(self.lbl_vuelto)
        self.panel_carrito.addWidget(self.lbl_error_pago)
        self.panel_carrito.addLayout(botones_carrito)

        # ================= ARMAR UI =================
        self.layout.addLayout(self.panel_productos, 2)
        self.layout.addLayout(self.panel_carrito, 3)

        self.setLayout(self.layout)

        # ================= EVENTOS =================
        self.input_busqueda.textChanged.connect(self.buscar_productos)
        self.btn_agregar.clicked.connect(self.agregar_producto)
        self.btn_cancelar.clicked.connect(self.cancelar_venta)
        self.btn_finalizar.clicked.connect(self.finalizar_venta)
        self.input_pago.textChanged.connect(self.calcular_vuelto)

        print("✅ VentaVista cargada correctamente")

    # ======================================================
    # 🔎 BUSCAR PRODUCTOS
    # ======================================================
    def buscar_productos(self):
        texto = self.input_busqueda.text().strip()

        self.lista_productos.clear()

        if not texto:
            self.resultados = []
            return

        self.resultados = self.controlador.buscar_productos(texto)

        for p in self.resultados:
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 56))
            self.lista_productos.addItem(item)
            self.lista_productos.setItemWidget(item, self._crear_item_producto(p))

    def _crear_item_producto(self, producto):
        """Widget de fila: nombre a la izquierda, precio en negrita a la derecha."""
        contenedor = QWidget()
        contenedor.setStyleSheet("background: transparent;")

        fila = QHBoxLayout(contenedor)
        fila.setContentsMargins(4, 0, 4, 0)

        lbl_nombre = self._crear_label_producto(
            producto.nombre,
            peso=self.FUENTE_PRODUCTO_PESO
        )

        lbl_precio = self._crear_label_producto(
            f"S/ {producto.precio_venta:.2f}",
            peso=self.FUENTE_PRECIO_PESO,
            alineacion=Qt.AlignRight | Qt.AlignVCenter
        )

        fila.addWidget(lbl_nombre)
        fila.addStretch()
        fila.addWidget(lbl_precio)

        return contenedor

    def _crear_label_producto(self, texto, peso, alineacion=None):
        """
        Crea un QLabel con la tipografía estándar de productos
        (self.FUENTE_FAMILIA / self.FUENTE_PRODUCTO_TAMANO), evitando
        repetir el mismo stylesheet en cada lugar donde se necesite.
        """
        label = QLabel(texto)
        label.setStyleSheet(f"""
            font-family: {self.FUENTE_FAMILIA};
            font-size: {self.FUENTE_PRODUCTO_TAMANO}px;
            font-weight: {peso};
            color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
        """)
        if alineacion is not None:
            label.setAlignment(alineacion)
        return label

    # ======================================================
    # ➕ AGREGAR PRODUCTO
    # ======================================================
    def agregar_producto(self):
        i = self.lista_productos.currentRow()

        if i < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona un producto")
            return

        producto = self.resultados[i]

        self.controlador.agregar_producto(producto)

        self.actualizar_tabla()
        self.actualizar_total()

    # ======================================================
    # 🧾 ACTUALIZAR TABLA CARRITO
    # ======================================================
    def actualizar_tabla(self):
        detalle = self.controlador.obtener_detalle()

        self.tabla.setRowCount(len(detalle))

        for i, item in enumerate(detalle):
            self.tabla.setItem(i, 0, QTableWidgetItem(item["nombre"]))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(item["precio"])))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(item["cantidad"])))
            self.tabla.setItem(i, 3, QTableWidgetItem(str(item["subtotal"])))

            btn_eliminar_fila = QPushButton("🗑️")
            btn_eliminar_fila.setObjectName("btnEliminarFila")
            btn_eliminar_fila.setCursor(Qt.PointingHandCursor)
            btn_eliminar_fila.clicked.connect(partial(self.eliminar_producto, i))
            self.tabla.setCellWidget(i, 4, btn_eliminar_fila)

        self.lbl_contador.setText(f"Productos: {len(detalle)}")

    # ======================================================
    # ❌ ELIMINAR PRODUCTO (por fila, vía ícono 🗑️)
    # ======================================================
    def eliminar_producto(self, row):
        if row < 0 or row >= len(self.controlador.venta.detalle):
            return

        del self.controlador.venta.detalle[row]
        self.controlador.venta.calcular_total()

        self.actualizar_tabla()
        self.actualizar_total()

    # ======================================================
    # 💰 ACTUALIZAR TOTAL
    # ======================================================
    def actualizar_total(self):
        total = self.controlador.obtener_total()
        self.lbl_total.setText(f"TOTAL: S/ {total:.2f}")

    # ======================================================
    # 💵 CALCULAR VUELTO (HU-02)
    # ======================================================
    def calcular_vuelto(self):
        try:
            pago = float(self.input_pago.text() or 0)
        except ValueError:
            self.lbl_error_pago.setText("Ingrese un número válido")
            self.lbl_vuelto.setText("VUELTO: S/ 0.00")
            return

        total = self.controlador.obtener_total()
        resultado = self.controlador.calcular_vuelto(pago, total)

        if resultado["error"]:
            self.lbl_error_pago.setText(resultado["error"])
            self.lbl_vuelto.setText("VUELTO: S/ 0.00")
            self.lbl_vuelto.setStyleSheet(f"""
                font-size: 26px;
                font-weight: {self.FUENTE_TOTAL_PESO};
                color: {BaseLayout.COLOR_PELIGRO};
            """)
        else:
            self.lbl_error_pago.setText("")
            self.lbl_vuelto.setText(f"VUELTO: S/ {resultado['vuelto']:.2f}")
            self.lbl_vuelto.setStyleSheet(f"""
                font-size: 26px;
                font-weight: {self.FUENTE_TOTAL_PESO};
                color: {BaseLayout.COLOR_PRIMARIO};
            """)

    # ======================================================
    # 🚫 CANCELAR VENTA (vacía el carrito actual)
    # ======================================================
    def cancelar_venta(self):
        if not self.controlador.venta.detalle:
            return

        respuesta = QMessageBox.question(
            self, "Cancelar venta",
            "¿Seguro que deseas vaciar el carrito?"
        )

        if respuesta == QMessageBox.Yes:
            self.controlador = VentaControlador()
            self.actualizar_tabla()
            self.actualizar_total()
            self.input_pago.clear()
            self.lbl_vuelto.setText("VUELTO: S/ 0.00")
            self.lbl_error_pago.setText("")

    # ======================================================
    # 💾 FINALIZAR VENTA
    # ======================================================
    def finalizar_venta(self):
        ok = self.controlador.confirmar_venta()

        if ok:
            QMessageBox.information(self, "OK", "Venta registrada")

            self.controlador = VentaControlador()
            self.actualizar_tabla()
            self.actualizar_total()
            self.input_pago.clear()
            self.lbl_vuelto.setText("VUELTO: S/ 0.00")
            self.lbl_error_pago.setText("")