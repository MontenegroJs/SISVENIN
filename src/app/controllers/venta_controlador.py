"""
Controlador del módulo Venta
"""

from src.app.models.venta_modelo import VentaModelo


class VentaControlador:
    """Controlador para la gestión de ventas."""

    def __init__(self):
        self.venta = VentaModelo()

    def agregar_producto(self, producto):
        """
        Agrega un producto a la venta actual.
        """

        class ProductoTemporal:
            pass

        producto_temp = ProductoTemporal()
        producto_temp.id = producto["id"]
        producto_temp.nombre = producto["nombre"]
        producto_temp.precio_venta = producto["precio_venta"]

        self.venta.agregar_producto(producto_temp)

    def obtener_total(self):
        """
        Obtiene el total actual de la venta.
        """
        return self.venta.total

    def confirmar_venta(self):
        """
        Confirma y guarda la venta.
        """
        return self.venta.guardar()