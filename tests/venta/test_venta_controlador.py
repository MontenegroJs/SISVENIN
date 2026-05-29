"""
Pruebas unitarias para el controlador de Venta
"""
import unittest
from src.app.controllers.venta_controlador import VentaControlador


class TestVentaControlador(unittest.TestCase):
    
    def test_validar_nombre_correcto(self):
        resultado = VentaControlador.validar_nombre("Válido")
        self.assertTrue(resultado)
    
    def test_validar_nombre_vacio(self):
        with self.assertRaises(ValueError):
            VentaControlador.validar_nombre("")
    
    def test_listar_ejemplo(self):
        lista = VentaControlador.listar_ejemplo()
        self.assertGreater(len(lista), 0)


if __name__ == "__main__":
    unittest.main()
