"""
BaseLayout - Layout genérico de la aplicación con menú lateral izquierdo
Diseño basado completamente en el Prompt 0 (Sistema de Diseño) de Figma SISVENIN

Ahora utiliza los componentes compartidos:
- SisButton, SisIconButton
- SisCard, SisMetricCard
- SisInput, SisNumberInput, SisSelect
- SisModal, SisConfirmModal
- SisAlert, SisAlertList, SisEmptyState

Especificaciones aplicadas:
- Paleta de colores: Verde #2E7D32, Rojo #D32F2F, Fondo #F5F5F5
- Tipografía: 'Segoe UI', 'Roboto', sans-serif
- Espaciado: Sistema octal (múltiplos de 8px)
- Botones: altura mínima 48px, border-radius 8px
- Tarjetas: border-radius 12px, sombra suave
- Inputs: focus con borde #2E7D32 y sombra suave
"""

import os
from datetime import datetime
from typing import Optional, Callable, List, Any

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QStackedWidget, QStatusBar, QFrame, QScrollArea,
    QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QSize, Signal
from PySide6.QtGui import QFont, QFontDatabase, QAction, QColor

# Importar componentes compartidos
from src.app.shared.components import (
    SisButton, SisIconButton, SisCard, SisMetricCard,
    SisInput, SisNumberInput, SisSelect, SisModal, SisConfirmModal,
    SisAlert, SisAlertList, SisEmptyState
)


class BaseLayout(QMainWindow):
    """
    Layout base con menú lateral izquierdo y área de contenido derecha.
    Siguiendo el diseño acordado en el Prompt 0 de Figma.
    Ahora utiliza los componentes compartidos para consistencia.
    """
    
    # ==================== CONSTANTES DE DISEÑO (Prompt 0) ====================
    
    # Colores
    COLOR_PRIMARIO = "#2E7D32"           # Verde principal
    COLOR_PRIMARIO_HOVER = "#1B5E20"     # Verde más oscuro
    COLOR_PRIMARIO_DESABILITADO = "#A5D6A7"  # Verde claro
    
    COLOR_PELIGRO = "#D32F2F"            # Rojo alerta
    COLOR_PELIGRO_HOVER = "#C62828"      # Rojo más oscuro
    
    COLOR_FONDO_VENTANA = "#F5F5F5"      # Gris muy claro
    COLOR_TARJETA = "#FFFFFF"            # Blanco
    COLOR_TEXTO_PRINCIPAL = "#212121"    # Casi negro
    COLOR_TEXTO_SECUNDARIO = "#757575"   # Gris medio
    COLOR_BORDE = "#E0E0E0"              # Gris para bordes
    COLOR_PLACEHOLDER = "#BDBDBD"        # Gris claro para placeholders
    COLOR_HOVER_FILA = "#FAFAFA"         # Hover sobre filas de tabla
    
    COLOR_ALERTA_STOCK_BG = "#FFEBEE"    # Fondo rojo muy claro
    COLOR_ALERTA_STOCK_BORDER = "#D32F2F"  # Borde rojo
    COLOR_ALERTA_VENCE_BG = "#FFF3E0"    # Fondo naranja muy claro
    COLOR_ALERTA_VENCE_BORDER = "#FF9800"  # Borde naranja
    COLOR_MENU_ACTIVO_BG = "#E8F5E9"     # Verde muy claro
    COLOR_MENU_ACTIVO_BORDER = "#2E7D32"  # Borde izquierdo verde
    
    # Tamaños de fuente
    FUENTE_TITULO = "24px"
    FUENTE_SUBTITULO = "18px"
    FUENTE_CUERPO = "14px"
    FUENTE_BOTON = "16px"
    FUENTE_TOTAL_POS = "32px"
    FUENTE_VUELTO_POS = "48px"
    FUENTE_ALERTA = "14px"
    
    # Espaciados (sistema octal)
    PADDING_PEQUENO = 8
    PADDING_MEDIANO = 16
    PADDING_GRANDE = 24
    MARGEN_ENTRE_ELEMENTOS = 16
    MARGEN_ENTRE_SECCIONES = 24
    
    BORDER_RADIUS_BOTON = 8
    BORDER_RADIUS_TARJETA = 12
    BORDER_RADIUS_MODAL = 16
    BORDER_RADIUS_ALERTA = 8
    BORDER_RADIUS_INPUT = 8
    
    # Dimensiones
    ANCHO_MENU_LATERAL = 240
    TAMANO_MINIMO_VENTANA = (1024, 600)
    TAMANO_RECOMENDADO_VENTANA = (1280, 720)
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.setWindowTitle("SISVENIN - Minimarket Villa Carrion")
        self.setGeometry(100, 100, *self.TAMANO_RECOMENDADO_VENTANA)
        self.setMinimumSize(*self.TAMANO_MINIMO_VENTANA)
        
        # Aplicar estilos base
        self._aplicar_estilos_base()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal (horizontal: menú + contenido)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ==================== MENÚ LATERAL IZQUIERDO ====================
        self._crear_menu_lateral()
        main_layout.addWidget(self.menu_lateral)
        
        # ==================== ÁREA DE CONTENIDO DERECHA ====================
        self._crear_area_contenido()
        main_layout.addWidget(self.contenido_widget, 1)
        
        # ==================== BARRA DE ESTADO ====================
        self._crear_barra_estado()
        
        # Diccionario para almacenar módulos
        self.modulos: dict = {}
        self.botones_menu: dict = {}
        
        # Timer para actualizar fecha/hora
        self.timer_fecha = QTimer()
        self.timer_fecha.timeout.connect(self.actualizar_fecha_hora)
        self.timer_fecha.start(1000)
        self.actualizar_fecha_hora()
    
    def _aplicar_estilos_base(self):
        """Aplica los estilos base a toda la aplicación"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.COLOR_FONDO_VENTANA};
            }}
            
            QWidget {{
                font-family: 'Roboto', 'Segoe UI', sans-serif;
            }}
            
            QScrollBar:vertical {{
                background-color: {self.COLOR_FONDO_VENTANA};
                width: 8px;
                border-radius: 4px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {self.COLOR_BORDE};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {self.COLOR_TEXTO_SECUNDARIO};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
    
    def _crear_menu_lateral(self):
        """Crea el menú lateral izquierdo usando componentes"""
        self.menu_lateral = QWidget()
        self.menu_lateral.setFixedWidth(self.ANCHO_MENU_LATERAL)
        self.menu_lateral.setObjectName("menuLateral")
        self.menu_lateral.setStyleSheet(f"""
            QWidget#menuLateral {{
                background-color: {self.COLOR_TARJETA};
                border-right: 1px solid {self.COLOR_BORDE};
            }}
        """)
        
        menu_layout = QVBoxLayout(self.menu_lateral)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)
        
        # ==================== LOGO / BRAND ====================
        logo_widget = QWidget()
        logo_widget.setStyleSheet(f"""
            border-bottom: 1px solid {self.COLOR_BORDE};
            padding: 16px 20px;
        """)
        logo_layout = QVBoxLayout(logo_widget)
        logo_layout.setSpacing(4)
        
        self.logo_label = QLabel("🛒 SISVENIN")
        self.logo_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 700;
            color: {self.COLOR_PRIMARIO};
        """)
        
        self.logo_sub = QLabel("Minimarket Villa Carrion")
        self.logo_sub.setStyleSheet(f"""
            font-size: 12px;
            color: {self.COLOR_TEXTO_SECUNDARIO};
        """)
        
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.logo_sub)
        menu_layout.addWidget(logo_widget)
        
        # ==================== CONTENEDOR DE BOTONES (SCROLL) ====================
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        scroll_content = QWidget()
        self.menu_scroll_layout = QVBoxLayout(scroll_content)
        self.menu_scroll_layout.setContentsMargins(0, 8, 0, 8)
        self.menu_scroll_layout.setSpacing(0)
        self.menu_scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        menu_layout.addWidget(scroll_area, 1)
        
        # ==================== FOOTER DEL MENÚ ====================
        footer_widget = QWidget()
        footer_widget.setStyleSheet(f"""
            border-top: 1px solid {self.COLOR_BORDE};
            padding: 16px 20px;
        """)
        footer_layout = QVBoxLayout(footer_widget)
        
        self.version_label = QLabel("Sistema de Diseño v1.0")
        self.version_label.setStyleSheet(f"font-size: 12px; color: {self.COLOR_TEXTO_SECUNDARIO};")
        footer_layout.addWidget(self.version_label)
        
        menu_layout.addWidget(footer_widget)
    
    def _estilo_boton_menu(self, activo: bool = False) -> str:
        """Estilo para botones del menú lateral"""
        if activo:
            return f"""
                QPushButton {{
                    background-color: {self.COLOR_MENU_ACTIVO_BG};
                    color: {self.COLOR_PRIMARIO};
                    text-align: left;
                    padding: 12px 20px;
                    border: none;
                    border-left: 3px solid {self.COLOR_MENU_ACTIVO_BORDER};
                    font-size: 16px;
                    font-weight: 500;
                    min-height: 48px;
                }}
                QPushButton:hover {{
                    background-color: #C8E6C9;
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: transparent;
                    color: {self.COLOR_TEXTO_PRINCIPAL};
                    text-align: left;
                    padding: 12px 20px;
                    border: none;
                    font-size: 16px;
                    font-weight: 500;
                    min-height: 48px;
                }}
                QPushButton:hover {{
                    background-color: {self.COLOR_FONDO_VENTANA};
                    border-left: 3px solid {self.COLOR_PRIMARIO};
                }}
            """
    
    def _crear_area_contenido(self):
        """Crea el área de contenido derecha"""
        self.contenido_widget = QWidget()
        self.contenido_widget.setStyleSheet(f"background-color: {self.COLOR_FONDO_VENTANA};")
        
        contenido_layout = QVBoxLayout(self.contenido_widget)
        contenido_layout.setContentsMargins(
            self.PADDING_GRANDE, self.PADDING_GRANDE,
            self.PADDING_GRANDE, self.PADDING_GRANDE
        )
        contenido_layout.setSpacing(self.MARGEN_ENTRE_SECCIONES)
        
        # Cabecera (título + fecha)
        cabecera_layout = QHBoxLayout()
        cabecera_layout.setSpacing(16)
        
        self.titulo_pantalla = QLabel("Dashboard")
        self.titulo_pantalla.setStyleSheet(f"""
            font-size: {self.FUENTE_TITULO};
            font-weight: 700;
            color: {self.COLOR_TEXTO_PRINCIPAL};
        """)
        
        cabecera_layout.addWidget(self.titulo_pantalla)
        cabecera_layout.addStretch()
        
        self.label_fecha_hora = QLabel("")
        self.label_fecha_hora.setStyleSheet(f"""
            font-size: 14px;
            color: {self.COLOR_TEXTO_SECUNDARIO};
        """)
        cabecera_layout.addWidget(self.label_fecha_hora)
        
        contenido_layout.addLayout(cabecera_layout)
        
        # Stacked widget para el contenido
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: transparent;")
        contenido_layout.addWidget(self.stacked_widget, 1)
    
    def _crear_barra_estado(self):
        """Crea la barra de estado inferior"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {self.COLOR_TARJETA};
                color: {self.COLOR_TEXTO_SECUNDARIO};
                border-top: 1px solid {self.COLOR_BORDE};
                padding: 4px 16px;
                font-size: 13px;
            }}
        """)
        self.status_bar.showMessage("✅ Sistema listo")
    
    # ==================== MÉTODOS PÚBLICOS ====================
    
    def actualizar_fecha_hora(self):
        """Actualiza la fecha y hora en la cabecera"""
        ahora = datetime.now()
        self.label_fecha_hora.setText(f"Hoy: {ahora.strftime('%d/%m/%Y %H:%M:%S')}")
    
    def agregar_modulo_menu(self, nombre: str, texto: str, icono: str = "", habilitar: bool = True):
        """
        Agrega un botón al menú lateral.
        
        Args:
            nombre: Identificador del módulo
            texto: Texto a mostrar
            icono: Icono (emoji) del botón
            habilitar: Si el botón está habilitado
        """
        texto_boton = f"{icono} {texto}" if icono else texto
        btn = QPushButton(texto_boton)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(self._estilo_boton_menu(activo=False))
        btn.setEnabled(habilitar)
        btn.setMinimumHeight(48)
        
        self.botones_menu[nombre] = btn
        
        # Insertar antes del stretch
        self.menu_scroll_layout.insertWidget(
            self.menu_scroll_layout.count() - 1, btn
        )
        
        return btn
    
    def registrar_modulo(
        self,
        nombre: str,
        widget: QWidget,
        texto_menu: str,
        icono: str = "📄",
        habilitar_boton: bool = True
    ) -> int:
        """
        Registra un módulo en la aplicación.
        
        Args:
            nombre: Identificador del módulo
            widget: Widget a mostrar
            texto_menu: Texto del botón en el menú
            icono: Icono del botón
            habilitar_boton: Si el botón está habilitado
            
        Returns:
            int: Índice del módulo
        """
        indice = self.stacked_widget.addWidget(widget)
        btn = self.agregar_modulo_menu(nombre, texto_menu, icono, habilitar_boton)
        
        btn.clicked.connect(lambda checked, idx=indice, nom=texto_menu: self._mostrar_modulo(idx, nom))
        
        self.modulos[nombre] = {
            "indice": indice,
            "widget": widget,
            "boton": btn,
            "texto_menu": texto_menu
        }
        
        return indice
    
    def _mostrar_modulo(self, indice: int, nombre_modulo: str):
        """Cambia la pantalla mostrada y actualiza el menú"""
        self.stacked_widget.setCurrentIndex(indice)
        self.titulo_pantalla.setText(nombre_modulo)
        self.status_bar.showMessage(f"📱 Módulo: {nombre_modulo}")
        
        # Actualizar estilo de los botones
        for btn in self.botones_menu.values():
            btn.setStyleSheet(self._estilo_boton_menu(activo=False))
        
        # Marcar el botón activo
        for btn in self.botones_menu.values():
            texto_btn = btn.text().split(" ", 1)[-1] if " " in btn.text() else btn.text()
            if texto_btn == nombre_modulo:
                btn.setStyleSheet(self._estilo_boton_menu(activo=True))
                break
    
    def mensaje_estado(self, mensaje: str):
        """Muestra un mensaje en la barra de estado"""
        self.status_bar.showMessage(mensaje)
    
    # ==================== MÉTODOS DE COMPONENTES (DELEGACIÓN) ====================
    
    def crear_boton_primario(self, texto: str, callback: Optional[Callable] = None) -> SisButton:
        """Crea un botón primario usando SisButton"""
        btn = SisButton(texto, variant="primary")
        if callback:
            btn.clicked.connect(callback)
        return btn
    
    def crear_boton_secundario(self, texto: str, callback: Optional[Callable] = None) -> SisButton:
        """Crea un botón secundario usando SisButton"""
        btn = SisButton(texto, variant="secondary")
        if callback:
            btn.clicked.connect(callback)
        return btn
    
    def crear_boton_peligro(self, texto: str, callback: Optional[Callable] = None) -> SisButton:
        """Crea un botón peligro usando SisButton"""
        btn = SisButton(texto, variant="danger")
        if callback:
            btn.clicked.connect(callback)
        return btn
    
    def crear_tarjeta(self, titulo: Optional[str] = None, contenido: Optional[QWidget] = None) -> SisCard:
        """Crea una tarjeta usando SisCard"""
        tarjeta = SisCard(title=titulo)
        if contenido:
            tarjeta.set_content(contenido)
        return tarjeta
    
    def crear_tarjeta_metrica(
        self,
        label: str,
        value: str,
        sub_value: Optional[str] = None,
        highlight: bool = False,
        icon: Optional[str] = None
    ) -> SisMetricCard:
        """Crea una tarjeta de métrica usando SisMetricCard"""
        return SisMetricCard(
            label=label,
            value=value,
            sub_value=sub_value,
            highlight=highlight,
            icon=icon
        )
    
    def crear_input(self, placeholder: str = "", align_right: bool = False) -> SisInput:
        """Crea un input usando SisInput"""
        return SisInput(placeholder=placeholder, align_right=align_right)
    
    def crear_input_numero(self, prefix: str = "", suffix: str = "") -> SisNumberInput:
        """Crea un input numérico usando SisNumberInput"""
        return SisNumberInput(prefix=prefix, suffix=suffix)
    
    def crear_modal(self, titulo: str, size: str = "sm", on_close: Optional[Callable] = None) -> SisModal:
        """Crea un modal usando SisModal"""
        return SisModal(title=titulo, size=size, on_close=on_close)
    
    def crear_alerta_stock(self, texto: str, on_click: Optional[Callable] = None) -> SisAlert:
        """Crea una alerta de stock bajo"""
        return SisAlert(type="stock", text=texto, on_click=on_click)
    
    def crear_alerta_vencimiento(self, texto: str, on_click: Optional[Callable] = None) -> SisAlert:
        """Crea una alerta de vencimiento próximo"""
        return SisAlert(type="expiry", text=texto, on_click=on_click)
    
    # ==================== CIERRE DE APLICACIÓN ====================
    
    def closeEvent(self, event):
        """Confirma antes de salir"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Salir de SISVENIN")
        msg_box.setText("¿Estás seguro de que deseas salir?")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {self.COLOR_TARJETA};
                border-radius: {self.BORDER_RADIUS_MODAL}px;
            }}
            QMessageBox QLabel {{
                color: {self.COLOR_TEXTO_PRINCIPAL};
                font-size: 14px;
            }}
            QPushButton {{
                min-width: 80px;
                padding: 8px 16px;
                border-radius: {self.BORDER_RADIUS_BOTON}px;
                font-weight: 600;
            }}
            QPushButton:first {{
                background-color: {self.COLOR_PELIGRO};
                color: white;
                border: none;
            }}
            QPushButton:first:hover {{
                background-color: {self.COLOR_PELIGRO_HOVER};
            }}
            QPushButton:last {{
                background-color: transparent;
                color: {self.COLOR_TEXTO_PRINCIPAL};
                border: 1px solid {self.COLOR_BORDE};
            }}
            QPushButton:last:hover {{
                background-color: {self.COLOR_FONDO_VENTANA};
            }}
        """)
        
        if msg_box.exec() == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()