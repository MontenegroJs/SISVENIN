"""
Pruebas unitarias para el controlador de Reporte
"""
import unittest
from src.app.controllers.reporte_controlador import ReporteControlador


class TestReporteControlador(unittest.TestCase):
    
    def test_validar_nombre_correcto(self):
        resultado = ReporteControlador.validar_nombre("Válido")
        self.assertTrue(resultado)
    
    def test_validar_nombre_vacio(self):
        with self.assertRaises(ValueError):
            ReporteControlador.validar_nombre("")
    
    def test_listar_ejemplo(self):
        lista = ReporteControlador.listar_ejemplo()
        self.assertGreater(len(lista), 0)


if __name__ == "__main__":
    unittest.main()
