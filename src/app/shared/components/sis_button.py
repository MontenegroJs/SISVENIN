"""
SisButton - Componente de botón compartido
Equivalente al sisvenin-button.tsx de React

Variantes:
- primary: Botón verde (#2E7D32) para acciones principales (Confirmar Venta, Guardar)
- secondary: Botón gris con borde para acciones secundarias (Cancelar, Cerrar)
- danger: Botón rojo (#D32F2F) para acciones destructivas (Eliminar)

Tamaños (seguir estándar React):
- Altura mínima: 48px (primary/secondary)
- Altura mínima: 40px (danger)
- Border radius: 8px
- Padding: 12px 24px
"""

from typing import Optional, Callable
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon


class SisButton(QPushButton):
    """
    Botón del sistema SISVENIN.
    Sigue el diseño del Prompt 0 de Figma.
    
    Variantes:
        primary: Verde #2E7D32 (acciones principales)
        secondary: Transparente con borde gris (acciones secundarias)
        danger: Rojo #D32F2F (acciones destructivas)
    
    Ejemplos:
        btn_guardar = SisButton("Guardar", variant="primary")
        btn_cancelar = SisButton("Cancelar", variant="secondary")
        btn_eliminar = SisButton("Eliminar", variant="danger")
    """
    
    # Constantes de estilo (usando colores del Prompt 0)
    _COLOR_PRIMARIO = "#2E7D32"
    _COLOR_PRIMARIO_HOVER = "#1B5E20"
    _COLOR_PRIMARIO_DESABILITADO = "#A5D6A7"
    
    _COLOR_PELIGRO = "#D32F2F"
    _COLOR_PELIGRO_HOVER = "#C62828"
    
    _COLOR_TEXTO_SECUNDARIO = "#757575"
    _COLOR_BORDE = "#E0E0E0"
    _COLOR_FONDO_VENTANA = "#F5F5F5"
    
    def __init__(
        self,
        texto: str,
        variant: str = "primary",
        icono: Optional[str] = None,
        enabled: bool = True,
        onClick: Optional[Callable] = None,
        parent=None
    ):
        """
        Inicializa el botón.
        
        Args:
            texto: Texto del botón
            variant: "primary", "secondary" o "danger"
            icono: Emoji o texto para ícono (ej: "✅", "➕")
            enabled: Si el botón está habilitado inicialmente
            onClick: Función a llamar al hacer clic
            parent: Widget padre
        """
        # Construir texto con ícono si se proporciona
        texto_final = f"{icono} {texto}" if icono else texto
        
        super().__init__(texto_final, parent)
        
        self._variant = variant
        self._setup_style()
        
        self.setCursor(Qt.PointingHandCursor)
        self.setEnabled(enabled)
        
        if onClick:
            self.clicked.connect(onClick)
    
    def _setup_style(self):
        """Configura el estilo según la variante (exacto al React)"""
        if self._variant == "primary":
            self._setup_primary_style()
        elif self._variant == "secondary":
            self._setup_secondary_style()
        elif self._variant == "danger":
            self._setup_danger_style()
        else:
            raise ValueError(f"Variante inválida: {self._variant}. Use 'primary', 'secondary' o 'danger'")
    
    def _setup_primary_style(self):
        """Estilo para botón primario (verde, grande)"""
        self.setProperty("type", "primary")
        self.setMinimumHeight(48)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._COLOR_PRIMARIO};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                font-family: 'Roboto', 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{
                background-color: {self._COLOR_PRIMARIO_HOVER};
            }}
            QPushButton:pressed {{
                background-color: #145218;
            }}
            QPushButton:disabled {{
                background-color: {self._COLOR_PRIMARIO_DESABILITADO};
                color: {self._COLOR_TEXTO_SECUNDARIO};
            }}
        """)
    
    def _setup_secondary_style(self):
        """Estilo para botón secundario (gris borde)"""
        self.setProperty("type", "secondary")
        self.setMinimumHeight(48)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {self._COLOR_TEXTO_SECUNDARIO};
                border: 1px solid {self._COLOR_BORDE};
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                font-family: 'Roboto', 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{
                background-color: {self._COLOR_FONDO_VENTANA};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
            }}
        """)
    
    def _setup_danger_style(self):
        """Estilo para botón peligro (rojo)"""
        self.setProperty("type", "danger")
        self.setMinimumHeight(40)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._COLOR_PELIGRO};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 600;
                font-family: 'Roboto', 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{
                background-color: {self._COLOR_PELIGRO_HOVER};
            }}
            QPushButton:disabled {{
                opacity: 0.6;
            }}
        """)
    
    def set_variant(self, variant: str):
        """
        Cambia la variante del botón en tiempo de ejecución.
        
        Args:
            variant: "primary", "secondary" o "danger"
        """
        self._variant = variant
        self._setup_style()
    
    def set_icon_text(self, icono: str, texto: str):
        """
        Actualiza el ícono y texto del botón.
        
        Args:
            icono: Emoji o texto del ícono
            texto: Texto principal
        """
        self.setText(f"{icono} {texto}")


class SisIconButton(QPushButton):
    """
    Botón de ícono (36x36) para acciones en tablas.
    Equivalente al SisIconButton de React.
    
    Ejemplos:
        btn_editar = SisIconButton("✏️", tooltip="Editar")
        btn_eliminar = SisIconButton("🗑️", tooltip="Eliminar")
    """
    
    _COLOR_TEXTO = "#757575"
    _COLOR_TEXTO_HOVER = "#212121"
    _COLOR_FONDO_VENTANA = "#F5F5F5"
    _COLOR_BORDE = "#E0E0E0"
    
    def __init__(
        self,
        icono: str,
        tooltip: str = "",
        onClick: Optional[Callable] = None,
        parent=None
    ):
        """
        Inicializa el botón de ícono.
        
        Args:
            icono: Emoji o texto del ícono (ej: "✏️", "🗑️")
            tooltip: Texto que aparece al hacer hover
            onClick: Función a llamar al hacer clic
            parent: Widget padre
        """
        super().__init__(icono, parent)
        
        self.setFixedSize(36, 36)
        self.setCursor(Qt.PointingHandCursor)
        
        if tooltip:
            self.setToolTip(tooltip)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {self._COLOR_BORDE};
                border-radius: 8px;
                font-size: 14px;
                color: {self._COLOR_TEXTO};
            }}
            QPushButton:hover {{
                background-color: {self._COLOR_FONDO_VENTANA};
                color: {self._COLOR_TEXTO_HOVER};
            }}
        """)
        
        if onClick:
            self.clicked.connect(onClick)