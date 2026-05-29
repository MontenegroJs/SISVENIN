"""
BarraBusqueda - Componente de búsqueda para la vista de Productos
Equivalente a la sección de búsqueda en productos-page.tsx de React

Características:
- Input de búsqueda con ícono 🔍
- Botón "Nuevo Producto" (primario)
- Mismo estilo que en React
- Focus con borde verde y sombra
"""

from typing import Optional, Callable
from PySide6.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel, QLineEdit
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor

from src.app.shared.components.sis_button import SisButton
from src.app.base_layout import BaseLayout


class BarraBusqueda(QWidget):
    """
    Barra de búsqueda y acción para la gestión de productos.
    Sigue el diseño del Prompt 0 de Figma (igual al React).
    
    Incluye:
    - Input de búsqueda con ícono 🔍
    - Botón "Nuevo Producto" (verde, primario)
    
    Ejemplo:
        barra = BarraBusqueda()
        barra.textChanged.connect(lambda texto: filtrar_productos(texto))
        barra.nuevoClicked.connect(lambda: abrir_formulario_nuevo())
    """
    
    # Señales
    textChanged = Signal(str)      # Se emite cuando cambia el texto de búsqueda
    nuevoClicked = Signal()        # Se emite cuando se hace clic en "Nuevo Producto"
    returnPressed = Signal()       # Se emite cuando se presiona Enter en la búsqueda
    
    def __init__(
        self,
        placeholder: str = "Buscar producto por nombre...",
        parent=None
    ):
        """
        Inicializa la barra de búsqueda.
        
        Args:
            placeholder: Texto de placeholder del input
            parent: Widget padre
        """
        super().__init__(parent)
        
        self._placeholder = placeholder
        self._search_timer: Optional[QTimer] = None
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Configura la interfaz de la barra de búsqueda"""
        # Contenedor principal con estilo de tarjeta (como en React)
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {BaseLayout.COLOR_TARJETA};
                border-radius: {BaseLayout.BORDER_RADIUS_TARJETA}px;
                border: 1px solid #F0F0F0;
            }}
        """)
        
        # Aplicar sombra suave (como en React)
        from PySide6.QtWidgets import QGraphicsDropShadowEffect
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(8)
        sombra.setXOffset(0)
        sombra.setYOffset(2)
        sombra.setColor(QColor(0, 0, 0, 30))  # rgba(0,0,0,0.05)
        container.setGraphicsEffect(sombra)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(20, 4, 20, 4)
        layout.setSpacing(16)
        
        # Contenedor del input de búsqueda (con ícono)
        search_container = QFrame()
        search_container.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(8)
        
        # Ícono de búsqueda
        self._icon_label = QLabel("🔍")
        self._icon_label.setStyleSheet(f"""
            font-size: 18px;
            color: {BaseLayout.COLOR_PLACEHOLDER};
        """)
        search_layout.addWidget(self._icon_label)
        
        # Input de búsqueda
        self._input = QLineEdit()
        self._input.setPlaceholderText(self._placeholder)
        self._input.setStyleSheet(self._estilo_input())
        self._input.setMinimumHeight(48)
        self._input.setCursor(Qt.IBeamCursor)
        search_layout.addWidget(self._input, 1)
        
        layout.addWidget(search_container, 1)
        
        # Botón Nuevo Producto (primario) - con ícono ➕ como en React
        self._btn_nuevo = SisButton(
            texto="Nuevo Producto",
            variant="primary",
            icono="➕"  # Ícono de más como en React
        )
        self._btn_nuevo.setMinimumWidth(160)
        layout.addWidget(self._btn_nuevo)
        
        # Layout principal
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
    
    def _estilo_input(self) -> str:
        """Estilo del input de búsqueda (con focus verde y sombra como en React)"""
        return f"""
            QLineEdit {{
                font-size: 14px;
                padding: 12px 12px 12px 8px;
                border: 1px solid {BaseLayout.COLOR_BORDE};
                border-radius: {BaseLayout.BORDER_RADIUS_INPUT}px;
                background-color: white;
                min-height: 48px;
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
            }}
            QLineEdit:focus {{
                border: 2px solid {BaseLayout.COLOR_PRIMARIO};
                outline: none;
            }}
            QLineEdit::placeholder {{
                color: {BaseLayout.COLOR_PLACEHOLDER};
            }}
        """
    
    def _connect_signals(self):
        """Conecta las señales internas"""
        self._input.textChanged.connect(self._on_text_changed)
        self._input.returnPressed.connect(self.returnPressed.emit)
        self._btn_nuevo.clicked.connect(self.nuevoClicked.emit)
    
    def _on_text_changed(self, texto: str):
        """
        Maneja el cambio de texto con debounce.
        Similar al comportamiento de React (retraso en la búsqueda)
        """
        # Usar debounce para evitar muchas búsquedas mientras se escribe
        if self._search_timer:
            self._search_timer.stop()
        
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(lambda: self.textChanged.emit(texto))
        self._search_timer.start(300)  # 300ms de debounce
    
    # ==================== MÉTODOS PÚBLICOS ====================
    
    def text(self) -> str:
        """
        Retorna el texto actual de búsqueda.
        
        Returns:
            str: Texto ingresado en el input
        """
        return self._input.text()
    
    def set_text(self, texto: str):
        """
        Establece el texto de búsqueda programáticamente.
        
        Args:
            texto: Texto a establecer
        """
        self._input.setText(texto)
    
    def clear(self):
        """Limpia el texto de búsqueda"""
        self._input.clear()
    
    def set_placeholder(self, placeholder: str):
        """
        Cambia el texto de placeholder.
        
        Args:
            placeholder: Nuevo texto de placeholder
        """
        self._placeholder = placeholder
        self._input.setPlaceholderText(placeholder)
    
    def set_focus(self):
        """Establece el foco en el input de búsqueda"""
        self._input.setFocus()
    
    def set_nuevo_enabled(self, enabled: bool):
        """
        Habilita o deshabilita el botón "Nuevo Producto".
        
        Args:
            enabled: True para habilitar, False para deshabilitar
        """
        self._btn_nuevo.setEnabled(enabled)
    
    def get_input(self) -> QLineEdit:
        """
        Retorna el input interno para configuraciones avanzadas.
        
        Returns:
            QLineEdit: Input de búsqueda
        """
        return self._input
    
    def get_button(self) -> SisButton:
        """
        Retorna el botón interno para configuraciones avanzadas.
        
        Returns:
            SisButton: Botón "Nuevo Producto"
        """
        return self._btn_nuevo


class BarraBusquedaConFiltro(BarraBusqueda):
    """
    Extensión de BarraBusqueda que incluye filtros adicionales.
    Útil para cuando se necesitan más opciones de búsqueda.
    
    Características adicionales:
    - Selector de filtro (por nombre, por código, etc.)
    - Botón de limpiar búsqueda
    
    Ejemplo:
        barra = BarraBusquedaConFiltro(
            filtros=["Nombre", "Código", "Categoría"],
            mostrar_limpiar=True
        )
        barra.filtroChanged.connect(lambda filtro: print(f"Filtro: {filtro}"))
    """
    
    # Señales adicionales
    filtroChanged = Signal(str)      # Se emite cuando cambia el tipo de filtro
    limpiarClicked = Signal()        # Se emite cuando se hace clic en limpiar
    
    def __init__(
        self,
        filtros: Optional[list] = None,
        mostrar_limpiar: bool = False,
        placeholder: str = "Buscar producto...",
        parent=None
    ):
        """
        Inicializa la barra de búsqueda con filtros.
        
        Args:
            filtros: Lista de opciones para el filtro (ej: ["Nombre", "Código"])
            mostrar_limpiar: Si es True, muestra un botón para limpiar
            placeholder: Texto de placeholder
            parent: Widget padre
        """
        self._filtros = filtros or ["Nombre"]
        self._mostrar_limpiar = mostrar_limpiar
        self._filtro_actual = self._filtros[0] if self._filtros else ""
        
        super().__init__(placeholder=placeholder, parent=parent)
        
        # Reconfigurar UI para incluir filtros si se proporcionan
        if len(self._filtros) > 1 or self._mostrar_limpiar:
            self._setup_filtros()
    
    def _setup_filtros(self):
        """Agrega los componentes de filtro a la UI"""
        from src.app.shared.components.sis_select import SisSelect
        
        # Obtener el contenedor principal
        container = self.findChild(QFrame)
        if not container:
            return
        
        # Limpiar el layout existente
        layout = container.layout()
        if not layout:
            return
        
        # Crear nuevo layout con filtros
        nuevo_layout = QHBoxLayout(container)
        nuevo_layout.setContentsMargins(20, 4, 20, 4)
        nuevo_layout.setSpacing(12)
        
        # Select de filtro
        if len(self._filtros) > 1:
            self._select_filtro = SisSelect(
                items=self._filtros,
                placeholder="Filtrar por..."
            )
            self._select_filtro.currentTextChanged.connect(self._on_filtro_cambiado)
            nuevo_layout.addWidget(self._select_filtro)
        
        # Input de búsqueda (expandible)
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)
        
        icon_label = QLabel("🔍")
        icon_label.setStyleSheet(f"font-size: 18px; color: {BaseLayout.COLOR_PLACEHOLDER};")
        search_layout.addWidget(icon_label)
        
        search_layout.addWidget(self._input, 1)
        nuevo_layout.addLayout(search_layout, 1)
        
        # Botón limpiar (opcional)
        if self._mostrar_limpiar:
            from src.app.shared.components.sis_button import SisButton
            self._btn_limpiar = SisButton(
                texto="Limpiar",
                variant="secondary",
                icono="🗑️"
            )
            self._btn_limpiar.clicked.connect(self._on_limpiar_clicked)
            nuevo_layout.addWidget(self._btn_limpiar)
        
        # Botón Nuevo Producto
        nuevo_layout.addWidget(self._btn_nuevo)
        
        # Reemplazar el layout
        old_widgets = []
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                old_widgets.append(item.widget())
        
        for w in old_widgets:
            if w not in [self._input, self._btn_nuevo]:
                w.deleteLater()
    
    def _on_filtro_cambiado(self, texto: str):
        """Maneja el cambio de filtro"""
        self._filtro_actual = texto
        self.filtroChanged.emit(texto)
    
    def _on_limpiar_clicked(self):
        """Maneja el clic en limpiar"""
        self.clear()
        self.limpiarClicked.emit()
    
    def get_filtro_actual(self) -> str:
        """Retorna el filtro actual seleccionado"""
        return self._filtro_actual