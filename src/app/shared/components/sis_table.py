"""
SisTable - Componente de tabla genérica compartido
Equivalente al sisvenin-table.tsx de React

Características:
- Cabecera: fondo #F5F5F5, texto #757575, 14px, semibold
- Filas: fondo blanco, borde inferior #E0E0E0
- Celdas: padding 12px 16px, texto #212121, 14px
- Hover sobre fila: #FAFAFA
- Ancho mínimo sugerido: 800px (scroll horizontal)
- Border radius: 12px
- Borde exterior: 1px #E0E0E0

Ejemplos:
    columnas = [
        {"key": "nombre", "header": "Nombre", "width": "30%"},
        {"key": "precio", "header": "Precio", "align": "right"},
        {"key": "acciones", "header": "Acciones", "render": lambda row: btn_editar}
    ]
    
    tabla = SisTable(columns=columnas, data=productos, get_key=lambda p: p.id)
"""

from typing import Optional, List, Dict, Any, Callable, TypeVar, Generic
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLabel, QFrame,
    QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QFont

from src.app.shared.components.sis_button import SisIconButton


T = TypeVar('T')  # Tipo genérico para los datos de la fila


class SisTable(Generic[T], QWidget):
    """
    Tabla genérica de SISVENIN.
    Sigue el diseño del Prompt 0 de Figma (igual al React).
    
    Características:
    - Columnas configurables
    - Render personalizado por celda
    - Hover en filas
    - Scroll horizontal para muchas columnas
    
    Type Parameters:
        T: Tipo de los objetos en data
    
    Ejemplo:
        productos = [Producto(id=1, nombre="Leche", precio=2.50), ...]
        
        columnas = [
            {"key": "nombre", "header": "Producto", "width": "30%"},
            {"key": "precio", "header": "Precio", "align": "right"},
            {"key": "acciones", "header": "", "render": lambda p: btn_editar}
        ]
        
        tabla = SisTable(columns=columnas, data=productos, get_key=lambda p: p.id)
    """
    
    # Constantes de estilo (Prompt 0)
    _COLOR_CABECERA_BG = "#F5F5F5"
    _COLOR_CABECERA_TEXTO = "#757575"
    _COLOR_FILA_BG = "#FFFFFF"
    _COLOR_FILA_HOVER = "#FAFAFA"
    _COLOR_BORDE = "#E0E0E0"
    _COLOR_TEXTO = "#212121"
    
    _BORDER_RADIUS = 12
    _PADDING_CELDA = 16
    _ANCHO_MINIMO = 800
    
    def __init__(
        self,
        columns: List[Dict[str, Any]],
        data: List[T],
        get_key: Callable[[T], Any],
        parent=None
    ):
        """
        Inicializa la tabla.
        
        Args:
            columns: Lista de definiciones de columnas.
                Cada columna puede tener:
                - key: identificador (para acceder al dato)
                - header: texto del encabezado
                - width: ancho (ej: "30%", "100px")
                - align: "left", "center" o "right"
                - render: función opcional para renderizar la celda
            data: Lista de datos a mostrar
            get_key: Función para obtener la clave única de cada fila
            parent: Widget padre
        """
        super().__init__(parent)
        
        self._columns = columns
        self._data = data
        self._get_key = get_key
        
        self._setup_ui()
        self._populate_table()
    
    def _setup_ui(self):
        """Configura la interfaz de la tabla"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Contenedor con scroll horizontal
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Widget contenedor de la tabla
        self._table_container = QWidget()
        self._table_container.setMinimumWidth(self._ANCHO_MINIMO)
        
        self._table_layout = QVBoxLayout(self._table_container)
        self._table_layout.setContentsMargins(0, 0, 0, 0)
        self._table_layout.setSpacing(0)
        
        # Cabecera
        self._setup_header()
        
        # Cuerpo de la tabla
        self._body_widget = QWidget()
        self._body_layout = QVBoxLayout(self._body_widget)
        self._body_layout.setContentsMargins(0, 0, 0, 0)
        self._body_layout.setSpacing(0)
        self._table_layout.addWidget(self._body_widget)
        
        # Mensaje de "sin datos"
        self._empty_label = QLabel("📭 No hay datos para mostrar")
        self._empty_label.setAlignment(Qt.AlignCenter)
        self._empty_label.setStyleSheet(f"""
            font-size: 14px;
            color: {self._COLOR_CABECERA_TEXTO};
            padding: 40px;
        """)
        self._empty_label.hide()
        self._table_layout.addWidget(self._empty_label)
        
        scroll_area.setWidget(self._table_container)
        layout.addWidget(scroll_area)
        
        # Aplicar estilo al contenedor
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self._COLOR_FILA_BG};
                border: 1px solid {self._COLOR_BORDE};
                border-radius: {self._BORDER_RADIUS}px;
            }}
        """)
    
    def _setup_header(self):
        """Configura la cabecera de la tabla"""
        header_widget = QWidget()
        header_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {self._COLOR_CABECERA_BG};
                border-bottom: 1px solid {self._COLOR_BORDE};
                border-top-left-radius: {self._BORDER_RADIUS}px;
                border-top-right-radius: {self._BORDER_RADIUS}px;
            }}
        """)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        for col in self._columns:
            # Celda de cabecera
            header_cell = QWidget()
            cell_layout = QHBoxLayout(header_cell)
            cell_layout.setContentsMargins(self._PADDING_CELDA, 12, self._PADDING_CELDA, 12)
            
            label = QLabel(col.get("header", ""))
            label.setStyleSheet(f"""
                font-size: 14px;
                font-weight: 600;
                color: {self._COLOR_CABECERA_TEXTO};
            """)
            
            # Alineación
            align = col.get("align", "left")
            if align == "right":
                cell_layout.setAlignment(Qt.AlignRight)
                label.setAlignment(Qt.AlignRight)
            elif align == "center":
                cell_layout.setAlignment(Qt.AlignCenter)
                label.setAlignment(Qt.AlignCenter)
            
            cell_layout.addWidget(label)
            cell_layout.addStretch()
            
            # Ancho
            if "width" in col:
                header_cell.setFixedWidth(self._parse_width(col["width"]))
            
            header_layout.addWidget(header_cell)
        
        header_layout.addStretch()
        self._table_layout.addWidget(header_widget)
    
    def _parse_width(self, width: str) -> int:
        """
        Convierte un ancho en string a píxeles.
        
        Args:
            width: Ancho (ej: "30%", "100px")
            
        Returns:
            int: Ancho en píxeles
        """
        if width.endswith("%"):
            # Para porcentajes, usar un valor base de 800px
            percent = int(width.rstrip("%"))
            return int(self._ANCHO_MINIMO * percent / 100)
        elif width.endswith("px"):
            return int(width.rstrip("px"))
        else:
            return int(width) if width.isdigit() else 100
    
    def _populate_table(self):
        """Llena la tabla con los datos"""
        # Limpiar filas existentes
        for i in reversed(range(self._body_layout.count())):
            widget = self._body_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Mostrar mensaje si no hay datos
        if not self._data:
            self._empty_label.show()
            return
        
        self._empty_label.hide()
        
        # Crear filas
        for index, row_data in enumerate(self._data):
            row_widget = self._create_row(row_data, index)
            self._body_layout.addWidget(row_widget)
    
    def _create_row(self, row_data: T, index: int) -> QWidget:
        """
        Crea una fila de la tabla.
        
        Args:
            row_data: Datos de la fila
            index: Índice de la fila
            
        Returns:
            QWidget: Widget de la fila
        """
        row_widget = QWidget()
        row_widget.setProperty("row_index", index)
        
        # Estilo con hover
        row_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {self._COLOR_FILA_BG};
                border-bottom: 1px solid {self._COLOR_BORDE};
            }}
            QWidget:hover {{
                background-color: {self._COLOR_FILA_HOVER};
            }}
        """)
        
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(0)
        
        for col in self._columns:
            cell_widget = self._create_cell(row_data, col)
            row_layout.addWidget(cell_widget)
        
        row_layout.addStretch()
        
        return row_widget
    
    def _create_cell(self, row_data: T, column: Dict[str, Any]) -> QWidget:
        """
        Crea una celda de la tabla.
        
        Args:
            row_data: Datos de la fila
            column: Definición de la columna
            
        Returns:
            QWidget: Widget de la celda
        """
        cell = QWidget()
        cell_layout = QHBoxLayout(cell)
        cell_layout.setContentsMargins(self._PADDING_CELDA, 12, self._PADDING_CELDA, 12)
        
        # Obtener el contenido
        content = None
        if "render" in column and column["render"]:
            content = column["render"](row_data)
        elif "key" in column:
            key = column["key"]
            if isinstance(row_data, dict):
                value = row_data.get(key, "")
            else:
                value = getattr(row_data, key, "")
            content = str(value) if value is not None else ""
        
        # Crear widget de contenido
        if isinstance(content, QWidget):
            content_widget = content
        else:
            content_widget = QLabel(str(content) if content else "")
            content_widget.setWordWrap(True)
            content_widget.setStyleSheet(f"""
                font-size: 14px;
                color: {self._COLOR_TEXTO};
                line-height: 1.4;
            """)
        
        # Alineación
        align = column.get("align", "left")
        if align == "right":
            cell_layout.setAlignment(Qt.AlignRight)
            if isinstance(content_widget, QLabel):
                content_widget.setAlignment(Qt.AlignRight)
        elif align == "center":
            cell_layout.setAlignment(Qt.AlignCenter)
            if isinstance(content_widget, QLabel):
                content_widget.setAlignment(Qt.AlignCenter)
        
        cell_layout.addWidget(content_widget)
        cell_layout.addStretch()
        
        # Ancho
        if "width" in column:
            cell.setFixedWidth(self._parse_width(column["width"]))
        
        return cell
    
    def update_data(self, new_data: List[T]):
        """
        Actualiza los datos de la tabla.
        
        Args:
            new_data: Nueva lista de datos
        """
        self._data = new_data
        self._populate_table()
    
    def get_data(self) -> List[T]:
        """Retorna los datos actuales de la tabla"""
        return self._data
    
    def clear(self):
        """Limpia todos los datos de la tabla"""
        self.update_data([])
    
    def set_empty_message(self, message: str):
        """
        Establece el mensaje cuando no hay datos.
        
        Args:
            message: Nuevo mensaje
        """
        self._empty_label.setText(f"📭 {message}")


class SisPaginatedTable(Generic[T], QWidget):
    """
    Tabla con paginación integrada.
    Extiende SisTable con controles de paginación.
    
    Características adicionales:
    - Paginación automática
    - Control de items por página
    - Navegación entre páginas
    
    Ejemplo:
        tabla = SisPaginatedTable(
            columns=columnas,
            data=productos,
            get_key=lambda p: p.id,
            items_per_page=10
        )
    """
    
    def __init__(
        self,
        columns: List[Dict[str, Any]],
        data: List[T],
        get_key: Callable[[T], Any],
        items_per_page: int = 10,
        parent=None
    ):
        """
        Inicializa la tabla paginada.
        
        Args:
            columns: Definiciones de columnas
            data: Lista de datos
            get_key: Función para obtener clave única
            items_per_page: Items por página (default 10)
            parent: Widget padre
        """
        super().__init__(parent)
        
        self._all_data = data
        self._items_per_page = items_per_page
        self._current_page = 1
        
        self._setup_ui(columns, get_key)
        self._update_page()
    
    def _setup_ui(self, columns: List[Dict[str, Any]], get_key: Callable[[T], Any]):
        """Configura la interfaz con paginación"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Tabla principal
        self._table = SisTable(columns, [], get_key)
        layout.addWidget(self._table)
        
        # Barra de paginación
        pagination_widget = QWidget()
        pagination_layout = QHBoxLayout(pagination_widget)
        pagination_layout.setContentsMargins(0, 0, 0, 0)
        
        # Info de paginación
        self._info_label = QLabel("")
        self._info_label.setStyleSheet("""
            font-size: 13px;
            color: #757575;
        """)
        pagination_layout.addWidget(self._info_label)
        pagination_layout.addStretch()
        
        # Botones de navegación
        self._btn_prev = SisIconButton("‹", tooltip="Página anterior")
        self._btn_prev.clicked.connect(self._prev_page)
        
        self._page_label = QLabel("Página 1")
        self._page_label.setStyleSheet("""
            font-size: 13px;
            color: #212121;
            min-width: 70px;
            text-align: center;
        """)
        self._page_label.setAlignment(Qt.AlignCenter)
        
        self._btn_next = SisIconButton("›", tooltip="Página siguiente")
        self._btn_next.clicked.connect(self._next_page)
        
        pagination_layout.addWidget(self._btn_prev)
        pagination_layout.addWidget(self._page_label)
        pagination_layout.addWidget(self._btn_next)
        
        layout.addWidget(pagination_widget)
    
    def _update_page(self):
        """Actualiza la tabla con los datos de la página actual"""
        total_items = len(self._all_data)
        total_pages = max(1, (total_items + self._items_per_page - 1) // self._items_per_page)
        
        # Ajustar página actual
        if self._current_page > total_pages:
            self._current_page = total_pages
        
        # Calcular índices
        start = (self._current_page - 1) * self._items_per_page
        end = min(start + self._items_per_page, total_items)
        
        # Obtener datos de la página
        page_data = self._all_data[start:end]
        
        # Actualizar tabla
        self._table.update_data(page_data)
        
        # Actualizar información de paginación
        self._info_label.setText(
            f"Mostrando {start + 1 if total_items > 0 else 0}–{end} de {total_items} items"
        )
        self._page_label.setText(f"Página {self._current_page} de {total_pages}")
        
        # Actualizar estado de botones
        self._btn_prev.setEnabled(self._current_page > 1)
        self._btn_next.setEnabled(self._current_page < total_pages)
    
    def _prev_page(self):
        """Va a la página anterior"""
        if self._current_page > 1:
            self._current_page -= 1
            self._update_page()
    
    def _next_page(self):
        """Va a la página siguiente"""
        total_pages = max(1, (len(self._all_data) + self._items_per_page - 1) // self._items_per_page)
        if self._current_page < total_pages:
            self._current_page += 1
            self._update_page()
    
    def update_data(self, new_data: List[T]):
        """
        Actualiza todos los datos y reinicia la paginación.
        
        Args:
            new_data: Nueva lista completa de datos
        """
        self._all_data = new_data
        self._current_page = 1
        self._update_page()
    
    def get_page_data(self) -> List[T]:
        """Retorna los datos de la página actual"""
        start = (self._current_page - 1) * self._items_per_page
        end = start + self._items_per_page
        return self._all_data[start:end]
    
    def set_items_per_page(self, items_per_page: int):
        """
        Cambia la cantidad de items por página.
        
        Args:
            items_per_page: Nuevo número de items por página
        """
        self._items_per_page = items_per_page
        self._current_page = 1
        self._update_page()