"""
ProductoVista - Vista principal del módulo de productos
Sigue el diseño del Prompt 0 de Figma (igual al productos-page.tsx de React)

Componentes utilizados:
- BarraBusqueda: Búsqueda y botón "Nuevo Producto"
- TablaProductos: Listado de productos con paginación
- FormularioProducto: Modal para crear/editar productos

Flujo:
1. Usuario busca productos → se actualiza la tabla
2. Usuario hace clic en "Nuevo Producto" → abre formulario
3. Usuario hace clic en editar/eliminar desde la tabla → acción correspondiente
4. Usuario guarda producto → se refresca la tabla
"""

from typing import Optional, List
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QLabel
from PySide6.QtCore import Qt, Signal, QTimer

from src.app.base_layout import BaseLayout
from src.app.controllers.producto_controlador import ProductoControlador
from src.app.models.producto_modelo import ProductoModelo
from src.app.views.producto.components.barra_busqueda import BarraBusqueda
from src.app.views.producto.components.tabla_productos import TablaProductos
from src.app.views.producto.components.formulario_producto import FormularioProducto


class ProductoVista(QWidget):
    """
    Vista principal de gestión de productos.
    Sigue el diseño del Prompt 0 de Figma (igual al React).
    
    Señales:
        productoGuardado: Emitida cuando se guarda un producto
        productoEliminado: Emitida cuando se elimina un producto
    
    Ejemplo:
        vista = ProductoVista()
        vista.productoGuardado.connect(lambda p: print(f"Producto guardado: {p.nombre}"))
        vista.show()
    """
    
    # Señales
    productoGuardado = Signal(ProductoModelo)
    productoEliminado = Signal(int)
    
    def __init__(self, parent=None):
        """
        Inicializa la vista de productos.
        
        Args:
            parent: Widget padre
        """
        super().__init__(parent)
        
        self._controlador = ProductoControlador()
        self._productos: List[ProductoModelo] = []
        self._filtro_actual: str = ""
        self._highlight_id: Optional[int] = None
        
        self._setup_ui()
        self._cargar_productos()
        self._conectar_signales()
    
    def _setup_ui(self):
        """Configura la interfaz principal"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # ==================== BARRA DE BÚSQUEDA ====================
        self._barra_busqueda = BarraBusqueda(
            placeholder="Buscar producto por nombre..."
        )
        layout.addWidget(self._barra_busqueda)
        
        # ==================== TABLA DE PRODUCTOS ====================
        self._tabla = TablaProductos(items_per_page=10)
        layout.addWidget(self._tabla)
        
        # ==================== FORMULARIO MODAL ====================
        self._formulario = FormularioProducto(parent=self)
    
    def _conectar_signales(self):
        """Conecta las señales entre componentes"""
        # Barra de búsqueda
        self._barra_busqueda.textChanged.connect(self._filtrar_productos)
        self._barra_busqueda.nuevoClicked.connect(self._abrir_nuevo_producto)
        self._barra_busqueda.returnPressed.connect(self._buscar_rapido)
        
        # Tabla de productos
        self._tabla.editarClicked.connect(self._abrir_editar_producto)
        self._tabla.eliminarClicked.connect(self._confirmar_eliminar_producto)
        
        # Formulario
        self._formulario.productoGuardado.connect(self._on_producto_guardado)
    
    def _cargar_productos(self):
        """Carga todos los productos desde el controlador"""
        self._productos = self._controlador.obtener_todos_productos(solo_activos=True)
        self._actualizar_tabla()
    
    def _filtrar_productos(self, texto: str):
        """
        Filtra los productos por nombre.
        
        Args:
            texto: Texto de búsqueda
        """
        self._filtro_actual = texto
        
        if not texto or len(texto.strip()) < 2:
            # Si el texto es corto, mostrar todos
            self._productos = self._controlador.obtener_todos_productos(solo_activos=True)
        else:
            # Buscar productos que coincidan
            self._productos = self._controlador.buscar_productos(texto)
        
        self._actualizar_tabla()
    
    def _buscar_rapido(self):
        """Realiza una búsqueda rápida (al presionar Enter)"""
        texto = self._barra_busqueda.text()
        if texto and len(texto.strip()) >= 2:
            self._filtrar_productos(texto)
    
    def _actualizar_tabla(self):
        """Actualiza la tabla con los productos actuales"""
        self._tabla.set_productos(self._productos)
    
    def _abrir_nuevo_producto(self):
        """Abre el formulario para crear un nuevo producto"""
        self._formulario.set_producto(None)  # None = nuevo producto
        self._formulario.open()
    
    def _abrir_editar_producto(self, producto: ProductoModelo):
        """
        Abre el formulario para editar un producto existente.
        
        Args:
            producto: Producto a editar
        """
        self._formulario.set_producto(producto)
        self._formulario.open()
    
    def _confirmar_eliminar_producto(self, producto: ProductoModelo):
        """
        Muestra un diálogo de confirmación antes de eliminar.
        
        Args:
            producto: Producto a eliminar
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmar eliminación")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(f"¿Está segura que desea eliminar el producto \"{producto.nombre}\"?")
        msg_box.setInformativeText("Esta acción no se puede deshacer.")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        # Estilo del QMessageBox (como SisModal)
        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {BaseLayout.COLOR_TARJETA};
                border-radius: {BaseLayout.BORDER_RADIUS_MODAL}px;
            }}
            QMessageBox QLabel {{
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
                font-size: 14px;
            }}
            QPushButton {{
                min-width: 80px;
                padding: 8px 16px;
                border-radius: {BaseLayout.BORDER_RADIUS_BOTON}px;
                font-weight: 600;
            }}
            QPushButton:first {{
                background-color: {BaseLayout.COLOR_PELIGRO};
                color: white;
                border: none;
            }}
            QPushButton:first:hover {{
                background-color: {BaseLayout.COLOR_PELIGRO_HOVER};
            }}
            QPushButton:last {{
                background-color: transparent;
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
                border: 1px solid {BaseLayout.COLOR_BORDE};
            }}
            QPushButton:last:hover {{
                background-color: {BaseLayout.COLOR_FONDO_VENTANA};
            }}
        """)
        
        if msg_box.exec() == QMessageBox.Yes:
            self._eliminar_producto(producto)
    
    def _eliminar_producto(self, producto: ProductoModelo):
        """
        Elimina un producto.
        
        Args:
            producto: Producto a eliminar
        """
        try:
            self._controlador.eliminar_producto(producto.id)
            self._cargar_productos()  # Recargar lista
            self.productoEliminado.emit(producto.id)
            
            # Mostrar mensaje de éxito
            self._mostrar_mensaje_temporal(f"✅ Producto \"{producto.nombre}\" eliminado")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto: {str(e)}")
    
    def _on_producto_guardado(self, producto: ProductoModelo):
        """
        Maneja el evento cuando se guarda un producto.
        
        Args:
            producto: Producto guardado
        """
        self._cargar_productos()  # Recargar lista
        self.productoGuardado.emit(producto)
        
        # Mostrar mensaje de éxito
        accion = "actualizado" if self._formulario._editando else "agregado"
        self._mostrar_mensaje_temporal(f"✅ Producto \"{producto.nombre}\" {accion} correctamente")
        
        # Si hay un filtro activo, mantenerlo
        if self._filtro_actual:
            self._filtrar_productos(self._filtro_actual)
    
    def _mostrar_mensaje_temporal(self, mensaje: str, duracion: int = 3000):
        """
        Muestra un mensaje temporal en la parte superior.
        
        Args:
            mensaje: Mensaje a mostrar
            duracion: Duración en milisegundos
        """
        # Crear label flotante
        label = QLabel(mensaje)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"""
            QLabel {{
                background-color: {BaseLayout.COLOR_PRIMARIO};
                color: white;
                border-radius: {BaseLayout.BORDER_RADIUS_BOTON}px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }}
        """)
        
        # Posicionar en el centro superior
        label.setParent(self)
        label.adjustSize()
        x = (self.width() - label.width()) // 2
        y = 20
        label.move(x, y)
        label.show()
        
        # Ocultar después de la duración
        QTimer.singleShot(duracion, label.deleteLater)
    
    # ==================== MÉTODOS PÚBLICOS ====================
    
    def refresh(self):
        """
        Refresca la lista de productos.
        Útil para actualizar desde otras vistas.
        """
        self._cargar_productos()
    
    def resaltar_producto(self, producto_id: int):
        """
        Resalta un producto en la tabla y navega a la página correspondiente.
        
        Args:
            producto_id: ID del producto a resaltar
        """
        # Buscar el producto
        producto = self._controlador.obtener_producto(producto_id)
        if not producto:
            return
        
        # Limpiar filtro para asegurar que el producto sea visible
        if self._filtro_actual:
            self._barra_busqueda.clear()
            self._filtro_actual = ""
            self._cargar_productos()
        
        # Calcular en qué página está el producto
        items_per_page = 10
        productos = self._productos
        index = None
        for i, p in enumerate(productos):
            if p.id == producto_id:
                index = i
                break
        
        if index is not None:
            pagina = (index // items_per_page) + 1
            # Cambiar a la página correspondiente
            self._tabla.set_items_per_page(items_per_page)
            # Nota: SisPaginatedTable no tiene set_current_page directamente
            # Por ahora, resaltamos sin cambiar página
            self._tabla.resaltar_producto(producto_id)
    
    def obtener_productos(self) -> List[ProductoModelo]:
        """
        Retorna la lista actual de productos.
        
        Returns:
            List[ProductoModelo]: Lista de productos
        """
        return self._productos
    
    def obtener_producto_por_id(self, producto_id: int) -> Optional[ProductoModelo]:
        """
        Obtiene un producto por su ID.
        
        Args:
            producto_id: ID del producto
            
        Returns:
            ProductoModelo o None si no existe
        """
        return self._controlador.obtener_producto(producto_id)
    
    def set_filtro(self, texto: str):
        """
        Establece un filtro de búsqueda programáticamente.
        
        Args:
            texto: Texto de búsqueda
        """
        self._barra_busqueda.set_text(texto)
        self._filtrar_productos(texto)
    
    def limpiar_filtro(self):
        """Limpia el filtro de búsqueda actual"""
        self._barra_busqueda.clear()
        self._cargar_productos()
    
    def get_total_productos(self) -> int:
        """
        Retorna el número total de productos.
        
        Returns:
            int: Cantidad de productos
        """
        return len(self._productos)
    
    def get_productos_stock_bajo(self, limite: int = 5) -> List[ProductoModelo]:
        """
        Retorna productos con stock bajo.
        
        Args:
            limite: Valor límite de stock
            
        Returns:
            List[ProductoModelo]: Productos con stock bajo
        """
        return self._controlador.obtener_productos_stock_bajo(limite=limite)
    
    def get_productos_por_vencer(self, dias: int = 7) -> List[ProductoModelo]:
        """
        Retorna productos próximos a vencer.
        
        Args:
            dias: Número de días para considerar
            
        Returns:
            List[ProductoModelo]: Productos próximos a vencer
        """
        return self._controlador.obtener_productos_por_vencer(dias=dias)
    
    def resizeEvent(self, event):
        """Maneja el redimensionamiento de la ventana"""
        super().resizeEvent(event)
        # Actualizar posición de mensajes temporales si es necesario
    
    def showEvent(self, event):
        """Maneja el evento de mostrar la vista"""
        super().showEvent(event)
        # Refrescar datos al mostrar
        self.refresh()