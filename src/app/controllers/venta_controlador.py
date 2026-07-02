"""
Controlador del módulo Venta - SISVENIN
Conectado con el módulo Producto (buscador real)
"""

from src.app.models.venta_modelo import VentaModelo
from src.app.controllers.producto_controlador import ProductoControlador


class VentaControlador:
    """Controlador para la gestión de ventas."""

    def __init__(self):
        self.venta = VentaModelo()
        self.productos = ProductoControlador()  

    # 🔎 BUSCADOR DE PRODUCTOS (para la vista)
    def buscar_productos(self, texto: str):
        """
        Busca productos en el módulo Productos.
        """
        return self.productos.buscar_productos(texto)

    # ➕ AGREGAR PRODUCTO A LA VENTA (CORREGIDO)
    def agregar_producto(self, producto):
        """
        Agrega un producto REAL (ProductoModelo) a la venta.
        """
        self.venta.agregar_producto(producto)

    # 💰 OBTENER TOTAL
    def obtener_total(self):
        """
        Obtiene el total actual de la venta.
        """
        return self.venta.total

    # 💾 CONFIRMAR VENTA
    def confirmar_venta(self):
        """
        Confirma y guarda la venta.
        """
        return self.venta.guardar()

    # 📄 OBTENER DETALLE DE VENTA
    def obtener_detalle(self):
        """
        Devuelve el carrito de la venta.
        """
        return self.venta.obtener_detalle()