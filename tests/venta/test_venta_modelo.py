"""
Pruebas unitarias para el modelo Venta
"""
import unittest
from src.app.models.venta_modelo import VentaModelo
from src.app.models.producto_modelo import ProductoModelo


class TestVentaModelo(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.venta = VentaModelo()

        self.producto1 = ProductoModelo(
            id=1,
            nombre="Coca Cola",
            precio_venta=5.0,
            stock=10
        )

        self.producto2 = ProductoModelo(
            id=2,
            nombre="Sandwich",
            precio_venta=8.0,
            stock=5
        )

    # 🧪 1. Agregar producto al carrito
    def test_agregar_producto(self):
        self.venta.agregar_producto(self.producto1, cantidad=2)

        self.assertEqual(len(self.venta.detalle), 1)
        self.assertEqual(self.venta.detalle[0]["cantidad"], 2)

    # 🧪 2. Calcular total automático
    def test_calcular_total(self):
        self.venta.agregar_producto(self.producto1, cantidad=2)  # 10
        self.venta.agregar_producto(self.producto2, cantidad=1)  # 8

        total = self.venta.calcular_total()

        self.assertEqual(total, 18.0)

    # 🧪 3. Guardar venta
    def test_guardar(self):
        self.venta.agregar_producto(self.producto1, cantidad=1)

        resultado = self.venta.guardar()

        self.assertTrue(resultado)


if __name__ == "__main__":
    unittest.main()