"""
BaseLayout - Layout genérico de la aplicación con menú lateral izquierdo
Diseño basado completamente en el Prompt 0 (Sistema de Diseño) de Figma SISVENIN

Especificaciones aplicadas:
- Paleta de colores: Verde #2E7D32, Rojo #D32F2F, Fondo #F5F5F5
- Tipografía: DM Sans (con fallback Segoe UI, sans-serif)
- Espaciado: Sistema octal (múltiplos de 8px)
- Line-height: 1.4 para legibilidad
"""

import os
from datetime import datetime
from typing import Optional, Callable, List, Any

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QStackedWidget, QFrame, QScrollArea,
    QPushButton, QMessageBox, QApplication
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QFontDatabase, QColor


class BaseLayout(QMainWindow):
    """
    Layout base con menú lateral izquierdo y área de contenido derecha.
    Siguiendo el diseño acordado en el Prompt 0 de Figma.
    
    Este layout NO importa componentes compartidos. Su responsabilidad es
    exclusivamente estructural. Las vistas deben importar y usar los
    componentes compartidos directamente.
    """
    
    # ==================== CONSTANTES DE DISEÑO (Prompt 0) ====================
    
    # Colores
    COLOR_PRIMARIO = "#2E7D32"
    COLOR_PRIMARIO_HOVER = "#1B5E20"
    COLOR_PRIMARIO_DESABILITADO = "#A5D6A7"
    
    COLOR_PELIGRO = "#D32F2F"
    COLOR_PELIGRO_HOVER = "#C62828"
    
    COLOR_FONDO_VENTANA = "#F5F5F5"
    COLOR_TARJETA = "#FFFFFF"
    COLOR_TEXTO_PRINCIPAL = "#212121"
    COLOR_TEXTO_SECUNDARIO = "#757575"
    COLOR_BORDE = "#E0E0E0"
    COLOR_PLACEHOLDER = "#BDBDBD"
    COLOR_HOVER_FILA = "#FAFAFA"
    
    COLOR_ALERTA_STOCK_BG = "#FFEBEE"
    COLOR_ALERTA_STOCK_BORDER = "#D32F2F"
    COLOR_ALERTA_VENCE_BG = "#FFF3E0"
    COLOR_ALERTA_VENCE_BORDER = "#FF9800"
    COLOR_MENU_ACTIVO_BG = "#E8F5E9"
    COLOR_MENU_ACTIVO_BORDER = "#2E7D32"
    
    # Tamaños de fuente (en píxeles)
    FUENTE_TITULO = 30
    FUENTE_SUBTITULO = 20
    FUENTE_CUERPO = 17
    FUENTE_BOTON = 16
    FUENTE_TOTAL_POS = 32
    FUENTE_VUELTO_POS = 48
    FUENTE_ALERTA = 14
    
    # Pesos de fuente (usando valores numéricos de Qt)
    PESO_NORMAL = QFont.Normal      # 50 - Regular
    PESO_MEDIUM = QFont.Medium      # 57 - Medium
    PESO_SEMIBOLD = QFont.DemiBold  # 63 - Semibold
    PESO_BOLD = QFont.Bold          # 75 - Bold
    
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
    ANCHO_MENU_LATERAL = 270
    TAMANO_MINIMO_VENTANA = (1024, 600)
    TAMANO_RECOMENDADO_VENTANA = (1280, 720)
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.setWindowTitle("SISVENIN - Minimarket Villa Carrion")
        self.setGeometry(100, 100, *self.TAMANO_RECOMENDADO_VENTANA)
        self.setMinimumSize(*self.TAMANO_MINIMO_VENTANA)
        
        # Cargar fuentes DM Sans
        self._cargar_fuentes()
        
        # Configurar fuente por defecto
        self._configurar_fuente_por_defecto()
        
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
        
        # Diccionario para almacenar módulos
        self.modulos: dict = {}
        self.botones_menu: dict = {}
        
        # Timer para actualizar fecha/hora
        self.timer_fecha = QTimer()
        self.timer_fecha.timeout.connect(self.actualizar_fecha_hora)
        self.timer_fecha.start(1000)
        self.actualizar_fecha_hora()
    
    def _cargar_fuentes(self):
        """
        Carga las fuentes DM Sans desde la carpeta de recursos.
        Registra las fuentes en Qt para que estén disponibles.
        """
        # Buscar la carpeta de fuentes
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        posibles_ubicaciones = [
            os.path.join(base_dir, "src", "app", "fonts"),
            os.path.join(base_dir, "src", "assets", "fonts"),
            os.path.join(base_dir, "src", "app", "assets", "fonts"),
        ]
        
        fonts_dir = None
        for ubicacion in posibles_ubicaciones:
            if os.path.exists(ubicacion):
                fonts_dir = ubicacion
                break
        
        if not fonts_dir:
            print("⚠️ No se encontró la carpeta de fuentes")
            return
        
        # Registrar todas las fuentes .ttf
        fuentes_registradas = 0
        for archivo in os.listdir(fonts_dir):
            if archivo.endswith(".ttf"):
                ruta_completa = os.path.join(fonts_dir, archivo)
                font_id = QFontDatabase.addApplicationFont(ruta_completa)
                if font_id != -1:
                    fuentes_registradas += 1
        
        print(f"📦 {fuentes_registradas} fuentes registradas")
        
        # Verificar fuentes disponibles (debug)
        familias = [f for f in QFontDatabase.families() if "DM Sans" in f or "DMSans" in f]
        if familias:
            print(f"🔤 Fuentes DM Sans disponibles: {familias[:3]}...")
        else:
            print("⚠️ DM Sans no encontrada, usando fallback")
    
    def _configurar_fuente_por_defecto(self):
        """
        Configura la fuente por defecto de toda la aplicación.
        Utiliza DM Sans como fuente principal con fallback Segoe UI.
        """
        # Intentar usar DM Sans como fuente principal
        fuente_base = QFont("DM Sans", self.FUENTE_CUERPO)
        fuente_base.setWeight(QFont.Normal)
        
        # Verificar si DM Sans está disponible
        dm_sans_disponible = any("DM Sans" in f or "DMSans" in f for f in QFontDatabase.families())
        
        if not dm_sans_disponible:
            # Fallback a Segoe UI (Windows) o sans-serif
            print("⚠️ DM Sans no disponible, usando Segoe UI como fallback")
            fuente_base = QFont("Segoe UI", self.FUENTE_CUERPO)
            fuente_base.setWeight(QFont.Normal)
        
        # Aplicar a toda la aplicación
        app = QApplication.instance()
        if app:
            app.setFont(fuente_base)
    
    def _aplicar_estilos_base(self):
        """
        Aplica los estilos base a toda la aplicación.
        Incluye configuración de line-height a través de padding.
        """
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.COLOR_FONDO_VENTANA};
            }}
            
            /* Estilo base para QLabel */
            QLabel {{
                background-color: transparent;
            }}
            
            /* Scrollbars */
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
            
            /* Estilo para mejorar la legibilidad (line-height simulado) */
            QAbstractItemView::item {{
                padding: 8px 4px;
            }}
        """)
    
    def _crear_menu_lateral(self):
        """Crea el menú lateral izquierdo"""
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
        logo_widget.setStyleSheet("""
            padding-left: 8px;
        """)
        logo_layout = QVBoxLayout(logo_widget)
        logo_layout.setSpacing(0)
        
        self.logo_label = QLabel("🛒 SISVENIN")
        self.logo_label.setStyleSheet(f"""
            font-size: {self.FUENTE_SUBTITULO}px;
            font-weight: {self.PESO_BOLD};
            color: {self.COLOR_PRIMARIO};
            margin-top: 16px;
        """)
        
        self.logo_sub = QLabel("Minimarket Villa Carrion")
        self.logo_sub.setStyleSheet(f"""
            font-size: 13px;
            font-weight: 600;
            color: {self.COLOR_TEXTO_SECUNDARIO};
            padding-top: 4px;
            margin-bottom: 16px;
        """)
        
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.logo_sub)
        menu_layout.addWidget(logo_widget)
        
        # ==================== SEPARADOR ====================
        separador = QWidget()
        separador.setFixedHeight(1)
        separador.setStyleSheet(f"""
            background-color: {self.COLOR_BORDE};
            margin: 8px 16px;
        """)
        menu_layout.addWidget(separador)
                
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
    
    def _estilo_boton_menu(self, activo: bool = False) -> str:
        """Estilo para botones del menú lateral"""
        peso_normal = 600
        peso_activo = 700
        
        padding_vertical = 2
        padding_horizontal = 16
        
        # Estilo base común para ambos estados
        base_style = f"""
            QPushButton {{
                text-align: left;
                padding: {padding_vertical}px {padding_horizontal}px;
                border: none;
                font-size: {self.FUENTE_CUERPO}px;
                min-height: 48px;
            }}
        """
        
        if activo:
            return base_style + f"""
                QPushButton {{
                    background-color: {self.COLOR_MENU_ACTIVO_BG};
                    color: {self.COLOR_PRIMARIO};
                    border-left: 3px solid {self.COLOR_MENU_ACTIVO_BORDER};
                    font-weight: {peso_activo};
                }}
                QPushButton:hover {{
                    background-color: #C8E6C9;
                }}
            """
        else:
            return base_style + f"""
                QPushButton {{
                    background-color: transparent;
                    color: {self.COLOR_TEXTO_PRINCIPAL};
                    font-weight: {peso_normal};
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
            font-size: {self.FUENTE_TITULO}px;
            font-weight: {self.PESO_BOLD};
            color: {self.COLOR_TEXTO_PRINCIPAL};
        """)
        
        cabecera_layout.addWidget(self.titulo_pantalla)
        cabecera_layout.addStretch()
        
        self.label_fecha_hora = QLabel("")
        self.label_fecha_hora.setStyleSheet(f"""
            font-size: 15px;
            font-weight: 700;
            color: {self.COLOR_TEXTO_SECUNDARIO};
        """)
        cabecera_layout.addWidget(self.label_fecha_hora)
        
        contenido_layout.addLayout(cabecera_layout)
        
        # Stacked widget para el contenido
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: transparent;")
        contenido_layout.addWidget(self.stacked_widget, 1)
    
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
        
        # Actualizar estilo de los botones
        for nombre, btn in self.botones_menu.items():
            # Verificar si este botón es el activo
            texto_btn = btn.text().split(" ", 1)[-1] if " " in btn.text() else btn.text()
            es_activo = (texto_btn == nombre_modulo)
            btn.setStyleSheet(self._estilo_boton_menu(activo=es_activo))
    
    def mensaje_estado(self, mensaje: str):
        """Muestra un mensaje temporal (para depuración)"""
        print(f"📢 {mensaje}")
    
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
                font-weight: {self.PESO_NORMAL};
            }}
            QPushButton {{
                min-width: 80px;
                padding: 8px 16px;
                border-radius: {self.BORDER_RADIUS_BOTON}px;
                font-weight: {self.PESO_SEMIBOLD};
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