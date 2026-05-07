# src/app/app.py
"""
APP - Aplicación principal SISVENIN
"""
from PySide6.QtWidgets import QMessageBox
from src.app.layout.base_layout import BaseLayout

# Importar módulos
from src.app.modules.producto.producto_vista import ProductoVista


class App(BaseLayout):
    """
    Aplicación principal.
    Extiende BaseLayout y registra los módulos específicos.
    """
    
    def __init__(self):
        super().__init__()
        
        # Registrar módulos
        self._registrar_modulos()
        
        # Mostrar primer módulo por defecto
        self.mostrar_modulo(0, "productos")
    
    def _registrar_modulos(self):
        """Registra todos los módulos de la aplicación"""
        
        # Crear instancias de los módulos
        self.modulo_productos = ProductoVista()
        
        # Placeholder para otros módulos (por ahora)
        from PySide6.QtWidgets import QLabel
        from PySide6.QtCore import Qt
        
        self.modulo_ventas = QLabel("💰 Módulo de Ventas\n\nPróximamente disponible")
        self.modulo_ventas.setAlignment(Qt.AlignCenter)
        self.modulo_ventas.setStyleSheet("font-size: 18px; color: #555; padding: 50px;")
        
        self.modulo_usuarios = QLabel("👥 Módulo de Usuarios\n\nPróximamente disponible")
        self.modulo_usuarios.setAlignment(Qt.AlignCenter)
        self.modulo_usuarios.setStyleSheet("font-size: 18px; color: #555; padding: 50px;")
        
        self.modulo_reportes = QLabel("📊 Módulo de Reportes\n\nPróximamente disponible")
        self.modulo_reportes.setAlignment(Qt.AlignCenter)
        self.modulo_reportes.setStyleSheet("font-size: 18px; color: #555; padding: 50px;")
        
        self.modulo_config = QLabel("⚙️ Configuración\n\nPróximamente disponible")
        self.modulo_config.setAlignment(Qt.AlignCenter)
        self.modulo_config.setStyleSheet("font-size: 18px; color: #555; padding: 50px;")
        
        # Registrar en el layout base
        self.registrar_modulo("productos", self.modulo_productos)
        self.registrar_modulo("ventas", self.modulo_ventas)
        self.registrar_modulo("usuarios", self.modulo_usuarios)
        self.registrar_modulo("reportes", self.modulo_reportes)
        self.registrar_modulo("configuración", self.modulo_config)
    
    def cerrar_aplicacion(self):
        """Sobrescribe el método de cierre"""
        respuesta = QMessageBox.question(
            self,
            "Salir de SISVENIN",
            "¿Estás seguro de que deseas salir de la aplicación?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            self.close()
    
    def closeEvent(self, event):
        """Evento al cerrar la ventana"""
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