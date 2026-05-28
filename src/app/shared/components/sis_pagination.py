"""
SisPagination - Componente de paginación independiente
Puede ser usado con cualquier lista o tabla

Características:
- Botones anterior/siguiente con estilo SisIconButton
- Indicador de página actual
- Info de items mostrados (ej: "Mostrando 1-10 de 25 items")
- Totalmente personalizable via callbacks

Ejemplos:
    # Uso básico
    pagination = SisPagination(
        total_items=100,
        items_per_page=10,
        current_page=1,
        on_page_change=lambda page: print(f"Página {page}")
    )
    
    # Integración con una lista
    def cargar_pagina(page):
        start = (page - 1) * items_por_pagina
        end = start + items_por_pagina
        datos = todos_datos[start:end]
        actualizar_tabla(datos)
"""

from typing import Optional, Callable
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

from src.app.shared.components.sis_button import SisIconButton


class SisPagination(QWidget):
    """
    Componente de paginación independiente de SISVENIN.
    Sigue el diseño del Prompt 0 de Figma.
    
    Características:
    - Diseño consistente con el resto de la aplicación
    - Totalmente desacoplado (no depende de ninguna tabla específica)
    - Callback personalizable para cambios de página
    """
    
    # Constantes de estilo
    _COLOR_TEXTO_INFO = "#757575"
    _COLOR_TEXTO_PAGINA = "#212121"
    _FONT_SIZE = 13
    
    def __init__(
        self,
        total_items: int = 0,
        items_per_page: int = 10,
        current_page: int = 1,
        on_page_change: Optional[Callable[[int], None]] = None,
        parent=None
    ):
        """
        Inicializa el componente de paginación.
        
        Args:
            total_items: Número total de items
            items_per_page: Items por página (default 10)
            current_page: Página actual (default 1)
            on_page_change: Callback llamado cuando cambia la página
                           Recibe el nuevo número de página como argumento
            parent: Widget padre
        """
        super().__init__(parent)
        
        self._total_items = total_items
        self._items_per_page = items_per_page
        self._current_page = current_page
        self._on_page_change = on_page_change
        
        self._setup_ui()
        self._update_ui()
    
    def _setup_ui(self):
        """Configura la interfaz del componente"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Información de items mostrados
        self._info_label = QLabel("")
        self._info_label.setStyleSheet(f"""
            font-size: {self._FONT_SIZE}px;
            color: {self._COLOR_TEXTO_INFO};
        """)
        layout.addWidget(self._info_label)
        layout.addStretch()
        
        # Botón anterior
        self._btn_prev = SisIconButton("‹", tooltip="Página anterior")
        self._btn_prev.clicked.connect(self._prev_page)
        layout.addWidget(self._btn_prev)
        
        # Indicador de página actual
        self._page_label = QLabel("")
        self._page_label.setStyleSheet(f"""
            font-size: {self._FONT_SIZE}px;
            color: {self._COLOR_TEXTO_PAGINA};
            min-width: 70px;
            text-align: center;
        """)
        self._page_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._page_label)
        
        # Botón siguiente
        self._btn_next = SisIconButton("›", tooltip="Página siguiente")
        self._btn_next.clicked.connect(self._next_page)
        layout.addWidget(self._btn_next)
    
    def _update_ui(self):
        """Actualiza la UI según el estado actual"""
        total_pages = self._get_total_pages()
        
        # Ajustar página actual si es necesario
        if self._current_page > total_pages and total_pages > 0:
            self._current_page = total_pages
        
        # Calcular índices para mostrar
        start = (self._current_page - 1) * self._items_per_page + 1
        end = min(self._current_page * self._items_per_page, self._total_items)
        
        # Actualizar etiqueta de información
        if self._total_items == 0:
            self._info_label.setText("Mostrando 0-0 de 0 items")
        else:
            self._info_label.setText(
                f"Mostrando {start}–{end} de {self._total_items} items"
            )
        
        # Actualizar etiqueta de página
        self._page_label.setText(f"Página {self._current_page} de {total_pages}")
        
        # Actualizar estado de botones
        self._btn_prev.setEnabled(self._current_page > 1)
        self._btn_next.setEnabled(self._current_page < total_pages)
    
    def _get_total_pages(self) -> int:
        """Retorna el número total de páginas"""
        if self._total_items == 0:
            return 1
        return (self._total_items + self._items_per_page - 1) // self._items_per_page
    
    def _prev_page(self):
        """Va a la página anterior"""
        if self._current_page > 1:
            self._current_page -= 1
            self._update_ui()
            if self._on_page_change:
                self._on_page_change(self._current_page)
    
    def _next_page(self):
        """Va a la página siguiente"""
        total_pages = self._get_total_pages()
        if self._current_page < total_pages:
            self._current_page += 1
            self._update_ui()
            if self._on_page_change:
                self._on_page_change(self._current_page)
    
    # ==================== MÉTODOS PÚBLICOS ====================
    
    def update_total(self, total_items: int, reset_page: bool = True):
        """
        Actualiza el número total de items.
        
        Args:
            total_items: Nuevo número total de items
            reset_page: Si es True, reinicia a la página 1
        """
        self._total_items = total_items
        if reset_page:
            self._current_page = 1
        self._update_ui()
    
    def set_current_page(self, page: int):
        """
        Establece la página actual.
        
        Args:
            page: Nuevo número de página (1-indexado)
        """
        total_pages = self._get_total_pages()
        if 1 <= page <= total_pages:
            self._current_page = page
            self._update_ui()
            if self._on_page_change:
                self._on_page_change(self._current_page)
    
    def set_items_per_page(self, items_per_page: int, reset_page: bool = True):
        """
        Cambia la cantidad de items por página.
        
        Args:
            items_per_page: Nuevo número de items por página
            reset_page: Si es True, reinicia a la página 1
        """
        self._items_per_page = items_per_page
        if reset_page:
            self._current_page = 1
        self._update_ui()
    
    def get_current_page(self) -> int:
        """Retorna la página actual"""
        return self._current_page
    
    def get_total_pages(self) -> int:
        """Retorna el número total de páginas"""
        return self._get_total_pages()
    
    def get_start_index(self) -> int:
        """
        Retorna el índice de inicio para la página actual (0-indexado).
        Útil para slice de listas.
        
        Returns:
            int: Índice de inicio (ej: para data[start:end])
        """
        return (self._current_page - 1) * self._items_per_page
    
    def get_end_index(self) -> int:
        """
        Retorna el índice de fin para la página actual (0-indexado).
        Útil para slice de listas.
        
        Returns:
            int: Índice de fin (ej: para data[start:end])
        """
        return min(self._current_page * self._items_per_page, self._total_items)
    
    def get_current_page_data(self, data: list) -> list:
        """
        Retorna los datos correspondientes a la página actual.
        Útil para filtrar listas automáticamente.
        
        Args:
            data: Lista completa de datos
            
        Returns:
            list: Sublista correspondiente a la página actual
        """
        start = self.get_start_index()
        end = self.get_end_index()
        return data[start:end]


class SisCompactPagination(SisPagination):
    """
    Versión compacta de la paginación (sin el label de información).
    Útil para espacios reducidos.
    
    Ejemplo:
        pagination = SisCompactPagination(
            total_items=100,
            on_page_change=lambda page: cargar_pagina(page)
        )
    """
    
    def _setup_ui(self):
        """Configura la interfaz compacta (sin info_label)"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        layout.addStretch()
        
        # Botón anterior
        self._btn_prev = SisIconButton("‹", tooltip="Página anterior")
        self._btn_prev.clicked.connect(self._prev_page)
        layout.addWidget(self._btn_prev)
        
        # Indicador de página actual
        self._page_label = QLabel("")
        self._page_label.setStyleSheet(f"""
            font-size: {self._FONT_SIZE}px;
            color: {self._COLOR_TEXTO_PAGINA};
            min-width: 60px;
            text-align: center;
        """)
        self._page_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._page_label)
        
        # Botón siguiente
        self._btn_next = SisIconButton("›", tooltip="Página siguiente")
        self._btn_next.clicked.connect(self._next_page)
        layout.addWidget(self._btn_next)
        
        layout.addStretch()
    
    def _update_ui(self):
        """Actualiza la UI compacta"""
        total_pages = self._get_total_pages()
        
        # Ajustar página actual si es necesario
        if self._current_page > total_pages and total_pages > 0:
            self._current_page = total_pages
        
        # Actualizar etiqueta de página
        self._page_label.setText(f"{self._current_page}/{total_pages}")
        
        # Actualizar estado de botones
        self._btn_prev.setEnabled(self._current_page > 1)
        self._btn_next.setEnabled(self._current_page < total_pages)