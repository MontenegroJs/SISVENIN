"""
Pruebas unitarias para el modelo Cliente
"""
import unittest
from src.app.modules.cliente.cliente_modelo import Cliente


class TestClienteModelo(unittest.TestCase):

    def test_crear_cliente(self):
        obj = Cliente(id=1, nombre="Test", descripcion="Descripción")
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.nombre, "Test")
        self.assertEqual(obj.descripcion, "Descripción")

    def test_to_dict(self):
        obj = Cliente(id=1, nombre="Test", descripcion="Desc")
        dic = obj.to_dict()
        self.assertEqual(dic["id"], 1)
        self.assertEqual(dic["nombre"], "Test")
        self.assertEqual(dic["descripcion"], "Desc")

    def test_str_representacion(self):
        obj = Cliente(id=1, nombre="Test")
        self.assertIn("Test", str(obj))


if __name__ == "__main__":
    unittest.main()
