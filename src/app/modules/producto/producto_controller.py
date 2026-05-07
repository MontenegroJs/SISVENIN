# src/app/modules/producto/producto_controller.py
"""
Controlador del módulo Producto
"""
from .producto_modelo import Producto


class ProductoController:
    
    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        return True
    
    @staticmethod
    def validar_precio(precio):
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return True
    
    @staticmethod
    def validar_stock(stock):
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        return True
    
    @staticmethod
    def listar_productos():
        """Retorna lista de productos de ejemplo para pruebas"""
        return [
            Producto(id=1, nombre="Arroz", precio=3.50, stock=50),
            Producto(id=2, nombre="Leche", precio=2.00, stock=30),
            Producto(id=3, nombre="Pan", precio=1.00, stock=100),
            Producto(id=4, nombre="Aceite", precio=8.00, stock=20),
            Producto(id=5, nombre="Azúcar", precio=2.50, stock=45),
        ]