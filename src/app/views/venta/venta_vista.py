"""
Módulo Venta - Vista (POS)
Sprint 2 - HU-01, HU-02, HU-09: Búsqueda de productos

"""
from typing import Optional, List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
    QListWidgetItem, QLabel, QSplitter, QPushButton,
    QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from src.app.shared.components.sis_input import SisInput
from src.app.controllers.producto_controlador import ProductoControlador
from src.app.models.producto_modelo import ProductoModelo
# PARA EL TICKET
from src.app.views.venta.components.ticket_modal import TicketModal

class PanelBusqueda(QWidget):
    """
    Panel de búsqueda de productos para el POS.
    Formato: "Nombre – S/ precio (stock: X)"
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
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Título
        titulo = QLabel("🔍 Buscar Producto")
        titulo.setFont(QFont("Roboto", 18, QFont.DemiBold))
        titulo.setStyleSheet("color: #212121; margin-bottom: 8px;")
        layout.addWidget(titulo)
        
        # Campo de búsqueda
        self.campo_busqueda = SisInput(placeholder="Buscar por nombre o código de barras...")
        self.campo_busqueda.textChanged.connect(self._on_texto_cambiado)
        layout.addWidget(self.campo_busqueda)
        
        # Lista de resultados
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
                font-size: 14px;
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
        
        # Estado
        self.estado_label = QLabel("💡 Ingrese un término para buscar")
        self.estado_label.setFont(QFont("Roboto", 12))
        self.estado_label.setStyleSheet("color: #757575;")
        self.estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.estado_label)
    
    def _on_texto_cambiado(self, texto: str) -> None:
        self.timer_busqueda.start(300)
    
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
        
        self.estado_label.setText(f"📦 {len(productos)} productos encontrados")
        self.estado_label.setStyleSheet("color: #2E7D32;")
        
        for producto in productos:
            # Formato: "Nombre – S/ precio (stock: X)"
            if producto.stock <= 0:
                stock_texto = f"stock: {producto.stock} - SIN STOCK"
                color = "#9E9E9E"
            elif producto.stock < 5:
                stock_texto = f"stock: {producto.stock} ⚠️"
                color = "#D32F2F"
            else:
                stock_texto = f"stock: {producto.stock}"
                color = "#212121"
            
            item_text = f"{producto.nombre} – S/ {producto.precio_venta:.2f} ({stock_texto})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, producto)
            item.setForeground(Qt.GlobalColor.black if color == "#212121" else self._color_from_hex(color))
            self.lista_resultados.addItem(item)
    
    def _color_from_hex(self, hex_color: str):
        """Convierte hex a QColor"""
        from PySide6.QtGui import QColor
        hex_color = hex_color.lstrip('#')
        return QColor(int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))
    
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


class PanelAlertasStock(QWidget):
    """Panel de alertas de stock bajo (lado izquierdo, debajo de búsqueda)"""
    
    producto_clickeado = Signal(int)  # Emite el ID del producto
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.controlador = ProductoControlador()
        self._setup_ui()
        self._cargar_alertas()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 16, 0, 0)
        
        # Título
        titulo = QLabel("⚠️ Alertas rápidas")
        titulo.setFont(QFont("Roboto", 14, QFont.DemiBold))
        titulo.setStyleSheet("color: #D32F2F; margin-top: 8px;")
        layout.addWidget(titulo)
        
        # Lista de alertas
        self.lista_alertas = QListWidget()
        self.lista_alertas.setMaximumHeight(120)
        self.lista_alertas.setStyleSheet("""
            QListWidget {
                border: 1px solid #FFEBEE;
                border-radius: 8px;
                padding: 4px;
                background-color: #FFEBEE;
            }
            QListWidget::item {
                padding: 6px;
                border-radius: 4px;
                color: #D32F2F;
                font-size: 12px;
            }
            QListWidget::item:hover {
                background-color: #FFCDD2;
            }
        """)
        self.lista_alertas.itemClicked.connect(self._on_alerta_clickeada)
        layout.addWidget(self.lista_alertas)
    
    def _cargar_alertas(self):
        """Carga los productos con stock bajo (<5)"""
        productos = self.controlador.obtener_productos_stock_bajo(limite=5)
        self.lista_alertas.clear()
        
        if not productos:
            item = QListWidgetItem("✅ No hay productos con stock bajo")
            item.setForeground(Qt.GlobalColor.darkGreen)
            self.lista_alertas.addItem(item)
        else:
            for producto in productos:
                item_text = f"⚠️ Stock bajo: {producto.nombre} (stock: {producto.stock})"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, producto.id)
                self.lista_alertas.addItem(item)
    
    def _on_alerta_clickeada(self, item: QListWidgetItem):
        producto_id = item.data(Qt.ItemDataRole.UserRole)
        if producto_id:
            self.producto_clickeado.emit(producto_id)
    
    def refresh(self):
        """Refresca las alertas"""
        self._cargar_alertas()


class VentaVista(QWidget):
    """Vista principal del Punto de Venta (POS) - Basado en modelo Figma"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.carrito: List[ProductoModelo] = []
        self.controlador = ProductoControlador()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(24, 24, 24, 24)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # ========== PANEL IZQUIERDO (40%) ==========
        panel_izquierdo = QWidget()
        left_layout = QVBoxLayout(panel_izquierdo)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # Búsqueda
        self.panel_busqueda = PanelBusqueda()
        self.panel_busqueda.producto_seleccionado.connect(self.agregar_al_carrito)
        left_layout.addWidget(self.panel_busqueda)
        
        # Alertas de stock
        self.panel_alertas = PanelAlertasStock()
        self.panel_alertas.producto_clickeado.connect(self._ir_a_producto)
        left_layout.addWidget(self.panel_alertas)
        
        left_layout.addStretch()
        
        # ========== PANEL DERECHO (60%) ==========
        panel_derecho = QWidget()
        right_layout = QVBoxLayout(panel_derecho)
        right_layout.setSpacing(16)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Título del carrito
        self.carrito_titulo = QLabel("🛒 Carrito (0 productos)")
        self.carrito_titulo.setFont(QFont("Roboto", 18, QFont.DemiBold))
        self.carrito_titulo.setStyleSheet("color: #212121;")
        right_layout.addWidget(self.carrito_titulo)
        
        # Lista del carrito (scroll)
        scroll_carrito = QScrollArea()
        scroll_carrito.setWidgetResizable(True)
        scroll_carrito.setFrameShape(QFrame.NoFrame)
        scroll_carrito.setStyleSheet("background-color: transparent; border: none;")
        
        self.carrito_contenido = QWidget()
        self.carrito_layout = QVBoxLayout(self.carrito_contenido)
        self.carrito_layout.setSpacing(8)
        self.carrito_layout.setContentsMargins(0, 0, 0, 0)
        self.carrito_layout.addStretch()
        
        scroll_carrito.setWidget(self.carrito_contenido)
        right_layout.addWidget(scroll_carrito, 1)
        
        # TOTAL
        self.total_label = QLabel("TOTAL: S/ 0.00")
        self.total_label.setFont(QFont("Roboto", 28, QFont.Bold))
        self.total_label.setStyleSheet("color: #2E7D32; padding: 16px; background-color: #E8F5E9; border-radius: 12px;")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_layout.addWidget(self.total_label)
        
        # PAGO CON y VUELTO (fila horizontal)
        pago_layout = QHBoxLayout()
        pago_layout.setSpacing(16)
        
        # PAGO CON
        pago_label = QLabel("PAGO CON:")
        pago_label.setFont(QFont("Roboto", 14, QFont.DemiBold))
        pago_label.setStyleSheet("color: #212121;")
        pago_layout.addWidget(pago_label)
        
        self.pago_input = SisInput(placeholder="0.00")
        self.pago_input.setFixedWidth(150)
        self.pago_input.textChanged.connect(self._calcular_vuelto)
        pago_layout.addWidget(self.pago_input)
        
        pago_layout.addStretch()
        
        # VUELTO
        vuelto_label = QLabel("VUELTO:")
        vuelto_label.setFont(QFont("Roboto", 14, QFont.DemiBold))
        vuelto_label.setStyleSheet("color: #212121;")
        pago_layout.addWidget(vuelto_label)
        
        self.vuelto_label = QLabel("S/ 0.00")
        self.vuelto_label.setFont(QFont("Roboto", 20, QFont.Bold))
        self.vuelto_label.setStyleSheet("color: #2E7D32;")
        self.vuelto_label.setMinimumWidth(120)
        pago_layout.addWidget(self.vuelto_label)
        
        right_layout.addLayout(pago_layout)
        
        # Botones (CERRAR CAJA y CONFIRMAR VENTA)
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(16)
        
        # Botón CERRAR CAJA (rojo)
        self.btn_cerrar_caja = QPushButton("🔒 CERRAR CAJA")
        self.btn_cerrar_caja.setMinimumHeight(48)
        self.btn_cerrar_caja.setCursor(Qt.PointingHandCursor)
        self.btn_cerrar_caja.setStyleSheet("""
            QPushButton {
                background-color: #D32F2F;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #C62828;
            }
        """)
        self.btn_cerrar_caja.clicked.connect(self._cerrar_caja)
        botones_layout.addWidget(self.btn_cerrar_caja)
        
        # Botón CONFIRMAR VENTA (verde)
        self.btn_confirmar = QPushButton("✅ CONFIRMAR VENTA")
        self.btn_confirmar.setMinimumHeight(48)
        self.btn_confirmar.setCursor(Qt.PointingHandCursor)
        self.btn_confirmar.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1B5E20;
            }
        """)
        self.btn_confirmar.clicked.connect(self._confirmar_venta)
        botones_layout.addWidget(self.btn_confirmar)
        
        right_layout.addLayout(botones_layout)
        
        # Agregar paneles al splitter
        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(panel_derecho)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
    
    def agregar_al_carrito(self, producto: ProductoModelo):
        """Agrega un producto al carrito"""
        self.carrito.append(producto)
        self._actualizar_carrito()
        self._actualizar_total()
        self.panel_alertas.refresh()  # Refrescar alertas (puede cambiar stock)
    
    def _actualizar_carrito(self):
        """Actualiza la lista visual del carrito"""
        # Limpiar layout (excepto el stretch)
        while self.carrito_layout.count() > 1:
            item = self.carrito_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Agrupar productos iguales para mostrar cantidades
        productos_agrupados = {}
        for p in self.carrito:
            if p.id not in productos_agrupados:
                productos_agrupados[p.id] = {"producto": p, "cantidad": 0}
            productos_agrupados[p.id]["cantidad"] += 1
        
        for data in productos_agrupados.values():
            producto = data["producto"]
            cantidad = data["cantidad"]
            
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(8, 8, 8, 8)
            item_layout.setSpacing(12)
            
            # Nombre y cantidad
            nombre_label = QLabel(f"{producto.nombre} x{cantidad}")
            nombre_label.setFont(QFont("Roboto", 14))
            nombre_label.setStyleSheet("color: #212121;")
            item_layout.addWidget(nombre_label)
            
            item_layout.addStretch()
            
            # Precio
            subtotal = producto.precio_venta * cantidad
            precio_label = QLabel(f"S/ {subtotal:.2f}")
            precio_label.setFont(QFont("Roboto", 14, QFont.DemiBold))
            precio_label.setStyleSheet("color: #2E7D32;")
            item_layout.addWidget(precio_label)
            
            # Botón eliminar
            btn_eliminar = QPushButton("✖")
            btn_eliminar.setFixedSize(30, 30)
            btn_eliminar.setCursor(Qt.PointingHandCursor)
            btn_eliminar.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #D32F2F;
                    border: 1px solid #E0E0E0;
                    border-radius: 8px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #FFEBEE;
                }
            """)
            btn_eliminar.clicked.connect(lambda checked, pid=producto.id: self._eliminar_producto(pid))
            item_layout.addWidget(btn_eliminar)
            
            self.carrito_layout.insertWidget(self.carrito_layout.count() - 1, item_widget)
        
        # Actualizar título
        self.carrito_titulo.setText(f"🛒 Carrito ({len(self.carrito)} productos)")
    
    def _eliminar_producto(self, producto_id: int):
        """Elimina un producto del carrito (una unidad)"""
        for i, p in enumerate(self.carrito):
            if p.id == producto_id:
                self.carrito.pop(i)
                break
        self._actualizar_carrito()
        self._actualizar_total()
        self._calcular_vuelto()
    
    def _actualizar_total(self):
        """Actualiza el total del carrito"""
        total = sum(p.precio_venta for p in self.carrito)
        self.total_label.setText(f"TOTAL: S/ {total:.2f}")
    
    def _calcular_vuelto(self):
        """Calcula el vuelto en tiempo real"""
        try:
            pago = float(self.pago_input.text() or "0")
        except ValueError:
            pago = 0
        
        total = sum(p.precio_venta for p in self.carrito)
        vuelto = pago - total
        
        if vuelto >= 0:
            self.vuelto_label.setText(f"S/ {vuelto:.2f}")
            self.vuelto_label.setStyleSheet("color: #2E7D32; font-size: 20px; font-weight: bold;")
        else:
            self.vuelto_label.setText(f"S/ {vuelto:.2f}")
            self.vuelto_label.setStyleSheet("color: #D32F2F; font-size: 20px; font-weight: bold;")
    
    def _confirmar_venta(self) -> None:
        """Confirma la venta y genera el ticket"""
        if not self.carrito:
            self._mostrar_mensaje_temporal("❌ No hay productos en el carrito")
            return
        
        # Calcular total
        total = sum(p.precio_venta for p in self.carrito)
            
        # Verificar que el pago sea suficiente
        try:
            pago = float(self.pago_input.text() or "0")
        except ValueError:
            pago = 0
    
        if pago < total:
            self._mostrar_mensaje_temporal("❌ Monto insuficiente. Verifique el PAGO CON")
            return
    
        vuelto = pago - total
            
        # ----- MOSTRAR TICKET OBLIGATORIO -----
        # HU-05: Ticket de venta obligatorio
        # No se puede confirmar una venta sin generar el ticket
            
        # Crear y mostrar el modal del ticket
        ticket_modal = TicketModal(
            productos=self.carrito.copy(),  # Copiar para que no se modifique
            total=total,
            pago=pago,
            vuelto=vuelto,
            parent=self
        )
    
        # El ticket se muestra como modal (bloquea la interacción hasta cerrarlo)
        ticket_modal.exec()
            
        # Después de cerrar el ticket, limpiar el carrito
        self.carrito.clear()
        self._actualizar_carrito()
        self._actualizar_total()
        self.pago_input.clear()
        self._calcular_vuelto()
            
        self._mostrar_mensaje_temporal("✅ Venta completada correctamente")

    
    def _cerrar_caja(self):
        """Cierra la caja y genera reporte del día"""
        self._mostrar_mensaje_temporal("🔒 Generando reporte de cierre de caja...")
        # Aquí iría la lógica de cierre de caja
    
    def _mostrar_mensaje_temporal(self, mensaje: str, segundos: int = 2):
        """Muestra un mensaje temporal (puedes conectar a un label de estado)"""
        print(f"📢 {mensaje}")
        # Opcional: conectar a un QLabel de estado si lo agregas
    
    def _ir_a_producto(self, producto_id: int):
        """Navega al producto en el módulo de productos"""
        print(f"🔍 Navegar a producto ID: {producto_id}")
        # Aquí puedes emitir una señal o llamar a un callback