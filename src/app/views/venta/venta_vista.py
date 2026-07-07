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

from src.app.base_layout import BaseLayout
from src.app.controllers.producto_controlador import ProductoControlador
from src.app.controllers.venta_controlador import VentaControlador
from src.app.shared.components.sis_button import SisButton

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


class VentaVista(QWidget):
    """
    Vista POS de ventas - SISVENIN
    Compatible con sistema modular (App.py)
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

        self.input_pago = _SpinBoxPago()
        self.input_pago.setDecimals(2)
        self.input_pago.setSingleStep(0.5)
        self.input_pago.setMinimum(0.0)
        self.input_pago.setMaximum(99_999.99)
        self.input_pago.setValue(0.0)
        self.input_pago.setAlignment(Qt.AlignRight)
        # Ocultamos las flechas nativas: en Windows (estilo nativo) ignoran
        # cualquier color que le pongamos por QSS/paleta. Las reemplazamos
        # por botones propios (▲/▼) más abajo, con color 100% controlado.
        self.input_pago.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.input_pago.setStyleSheet(f"""
            QDoubleSpinBox {{
                font-size: 16px;
                padding: 6px 8px;
                background-color: transparent;
                border: none;
            }}
        """)

        # Contenedor: input de pago + flechas propias, con el borde/fondo
        # que antes tenía el QDoubleSpinBox solo, para que se vea como un
        # único campo.
        contenedor_pago = QWidget()
        contenedor_pago.setObjectName("contenedorPago")
        contenedor_pago.setStyleSheet(f"""
            QWidget#contenedorPago {{
                background-color: {BaseLayout.COLOR_TARJETA};
                border: 1px solid {BaseLayout.COLOR_BORDE};
                border-radius: {BaseLayout.BORDER_RADIUS_TARJETA}px;
            }}
            QWidget#contenedorPago[focused="true"] {{
                border: 1px solid {BaseLayout.COLOR_PRIMARIO};
            }}
        """)
        fila_input_pago = QHBoxLayout(contenedor_pago)
        fila_input_pago.setContentsMargins(0, 0, 0, 0)
        fila_input_pago.setSpacing(0)
        fila_input_pago.addWidget(self.input_pago)

        flechas_pago = QWidget()
        flechas_pago.setStyleSheet(f"border-left: 1px solid {BaseLayout.COLOR_BORDE};")
        col_flechas = QVBoxLayout(flechas_pago)
        col_flechas.setContentsMargins(0, 0, 0, 0)
        col_flechas.setSpacing(0)

        btn_pago_subir = QPushButton("▲")
        btn_pago_subir.setObjectName("btnFlechaPago")
        btn_pago_subir.setFixedSize(20, 15)
        btn_pago_subir.setCursor(Qt.PointingHandCursor)
        btn_pago_subir.clicked.connect(self.input_pago.stepUp)

        btn_pago_bajar = QPushButton("▼")
        btn_pago_bajar.setObjectName("btnFlechaPago")
        btn_pago_bajar.setFixedSize(20, 15)
        btn_pago_bajar.setCursor(Qt.PointingHandCursor)
        btn_pago_bajar.clicked.connect(self.input_pago.stepDown)

        col_flechas.addWidget(btn_pago_subir)
        col_flechas.addWidget(btn_pago_bajar)
        fila_input_pago.addWidget(flechas_pago)

        contenedor_pago.setStyleSheet(contenedor_pago.styleSheet() + f"""
            QPushButton#btnFlechaPago {{
                background-color: {BaseLayout.COLOR_FONDO_VENTANA};
                border: none;
                color: {BaseLayout.COLOR_PRIMARIO};
                font-size: 8px;
                padding: 0px;
            }}
            QPushButton#btnFlechaPago:hover {{
                background-color: {BaseLayout.COLOR_TARJETA};
                color: {BaseLayout.COLOR_PRIMARIO};
            }}
        """)

        self.input_pago.contenedor_focus = contenedor_pago

        separador = QLabel("|")
        separador.setStyleSheet(f"color: {BaseLayout.COLOR_BORDE};")

        self.lbl_vuelto_titulo = QLabel("💵  VUELTO:")
        self.lbl_vuelto_titulo.setStyleSheet(f"""
            font-weight: {self.FUENTE_ETIQUETA_PESO};
            color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
        """)

        self.lbl_vuelto_valor = QLabel("Ingrese monto recibido")
        self._estilo_vuelto_neutro()

        self.lbl_error_pago = QLabel("")
        self.lbl_error_pago.setStyleSheet(f"color: {BaseLayout.COLOR_PELIGRO}; font-weight: bold;")

        fila.addWidget(self.lbl_pago)
        fila.addWidget(contenedor_pago)
        fila.addWidget(separador)
        fila.addWidget(self.lbl_vuelto_titulo)
        fila.addWidget(self.lbl_vuelto_valor)
        fila.addWidget(self.lbl_error_pago)
        fila.addStretch()

        self.layout_principal.addWidget(self.widget_pago)

    def _construir_footer(self):
        """Botones de acción al pie: Cancelar / Finalizar venta."""
        footer = QHBoxLayout()

        self.btn_cancelar = SisButton("🧾 Cancelar", variant="secondary")
        self.btn_finalizar = SisButton("✅ Finalizar venta", variant="primary")

        footer.addWidget(self.btn_cancelar)
        footer.addStretch()
        footer.addWidget(self.btn_finalizar)

        self.layout_principal.addLayout(footer)

    # ======================================================
    # 🔎 BUSCAR PRODUCTOS
    # ======================================================
    def buscar_productos(self):
        texto = self.input_busqueda.text().strip()

        self.lista_productos.clear()

        if not texto:
            self.resultados = []
            self._mostrar_placeholder_busqueda("Empieza a escribir para buscar...")
            return

        self.resultados = self.controlador.buscar_productos(texto)

        if not self.resultados:
            self._mostrar_placeholder_busqueda("No se encontraron productos")
            return

        for p in self.resultados:
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 56))
            if p.stock <= 0:
                item.setFlags(Qt.NoItemFlags)   # sin stock: no se puede agregar
            self.lista_productos.addItem(item)
            self.lista_productos.setItemWidget(item, self._crear_item_producto(p))

    def _mostrar_placeholder_busqueda(self, texto):
        item = QListWidgetItem(texto)
        item.setFlags(Qt.NoItemFlags)
        item.setTextAlignment(Qt.AlignCenter)
        item.setForeground(QColor(BaseLayout.COLOR_TEXTO_SECUNDARIO))
        self.lista_productos.addItem(item)

    def _crear_item_producto(self, producto):
        """
        Widget de fila: • nombre — S/ precio (stock: N)
        El stock se colorea según su nivel; si está en 0, la fila se tacha
        y queda deshabilitada (ver buscar_productos).
        """
        contenedor = QWidget()
        contenedor.setStyleSheet("background: transparent;")

        fila = QHBoxLayout(contenedor)
        fila.setContentsMargins(4, 0, 4, 0)

        stock = producto.stock
        sin_stock = stock <= 0

        if sin_stock:
            color_stock = BaseLayout.COLOR_PELIGRO
            texto = f"<s>• {producto.nombre} (stock: {stock})</s>"
        else:
            color_stock = "#FF9800" if stock < self.UMBRAL_STOCK_BAJO else BaseLayout.COLOR_TEXTO_SECUNDARIO
            texto = (
                f"• {producto.nombre} — "
                f"<span style='color:{BaseLayout.COLOR_PRIMARIO}; font-weight:700;'>"
                f"S/ {producto.precio_venta:.2f}</span> "
                f"<span style='color:{color_stock};'>(stock: {stock})</span>"
            )

        lbl = QLabel(texto)
        lbl.setTextFormat(Qt.RichText)
        lbl.setStyleSheet(f"""
            font-family: {self.FUENTE_FAMILIA};
            font-size: {self.FUENTE_PRODUCTO_TAMANO}px;
            font-weight: {self.FUENTE_PRODUCTO_PESO};
            color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
        """)

        fila.addWidget(lbl)
        fila.addStretch()

        return contenedor

    # ======================================================
    # ➕ AGREGAR PRODUCTO (clic directo en el resultado)
    # ======================================================
    def _on_producto_clic(self, item):
        row = self.lista_productos.row(item)

        if row < 0 or row >= len(self.resultados):
            return

        producto = self.resultados[row]

        fila_existente = self._buscar_fila_en_carrito(producto)
        if fila_existente is not None:
            # El producto ya está en el carrito: solo se incrementa la cantidad
            self.cambiar_cantidad(fila_existente, 1)
            return

        self.controlador.agregar_producto(producto)

        self.actualizar_tabla()
        self.actualizar_total()

    def _buscar_fila_en_carrito(self, producto):
        """
        Busca si el producto ya está en el carrito (por id, o por nombre si
        el detalle no guarda id). Devuelve el índice de la fila o None.
        """
        detalle = self.controlador.venta.detalle
        producto_id = getattr(producto, "id", None)

        for i, item in enumerate(detalle):
            try:
                item_id = self._obtener_atributo(item, "id")
            except (KeyError, AttributeError):
                item_id = None

            if producto_id is not None and item_id is not None:
                if item_id == producto_id:
                    return i
                continue

            try:
                item_nombre = self._obtener_atributo(item, "nombre")
            except (KeyError, AttributeError):
                item_nombre = None

            if item_nombre is not None and item_nombre == producto.nombre:
                return i

        return None

    # ======================================================
    # 🧾 ACTUALIZAR TABLA CARRITO
    # ======================================================
    def actualizar_tabla(self):
        detalle = self.controlador.obtener_detalle()
        vacio = len(detalle) == 0

        self.stack_carrito.setCurrentWidget(self.widget_carrito_vacio if vacio else self.tabla)
        self.tabla.setRowCount(len(detalle))

        for i, item in enumerate(detalle):
            self.tabla.setItem(i, 0, QTableWidgetItem(item["nombre"]))
            self.tabla.setCellWidget(i, 1, self._crear_widget_cantidad(i, item["cantidad"]))
            self.tabla.setItem(i, 2, QTableWidgetItem(f"S/ {item['precio']:.2f}"))
            self.tabla.setItem(i, 3, QTableWidgetItem(f"S/ {item['subtotal']:.2f}"))

            btn_eliminar_fila = QPushButton("🗑️")
            btn_eliminar_fila.setObjectName("btnEliminarFila")
            btn_eliminar_fila.setCursor(Qt.PointingHandCursor)
            btn_eliminar_fila.clicked.connect(partial(self.eliminar_producto, i))
            self.tabla.setCellWidget(i, 4, btn_eliminar_fila)

        self.lbl_contador.setText(f"Productos: {len(detalle)}")

    def _crear_widget_cantidad(self, row, cantidad):
        """Control − [cantidad] + para editar la cantidad directamente en la fila."""
        contenedor = QWidget()
        fila = QHBoxLayout(contenedor)
        fila.setContentsMargins(0, 0, 0, 0)
        fila.setSpacing(6)
        fila.setAlignment(Qt.AlignCenter)

        btn_menos = QPushButton("−")
        btn_menos.setObjectName("btnCantidad")
        btn_menos.setFixedSize(24, 24)
        btn_menos.setCursor(Qt.PointingHandCursor)
        btn_menos.clicked.connect(partial(self.cambiar_cantidad, row, -1))

        lbl_cantidad = QLabel(str(cantidad))
        lbl_cantidad.setFixedWidth(20)
        lbl_cantidad.setAlignment(Qt.AlignCenter)
        lbl_cantidad.setStyleSheet("font-weight: 600;")

        btn_mas = QPushButton("+")
        btn_mas.setObjectName("btnCantidad")
        btn_mas.setFixedSize(24, 24)
        btn_mas.setCursor(Qt.PointingHandCursor)
        btn_mas.clicked.connect(partial(self.cambiar_cantidad, row, 1))

        fila.addWidget(btn_menos)
        fila.addWidget(lbl_cantidad)
        fila.addWidget(btn_mas)

        return contenedor

    # ======================================================
    # 🔢 CAMBIAR CANTIDAD (+ / − desde la fila del carrito)
    # ======================================================
    def cambiar_cantidad(self, row, delta):
        detalle = self.controlador.venta.detalle

        if row < 0 or row >= len(detalle):
            return

        item = detalle[row]
        cantidad_actual = self._obtener_atributo(item, "cantidad")
        nueva_cantidad = cantidad_actual + delta

        if nueva_cantidad <= 0:
            self.eliminar_producto(row)
            return

        precio = self._obtener_atributo(item, "precio")
        self._asignar_atributo(item, "cantidad", nueva_cantidad)
        self._asignar_atributo(item, "subtotal", precio * nueva_cantidad)

        self.controlador.venta.calcular_total()
        self.actualizar_tabla()
        self.actualizar_total()

    @staticmethod
    def _obtener_atributo(item, nombre):
        if isinstance(item, dict):
            return item[nombre]
        return getattr(item, nombre)

    @staticmethod
    def _asignar_atributo(item, nombre, valor):
        if isinstance(item, dict):
            item[nombre] = valor
        else:
            setattr(item, nombre, valor)

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
        self.calcular_vuelto()

    # ======================================================
    # 💵 CALCULAR VUELTO (HU-02)
    # ======================================================
    def calcular_vuelto(self):
        texto_actual = self.input_pago.lineEdit().text().strip()

        if texto_actual in ("", "-"):
            pago = 0.0
        else:
            pago = self.input_pago.value()

        if pago <= 0:
            self.lbl_vuelto_valor.setText("Ingrese monto recibido")
            self._estilo_vuelto_neutro()
            self.lbl_error_pago.setText("")
            return

        total = self.controlador.obtener_total()
        resultado = self.controlador.calcular_vuelto(pago, total)

        if resultado["error"]:
            self.lbl_error_pago.setText(f"⚠️ {resultado['error']}")
            self.lbl_vuelto_valor.setText(f"S/ {resultado.get('vuelto', pago - total):.2f}")
            self._estilo_vuelto_error()
        else:
            self.lbl_error_pago.setText("")
            self.lbl_vuelto_valor.setText(f"S/ {resultado['vuelto']:.2f}")
            self._estilo_vuelto_ok()

    def _estilo_vuelto_neutro(self):
        self.lbl_vuelto_valor.setStyleSheet(f"""
            color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
            font-style: italic;
        """)

    def _estilo_vuelto_ok(self):
        self.lbl_vuelto_valor.setStyleSheet(f"""
            font-size: {self.FUENTE_TOTAL_TAMANO}px;
            font-weight: {self.FUENTE_TOTAL_PESO};
            color: {BaseLayout.COLOR_PRIMARIO};
        """)

    def _estilo_vuelto_error(self):
        self.lbl_vuelto_valor.setStyleSheet(f"""
            font-size: {self.FUENTE_TOTAL_TAMANO}px;
            font-weight: {self.FUENTE_TOTAL_PESO};
            color: {BaseLayout.COLOR_PELIGRO};
        """)

    # ======================================================
    # ⚠️ ALERTAS RÁPIDAS DE STOCK BAJO
    # ======================================================
    def _cargar_alertas(self):
        while self.layout_alertas.count():
            hijo = self.layout_alertas.takeAt(0)
            if hijo.widget():
                hijo.widget().deleteLater()

        try:
            productos_bajo_stock = self.controlador_productos.obtener_productos_stock_bajo(
                limite=self.UMBRAL_STOCK_BAJO
            )
        except Exception:
            self.widget_alertas.setVisible(False)
            return

        if not productos_bajo_stock:
            self.widget_alertas.setVisible(False)
            return

        self.widget_alertas.setVisible(True)

        for p in productos_bajo_stock[:3]:
            nombre = self._obtener_atributo(p, "nombre")
            stock = self._obtener_atributo(p, "stock")
            producto_id = self._obtener_atributo(p, "id")

            btn = QPushButton(f"🔴 Stock bajo: {nombre} (stock: {stock})")
            btn.setObjectName("btnAlerta")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(partial(self._ir_a_productos, producto_id))
            self.layout_alertas.addWidget(btn)

    def _ir_a_productos(self, producto_id=None):
        """
        Navega al módulo de productos, resaltando el producto por su id
        (highlight_id en App.py). Si algo falla del lado de App.py o
        producto_vista.py (fuera de nuestro control), se captura el error
        para que la app no se caiga — solo se avisa por consola.
        """
        if not callable(self.on_navigate_to_products):
            return

        try:
            self.on_navigate_to_products(producto_id)
        except TypeError:
            try:
                self.on_navigate_to_products()
            except Exception as e:
                print(f"⚠️ No se pudo navegar a productos: {e}")
        except Exception as e:
            print(f"⚠️ No se pudo navegar a productos: {e}")

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
            self.input_pago.setValue(0.0)

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
            self.input_pago.setValue(0.0)
            self._cargar_alertas()