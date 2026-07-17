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

    # ➕ AGREGAR PRODUCTO A LA VENTA
    def agregar_producto(self, producto, cantidad=1):
        """
        Agrega un producto a la venta.
        Puede recibir ProductoModelo.
        """
        self.venta.agregar_producto(producto, cantidad)

    # 💰 OBTENER TOTAL DE VENTA
    def obtener_total(self):
        """
        Retorna el total calculado de la venta.
        """
        return self.venta.calcular_total()

    # 💵 HU-02: CALCULAR VUELTO
    def calcular_vuelto(self, pago, total):
        """
        Calcula el vuelto según el pago del cliente.
        """

        if pago < total:
            return {
                "vuelto": 0,
                "error": f"Falta S/ {total - pago:.2f}"
            }

        return {
            "vuelto": pago - total,
            "error": ""
        }

    # 💾 CONFIRMAR VENTA
    def confirmar_venta(self):
        """
        Confirma y guarda la venta.
        """
        return self.venta.guardar()

    # 📄 OBTENER DETALLE DE VENTA
    def obtener_detalle(self):
        """
        Devuelve el detalle de la venta actual.
        """
        return self.venta.obtener_detalle()