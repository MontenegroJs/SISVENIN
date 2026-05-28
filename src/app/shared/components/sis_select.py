"""
SisSelect - Componente de select desplegable
Equivalente al sisvenin-select.tsx de React

Características:
- Mismo estilo que SisInput
- Ícono flecha abajo a la derecha
- Focus con borde verde (#2E7D32)
- Label opcional arriba
- Placeholder configurable

Ejemplos:
    select = SisSelect(label="Categoría")
    select.add_items(["Electrónicos", "Ropa", "Alimentos"])
    
    # Con placeholder personalizado
    select = SisSelect(placeholder="Seleccione un producto...")
    select.add_items(["Producto A", "Producto B"])
"""

from typing import Optional, List
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QColor


class SisSelect(QComboBox):
    """
    Select desplegable de SISVENIN.
    Sigue el diseño del Prompt 0 de Figma (igual al React).
    
    Características:
    - Mismo estilo que SisInput
    - Focus con borde verde (#2E7D32)
    - Altura mínima 48px
    - Label opcional
    
    Ejemplos:
        # Select simple
        select = SisSelect()
        select.add_items(["Opción 1", "Opción 2"])
        
        # Select con label
        select = SisSelect(label="Categoría")
        
        # Select con placeholder
        select = SisSelect(placeholder="Seleccione...")
    """
    
    # Constantes de estilo (Prompt 0)
    _COLOR_PRIMARIO = "#2E7D32"
    _COLOR_BORDE = "#E0E0E0"
    _COLOR_TEXTO = "#212121"
    _COLOR_FONDO = "white"
    _BORDER_RADIUS = 8
    _ALTURA = 48
    
    def __init__(
        self,
        label: Optional[str] = None,
        items: Optional[List[str]] = None,
        placeholder: str = "Seleccione una opción",
        parent=None
    ):
        """
        Inicializa el select.
        
        Args:
            label: Texto del label (opcional, aparece arriba)
            items: Lista inicial de opciones
            placeholder: Texto por defecto cuando no hay selección
            parent: Widget padre
        """
        super().__init__(parent)
        
        self._label = None
        self._label_widget = None
        self._focused = False
        self._placeholder = placeholder
        
        # Configurar estilo
        self.setMinimumHeight(self._ALTURA)
        self.setCursor(Qt.PointingHandCursor)
        
        # Configurar placeholder como primer item
        if placeholder:
            self.addItem(placeholder)
            self.setCurrentIndex(0)
        
        # Agregar items si se proporcionaron
        if items:
            self.add_items(items)
        
        # Instalar event filter para capturar focus
        self.installEventFilter(self)
        
        self._setup_ui(label)
        self._actualizar_estilo()
    
    def _setup_ui(self, label: Optional[str]):
        """
        Configura la UI con label opcional.
        
        Si se proporciona label, se crea un widget contenedor que incluye
        el label arriba y el select abajo.
        """
        if label:
            self._label_widget = QWidget()
            layout = QVBoxLayout(self._label_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(8)
            
            self._label = QLabel(label)
            self._label.setStyleSheet("""
                font-size: 14px;
                font-weight: 600;
                color: #212121;
            """)
            layout.addWidget(self._label)
            layout.addWidget(self)
    
    def _actualizar_estilo(self):
        """Actualiza el estilo según el estado de focus"""
        borde_color = self._COLOR_PRIMARIO if self._focused else self._COLOR_BORDE
        borde_width = "2px" if self._focused else "1px"
        
        self.setStyleSheet(f"""
            QComboBox {{
                font-size: 14px;
                padding: 12px;
                border: {borde_width} solid {borde_color};
                border-radius: {self._BORDER_RADIUS}px;
                background-color: {self._COLOR_FONDO};
                min-height: {self._ALTURA - 24}px;
                color: {self._COLOR_TEXTO};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid {self._COLOR_BORDE};
                border-radius: {self._BORDER_RADIUS}px;
                selection-background-color: {self._COLOR_PRIMARIO};
                selection-color: white;
            }}
        """)
    
    def eventFilter(self, obj, event):
        """Captura eventos de focus para cambiar el estilo"""
        if obj == self:
            if event.type() == QEvent.FocusIn:
                self._focused = True
                self._actualizar_estilo()
            elif event.type() == QEvent.FocusOut:
                self._focused = False
                self._actualizar_estilo()
        return super().eventFilter(obj, event)
    
    def add_items(self, items: List[str]):
        """
        Agrega múltiples items al select.
        
        Args:
            items: Lista de strings a agregar
        """
        # Limpiar placeholder si es el primer item agregado
        if self.count() == 1 and self.currentText() == self._placeholder:
            self.clear()
        
        for item in items:
            self.addItem(item)
    
    def set_items(self, items: List[str]):
        """
        Reemplaza todos los items del select.
        
        Args:
            items: Nueva lista de items
        """
        self.clear()
        self._focused = False
        self.add_items(items)
    
    def get_current_text(self) -> str:
        """Retorna el texto del item seleccionado"""
        return self.currentText()
    
    def get_current_index(self) -> int:
        """Retorna el índice del item seleccionado"""
        return self.currentIndex()
    
    def set_current_index(self, index: int):
        """Establece el índice seleccionado"""
        self.setCurrentIndex(index)
    
    def get_label_widget(self) -> Optional[QWidget]:
        """
        Retorna el widget contenedor con label (si existe).
        Útil para agregar a layouts.
        
        Returns:
            QWidget: Widget contenedor con label, o el mismo select si no hay label
        """
        return self._label_widget if self._label_widget else self
    
    def clear_selection(self):
        """Limpia la selección actual (vuelve al placeholder)"""
        self.setCurrentIndex(0)
    
    def is_placeholder_selected(self) -> bool:
        """Retorna True si el placeholder está seleccionado"""
        return self.currentIndex() == 0 and self.currentText() == self._placeholder