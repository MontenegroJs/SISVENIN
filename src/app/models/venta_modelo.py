"""
Modelo del módulo Venta - SISVENIN
HU: Venta rápida en 3 clics
"""

from typing import List, Dict, Optional


class VentaModelo:
    """Modelo de datos para una venta."""

    def __init__(self, id: Optional[int] = None):
        self.id: Optional[int] = id
        self.detalle: List[Dict] = []  # carrito de productos
        self.total: float = 0.0
        self.activo: bool = True

    # 🧩 1. Agregar producto al carrito
    def agregar_producto(self, producto, cantidad: int = 1) -> None:
        """
        Agrega un producto a la venta (soporta dict y ProductoModelo).
        """

        # 🔥 compatibilidad dict / objeto (IMPORTANTE PARA TU ERROR)
        producto_id = producto["id"] if isinstance(producto, dict) else producto.id
        nombre = producto["nombre"] if isinstance(producto, dict) else producto.nombre
        precio = producto["precio_venta"] if isinstance(producto, dict) else producto.precio_venta

        item = {
            "producto_id": producto_id,
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": precio * cantidad
        }

        self.detalle.append(item)
        self.calcular_total()

    # 🧮 2. Calcular total automático
    def calcular_total(self) -> float:
        """
        Calcula el total de la venta.
        """
        self.total = sum(item["subtotal"] for item in self.detalle)
        return self.total

    # 💾 3. Guardar venta (simulado por ahora)
    def guardar(self) -> bool:
        """
        Guarda la venta en la base de datos.
        """
        try:
            print("Venta guardada:", self.detalle)
            return True
        except Exception:
            return False

    # 📄 4. Obtener detalle
    def obtener_detalle(self) -> List[Dict]:
        return self.detalle