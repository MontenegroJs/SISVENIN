"""
VentaVista - SISVENIN
POS rápido 3 clics (compatible con App.py + navegación)
"""

from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QListWidget, QLabel,
    QMessageBox, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView
)

from src.app.controllers.venta_controlador import VentaControlador
from src.app.shared.components.sis_button import SisButton


class VentaVista(QWidget):
    """
    Vista POS de ventas - SISVENIN
    Compatible con sistema modular (App.py)
    """

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
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                color: #212121;
                font-size: 14px;
                font-family: Arial;
            }

            QLineEdit {
                background-color: white;
                border: 1px solid #E0E0E0;
                padding: 8px;
                border-radius: 6px;
            }

            QListWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                outline: 0;
            }

            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
                margin: 2px 4px;
            }

            QListWidget::item:hover {
                background-color: #F1F8E9;
            }

            QListWidget::item:selected {
                background-color: #C8E6C9;
                color: #1B5E20;
                font-weight: bold;
                border-left: 4px solid #2E7D32;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                gridline-color: #E0E0E0;
            }

            QHeaderView::section {
                background-color: #FAFAFA;
                color: #616161;
                padding: 6px;
                border: none;
                border-bottom: 1px solid #E0E0E0;
                font-weight: bold;
            }

            QPushButton#btnEliminarFila {
                background-color: transparent;
                border: none;
                color: #D32F2F;
                font-size: 15px;
                padding: 0px;
            }

            QPushButton#btnEliminarFila:hover {
                color: #B71C1C;
            }
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
        self.lbl_productos.setStyleSheet("font-weight: bold; color: #616161;")

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
        self.lbl_carrito.setStyleSheet("font-weight: bold; color: #616161;")

        self.lbl_contador = QLabel("Productos: 0")
        self.lbl_contador.setStyleSheet("color: #9E9E9E;")
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
        self.lbl_total.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2E7D32;
        """)
        self.lbl_total.setAlignment(Qt.AlignRight)

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
            self.lista_productos.addItem(
                f"{p.id} - {p.nombre} - S/ {p.precio_venta}"
            )

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