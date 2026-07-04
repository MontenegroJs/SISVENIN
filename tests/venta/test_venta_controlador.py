"""
Pruebas unitarias para el controlador de Venta
"""

import unittest

from src.app.controllers.venta_controlador import VentaControlador
from src.app.models.producto_modelo import ProductoModelo


class TestVentaControlador(unittest.TestCase):

    def setUp(self):
        self.controlador = VentaControlador()

    def test_crear_venta(self):
        self.assertIsNotNone(self.controlador.venta)

    def test_agregar_producto_al_carrito(self):
        producto = {
            "id": 1,
            "nombre": "Coca Cola",
            "precio_venta": 5.0
        }

        self.controlador.agregar_producto(producto)

        self.assertEqual(
            len(self.controlador.venta.detalle),
            1
        )

    def test_obtener_total(self):
        producto = {
            "id": 1,
            "nombre": "Coca Cola",
            "precio_venta": 5.0
        }

        self.controlador.agregar_producto(producto)

        total = self.controlador.obtener_total()

        self.assertEqual(total, 5.0)

    def test_confirmar_venta(self):
        producto = {
            "id": 1,
            "nombre": "Coca Cola",
            "precio_venta": 5.0
        }

        self.controlador.agregar_producto(producto)

        resultado = self.controlador.confirmar_venta()

        self.assertTrue(resultado)

    # -------------------------
    # TESTS DE VUELTO
    # -------------------------

    def test_calcular_vuelto_correcto(self):
        producto = ProductoModelo(
            id=1,
            nombre="Coca Cola",
            precio_venta=10.0,
            stock=10
        )

        self.controlador.agregar_producto(producto)

        total = self.controlador.obtener_total()

        resultado = self.controlador.calcular_vuelto(20, total)

        self.assertEqual(resultado["vuelto"], 10.0)
        self.assertEqual(resultado["error"], "")

    def test_calcular_vuelto_insuficiente(self):
        producto = ProductoModelo(
            id=1,
            nombre="Coca Cola",
            precio_venta=10.0,
            stock=10
        )

        self.controlador.agregar_producto(producto)

        total = self.controlador.obtener_total()

        resultado = self.controlador.calcular_vuelto(5, total)

        self.assertEqual(resultado["vuelto"], 0)
        self.assertIn("Falta", resultado["error"])

    def test_calcular_vuelto_exacto(self):
        producto = ProductoModelo(
            id=1,
            nombre="Coca Cola",
            precio_venta=10.0,
            stock=10
        )

        self.controlador.agregar_producto(producto)

        total = self.controlador.obtener_total()

        resultado = self.controlador.calcular_vuelto(10, total)

        self.assertEqual(resultado["vuelto"], 0)
        self.assertEqual(resultado["error"], "")


if __name__ == "__main__":
    unittest.main()