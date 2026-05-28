"""
Pruebas unitarias para el controlador de Velocidad
"""
import unittest
from src.app.controllers.velocidad_controlador import VelocidadControlador


class TestVelocidadControlador(unittest.TestCase):
    
    def test_validar_nombre_correcto(self):
        resultado = VelocidadControlador.validar_nombre("Válido")
        self.assertTrue(resultado)
    
    def test_validar_nombre_vacio(self):
        with self.assertRaises(ValueError):
            VelocidadControlador.validar_nombre("")
    
    def test_listar_ejemplo(self):
        lista = VelocidadControlador.listar_ejemplo()
        self.assertGreater(len(lista), 0)


if __name__ == "__main__":
    unittest.main()
