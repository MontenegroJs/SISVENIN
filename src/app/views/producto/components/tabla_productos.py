"""
TablaProductos - Componente de tabla específica para productos
Equivalente a la tabla en productos-page.tsx de React

Características:
- Columnas específicas: Producto, Precio Venta, Stock, Precio Compra, Margen, Vencimiento, Acciones
- Stock bajo (<5) se muestra en rojo con emoji 🔴
- Vencimiento próximo (<7 días) se muestra en naranja con emoji ⚠️
- Botones de acción: Editar (✏️) y Eliminar (🗑️)
- Paginación integrada
- Soporte para resaltado de filas (highlight)
"""

from typing import Optional, List
from datetime import date
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, Signal, QTimer, QCoreApplication
from PySide6.QtGui import QColor, QFont

from src.app.base_layout import BaseLayout
from src.app.models.producto_modelo import ProductoModelo


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
        self._table.setColumnCount(7)
        self._table.setHorizontalHeaderLabels([
            "Producto", "Precio Venta", "Stock", "Precio Compra", "Margen", "Vencimiento", "Acciones"
        ])
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.setSelectionMode(QTableWidget.SingleSelection)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)
        self._table.setShowGrid(False)
        
        # Configurar ancho de columnas (como en React)
        header = self._table.horizontalHeader()
        
        # Columna Producto: ocupa el espacio restante
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        
        # Las demás columnas: se ajustan al contenido
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Precio Venta
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Stock
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Precio Compra
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Margen
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Vencimiento
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Acciones
        
        # Asegurar que la última columna no se estire
        header.setStretchLastSection(False)
        
        # Estilo de la tabla (como en React)
        self._table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {BaseLayout.COLOR_TARJETA};
                border: 1px solid {BaseLayout.COLOR_BORDE};
                border-radius: {BaseLayout.BORDER_RADIUS_TARJETA}px;
                font-size: 14px;
                alternate-background-color: {BaseLayout.COLOR_HOVER_FILA};
                selection-background-color: {BaseLayout.COLOR_HOVER_FILA};
            }}
            QTableWidget::item {{
                padding: 12px 16px;
                border-bottom: 1px solid {BaseLayout.COLOR_BORDE};
            }}
            QTableWidget::item:selected {{
                background-color: {BaseLayout.COLOR_HOVER_FILA};
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
            }}
            QHeaderView::section {{
                background-color: {BaseLayout.COLOR_FONDO_VENTANA};
                padding: 12px 16px;
                border: none;
                border-bottom: 1px solid {BaseLayout.COLOR_BORDE};
                font-size: 13px;
                font-weight: 600;
                color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};
            }}
        """)
        
        layout.addWidget(self._table)
        
        # ==================== PAGINACIÓN ====================
        pag_widget = QWidget()
        pag_layout = QHBoxLayout(pag_widget)
        pag_layout.setContentsMargins(0, 12, 0, 0)
        
        self._info_label = QLabel("")
        self._info_label.setStyleSheet(f"font-size: 13px; color: {BaseLayout.COLOR_TEXTO_SECUNDARIO};")
        pag_layout.addWidget(self._info_label)
        pag_layout.addStretch()
        
        # Botones de paginación
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
        
        self._page_label = QLabel("")
        self._page_label.setStyleSheet(f"""
            font-size: 13px;
            color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
            min-width: 70px;
            text-align: center;
        """)
        self._page_label.setAlignment(Qt.AlignCenter)
        
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
        
        layout.addWidget(pag_widget)
        
        # Conectar señal de selección
        self._table.itemSelectionChanged.connect(self._on_selection_changed)
    
    def _clear_table_completely(self):
        """Limpia completamente la tabla"""
        # Desconectar temporalmente la señal para evitar efectos secundarios
        self._table.blockSignals(True)
        
        # Limpiar items
        self._table.clearContents()
        
        # Eliminar cell widgets
        for row in range(self._table.rowCount()):
            self._table.removeCellWidget(row, 6)
        
        # Resetear número de filas
        self._table.setRowCount(0)
        
        # Forzar actualización
        self._table.viewport().update()
        self._table.update()
        
        self._table.blockSignals(False)
    
    def _populate_table(self):
        """Llena la tabla con los productos de la página actual"""
        # Limpiar tabla completamente
        self._clear_table_completely()
        
        if not self._productos:
            self._update_pagination_info()
            # Forzar actualización de la vista
            self._table.viewport().update()
            return
        
        total_pages = max(1, (len(self._productos) + self._items_per_page - 1) // self._items_per_page)
        if self._current_page > total_pages:
            self._current_page = total_pages
        
        start = (self._current_page - 1) * self._items_per_page
        end = min(start + self._items_per_page, len(self._productos))
        page_productos = self._productos[start:end]
        
        self._table.blockSignals(True)
        self._table.setRowCount(len(page_productos))
        
        # Configurar altura de filas
        self._table.verticalHeader().setDefaultSectionSize(60)
        
        for row, p in enumerate(page_productos):
            # Nombre
            nombre_item = QTableWidgetItem(p.nombre)
            nombre_item.setFlags(nombre_item.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 0, nombre_item)
            
            # Precio Venta (verde, negrita, derecha)
            item_precio = QTableWidgetItem(f"S/ {p.precio_venta:.2f}")
            item_precio.setForeground(QColor(BaseLayout.COLOR_PRIMARIO))
            item_precio.setFont(QFont("DM Sans", 14, QFont.Bold))
            item_precio.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_precio.setFlags(item_precio.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 1, item_precio)
            
            # Stock (con 🔴 si es bajo)
            if p.stock < 5:
                stock_text = f"{p.stock} 🔴"
                stock_item = QTableWidgetItem(stock_text)
                stock_item.setForeground(QColor(self._COLOR_STOCK_BAJO))
                stock_item.setFont(QFont("DM Sans", 14, QFont.Bold))
            else:
                stock_item = QTableWidgetItem(str(p.stock))
                stock_item.setFont(QFont("DM Sans", 14))
            stock_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            stock_item.setFlags(stock_item.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 2, stock_item)
            
            # Precio Compra
            item_compra = QTableWidgetItem(f"S/ {p.precio_compra:.2f}")
            item_compra.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_compra.setFlags(item_compra.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 3, item_compra)
            
            # Margen
            item_margen = QTableWidgetItem(f"{p.margen:.0f}%")
            item_margen.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            item_margen.setFlags(item_margen.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 4, item_margen)
            
            # Vencimiento (con ⚠️ si es próximo)
            if p.vencimiento:
                vence_str = p.vencimiento.strftime("%d/%m/%Y")
                hoy = date.today()
                dias_restantes = (p.vencimiento - hoy).days
                
                if 0 <= dias_restantes <= 7:
                    vence_item = QTableWidgetItem(f"⚠️ {vence_str}")
                    vence_item.setForeground(QColor(self._COLOR_VENCE_PROXIMO))
                    vence_item.setFont(QFont("DM Sans", 14, QFont.Bold))
                else:
                    vence_item = QTableWidgetItem(vence_str)
                    vence_item.setFont(QFont("DM Sans", 14))
                vence_item.setFlags(vence_item.flags() & ~Qt.ItemIsEditable)
                self._table.setItem(row, 5, vence_item)
            else:
                item = QTableWidgetItem("—")
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self._table.setItem(row, 5, item)
            
            # Botones de acción
            acciones_widget = self._create_acciones_widget(p)
            self._table.setCellWidget(row, 6, acciones_widget)
        
        self._table.blockSignals(False)
        
        # FORZAR ACTUALIZACIÓN COMPLETA
        self._table.resizeColumnsToContents()
        self._table.resizeRowsToContents()
        self._table.viewport().update()
        self._table.update()
        
        # Forzar un repaint del widget padre también
        if self.parent():
            self.parent().update()
        
        self._update_pagination_info()
    
    def _create_acciones_widget(self, producto: ProductoModelo) -> QWidget:
        """Crea el widget con los botones de acción"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignCenter)
        
        # Botón editar
        btn_editar = QPushButton("✏️")
        btn_editar.setFixedSize(36, 36)
        btn_editar.setCursor(Qt.PointingHandCursor)
        btn_editar.setToolTip("Editar producto")
        btn_editar.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                font-size: 14px;
                color: #757575;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
                color: #212121;
            }
            QPushButton:pressed {
                background-color: #E0E0E0;
            }
        """)
        btn_editar.clicked.connect(lambda: self.editarClicked.emit(producto))
        layout.addWidget(btn_editar)
        
        # Botón eliminar
        btn_eliminar = QPushButton("🗑️")
        btn_eliminar.setFixedSize(36, 36)
        btn_eliminar.setCursor(Qt.PointingHandCursor)
        btn_eliminar.setToolTip("Eliminar producto")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                font-size: 14px;
                color: #757575;
            }
            QPushButton:hover {
                background-color: #FFEBEE;
                color: #D32F2F;
            }
            QPushButton:pressed {
                background-color: #FFCDD2;
            }
        """)
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
        """Resalta un producto en la tabla"""
        for i, p in enumerate(self._productos):
            if p.id == producto_id:
                page = i // self._items_per_page + 1
                if page != self._current_page:
                    self._current_page = page
                self._populate_table()
                
                # Resaltar visualmente la fila
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
        self._clear_table_completely()
        self._update_pagination_info()


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
        
        header = self._table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        
        self._table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {BaseLayout.COLOR_BORDE};
                border-radius: {BaseLayout.BORDER_RADIUS_TARJETA}px;
                font-size: 14px;
                alternate-background-color: {BaseLayout.COLOR_HOVER_FILA};
            }}
            QTableWidget::item {{
                padding: 10px 12px;
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
        
        for row, p in enumerate(productos):
            # Producto
            nombre_item = QTableWidgetItem(p.nombre)
            nombre_item.setFlags(nombre_item.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 0, nombre_item)
            
            # Precio Venta
            item_precio = QTableWidgetItem(f"S/ {p.precio_venta:.2f}")
            item_precio.setForeground(QColor(BaseLayout.COLOR_PRIMARIO))
            item_precio.setFont(QFont("DM Sans", 14, QFont.Bold))
            item_precio.setFlags(item_precio.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 1, item_precio)
            
            # Stock (con 🔴 si es bajo)
            if p.stock < 5:
                stock_text = f"{p.stock} 🔴"
                stock_item = QTableWidgetItem(stock_text)
                stock_item.setForeground(QColor(BaseLayout.COLOR_PELIGRO))
                stock_item.setFont(QFont("DM Sans", 14, QFont.Bold))
            else:
                stock_item = QTableWidgetItem(str(p.stock))
                stock_item.setFont(QFont("DM Sans", 14))
            stock_item.setFlags(stock_item.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 2, stock_item)
            
            # Precio Compra
            item_compra = QTableWidgetItem(f"S/ {p.precio_compra:.2f}")
            item_compra.setFlags(item_compra.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 3, item_compra)
            
            # Margen
            item_margen = QTableWidgetItem(f"{p.margen:.0f}%")
            item_margen.setFlags(item_margen.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 4, item_margen)
            
            # Vencimiento
            if p.vencimiento:
                vence_str = p.vencimiento.strftime("%d/%m/%Y")
                self._table.setItem(row, 5, QTableWidgetItem(vence_str))
            else:
                item = QTableWidgetItem("—")
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self._table.setItem(row, 5, item)
        
        self._table.resizeRowsToContents()
        self._table.viewport().update()
    
    def clear(self):
        """Limpia la tabla"""
        self._table.setRowCount(0)
        self._productos = []