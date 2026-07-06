"""
Ticket Modal - SISVENIN
HU-05: Ticket de venta obligatorio

Muestra el ticket de venta en formato legible con:
- Nombre del negocio
- Fecha y hora
- Lista de productos con cantidades y precios
- Total
- Botones: Imprimir y Cerrar
"""

from typing import List, Optional
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QDialog
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor

from src.app.models.producto_modelo import ProductoModelo
from src.app.utils.impresora import ImpresoraTicket


class TicketModal(QDialog):
    """
    Modal que muestra el ticket de venta.
    Se abre automáticamente después de confirmar una venta.
    """
    
    def __init__(
        self,
        productos: List[ProductoModelo],
        total: float,
        pago: float,
        vuelto: float,
        parent: Optional[QWidget] = None
    ):
        """
        Inicializa el modal del ticket.
        
        Args:
            productos: Lista de productos vendidos
            total: Monto total de la venta
            pago: Monto recibido del cliente
            vuelto: Vuelto a devolver
            parent: Widget padre
        """
        super().__init__(parent)
        
        self.productos = productos
        self.total = total
        self.pago = pago
        self.vuelto = vuelto
        self.impresora = ImpresoraTicket()
        
        self.setWindowTitle("🧾 Ticket de Venta")
        self.setModal(True)
        self.setMinimumSize(400, 500)
        self.setMaximumWidth(500)
        
        # Estilo del modal
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F5F5;
            }
        """)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura la interfaz del ticket"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # ===== TICKET CONTENT =====
        ticket_frame = QFrame()
        ticket_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 24px;
            }
        """)
        
        ticket_layout = QVBoxLayout(ticket_frame)
        ticket_layout.setSpacing(8)
        
        # Scroll para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        
        # Contenedor del contenido del ticket
        contenido_widget = QWidget()
        contenido_layout = QVBoxLayout(contenido_widget)
        contenido_layout.setSpacing(6)
        contenido_layout.setContentsMargins(0, 0, 0, 0)
        
        # ----- NOMBRE DEL NEGOCIO -----
        nombre_negocio = QLabel("🛒 SISVENIN")
        nombre_negocio.setFont(QFont("Roboto", 22, QFont.Bold))
        nombre_negocio.setStyleSheet("color: #2E7D32;")
        nombre_negocio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contenido_layout.addWidget(nombre_negocio)
        
        subtitulo = QLabel("Minimarket Villa Carrion")
        subtitulo.setFont(QFont("Roboto", 12))
        subtitulo.setStyleSheet("color: #757575;")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contenido_layout.addWidget(subtitulo)
        
        # ----- SEPARADOR -----
        contenido_layout.addWidget(self._crear_separador())
        
        # ----- FECHA -----
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        fecha_label = QLabel(f"📅 {fecha_actual}")
        fecha_label.setFont(QFont("Roboto", 12))
        fecha_label.setStyleSheet("color: #212121;")
        contenido_layout.addWidget(fecha_label)
        
        # ----- SEPARADOR -----
        contenido_layout.addWidget(self._crear_separador())
        
        # ----- PRODUCTOS -----
        header = QLabel("PRODUCTOS")
        header.setFont(QFont("Roboto", 12, QFont.DemiBold))
        header.setStyleSheet("color: #212121;")
        contenido_layout.addWidget(header)
        
        # Agrupar productos por ID para mostrar cantidades
        productos_agrupados = {}
        for p in self.productos:
            if p.id not in productos_agrupados:
                productos_agrupados[p.id] = {"producto": p, "cantidad": 0}
            productos_agrupados[p.id]["cantidad"] += 1
        
        # Mostrar cada producto
        for data in productos_agrupados.values():
            producto = data["producto"]
            cantidad = data["cantidad"]
            subtotal = producto.precio_venta * cantidad
            
            # Fila: nombre x cantidad | precio
            fila = QWidget()
            fila_layout = QHBoxLayout(fila)
            fila_layout.setContentsMargins(0, 2, 0, 2)
            fila_layout.setSpacing(8)
            
            nombre_label = QLabel(f"{producto.nombre} x{cantidad}")
            nombre_label.setFont(QFont("Roboto", 12))
            nombre_label.setStyleSheet("color: #212121;")
            fila_layout.addWidget(nombre_label)
            
            fila_layout.addStretch()
            
            precio_label = QLabel(f"S/ {subtotal:.2f}")
            precio_label.setFont(QFont("Roboto", 12))
            precio_label.setStyleSheet("color: #2E7D32; font-weight: 600;")
            fila_layout.addWidget(precio_label)
            
            contenido_layout.addWidget(fila)
        
        # ----- SEPARADOR -----
        contenido_layout.addWidget(self._crear_separador())
        
        # ----- TOTAL -----
        total_widget = QWidget()
        total_layout = QHBoxLayout(total_widget)
        total_layout.setContentsMargins(0, 4, 0, 4)
        total_layout.setSpacing(8)
        
        total_label = QLabel("TOTAL:")
        total_label.setFont(QFont("Roboto", 16, QFont.DemiBold))
        total_label.setStyleSheet("color: #212121;")
        total_layout.addWidget(total_label)
        
        total_layout.addStretch()
        
        total_monto = QLabel(f"S/ {self.total:.2f}")
        total_monto.setFont(QFont("Roboto", 18, QFont.Bold))
        total_monto.setStyleSheet("color: #2E7D32;")
        total_layout.addWidget(total_monto)
        
        contenido_layout.addWidget(total_widget)
        
        # ----- PAGO Y VUELTO -----
        pago_label = QLabel(f"PAGO CON: S/ {self.pago:.2f}")
        pago_label.setFont(QFont("Roboto", 12))
        pago_label.setStyleSheet("color: #757575;")
        contenido_layout.addWidget(pago_label)
        
        vuelto_label = QLabel(f"VUELTO: S/ {self.vuelto:.2f}")
        vuelto_label.setFont(QFont("Roboto", 14, QFont.Bold))
        if self.vuelto >= 0:
            vuelto_label.setStyleSheet("color: #2E7D32;")
        else:
            vuelto_label.setStyleSheet("color: #D32F2F;")
        contenido_layout.addWidget(vuelto_label)
        
        # ----- SEPARADOR -----
        contenido_layout.addWidget(self._crear_separador())
        
        # ----- PIE DE PÁGINA -----
        gracias = QLabel("¡Gracias por su compra!")
        gracias.setFont(QFont("Roboto", 12))
        gracias.setStyleSheet("color: #757575;")
        gracias.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contenido_layout.addWidget(gracias)
        
        contenido_layout.addStretch()
        
        # Asignar contenido al scroll
        scroll.setWidget(contenido_widget)
        ticket_layout.addWidget(scroll)
        
        layout.addWidget(ticket_frame)
        
        # ===== BOTONES =====
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(16)
        
        # Botón CERRAR (secundario)
        self.btn_cerrar = QPushButton("✖ Cerrar")
        self.btn_cerrar.setMinimumHeight(48)
        self.btn_cerrar.setCursor(Qt.PointingHandCursor)
        self.btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #757575;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
        """)
        self.btn_cerrar.clicked.connect(self.close)
        botones_layout.addWidget(self.btn_cerrar)
        
        # Botón IMPRIMIR (primario)
        self.btn_imprimir = QPushButton("🖨️ Imprimir")
        self.btn_imprimir.setMinimumHeight(48)
        self.btn_imprimir.setCursor(Qt.PointingHandCursor)
        self.btn_imprimir.setStyleSheet("""
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
        self.btn_imprimir.clicked.connect(self._imprimir_ticket)
        botones_layout.addWidget(self.btn_imprimir)
        
        layout.addLayout(botones_layout)
    
    def _crear_separador(self) -> QFrame:
        """Crea un separador visual"""
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setStyleSheet("background-color: #E0E0E0; max-height: 1px;")
        return separador
    
    def _imprimir_ticket(self) -> None:
        """Imprime el ticket usando la impresora"""
        try:
            self.impresora.imprimir(
                productos=self.productos,
                total=self.total,
                pago=self.pago,
                vuelto=self.vuelto
            )
            self._mostrar_mensaje("✅ Ticket enviado a la impresora")
        except Exception as e:
            self._mostrar_mensaje(f"❌ Error al imprimir: {e}")
    
    def _mostrar_mensaje(self, mensaje: str) -> None:
        """Muestra un mensaje temporal en el botón"""
        texto_original = self.btn_imprimir.text()
        self.btn_imprimir.setText(mensaje)
        QTimer.singleShot(2000, lambda: self.btn_imprimir.setText(texto_original))