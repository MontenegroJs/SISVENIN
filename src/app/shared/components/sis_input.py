"""
SisInput - Componente de input compartido
Equivalente al sisvenin-input.tsx de React

Características:
- Borde: 1px sólido #E0E0E0
- Border radius: 8px
- Padding: 12px
- Altura: 48px (fácil de tocar)
- Focus: borde #2E7D32 (2px) + sombra suave
- Placeholder: #BDBDBD

Variantes:
- SisInput: Input de texto estándar
- SisNumberInput: Input numérico (con alineación derecha)

Nota: SisSelect ahora está en su propio archivo sis_select.py
"""

from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel,
    QDoubleSpinBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor


class SisInput(QWidget):
    """
    Input de texto estándar de SISVENIN.
    Sigue el diseño del Prompt 0 de Figma (igual al React).
    
    Características:
    - Focus con borde verde (#2E7D32) y sombra
    - Altura mínima 48px
    - Label opcional arriba
    
    Ejemplos:
        nombre_input = SisInput(placeholder="Nombre del producto")
        
        # Con label
        email_input = SisInput(label="Correo electrónico", placeholder="usuario@ejemplo.com")
        
        # Alineado a la derecha (para números)
        precio_input = SisInput(placeholder="0.00", align_right=True)
    """
    
    # Señales
    textChanged = Signal(str)
    returnPressed = Signal()
    
    # Constantes de estilo (Prompt 0)
    _COLOR_PRIMARIO = "#2E7D32"
    _COLOR_BORDE = "#E0E0E0"
    _COLOR_TEXTO = "#212121"
    _COLOR_PLACEHOLDER = "#BDBDBD"
    _BORDER_RADIUS = 8
    _ALTURA_MINIMA = 48
    
    def __init__(
        self,
        label: Optional[str] = None,
        placeholder: str = "",
        align_right: bool = False,
        parent=None
    ):
        """
        Inicializa el input.
        
        Args:
            label: Texto del label (opcional, aparece arriba)
            placeholder: Texto de placeholder
            align_right: Si es True, el texto se alinea a la derecha
            parent: Widget padre
        """
        super().__init__(parent)
        
        self._align_right = align_right
        self._focused = False
        
        # Layout principal
        if label:
            self._main_layout = QVBoxLayout(self)
            self._main_layout.setContentsMargins(0, 0, 0, 0)
            self._main_layout.setSpacing(8)
            
            self._label = QLabel(label)
            self._label.setStyleSheet("""
                font-size: 14px;
                font-weight: 600;
                color: #212121;
            """)
            self._main_layout.addWidget(self._label)
        else:
            self._main_layout = QHBoxLayout(self)
            self._main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Input interno
        self._input = QLineEdit()
        self._input.setPlaceholderText(placeholder)
        self._input.setMinimumHeight(self._ALTURA_MINIMA)
        
        if align_right:
            self._input.setAlignment(Qt.AlignRight)
        
        self._input.textChanged.connect(self.textChanged.emit)
        self._input.returnPressed.connect(self.returnPressed.emit)
        self._input.installEventFilter(self)
        
        self._actualizar_estilo()
        
        self._main_layout.addWidget(self._input)
    
    def _actualizar_estilo(self):
        """Actualiza el estilo del input según el estado de focus"""
        borde_color = self._COLOR_PRIMARIO if self._focused else self._COLOR_BORDE
        borde_width = "2px" if self._focused else "1px"
        
        self._input.setStyleSheet(f"""
            QLineEdit {{
                font-size: 14px;
                padding: 12px;
                border: {borde_width} solid {borde_color};
                border-radius: {self._BORDER_RADIUS}px;
                background-color: white;
                min-height: {self._ALTURA_MINIMA - 24}px;
                color: {self._COLOR_TEXTO};
            }}
            QLineEdit::placeholder {{
                color: {self._COLOR_PLACEHOLDER};
            }}
        """)
    
    def eventFilter(self, obj, event):
        """Captura eventos de focus para cambiar el estilo"""
        if obj == self._input:
            from PySide6.QtCore import QEvent
            if event.type() == QEvent.FocusIn:
                self._focused = True
                self._actualizar_estilo()
            elif event.type() == QEvent.FocusOut:
                self._focused = False
                self._actualizar_estilo()
        return super().eventFilter(obj, event)
    
    def text(self) -> str:
        """Retorna el texto actual del input"""
        return self._input.text()
    
    def set_text(self, text: str):
        """Establece el texto del input"""
        self._input.setText(text)
    
    def clear(self):
        """Limpia el texto del input"""
        self._input.clear()
    
    def set_placeholder(self, placeholder: str):
        """Establece el texto de placeholder"""
        self._input.setPlaceholderText(placeholder)
    
    def set_enabled(self, enabled: bool):
        """Habilita o deshabilita el input"""
        self._input.setEnabled(enabled)
    
    def set_focus(self):
        """Establece el foco en el input"""
        self._input.setFocus()
    
    def get_line_edit(self) -> QLineEdit:
        """Retorna el QLineEdit interno para configuraciones avanzadas"""
        return self._input


class SisNumberInput(QWidget):
    """
    Input numérico de SISVENIN.
    Clase independiente (no hereda de SisInput) para mayor robustez.
    
    Características adicionales:
    - Alineación derecha por defecto
    - Mínimo y máximo configurables
    - Prefijo y sufijo (ej: S/ , %)
    
    Ejemplos:
        cantidad = SisNumberInput(placeholder="0", min_value=0, max_value=999)
        precio = SisNumberInput(label="Precio", decimals=2, prefix="S/ ")
    """
    
    # Señales
    textChanged = Signal(str)
    valueChanged = Signal(float)
    
    # Constantes de estilo (Prompt 0)
    _COLOR_PRIMARIO = "#2E7D32"
    _COLOR_BORDE = "#E0E0E0"
    _COLOR_TEXTO = "#212121"
    _BORDER_RADIUS = 8
    _ALTURA_MINIMA = 48
    
    def __init__(
        self,
        label: Optional[str] = None,
        placeholder: str = "",
        min_value: float = 0,
        max_value: float = 999999.99,
        decimals: int = 2,
        prefix: str = "",
        suffix: str = "",
        parent=None
    ):
        """
        Inicializa el input numérico.
        
        Args:
            label: Texto del label (opcional, aparece arriba)
            placeholder: Texto de placeholder (no muestra nada, solo referencia)
            min_value: Valor mínimo permitido
            max_value: Valor máximo permitido
            decimals: Número de decimales
            prefix: Texto antes del valor (ej: "S/ ")
            suffix: Texto después del valor (ej: " %")
            parent: Widget padre
        """
        super().__init__(parent)
        
        self._focused = False
        
        # Layout principal
        if label:
            self._main_layout = QVBoxLayout(self)
            self._main_layout.setContentsMargins(0, 0, 0, 0)
            self._main_layout.setSpacing(8)
            
            self._label = QLabel(label)
            self._label.setStyleSheet("""
                font-size: 14px;
                font-weight: 600;
                color: #212121;
            """)
            self._main_layout.addWidget(self._label)
        else:
            self._main_layout = QHBoxLayout(self)
            self._main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Input numérico
        self._input = QDoubleSpinBox()
        self._input.setMinimum(min_value)
        self._input.setMaximum(max_value)
        self._input.setDecimals(decimals)
        self._input.setPrefix(prefix)
        self._input.setSuffix(suffix)
        self._input.setMinimumHeight(self._ALTURA_MINIMA)
        self._input.setAlignment(Qt.AlignRight)
        self._input.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self._input.setCorrectionMode(QDoubleSpinBox.CorrectToPreviousValue)
        
        # Placeholder: QDoubleSpinBox no soporta placeholder nativamente,
        # pero podemos usar setSpecialValueText o simplemente ignorarlo
        
        # Conectar señales
        self._input.textChanged.connect(self.textChanged.emit)
        self._input.valueChanged.connect(self.valueChanged.emit)
        self._input.installEventFilter(self)
        
        self._actualizar_estilo()
        
        self._main_layout.addWidget(self._input)
    
    def _actualizar_estilo(self):
        """Actualiza el estilo del input según el estado de focus"""
        borde_color = self._COLOR_PRIMARIO if self._focused else self._COLOR_BORDE
        borde_width = "2px" if self._focused else "1px"
        
        self._input.setStyleSheet(f"""
            QDoubleSpinBox {{
                font-size: 14px;
                padding: 12px;
                border: {borde_width} solid {borde_color};
                border-radius: {self._BORDER_RADIUS}px;
                background-color: white;
                min-height: {self._ALTURA_MINIMA - 24}px;
                color: {self._COLOR_TEXTO};
            }}
            QDoubleSpinBox:focus {{
                border: 2px solid {self._COLOR_PRIMARIO};
                outline: none;
            }}
        """)
    
    def eventFilter(self, obj, event):
        """Captura eventos de focus para cambiar el estilo"""
        if obj == self._input:
            from PySide6.QtCore import QEvent
            if event.type() == QEvent.FocusIn:
                self._focused = True
                self._actualizar_estilo()
            elif event.type() == QEvent.FocusOut:
                self._focused = False
                self._actualizar_estilo()
        return super().eventFilter(obj, event)
    
    def value(self) -> float:
        """Retorna el valor numérico actual"""
        return self._input.value()
    
    def set_value(self, value: float):
        """Establece el valor numérico"""
        self._input.setValue(value)
    
    def set_prefix(self, prefix: str):
        """Establece el prefijo (ej: S/ )"""
        self._input.setPrefix(prefix)
    
    def set_suffix(self, suffix: str):
        """Establece el sufijo (ej: %)"""
        self._input.setSuffix(suffix)
    
    def set_range(self, min_val: float, max_val: float):
        """Establece el rango de valores permitidos"""
        self._input.setMinimum(min_val)
        self._input.setMaximum(max_val)
    
    def set_decimals(self, decimals: int):
        """Establece el número de decimales"""
        self._input.setDecimals(decimals)
    
    def set_enabled(self, enabled: bool):
        """Habilita o deshabilita el input"""
        self._input.setEnabled(enabled)
    
    def set_focus(self):
        """Establece el foco en el input"""
        self._input.setFocus()
    
    def clear(self):
        """Limpia el valor (lo establece a 0)"""
        self._input.setValue(0)
    
    def get_spinbox(self) -> QDoubleSpinBox:
        """Retorna el QDoubleSpinBox interno para configuraciones avanzadas"""
        return self._input