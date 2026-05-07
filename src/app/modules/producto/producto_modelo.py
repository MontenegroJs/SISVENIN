# src/app/modules/producto/producto_modelo.py
"""
Modelo del módulo Producto
"""
class Producto:
    def __init__(self, id=None, nombre="", precio=0.0, stock=0):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
    
    def reducir_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
        else:
            raise ValueError(f"Stock insuficiente. Solo hay {self.stock} unidades")
    
    def aumentar_stock(self, cantidad):
        self.stock += cantidad
    
    def __str__(self):
        return f"{self.nombre} - S/.{self.precio:.2f} (stock: {self.stock})"