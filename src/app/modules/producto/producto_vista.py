# src/app/modules/producto/producto_vista.py
"""
Módulo Producto - Vista
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QMessageBox, QLabel)
from .components.tabla_stock import TablaStock
from .producto_controller import ProductoController


class ProductoVista(QWidget):
    """Vista del módulo de productos"""
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        
        # Título
        titulo = QLabel("📦 Gestión de Productos")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(titulo)
        
        # Tabla de productos (componente local)
        self.tabla = TablaStock()
        layout.addWidget(self.tabla)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        self.btn_refrescar = QPushButton("🔄 Refrescar")
        self.btn_refrescar.clicked.connect(self.refrescar_lista)
        
        self.btn_nuevo = QPushButton("➕ Nuevo Producto")
        self.btn_nuevo.clicked.connect(self.nuevo_producto)
        
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.clicked.connect(self.editar_producto)
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setStyleSheet("background-color: #e74c3c; color: white;")
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        
        botones_layout.addWidget(self.btn_refrescar)
        botones_layout.addWidget(self.btn_nuevo)
        botones_layout.addWidget(self.btn_editar)
        botones_layout.addWidget(self.btn_eliminar)
        botones_layout.addStretch()
        
        layout.addLayout(botones_layout)
        
        # Cargar datos
        self.refrescar_lista()
    
    def refrescar_lista(self):
        """Carga los productos en la tabla"""
        try:
            productos = ProductoController.listar_productos()
            self.tabla.cargar_productos(productos)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron cargar los productos: {e}")
    
    def nuevo_producto(self):
        """Abre diálogo para crear nuevo producto"""
        QMessageBox.information(self, "Nuevo Producto", 
                                "Funcionalidad en desarrollo.\nPróximamente podrás agregar productos.")
    
    def editar_producto(self):
        """Edita el producto seleccionado"""
        fila = self.tabla.obtener_producto_seleccionado()
        if fila is None:
            QMessageBox.warning(self, "Editar", "Selecciona un producto para editar")
            return
        
        QMessageBox.information(self, "Editar Producto", 
                                "Funcionalidad en desarrollo.\nPróximamente podrás editar productos.")
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        fila = self.tabla.obtener_producto_seleccionado()
        if fila is None:
            QMessageBox.warning(self, "Eliminar", "Selecciona un producto para eliminar")
            return
        
        respuesta = QMessageBox.question(
            self, "Eliminar Producto",
            "¿Estás seguro de que deseas eliminar este producto?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            QMessageBox.information(self, "Eliminar Producto", 
                                    "Funcionalidad en desarrollo.\nPróximamente podrás eliminar productos.")