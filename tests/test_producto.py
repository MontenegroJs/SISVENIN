"""
Pruebas para el módulo Producto
"""
import unittest
from src.app.models.producto_modelo import ProductoModelo
from src.app.controllers.producto_controlador import ProductoControlador


class TestProductoModelo(unittest.TestCase):
    def test_crear(self):
        obj = ProductoModelo(id=1, nombre="Test")
        self.assertEqual(obj.nombre, "Test")


if __name__ == "__main__":
    unittest.main()
