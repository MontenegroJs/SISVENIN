"""
Pruebas unitarias para el controlador de Producto
"""
import unittest
from src.app.modules.producto.producto_controlador import ProductoControlador


class TestProductoControlador(unittest.TestCase):

    def test_validar_nombre_correcto(self):
        resultado = ProductoControlador.validar_nombre("Válido")
        self.assertTrue(resultado)

    def test_validar_nombre_vacio(self):
        with self.assertRaises(ValueError):
            ProductoControlador.validar_nombre("")

    def test_validar_nombre_espacios(self):
        with self.assertRaises(ValueError):
            ProductoControlador.validar_nombre("   ")

    def test_listar_ejemplo(self):
        lista = ProductoControlador.listar_ejemplo()
        self.assertGreater(len(lista), 0)
        self.assertTrue(hasattr(lista[0], 'id'))
        self.assertTrue(hasattr(lista[0], 'nombre'))


if __name__ == "__main__":
    unittest.main()
