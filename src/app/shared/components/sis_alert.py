"""
SisAlert - Componente de alertas visuales no intrusivas
Equivalente al sisvenin-alert.tsx de React

Características:
- Fondo especial según tipo:
  - stock: #FFEBEE (rojo muy claro) + borde izquierdo #D32F2F
  - expiry: #FFF3E0 (naranja muy claro) + borde izquierdo #FF9800
- Border radius: 8px
- Clickeable (cursor: pointer)
- Hover: opacidad 0.9
- Ícono a la izquierda:
  - stock: 📦 o 🔴
  - expiry: ⚠️

Ejemplos:
    alerta = SisAlert(
        type="stock",
        text="Stock bajo: Leche evaporada (stock: 2)",
        on_click=lambda: navegar_a_producto(1)
    )
    
    alerta_vencimiento = SisAlert(
        type="expiry",
        text="Próximo a vencer: Yogur fresa (vence: 28/05/2026)",
        on_click=lambda: navegar_a_producto(4)
    )
"""

from typing import Optional, Callable
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
    QPushButton, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor


class SisAlert(QPushButton):
    """
    Alerta visual clickeable de SISVENIN.
    Sigue el diseño del Prompt 0 de Figma (igual al React).
    
    Características:
    - No intrusiva (no bloquea la interacción)
    - Clickeable para navegar al producto
    - Colores según tipo (stock bajo / vencimiento)
    
    Tipos:
        "stock": Stock bajo (<5 unidades) - fondo #FFEBEE, borde #D32F2F, ícono 📦
        "expiry": Próximo a vencer (<7 días) - fondo #FFF3E0, borde #FF9800, ícono ⚠️
    """
    
    # Constantes de estilo (Prompt 0)
    _BORDER_RADIUS = 8
    _PADDING_VERTICAL = 12
    _PADDING_HORIZONTAL = 16
    
    # Colores para alerta de STOCK
    _STOCK_BG = "#FFEBEE"
    _STOCK_BORDER = "#D32F2F"
    _STOCK_ICON = "📦"
    
    # Colores para alerta de VENCIMIENTO
    _EXPIRY_BG = "#FFF3E0"
    _EXPIRY_BORDER = "#FF9800"
    _EXPIRY_ICON = "⚠️"
    
    # Colores comunes
    _TEXTO_COLOR = "#212121"
    _HOVER_OPACITY = "0.9"
    
    def __init__(
        self,
        type: str,  # "stock" o "expiry"
        text: str,
        on_click: Optional[Callable] = None,
        parent=None
    ):
        """
        Inicializa la alerta.
        
        Args:
            type: Tipo de alerta ("stock" o "expiry")
            text: Texto de la alerta
            on_click: Función a llamar al hacer clic
            parent: Widget padre
        """
        super().__init__(parent)
        
        self._alert_type = type
        self._text = text
        
        # Configurar botón
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(48)
        
        if on_click:
            self.clicked.connect(on_click)
        
        self._setup_ui()
        self._apply_style()
    
    def _setup_ui(self):
        """Configura la UI de la alerta"""
        # Layout principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            self._PADDING_HORIZONTAL, 
            self._PADDING_VERTICAL,
            self._PADDING_HORIZONTAL, 
            self._PADDING_VERTICAL
        )
        layout.setSpacing(12)
        
        # Ícono según tipo
        icono_texto = self._STOCK_ICON if self._alert_type == "stock" else self._EXPIRY_ICON
        self._icon_label = QLabel(icono_texto)
        self._icon_label.setFixedSize(20, 20)
        self._icon_label.setAlignment(Qt.AlignCenter)
        self._icon_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self._icon_label)
        
        # Texto
        self._text_label = QLabel(self._text)
        self._text_label.setWordWrap(True)
        self._text_label.setStyleSheet(f"""
            font-size: 14px;
            color: {self._TEXTO_COLOR};
            line-height: 1.4;
        """)
        layout.addWidget(self._text_label, 1)
        
        # Flecha indicadora (opcional, como en React)
        self._arrow_label = QLabel("→")
        self._arrow_label.setStyleSheet("""
            font-size: 14px;
            color: #757575;
        """)
        layout.addWidget(self._arrow_label)
    
    def _apply_style(self):
        """Aplica los estilos CSS según el tipo de alerta"""
        if self._alert_type == "stock":
            bg_color = self._STOCK_BG
            border_color = self._STOCK_BORDER
        else:  # expiry
            bg_color = self._EXPIRY_BG
            border_color = self._EXPIRY_BORDER
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                border-left: 4px solid {border_color};
                border-radius: {self._BORDER_RADIUS}px;
                text-align: left;
                font-family: 'Roboto', 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{
                opacity: {self._HOVER_OPACITY};
            }}
            QPushButton:pressed {{
                opacity: 0.8;
            }}
        """)
    
    def set_text(self, text: str):
        """
        Actualiza el texto de la alerta.
        
        Args:
            text: Nuevo texto
        """
        self._text = text
        self._text_label.setText(text)
    
    def get_text(self) -> str:
        """Retorna el texto de la alerta"""
        return self._text
    
    def get_alert_type(self) -> str:
        """Retorna el tipo de alerta ("stock" o "expiry")"""
        return self._alert_type


class SisAlertList(QWidget):
    """
    Contenedor para lista de alertas.
    Agrupa múltiples alertas con espaciado adecuado.
    
    Ejemplo:
        alertas = SisAlertList()
        alertas.add_alert("stock", "Stock bajo: Leche (stock: 2)", lambda: print("Ir a Leche"))
        alertas.add_alert("expiry", "Vence pronto: Yogur (vence: 28/05)", lambda: print("Ir a Yogur"))
    """
    
    def __init__(self, parent=None):
        """Inicializa el contenedor de alertas"""
        super().__init__(parent)
        
        self._alerts: list[SisAlert] = []
        
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(12)
    
    def add_alert(
        self,
        type: str,
        text: str,
        on_click: Optional[Callable] = None
    ) -> SisAlert:
        """
        Agrega una nueva alerta al contenedor.
        
        Args:
            type: Tipo de alerta ("stock" o "expiry")
            text: Texto de la alerta
            on_click: Función al hacer clic
            
        Returns:
            SisAlert: La alerta creada
        """
        alerta = SisAlert(type, text, on_click, parent=self)
        self._alerts.append(alerta)
        self._layout.addWidget(alerta)
        return alerta
    
    def clear(self):
        """Limpia todas las alertas del contenedor"""
        for alerta in self._alerts:
            alerta.deleteLater()
        self._alerts.clear()
    
    def count(self) -> int:
        """Retorna el número de alertas"""
        return len(self._alerts)
    
    def remove_alert(self, index: int):
        """
        Elimina una alerta por índice.
        
        Args:
            index: Índice de la alerta a eliminar
        """
        if 0 <= index < len(self._alerts):
            alerta = self._alerts.pop(index)
            alerta.deleteLater()
    
    def is_empty(self) -> bool:
        """Retorna True si no hay alertas"""
        return len(self._alerts) == 0
    
    def get_alerts(self) -> list[SisAlert]:
        """Retorna la lista de alertas"""
        return self._alerts.copy()


class SisEmptyState(QWidget):
    """
    Estado vacío para cuando no hay alertas.
    Muestra un mensaje amigable indicando que todo está en orden.
    
    Ejemplo:
        empty = SisEmptyState(
            message="¡Todo en orden! No hay productos con stock bajo ni próximos a vencer."
        )
    """
    
    _COLOR_PRIMARIO = "#2E7D32"
    _COLOR_TEXTO_SECUNDARIO = "#757575"
    
    def __init__(
        self,
        message: str = "¡Todo en orden! No hay productos con stock bajo ni próximos a vencer.",
        icon: str = "✅",
        parent=None
    ):
        """
        Inicializa el estado vacío.
        
        Args:
            message: Mensaje a mostrar
            icon: Emoji o texto del ícono
            parent: Widget padre
        """
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 32, 0, 32)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignCenter)
        
        # Ícono
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            font-size: 40px;
            color: {self._COLOR_PRIMARIO};
        """)
        layout.addWidget(icon_label)
        
        # Mensaje
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet(f"""
            font-size: 14px;
            color: {self._COLOR_TEXTO_SECUNDARIO};
            line-height: 1.4;
        """)
        layout.addWidget(message_label)