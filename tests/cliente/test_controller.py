"""
Pruebas unitarias para el controlador de Cliente
"""
import unittest
from src.app.modules.cliente.cliente_controller import ClienteController


class TestClienteController(unittest.TestCase):

    def test_validar_nombre_correcto(self):
        resultado = ClienteController.validar_nombre("Válido")
        self.assertTrue(resultado)

    def test_validar_nombre_vacio(self):
        with self.assertRaises(ValueError):
            ClienteController.validar_nombre("")

    def test_validar_nombre_espacios(self):
        with self.assertRaises(ValueError):
            ClienteController.validar_nombre("   ")

    def test_listar_ejemplo(self):
        lista = ClienteController.listar_ejemplo()
        self.assertGreater(len(lista), 0)
        self.assertTrue(hasattr(lista[0], 'id'))
        self.assertTrue(hasattr(lista[0], 'nombre'))


if __name__ == "__main__":
    unittest.main()
