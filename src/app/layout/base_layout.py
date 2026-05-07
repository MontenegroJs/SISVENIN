# src/app/layout/base_layout.py
"""
BaseLayout - Componentes genéricos de la aplicación
Cabecera, navegación, barra de estado, estructura base
"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QStatusBar, QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class BaseLayout(QMainWindow):
    """
    Layout base de la aplicación.
    Contiene todo lo genérico: cabecera, navegación, área de contenido, barra de estado.
    """
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.setWindowTitle("SISVENIN - Minimarket Villa Carrion")
        self.setGeometry(100, 100, 1200, 800)
        
        # Estilos generales
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Construir componentes genéricos
        self._crear_cabecera()
        self._crear_navegacion()
        self._crear_area_contenido()
        self._crear_barra_estado()
        
        # Conectar señales de navegación
        self._conectar_navegacion()
    
    def _crear_cabecera(self):
        """Crea la cabecera genérica de la aplicación"""
        self.cabecera = QWidget()
        self.cabecera.setStyleSheet("""
            background-color: #2c3e50;
            min-height: 100px;
        """)
        
        layout = QVBoxLayout(self.cabecera)
        layout.setAlignment(Qt.AlignCenter)
        
        # Título
        titulo = QLabel("🏪 SISVENIN")
        titulo.setAlignment(Qt.AlignCenter)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(28)
        fuente_titulo.setBold(True)
        titulo.setFont(fuente_titulo)
        titulo.setStyleSheet("color: white;")
        layout.addWidget(titulo)
        
        # Subtítulo
        subtitulo = QLabel("Sistema de Ventas e Inventario")
        subtitulo.setAlignment(Qt.AlignCenter)
        fuente_sub = QFont()
        fuente_sub.setPointSize(12)
        subtitulo.setFont(fuente_sub)
        subtitulo.setStyleSheet("color: #ecf0f1;")
        layout.addWidget(subtitulo)
        
        self.main_layout.addWidget(self.cabecera)
    
    def _crear_navegacion(self):
        """Crea la barra de navegación genérica"""
        self.navbar = QWidget()
        self.navbar.setStyleSheet("""
            background-color: #34495e;
            min-height: 50px;
        """)
        
        layout = QHBoxLayout(self.navbar)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Estilo base para botones de navegación
        estilo_boton = """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2c3e50;
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
            }
        """
        
        # Botones de navegación
        self.botones_navegacion = {}
        
        botones_config = [
            ("productos", "📦 Productos"),
            ("ventas", "💰 Ventas"),
            ("usuarios", "👥 Usuarios"),
            ("reportes", "📊 Reportes"),
            ("configuración", "⚙️ Configuración"),
        ]
        
        for modulo_id, texto in botones_config:
            btn = QPushButton(texto)
            btn.setStyleSheet(estilo_boton)
            btn.setProperty("modulo", modulo_id)
            self.botones_navegacion[modulo_id] = btn
            layout.addWidget(btn)
        
        # Espaciador para empujar el botón de salir a la derecha
        layout.addStretch()
        
        # Botón de salir
        self.btn_salir = QPushButton("🚪 Salir")
        self.btn_salir.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        layout.addWidget(self.btn_salir)
        
        self.main_layout.addWidget(self.navbar)
    
    def _crear_area_contenido(self):
        """Crea el área donde se mostrarán los módulos específicos"""
        self.area_contenido = QStackedWidget()
        self.area_contenido.setStyleSheet("""
            QStackedWidget {
                background-color: #f5f5f5;
                padding: 20px;
            }
        """)
        self.main_layout.addWidget(self.area_contenido)
    
    def _crear_barra_estado(self):
        """Crea la barra de estado genérica"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("✅ Sistema listo")
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #ecf0f1;
                color: #2c3e50;
            }
        """)
    
    def _conectar_navegacion(self):
        """Conecta los botones de navegación"""
        self.btn_salir.clicked.connect(self.cerrar_aplicacion)
    
    def registrar_modulo(self, nombre, widget):
        """
        Registra un módulo en el área de contenido
        
        Args:
            nombre: Nombre del módulo (productos, ventas, etc.)
            widget: Widget del módulo (debe ser QWidget)
        """
        indice = self.area_contenido.addWidget(widget)
        
        # Conectar el botón correspondiente si existe
        if nombre in self.botones_navegacion:
            # Desconectar conexiones anteriores para evitar duplicados
            try:
                self.botones_navegacion[nombre].clicked.disconnect()
            except:
                pass
            # Conectar nueva
            self.botones_navegacion[nombre].clicked.connect(
                lambda checked, idx=indice, nom=nombre: self.mostrar_modulo(idx, nom)
            )
        
        return indice
    
    def mostrar_modulo(self, indice, nombre_modulo):
        """
        Muestra un módulo específico
        
        Args:
            indice: Índice en el StackedWidget
            nombre_modulo: Nombre del módulo (para la barra de estado)
        """
        self.area_contenido.setCurrentIndex(indice)
        nombre_display = nombre_modulo.capitalize()
        self.status_bar.showMessage(f"📱 Módulo: {nombre_display}")
    
    def cerrar_aplicacion(self):
        """Cierra la aplicación (se sobrescribe en app.py)"""
        self.close()
    
    def set_mensaje_estado(self, mensaje):
        """Actualiza el mensaje de la barra de estado"""
        self.status_bar.showMessage(mensaje)