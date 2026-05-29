"""
Pruebas unitarias para el controlador de Dashboard
"""
import unittest
from src.app.controllers.dashboard_controlador import DashboardControlador


class TestDashboardControlador(unittest.TestCase):
    
    def test_validar_nombre_correcto(self):
        resultado = DashboardControlador.validar_nombre("Válido")
        self.assertTrue(resultado)
    
    def test_validar_nombre_vacio(self):
        with self.assertRaises(ValueError):
            DashboardControlador.validar_nombre("")
    
    def test_listar_ejemplo(self):
        lista = DashboardControlador.listar_ejemplo()
        self.assertGreater(len(lista), 0)


if __name__ == "__main__":
    unittest.main()
