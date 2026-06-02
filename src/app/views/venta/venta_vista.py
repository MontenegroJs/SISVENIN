"""
Módulo Venta - Vista (POS)
Sprint 2 - HU-01, HU-02, HU-09: Búsqueda de productos
"""

from typing import Optional, List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
    QListWidgetItem, QLabel, QSplitter
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from src.app.shared.components.sis_input import SisInput
from src.app.controllers.producto_controlador import ProductoControlador
from src.app.models.producto_modelo import ProductoModelo


class PanelBusqueda(QWidget):
    """
    Panel de búsqueda de productos para el POS.
    Permite buscar por nombre o código de barras.
    """
    
    producto_seleccionado = Signal(ProductoModelo)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.controlador = ProductoControlador()
        self.timer_busqueda = QTimer()
        self.timer_busqueda.setSingleShot(True)
        self.timer_busqueda.timeout.connect(self._ejecutar_busqueda)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        titulo = QLabel("🔍 Buscar Producto")
        titulo.setFont(QFont("Roboto", 18, QFont.DemiBold))
        titulo.setStyleSheet("color: #212121; margin-bottom: 8px;")
        layout.addWidget(titulo)
        
        self.campo_busqueda = SisInput(placeholder="Buscar por nombre o código de barras...")
        self.campo_busqueda.textChanged.connect(self._on_texto_cambiado)
        layout.addWidget(self.campo_busqueda)
        
        self.lista_resultados = QListWidget()
        self.lista_resultados.setStyleSheet("""
            QListWidget {
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                padding: 8px;
                background-color: white;
                min-height: 300px;
            }
            QListWidget::item {
                padding: 12px;
                border-radius: 8px;
                margin: 2px 0;
            }
            QListWidget::item:hover {
                background-color: #F5F5F5;
            }
            QListWidget::item:selected {
                background-color: #E8F5E9;
                border-left: 3px solid #2E7D32;
            }
        """)
        self.lista_resultados.itemClicked.connect(self._on_producto_seleccionado)
        layout.addWidget(self.lista_resultados)
        
        self.estado_label = QLabel("💡 Ingrese un término para buscar")
        self.estado_label.setFont(QFont("Roboto", 12))
        self.estado_label.setStyleSheet("color: #757575;")
        self.estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.estado_label)
    
    def _on_texto_cambiado(self, texto: str) -> None:
        self.timer_busqueda.start(300)  # Esperar 300ms después de la última tecla
    
    def _ejecutar_busqueda(self) -> None:
        termino = self.campo_busqueda.text().strip()
        
        if not termino:
            self.lista_resultados.clear()
            self.estado_label.setText("💡 Ingrese un término para buscar")
            self.estado_label.setStyleSheet("color: #757575;")
            return
        
        self.estado_label.setText("⏳ Buscando...")
        self.estado_label.setStyleSheet("color: #2E7D32;")
        
        productos = self.controlador.buscar_rapido_pos(termino, limite=10)
        self._actualizar_lista(productos)
    
    def _actualizar_lista(self, productos: List[ProductoModelo]) -> None:
        self.lista_resultados.clear()
        
        if not productos:
            self.estado_label.setText("❌ No se encontraron productos")
            self.estado_label.setStyleSheet("color: #D32F2F;")
            return
        
        self.estado_label.setText(f"📦 Se encontraron {len(productos)} productos")
        self.estado_label.setStyleSheet("color: #757575;")
        
        for producto in productos:
            stock_texto = f"Stock: {producto.stock}"
            if producto.stock <= 0:
                stock_texto = f"⚠️ SIN STOCK"
            elif producto.stock < 5:
                stock_texto = f"⚠️ {stock_texto}"
            
            item_text = f"{producto.nombre}\n💰 S/ {producto.precio_venta:.2f}  |  📦 {stock_texto}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, producto)
            
            if producto.stock <= 0:
                item.setForeground(Qt.GlobalColor.gray)
            elif producto.stock < 5:
                item.setForeground(Qt.GlobalColor.darkRed)
            
            self.lista_resultados.addItem(item)
    
    def _on_producto_seleccionado(self, item: QListWidgetItem) -> None:
        producto = item.data(Qt.ItemDataRole.UserRole)
        if producto and producto.stock > 0:
            self.producto_seleccionado.emit(producto)
            self.campo_busqueda.clear()
            self.lista_resultados.clear()
            self.estado_label.setText("✅ Producto agregado al carrito")
            self.estado_label.setStyleSheet("color: #2E7D32;")
            QTimer.singleShot(2000, self._resetear_estado)
        elif producto and producto.stock <= 0:
            self.estado_label.setText("❌ Producto sin stock disponible")
            self.estado_label.setStyleSheet("color: #D32F2F;")
            QTimer.singleShot(2000, self._resetear_estado)
    
    def _resetear_estado(self) -> None:
        if not self.campo_busqueda.text().strip():
            self.estado_label.setText("💡 Ingrese un término para buscar")
            self.estado_label.setStyleSheet("color: #757575;")
    
    def limpiar_busqueda(self) -> None:
        """Limpia el campo de búsqueda y los resultados."""
        self.campo_busqueda.clear()
        self.lista_resultados.clear()
        self.estado_label.setText("💡 Ingrese un término para buscar")
        self.estado_label.setStyleSheet("color: #757575;")


class VentaVista(QWidget):
    """Vista principal del Punto de Venta (POS)."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.carrito = []
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(24, 24, 24, 24)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo: Búsqueda (40%)
        self.panel_busqueda = PanelBusqueda()
        self.panel_busqueda.producto_seleccionado.connect(self.agregar_al_carrito)
        splitter.addWidget(self.panel_busqueda)
        
        # Panel derecho: Carrito (60%) - Placeholder
        self.panel_carrito = self._crear_panel_carrito()
        splitter.addWidget(self.panel_carrito)
        
        splitter.setSizes([400, 600])
        layout.addWidget(splitter)
    
    def _crear_panel_carrito(self):
        """Crea el panel del carrito de compras (placeholder por ahora)."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        titulo = QLabel("🛒 Carrito de Compras")
        titulo.setFont(QFont("Roboto", 18, QFont.DemiBold))
        titulo.setStyleSheet("color: #212121; margin-bottom: 16px;")
        layout.addWidget(titulo)
        
        # Placeholder para productos
        placeholder = QLabel("No hay productos en el carrito\n\nSeleccione un producto de la lista para agregar")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #757575; font-size: 14px; padding: 40px;")
        placeholder.setWordWrap(True)
        layout.addWidget(placeholder)
        
        layout.addStretch()
        return widget
    
    def agregar_al_carrito(self, producto: ProductoModelo):
        """Agrega un producto al carrito de compras."""
        self.carrito.append(producto)
        print(f"✅ Producto agregado: {producto.nombre} - S/ {producto.precio_venta:.2f}")
        print(f"📦 Total en carrito: {len(self.carrito)} productos")
        
        # Actualizar el panel del carrito (mostrar conteo)
        self._actualizar_carrito()
    
    def _actualizar_carrito(self):
        """Actualiza la visualización del carrito."""
        total = sum(p.precio_venta for p in self.carrito)
        from PySide6.QtWidgets import QVBoxLayout
        
        # Limpiar y recrear el panel del carrito
        old_widget = self.panel_carrito
        self.panel_carrito = self._crear_panel_carrito_con_items()
        
        # Reemplazar en el layout padre
        parent_layout = self.layout()
        if parent_layout:
            # Encontrar el splitter
            splitter = parent_layout.itemAt(0).widget()
            if splitter:
                splitter.replaceWidget(1, self.panel_carrito)
                old_widget.deleteLater()
    
    def _crear_panel_carrito_con_items(self):
        """Crea el panel del carrito con los productos actuales."""
        from PySide6.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QFrame
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        titulo = QLabel(f"🛒 Carrito ({len(self.carrito)} productos)")
        titulo.setFont(QFont("Roboto", 18, QFont.DemiBold))
        titulo.setStyleSheet("color: #212121; margin-bottom: 16px;")
        layout.addWidget(titulo)
        
        # Scroll area para los productos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(8)
        
        for producto in self.carrito:
            item = QLabel(f"• {producto.nombre} - S/ {producto.precio_venta:.2f}")
            item.setStyleSheet("padding: 8px; background-color: #F5F5F5; border-radius: 8px;")
            scroll_layout.addWidget(item)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        total = sum(p.precio_venta for p in self.carrito)
        total_label = QLabel(f"💰 TOTAL: S/ {total:.2f}")
        total_label.setFont(QFont("Roboto", 24, QFont.Bold))
        total_label.setStyleSheet(f"color: #2E7D32; padding: 16px; background-color: #E8F5E9; border-radius: 12px; margin-top: 16px;")
        total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(total_label)
        
        return widget