"""
SisCard - Componente de tarjeta compartido
Equivalente al sisvenin-card.tsx de React

Características:
- Fondo blanco (#FFFFFF)
- Border radius: 12px
- Borde: 1px sólido #F0F0F0
- Sombra suave (como en React)
- Padding interno: 16px (por defecto)

Variantes:
- SisCard: Tarjeta genérica para cualquier contenido
- SisMetricCard: Tarjeta específica para métricas (con valor destacado)
"""

from typing import Optional
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect


class SisCard(QFrame):
    """
    Tarjeta estándar de SISVENIN.
    Sigue el diseño del Prompt 0 de Figma (igual al React).
    
    Ejemplos:
        tarjeta = SisCard()
        tarjeta.setLayout(layout_con_contenido)
        
        # O con título
        tarjeta = SisCard(title="Mi título")
        tarjeta.set_content(widget_contenido)
    """
    
    # Constantes de estilo (Prompt 0)
    _COLOR_TARJETA = "#FFFFFF"
    _COLOR_BORDE = "#F0F0F0"
    _BORDER_RADIUS = 12
    _PADDING = 16
    
    def __init__(
        self,
        title: Optional[str] = None,
        padding: int = None,
        parent=None
    ):
        """
        Inicializa la tarjeta.
        
        Args:
            title: Título opcional de la tarjeta
            padding: Padding interno (por defecto 16px)
            parent: Widget padre
        """
        super().__init__(parent)
        
        self._padding = padding if padding is not None else self._PADDING
        
        # Configurar frame
        self.setFrameShape(QFrame.NoFrame)
        self._setup_style()
        
        # Layout principal
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(self._padding, self._padding, 
                                            self._padding, self._padding)
        self._main_layout.setSpacing(self._padding)
        
        # Título opcional
        self._title_label = None
        if title:
            self.set_title(title)
    
    def _setup_style(self):
        """Configura el estilo de la tarjeta (sombra, bordes, etc.)"""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self._COLOR_TARJETA};
                border-radius: {self._BORDER_RADIUS}px;
                border: 1px solid {self._COLOR_BORDE};
            }}
        """)
        
        # Aplicar sombra suave (como en React)
        self._aplicar_sombra()
    
    def _aplicar_sombra(self):
        """Aplica la sombra suave (como en React)"""
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(12)
        sombra.setXOffset(0)
        sombra.setYOffset(2)
        # rgba(0,0,0,0.08) - 30/255 ≈ 0.12, ajustamos a 20 para 0.08
        sombra.setColor(QColor(0, 0, 0, 20))  # alpha 20/255 ≈ 0.08
        self.setGraphicsEffect(sombra)
    
    def set_title(self, title: str):
        """
        Establece el título de la tarjeta.
        
        Args:
            title: Texto del título
        """
        if self._title_label is None:
            self._title_label = QLabel(title)
            self._title_label.setWordWrap(True)
            self._title_label.setStyleSheet("""
                font-size: 18px;
                font-weight: 600;
                color: #212121;
            """)
            self._main_layout.insertWidget(0, self._title_label)
        else:
            self._title_label.setText(title)
    
    def set_content(self, widget: QWidget):
        """
        Establece el contenido de la tarjeta.
        
        Args:
            widget: Widget a colocar dentro de la tarjeta
        """
        # Limpiar contenido anterior (excepto título)
        for i in reversed(range(self._main_layout.count())):
            item = self._main_layout.itemAt(i)
            if item.widget() and item.widget() != self._title_label:
                item.widget().deleteLater()
        
        self._main_layout.addWidget(widget)
    
    def add_widget(self, widget: QWidget):
        """
        Agrega un widget al final del contenido.
        
        Args:
            widget: Widget a agregar
        """
        self._main_layout.addWidget(widget)
    
    def clear(self):
        """Limpia todo el contenido de la tarjeta (incluyendo título)"""
        for i in reversed(range(self._main_layout.count())):
            item = self._main_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        self._title_label = None
    
    def get_layout(self) -> QVBoxLayout:
        """
        Retorna el layout interno para agregar widgets directamente.
        
        Returns:
            QVBoxLayout: Layout de la tarjeta
        """
        return self._main_layout


class SisMetricCard(SisCard):
    """
    Tarjeta específica para métricas (como Ganancia del Día, Total Ventas).
    Sigue el diseño del SisMetricCard en React.
    
    Características adicionales:
    - Valor destacado (más grande)
    - Color especial para valores positivos
    - Ícono opcional
    
    Ejemplos:
        tarjeta_ganancia = SisMetricCard(
            label="GANANCIA ESTIMADA DEL DÍA",
            value="S/ 247.50",
            sub_value="Basado en 3 ventas",
            highlight=True
        )
    """
    
    # Tamaños de fuente (Prompt 0)
    _FONT_SIZE_NORMAL = "24px"
    _FONT_SIZE_HIGHLIGHT = "32px"
    _FONT_SIZE_LABEL = "18px"
    
    _COLOR_HIGHLIGHT = "#2E7D32"
    _COLOR_NORMAL = "#212121"
    _COLOR_LABEL = "#757575"
    
    def __init__(
        self,
        label: str,
        value: str,
        sub_value: Optional[str] = None,
        highlight: bool = False,
        icon: Optional[str] = None,
        parent=None
    ):
        """
        Inicializa la tarjeta de métrica.
        
        Args:
            label: Etiqueta descriptiva (ej: "GANANCIA ESTIMADA DEL DÍA")
            value: Valor principal (ej: "S/ 247.50")
            sub_value: Texto secundario opcional
            highlight: Si es True, el valor se muestra en verde y más grande
            icon: Emoji o texto para ícono (ej: "💰")
            parent: Widget padre
        """
        super().__init__(parent=parent)
        
        self._highlight = highlight
        
        # Layout principal
        layout = QVBoxLayout(self.get_layout())
        layout.setSpacing(12)
        
        # Fila superior: label + ícono
        header_layout = QHBoxLayout()
        
        self._label = QLabel(label)
        self._label.setWordWrap(True)
        self._label.setStyleSheet(f"""
            font-size: {self._FONT_SIZE_LABEL};
            font-weight: 600;
            color: {self._COLOR_LABEL};
            letter-spacing: 0.5px;
        """)
        header_layout.addWidget(self._label)
        header_layout.addStretch()
        
        if icon:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 20px;")
            header_layout.addWidget(icon_label)
        
        layout.addLayout(header_layout)
        
        # Valor principal
        self._value_label = QLabel(value)
        self._value_label.setWordWrap(True)
        self._actualizar_estilo_valor()
        layout.addWidget(self._value_label)
        
        # Valor secundario (opcional)
        if sub_value:
            self._sub_value_label = QLabel(sub_value)
            self._sub_value_label.setWordWrap(True)
            self._sub_value_label.setStyleSheet(f"""
                font-size: 14px;
                color: {self._COLOR_LABEL};
            """)
            layout.addWidget(self._sub_value_label)
    
    def _actualizar_estilo_valor(self):
        """Actualiza el estilo del valor según si está destacado o no"""
        if self._highlight:
            font_size = self._FONT_SIZE_HIGHLIGHT
            color = self._COLOR_HIGHLIGHT
        else:
            font_size = self._FONT_SIZE_NORMAL
            color = self._COLOR_NORMAL
        
        self._value_label.setStyleSheet(f"""
            font-size: {font_size};
            font-weight: 700;
            color: {color};
            line-height: 1.1;
        """)
    
    def set_value(self, value: str, highlight: bool = None):
        """
        Actualiza el valor mostrado.
        
        Args:
            value: Nuevo valor
            highlight: Si es True, el valor se muestra destacado
        """
        self._value_label.setText(value)
        if highlight is not None:
            self._highlight = highlight
            self._actualizar_estilo_valor()
    
    def set_sub_value(self, sub_value: str):
        """
        Actualiza el valor secundario.
        
        Args:
            sub_value: Nuevo texto secundario
        """
        if hasattr(self, '_sub_value_label'):
            self._sub_value_label.setText(sub_value)
        else:
            self._sub_value_label = QLabel(sub_value)
            self._sub_value_label.setStyleSheet(f"""
                font-size: 14px;
                color: {self._COLOR_LABEL};
            """)
            self.get_layout().addWidget(self._sub_value_label)
    
    def set_label(self, label: str):
        """
        Actualiza la etiqueta.
        
        Args:
            label: Nueva etiqueta
        """
        self._label.setText(label)
        
# Alias para mantener consistencia con los nombres de React
SisCard = SisCard
SisMetricCard = SisMetricCard