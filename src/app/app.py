"""
Aplicación principal SISVENIN
"""

from src.app.base_layout import BaseLayout
from src.app.views.producto.producto_vista import ProductoVista  # ← CORREGIDO: añadir 'src.app.'


class App(BaseLayout):
    """Aplicación principal que extiende BaseLayout con menú lateral"""
    
    def __init__(self):
        super().__init__()
        self._registrar_modulos()
        # Mostrar Productos por defecto (único módulo disponible)
        self._mostrar_modulo_por_nombre("productos")
    
    def _registrar_modulos(self):
        """Registra todos los módulos de la aplicación"""
        
        # Módulo Productos (completo)
        self.vista_productos = ProductoVista()
        self.registrar_modulo(
            nombre="productos",
            widget=self.vista_productos,
            texto_menu="Productos",
            icono="📦"
        )
        
        # Placeholders para módulos futuros (deshabilitados)
        self._registrar_modulo_placeholder("dashboard", "Dashboard", "🏠", habilitado=False)
        self._registrar_modulo_placeholder("pos", "POS", "🛒", habilitado=False)
        self._registrar_modulo_placeholder("reporte", "Reporte del día", "📄", habilitado=False)
        self._registrar_modulo_placeholder("velocidad", "Prueba velocidad", "⏱️", habilitado=False)
        self._registrar_modulo_placeholder("ventas", "Ventas", "💰", habilitado=False)
        self._registrar_modulo_placeholder("configuracion", "Configuración", "⚙️", habilitado=False)
    
    def _registrar_modulo_placeholder(self, nombre, texto_menu, icono, habilitado=False):
        """Registra un módulo placeholder para funcionalidades futuras"""
        from PySide6.QtWidgets import QLabel
        from PySide6.QtCore import Qt
        
        placeholder = QLabel(f"{icono} {texto_menu}\n\n🚧 Próximamente disponible")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet(f"""
            font-size: 18px; 
            color: {self.COLOR_TEXTO_SECUNDARIO}; 
            padding: 50px;
        """)
        self.registrar_modulo(
            nombre=nombre,
            widget=placeholder,
            texto_menu=texto_menu,
            icono=icono,
            habilitar_boton=habilitado
        )
    
    def _mostrar_modulo_por_nombre(self, nombre):
        """Muestra un módulo específico por su nombre"""
        if nombre in self.modulos:
            info = self.modulos[nombre]
            self._mostrar_modulo(info["indice"], info["texto_menu"])