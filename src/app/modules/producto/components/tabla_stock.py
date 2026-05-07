# src/app/modules/producto/components/tabla_stock.py
"""
Componente exclusivo del módulo Producto
"""
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt


class TablaStock(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["ID", "Nombre", "Precio (S/.)", "Stock"])
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Ajustar ancho de columnas
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
    
    def cargar_productos(self, productos):
        """
        Carga una lista de productos en la tabla
        
        Args:
            productos: Lista de objetos Producto
        """
        self.setRowCount(len(productos))
        
        for i, producto in enumerate(productos):
            # ID
            self.setItem(i, 0, QTableWidgetItem(str(producto.id)))
            
            # Nombre
            self.setItem(i, 1, QTableWidgetItem(producto.nombre))
            
            # Precio
            self.setItem(i, 2, QTableWidgetItem(f"S/. {producto.precio:.2f}"))
            
            # Stock
            stock_item = QTableWidgetItem(str(producto.stock))
            if producto.stock < 10:
                stock_item.setBackground(Qt.red)
                stock_item.setForeground(Qt.white)
            self.setItem(i, 3, stock_item)
    
    def obtener_producto_seleccionado(self):
        """Retorna el índice de la fila seleccionada o None"""
        current_row = self.currentRow()
        if current_row >= 0:
            return current_row
        return None