# src/app/base_layout.py
"""
BaseLayout - Layout genérico de la aplicación
"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QStackedWidget, QStatusBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class BaseLayout(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 1100, 750)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QPushButton { font-family: 'Segoe UI', Arial, sans-serif; }
            QLabel { font-family: 'Segoe UI', Arial, sans-serif; }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.modulos = {}
        
        self._crear_cabecera()
        self._crear_navegacion()
        self._crear_area_contenido()
        self._crear_barra_estado()
        
        self.btn_salir.clicked.connect(self.close)
    
    def _crear_cabecera(self):
        cabecera = QWidget()
        cabecera.setStyleSheet("background-color: #2c3e50; min-height: 100px;")
        
        layout = QVBoxLayout(cabecera)
        layout.setAlignment(Qt.AlignCenter)
        
        titulo = QLabel("🏪 SISVENIN")
        titulo.setAlignment(Qt.AlignCenter)
        fuente = QFont()
        fuente.setPointSize(28)
        fuente.setBold(True)
        titulo.setFont(fuente)
        titulo.setStyleSheet("color: white; padding: 10px;")
        layout.addWidget(titulo)
        
        subtitulo = QLabel("Sistema de Ventas e Inventario")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("color: #ecf0f1;")
        layout.addWidget(subtitulo)
        
        self.main_layout.addWidget(cabecera)
    
    def _crear_navegacion(self):
        navbar = QWidget()
        navbar.setStyleSheet("background-color: #34495e; min-height: 50px;")
        
        layout = QHBoxLayout(navbar)
        layout.setContentsMargins(20, 0, 20, 0)
        
        estilo = """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2c3e50;
                border-radius: 5px;
            }
        """
        
        self.btn_productos = QPushButton("📦 Productos")
        self.btn_productos.setStyleSheet(estilo)
        
        self.btn_clientes = QPushButton("👥 Clientes")
        self.btn_clientes.setStyleSheet(estilo)
        self.btn_clientes.setEnabled(False)
        
        self.btn_ventas = QPushButton("💰 Ventas")
        self.btn_ventas.setStyleSheet(estilo)
        self.btn_ventas.setEnabled(False)
        
        self.btn_reportes = QPushButton("📊 Reportes")
        self.btn_reportes.setStyleSheet(estilo)
        self.btn_reportes.setEnabled(False)
        
        self.btn_config = QPushButton("⚙️ Configuración")
        self.btn_config.setStyleSheet(estilo)
        self.btn_config.setEnabled(False)
        
        self.botones = {
            "productos": self.btn_productos,
            "clientes": self.btn_clientes,
            "ventas": self.btn_ventas,
            "reportes": self.btn_reportes,
            "configuracion": self.btn_config,
        }
        
        layout.addWidget(self.btn_productos)
        layout.addWidget(self.btn_clientes)
        layout.addWidget(self.btn_ventas)
        layout.addWidget(self.btn_reportes)
        layout.addWidget(self.btn_config)
        layout.addStretch()
        
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
        
        self.main_layout.addWidget(navbar)
    
    def _crear_area_contenido(self):
        self.area_contenido = QStackedWidget()
        self.area_contenido.setStyleSheet("""
            QStackedWidget {
                background-color: #f5f5f5;
                padding: 20px;
            }
        """)
        self.main_layout.addWidget(self.area_contenido)
    
    def _crear_barra_estado(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("✅ Sistema listo")
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #ecf0f1;
                color: #2c3e50;
            }
        """)
    
    def registrar_modulo(self, nombre, widget, habilitar_boton=False):
        """Registra un módulo en el área de contenido"""
        indice = self.area_contenido.addWidget(widget)
        
        if nombre in self.botones:
            self.botones[nombre].clicked.connect(
                lambda checked, idx=indice, nom=nombre: self._mostrar_modulo(idx, nom)
            )
            if habilitar_boton:
                self.botones[nombre].setEnabled(True)
        
        return indice
    
    def _mostrar_modulo(self, indice, nombre_modulo):
        self.area_contenido.setCurrentIndex(indice)
        self.status_bar.showMessage(f"📱 Módulo: {nombre_modulo.capitalize()}")
    
    def mensaje_estado(self, mensaje):
        self.status_bar.showMessage(mensaje)
    
    def closeEvent(self, event):
        from PySide6.QtWidgets import QMessageBox
        
        respuesta = QMessageBox.question(
            self,
            "Salir de SISVENIN",
            "¿Estás seguro de que deseas salir?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()