"""
TablaProductos - Componente de tabla específica para productos
Equivalente a la tabla en productos-page.tsx de React

Características:
- Columnas específicas: Producto, Precio Venta, Stock, Precio Compra, Margen, Vencimiento, Acciones
- Stock bajo (<5) se muestra en rojo con emoji 🔴
- Vencimiento próximo (<7 días) se muestra en naranja con emoji ⚠️
- Botones de acción: Editar (✏️) y Eliminar (🗑️) con estilo SisIconButton
- Paginación integrada
- Soporte para resaltado de filas (highlight)
- CONTROL TOTAL: Anchos de columnas, tamaños de fuente, estilos
"""

from typing import Optional, List
from datetime import date
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QFont

from src.app.base_layout import BaseLayout
from src.app.models.producto_modelo import ProductoModelo
from src.app.shared.components.sis_button import SisIconButton


class TablaProductos(QWidget):
    """
    Tabla específica para la gestión de productos.
    Sigue el diseño del Prompt 0 de Figma (igual al React).
    """
    
    # Señales
    editarClicked = Signal(ProductoModelo)
    eliminarClicked = Signal(ProductoModelo)
    productoSeleccionado = Signal(ProductoModelo)
    
    # Constantes
    _COLOR_STOCK_BAJO = BaseLayout.COLOR_PELIGRO
    _COLOR_VENCE_PROXIMO = "#FF9800"
    _COLOR_HIGHLIGHT = "#FFF9C4"
    
    # 🔧 CONFIGURACIÓN DE COLUMNAS (como en React)
    # Formato: (título, ancho, alineación, fuente_peso)
    COLUMNAS = [
        {"titulo": "Producto",        "ancho": 300, "align": "left",   "peso": "normal"},
        {"titulo": "Precio Venta",    "ancho": 120, "align": "right",  "peso": "bold"},
        {"titulo": "Stock",           "ancho": 100, "align": "center", "peso": "normal"},
        {"titulo": "Precio Compra",   "ancho": 120, "align": "right",  "peso": "normal"},
        {"titulo": "Margen",          "ancho": 80,  "align": "center", "peso": "normal"},
        {"titulo": "Vencimiento",     "ancho": 130, "align": "left",   "peso": "normal"},
        {"titulo": "Acciones",        "ancho": 100, "align": "center", "peso": "normal"},
    ]
    
    # 🔧 TAMAÑOS DE FUENTE
    FUENTE_TITULO_TAMANO = 13
    FUENTE_TITULO_PESO = 600
    
    FUENTE_CELDA_TAMANO = 14
    FUENTE_CELDA_BOLD_PESO = 700
    
    def __init__(
        self,
        items_per_page: int = 10,
        parent=None
    ):
        super().__init__(parent)
        
        self._productos: List[ProductoModelo] = []
        self._items_per_page = items_per_page
        self._current_page = 1
        self._highlight_id: Optional[int] = None
        self._highlight_timer: Optional[QTimer] = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de la tabla"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # ==================== TABLA ====================
        self._table = QTableWidget()
        self._table.setColumnCount(len(self.COLUMNAS))
        
        # Configurar encabezados y anchos
        for col, config in enumerate(self.COLUMNAS):
            self._table.setHorizontalHeaderItem(col, QTableWidgetItem(config["titulo"]))
            # Establecer ancho mínimo en lugar de fijo para la columna Producto
            if col == 0:  # Columna Producto
                self._table.setColumnWidth(col, config["ancho"])
            else:
                self._table.setColumnWidth(col, config["ancho"])
        
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.setSelectionMode(QTableWidget.SingleSelection)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)
        self._table.setShowGrid(False)
        
        # Configurar comportamiento del header
        header = self._table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionsMovable(False)
        
        # 🔧 CLAVE: Hacer que la columna Producto se expanda
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Producto se expande
        for col in range(1, len(self.COLUMNAS)):
            header.setSectionResizeMode(col, QHeaderView.Fixed)  # Las demás mantienen ancho fijo
        
        # ==================== ESTILO EXPLÍCITO DE LA TABLA ====================
        self._table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {BaseLayout.COLOR_TARJETA};
                border: 1px solid {BaseLayout.COLOR_BORDE};
                border-radius: {BaseLayout.BORDER_RADIUS_TARJETA}px;
                alternate-background-color: {BaseLayout.COLOR_HOVER_FILA};
                selection-background-color: {BaseLayout.COLOR_HOVER_FILA};
                outline: none;
                gridline-color: transparent;
            }}
            QTableWidget::item {{
                padding: 12px 16px;
                border-bottom: 1px solid {BaseLayout.COLOR_BORDE};
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
            }}
            QTableWidget::item:selected {{
                background-color: {BaseLayout.COLOR_HOVER_FILA};
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
            }}
            QHeaderView::section {{
                background-color: {BaseLayout.COLOR_FONDO_VENTANA};
                padding: 12px 16px;
                border: none;
                border-bottom: 2px solid {BaseLayout.COLOR_BORDE};
                font-size: {self.FUENTE_TITULO_TAMANO}px;
                font-weight: {self.FUENTE_TITULO_PESO};
                color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
            }}
        """)
        
        layout.addWidget(self._table)
        
        # ==================== PAGINACIÓN ====================
        self._setup_pagination()
        layout.addWidget(self._pagination_widget)
        
        # Conectar señal de selección
        self._table.itemSelectionChanged.connect(self._on_selection_changed)
    
    def _setup_pagination(self):
        """Configura la barra de paginación"""
        self._pagination_widget = QWidget()
        pag_layout = QHBoxLayout(self._pagination_widget)
        pag_layout.setContentsMargins(0, 12, 0, 0)
        
        self._info_label = QLabel("")
        self._info_label.setStyleSheet(f"""
            font-size: 13px;
            color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
        """)
        pag_layout.addWidget(self._info_label)
        pag_layout.addStretch()
        
        # Botón anterior
        self._btn_prev = QPushButton("‹")
        self._btn_prev.setFixedSize(32, 32)
        self._btn_prev.setCursor(Qt.PointingHandCursor)
        self._btn_prev.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                font-size: 14px;
                color: #757575;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
            QPushButton:disabled {
                opacity: 0.4;
            }
        """)
        self._btn_prev.clicked.connect(self._prev_page)
        
        # Indicador de página
        self._page_label = QLabel("")
        self._page_label.setStyleSheet(f"""
            font-size: 13px;
            color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
            min-width: 70px;
            text-align: center;
        """)
        self._page_label.setAlignment(Qt.AlignCenter)
        
        # Botón siguiente
        self._btn_next = QPushButton("›")
        self._btn_next.setFixedSize(32, 32)
        self._btn_next.setCursor(Qt.PointingHandCursor)
        self._btn_next.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                font-size: 14px;
                color: #757575;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
            QPushButton:disabled {
                opacity: 0.4;
            }
        """)
        self._btn_next.clicked.connect(self._next_page)
        
        pag_layout.addWidget(self._btn_prev)
        pag_layout.addWidget(self._page_label)
        pag_layout.addWidget(self._btn_next)
    
    def _populate_table(self):
        """Llena la tabla con los productos de la página actual"""
        # Limpiar tabla
        self._table.clearContents()
        
        if not self._productos:
            self._table.setRowCount(0)
            self._update_pagination_info()
            return
        
        total_pages = max(1, (len(self._productos) + self._items_per_page - 1) // self._items_per_page)
        if self._current_page > total_pages:
            self._current_page = total_pages
        
        start = (self._current_page - 1) * self._items_per_page
        end = min(start + self._items_per_page, len(self._productos))
        page_productos = self._productos[start:end]
        
        self._table.setRowCount(len(page_productos))
        
        # Configurar altura de filas
        self._table.verticalHeader().setDefaultSectionSize(60)
        
        # Crear fuentes
        regular_font = QFont()
        regular_font.setPointSize(self.FUENTE_CELDA_TAMANO)
        
        bold_font = QFont()
        bold_font.setPointSize(self.FUENTE_CELDA_TAMANO)
        bold_font.setBold(True)
        
        for row, p in enumerate(page_productos):
            # Columna 0: Nombre
            item = QTableWidgetItem(p.nombre)
            item.setFont(regular_font)
            self._table.setItem(row, 0, item)
            
            # Columna 1: Precio Venta (verde, negrita)
            item = QTableWidgetItem(f"S/ {p.precio_venta:.2f}")
            item.setData(Qt.ForegroundRole, QColor(BaseLayout.COLOR_PRIMARIO))
            item.setFont(bold_font)
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self._table.setItem(row, 1, item)
            
            # Columna 2: Stock
            if p.stock < 5:
                item = QTableWidgetItem(f"{p.stock} 🔴")
                item.setForeground(QColor(self._COLOR_STOCK_BAJO))
                item.setFont(bold_font)
            else:
                item = QTableWidgetItem(str(p.stock))
                item.setFont(regular_font)
            item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self._table.setItem(row, 2, item)
            
            # Columna 3: Precio Compra
            item = QTableWidgetItem(f"S/ {p.precio_compra:.2f}")
            item.setFont(regular_font)
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self._table.setItem(row, 3, item)
            
            # Columna 4: Margen
            item = QTableWidgetItem(f"{p.margen:.0f}%")
            item.setFont(regular_font)
            item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self._table.setItem(row, 4, item)
            
            # Columna 5: Vencimiento
            if p.vencimiento:
                vence_str = p.vencimiento.strftime("%d/%m/%Y")
                hoy = date.today()
                dias_restantes = (p.vencimiento - hoy).days
                
                if 0 <= dias_restantes <= 7:
                    item = QTableWidgetItem(f"⚠️ {vence_str}")
                    item.setForeground(QColor(self._COLOR_VENCE_PROXIMO))
                    item.setFont(bold_font)
                else:
                    item = QTableWidgetItem(vence_str)
                    item.setFont(regular_font)
                self._table.setItem(row, 5, item)
            else:
                item = QTableWidgetItem("—")
                item.setFont(regular_font)
                self._table.setItem(row, 5, item)
            
            # Columna 6: Acciones (botones)
            acciones_widget = self._create_acciones_widget(p)
            self._table.setCellWidget(row, 6, acciones_widget)
        
        self._table.resizeRowsToContents()
        self._update_pagination_info()
    
    def _create_acciones_widget(self, producto: ProductoModelo) -> QWidget:
        """Crea el widget con los botones de acción usando SisIconButton"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignCenter)
        
        # Botón editar (✏️)
        btn_editar = SisIconButton("✏️", tooltip="Editar producto")
        btn_editar.clicked.connect(lambda: self.editarClicked.emit(producto))
        layout.addWidget(btn_editar)
        
        # Botón eliminar (🗑️)
        btn_eliminar = SisIconButton("🗑️", tooltip="Eliminar producto")
        btn_eliminar.clicked.connect(lambda: self.eliminarClicked.emit(producto))
        layout.addWidget(btn_eliminar)
        
        return widget
    
    def _update_pagination_info(self):
        """Actualiza la información de paginación"""
        if not self._productos:
            self._info_label.setText("Mostrando 0-0 de 0 productos")
            self._page_label.setText("Página 0 de 0")
            self._btn_prev.setEnabled(False)
            self._btn_next.setEnabled(False)
            return
        
        total_pages = max(1, (len(self._productos) + self._items_per_page - 1) // self._items_per_page)
        start = (self._current_page - 1) * self._items_per_page + 1
        end = min(self._current_page * self._items_per_page, len(self._productos))
        
        self._info_label.setText(f"Mostrando {start}–{end} de {len(self._productos)} productos")
        self._page_label.setText(f"Página {self._current_page} de {total_pages}")
        self._btn_prev.setEnabled(self._current_page > 1)
        self._btn_next.setEnabled(self._current_page < total_pages)
    
    def _prev_page(self):
        """Página anterior"""
        if self._current_page > 1:
            self._current_page -= 1
            self._populate_table()
    
    def _next_page(self):
        """Página siguiente"""
        total_pages = max(1, (len(self._productos) + self._items_per_page - 1) // self._items_per_page)
        if self._current_page < total_pages:
            self._current_page += 1
            self._populate_table()
    
    def _on_selection_changed(self):
        """Maneja el cambio de selección"""
        selected_rows = self._table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            start = (self._current_page - 1) * self._items_per_page
            index = start + row
            if index < len(self._productos):
                self.productoSeleccionado.emit(self._productos[index])
    
    # ==================== MÉTODOS PÚBLICOS ====================
    
    def set_productos(self, productos: List[ProductoModelo]):
        """Establece la lista de productos a mostrar"""
        self._productos = productos
        self._current_page = 1
        self._populate_table()
    
    def get_productos(self) -> List[ProductoModelo]:
        """Retorna la lista de productos actual"""
        return self._productos
    
    def resaltar_producto(self, producto_id: int):
        """Resalta un producto en la tabla (fondo amarillo temporal)"""
        for i, p in enumerate(self._productos):
            if p.id == producto_id:
                page = i // self._items_per_page + 1
                if page != self._current_page:
                    self._current_page = page
                self._populate_table()
                
                row_in_page = i - (self._current_page - 1) * self._items_per_page
                if 0 <= row_in_page < self._table.rowCount():
                    for col in range(self._table.columnCount()):
                        item = self._table.item(row_in_page, col)
                        if item:
                            item.setBackground(QColor(self._COLOR_HIGHLIGHT))
                    # También resaltar el cell widget
                    cell_widget = self._table.cellWidget(row_in_page, 6)
                    if cell_widget:
                        cell_widget.setStyleSheet(f"background-color: {self._COLOR_HIGHLIGHT};")
                
                # Temporizador para limpiar resaltado
                if self._highlight_timer:
                    self._highlight_timer.stop()
                self._highlight_timer = QTimer()
                self._highlight_timer.setSingleShot(True)
                self._highlight_timer.timeout.connect(self._clear_highlight)
                self._highlight_timer.start(3000)
                break
    
    def _clear_highlight(self):
        """Limpia el resaltado de la tabla"""
        for row in range(self._table.rowCount()):
            for col in range(self._table.columnCount()):
                item = self._table.item(row, col)
                if item:
                    item.setBackground(QColor())
            # Limpiar resaltado del cell widget
            cell_widget = self._table.cellWidget(row, 6)
            if cell_widget:
                cell_widget.setStyleSheet("")
    
    def refresh(self):
        """Refresca la tabla"""
        self._populate_table()
    
    def clear(self):
        """Limpia la tabla"""
        self._productos = []
        self._current_page = 1
        self._table.clearContents()
        self._table.setRowCount(0)
        self._update_pagination_info()
    
    # ==================== MÉTODOS DE CONFIGURACIÓN ====================
    
    def set_column_width(self, column: int, width: int):
        """Establece el ancho de una columna específica"""
        if 0 <= column < len(self.COLUMNAS):
            self._table.setColumnWidth(column, width)
            self.COLUMNAS[column]["ancho"] = width
    
    def get_column_width(self, column: int) -> int:
        """Obtiene el ancho de una columna específica"""
        if 0 <= column < len(self.COLUMNAS):
            return self._table.columnWidth(column)
        return 0
    
    def set_font_size(self, size: int):
        """Establece el tamaño de fuente de las celdas"""
        self.FUENTE_CELDA_TAMANO = size
        self.refresh()
    
    def set_header_font_size(self, size: int):
        """Establece el tamaño de fuente de los encabezados"""
        self.FUENTE_TITULO_TAMANO = size
        self._table.setStyleSheet(self._table.styleSheet())  # Recargar estilo


class TablaProductosSimple(QWidget):
    """
    Versión simple de la tabla de productos (sin paginación).
    Útil para reportes o vistas rápidas.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._productos: List[ProductoModelo] = []
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self._table = QTableWidget()
        self._table.setColumnCount(6)
        self._table.setHorizontalHeaderLabels([
            "Producto", "Precio Venta", "Stock", "Precio Compra", "Margen", "Vencimiento"
        ])
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)
        
        # Configurar anchos de columnas
        header = self._table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for col in range(1, 6):
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
        
        # Estilo explícito para la tabla simple
        self._table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {BaseLayout.COLOR_TARJETA};
                border: 1px solid {BaseLayout.COLOR_BORDE};
                border-radius: {BaseLayout.BORDER_RADIUS_TARJETA}px;
                font-size: 14px;
                alternate-background-color: {BaseLayout.COLOR_HOVER_FILA};
            }}
            QTableWidget::item {{
                padding: 10px 12px;
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
            }}
            QHeaderView::section {{
                background-color: {BaseLayout.COLOR_FONDO_VENTANA};
                padding: 10px 12px;
                border: none;
                border-bottom: 1px solid {BaseLayout.COLOR_BORDE};
                font-weight: 600;
                color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
            }}
        """)
        
        layout.addWidget(self._table)
    
    def set_productos(self, productos: List[ProductoModelo]):
        """Establece los productos en la tabla"""
        self._productos = productos
        self._table.setRowCount(len(productos))
        
        bold_font = QFont()
        bold_font.setPointSize(14)
        bold_font.setBold(True)
        
        for row, p in enumerate(productos):
            # Producto
            self._table.setItem(row, 0, QTableWidgetItem(p.nombre))
            
            # Precio Venta
            item = QTableWidgetItem(f"S/ {p.precio_venta:.2f}")
            item.setForeground(QColor(BaseLayout.COLOR_PRIMARIO))
            item.setFont(bold_font)
            self._table.setItem(row, 1, item)
            
            # Stock
            if p.stock < 5:
                item = QTableWidgetItem(f"{p.stock} 🔴")
                item.setForeground(QColor(BaseLayout.COLOR_PELIGRO))
                item.setFont(bold_font)
            else:
                item = QTableWidgetItem(str(p.stock))
            self._table.setItem(row, 2, item)
            
            # Precio Compra
            self._table.setItem(row, 3, QTableWidgetItem(f"S/ {p.precio_compra:.2f}"))
            
            # Margen
            self._table.setItem(row, 4, QTableWidgetItem(f"{p.margen:.0f}%"))
            
            # Vencimiento
            if p.vencimiento:
                self._table.setItem(row, 5, QTableWidgetItem(p.vencimiento.strftime("%d/%m/%Y")))
            else:
                self._table.setItem(row, 5, QTableWidgetItem("—"))
        
        self._table.resizeRowsToContents()
    
    def clear(self):
        """Limpia la tabla"""
        self._table.setRowCount(0)
        self._productos = []