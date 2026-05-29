"""
SisModal - Componente de diálogo modal compartido
Equivalente al sisvenin-modal.tsx de React
"""

from typing import Optional, List, Callable
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QDialog
)
from PySide6.QtCore import Qt, QEvent, QSize
from PySide6.QtGui import QFont, QColor, QKeyEvent


class SisModal(QDialog):
    """
    Modal (diálogo) de SISVENIN.
    Sigue el diseño del Prompt 0 de Figma (igual al React).
    
    Características:
    - Overlay semitransparente
    - Centrado en la pantalla
    - Cierre con ESC o clic fuera
    """
    
    # Constantes de estilo (Prompt 0)
    _COLOR_TARJETA = "#FFFFFF"
    _COLOR_BORDE = "#E0E0E0"
    _COLOR_TEXTO_PRINCIPAL = "#212121"
    _BORDER_RADIUS = 16
    _PADDING = 24
    
    # Tamaños
    _WIDTH_SM = 500
    _WIDTH_LG = 600
    
    def __init__(
        self,
        title: str,
        size: str = "sm",
        on_close: Optional[Callable] = None,
        parent=None
    ):
        """
        Inicializa el modal.
        
        Args:
            title: Título del modal
            size: "sm" (500px) o "lg" (600px)
            on_close: Función a llamar al cerrar el modal
            parent: Widget padre
        """
        super().__init__(parent)
        
        self._title_text = title
        self._size = size
        self._on_close = on_close
        self._is_open = False
        self._content_widget: Optional[QWidget] = None
        self._footer_widgets: List[QWidget] = []
        
        # Configurar ventana modal
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        
        # Configurar tamaño
        ancho = self._WIDTH_LG if size == "lg" else self._WIDTH_SM
        self.setFixedWidth(ancho)
        
        self._setup_ui()
        self._apply_styles()
        
        # Conectar tecla ESC para cerrar
        self.installEventFilter(self)
    
    def _setup_ui(self):
        """Configura la interfaz del modal"""
        # Layout principal
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        
        # Contenedor blanco (contenido)
        self._container = QFrame()
        self._container_layout = QVBoxLayout(self._container)
        self._container_layout.setContentsMargins(
            self._PADDING, self._PADDING, 
            self._PADDING, self._PADDING
        )
        self._container_layout.setSpacing(20)
        
        # Header
        self._setup_header()
        
        # Separador después del header
        self._separador = QFrame()
        self._separador.setFrameShape(QFrame.HLine)
        self._separador.setFixedHeight(1)
        self._container_layout.addWidget(self._separador)
        
        # Body (contenido dinámico)
        self._body_layout = QVBoxLayout()
        self._body_layout.setSpacing(16)
        self._container_layout.addLayout(self._body_layout)
        
        # Footer (botones)
        self._footer_layout = QHBoxLayout()
        self._footer_layout.setSpacing(12)
        self._footer_layout.addStretch()
        self._container_layout.addLayout(self._footer_layout)
        
        self._main_layout.addWidget(self._container)
    
    def _setup_header(self):
        """Configura el header del modal"""
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        # Título
        self._title_label = QLabel(self._title_text)
        self._title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #212121;
        """)
        header_layout.addWidget(self._title_label)
        header_layout.addStretch()
        
        # Botón cerrar (X)
        self._btn_close = QPushButton("✕")
        self._btn_close.setFixedSize(36, 36)
        self._btn_close.setCursor(Qt.PointingHandCursor)
        self._btn_close.clicked.connect(self.close)
        self._btn_close.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                font-size: 16px;
                color: #757575;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
                color: #212121;
            }
        """)
        header_layout.addWidget(self._btn_close)
        
        self._container_layout.addLayout(header_layout)
    
    def _apply_styles(self):
        """Aplica los estilos CSS al modal"""
        self.setStyleSheet(f"""
            SisModal {{
                background-color: transparent;
            }}
            QFrame {{
                background-color: {self._COLOR_TARJETA};
                border-radius: {self._BORDER_RADIUS}px;
            }}
        """)
        
        # Aplicar sombra al contenedor
        from PySide6.QtWidgets import QGraphicsDropShadowEffect
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25)
        sombra.setXOffset(0)
        sombra.setYOffset(5)
        sombra.setColor(QColor(0, 0, 0, 25))
        self._container.setGraphicsEffect(sombra)
    
    def set_content(self, widget: QWidget):
        """
        Establece el contenido principal del modal.
        
        Args:
            widget: Widget a mostrar en el cuerpo del modal
        """
        # Limpiar contenido anterior
        self._clear_body()
        
        self._content_widget = widget
        self._body_layout.addWidget(widget)
    
    def _clear_body(self):
        """Limpia el contenido del cuerpo"""
        while self._body_layout.count():
            item = self._body_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def set_footer(self, widgets: List[QWidget]):
        """
        Establece los botones del footer.
        Los widgets se alinean a la derecha.
        
        Args:
            widgets: Lista de widgets (generalmente botones)
        """
        # Limpiar footer anterior
        self._clear_footer()
        
        self._footer_widgets = widgets
        
        # Agregar stretch para alinear a la derecha
        self._footer_layout.addStretch()
        
        for widget in widgets:
            self._footer_layout.addWidget(widget)
    
    def _clear_footer(self):
        """Limpia el footer"""
        while self._footer_layout.count():
            item = self._footer_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def set_title(self, title: str):
        """
        Actualiza el título del modal.
        
        Args:
            title: Nuevo título
        """
        self._title_text = title
        self._title_label.setText(title)
    
    def open(self):
        """Abre el modal (lo muestra)"""
        self._is_open = True
        self.show()
        self.raise_()
        self.activateWindow()
    
    def close(self):
        """Cierra el modal"""
        self._is_open = False
        if self._on_close:
            self._on_close()
        self.hide()
        # Aceptar el diálogo para liberar el modal
        self.accept()
    
    def is_open(self) -> bool:
        """Retorna True si el modal está abierto"""
        return self._is_open
    
    def eventFilter(self, obj, event):
        """Captura la tecla ESC para cerrar el modal"""
        if event.type() == QEvent.KeyPress:
            key_event = event
            if key_event.key() == Qt.Key_Escape:
                self.close()
                return True
        return super().eventFilter(obj, event)
    
    def mousePressEvent(self, event):
        """Cierra el modal si se hace clic fuera del contenedor"""
        if not self._container.geometry().contains(event.pos()):
            self.close()
        super().mousePressEvent(event)
    
    def showEvent(self, event):
        """Centra el modal cuando se muestra"""
        self._center_on_screen()
        super().showEvent(event)
    
    def _center_on_screen(self):
        """Centra el modal en la pantalla"""
        # Obtener geometría de la pantalla
        screen = self.screen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = screen_geometry.x() + (screen_geometry.width() - self.width()) // 2
            y = screen_geometry.y() + (screen_geometry.height() - self.height()) // 2
            self.move(x, y)


class SisConfirmModal(SisModal):
    """
    Modal de confirmación simplificado.
    Extiende SisModal para casos comunes de confirmación.
    """
    
    def __init__(
        self,
        title: str,
        message: str,
        on_confirm: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None,
        confirm_text: str = "Confirmar",
        cancel_text: str = "Cancelar",
        parent=None
    ):
        """
        Inicializa el modal de confirmación.
        
        Args:
            title: Título del modal
            message: Mensaje de confirmación
            on_confirm: Función al confirmar
            on_cancel: Función al cancelar
            confirm_text: Texto del botón confirmar
            cancel_text: Texto del botón cancelar
            parent: Widget padre
        """
        super().__init__(title, size="sm", parent=parent)
        
        # Crear contenido
        content = QLabel(message)
        content.setWordWrap(True)
        content.setStyleSheet("""
            font-size: 14px;
            color: #212121;
            line-height: 1.5;
        """)
        self.set_content(content)
        
        # Crear botones
        from .sis_button import SisButton
        
        btn_cancel = SisButton(cancel_text, variant="secondary")
        btn_confirm = SisButton(confirm_text, variant="primary")
        
        btn_cancel.clicked.connect(self._on_cancel)
        btn_confirm.clicked.connect(self._on_confirm)
        
        self.set_footer([btn_cancel, btn_confirm])
        
        self._on_confirm_callback = on_confirm
        self._on_cancel_callback = on_cancel
    
    def _on_confirm(self):
        """Maneja la confirmación"""
        if self._on_confirm_callback:
            self._on_confirm_callback()
        self.close()
    
    def _on_cancel(self):
        """Maneja la cancelación"""
        if self._on_cancel_callback:
            self._on_cancel_callback()
        self.close()