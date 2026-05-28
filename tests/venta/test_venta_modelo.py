"""
Pruebas unitarias para el modelo Venta
"""
import unittest
from src.app.models.venta_modelo import VentaModelo


class TestVentaModelo(unittest.TestCase):
    
    def test_crear_venta(self):
        obj = VentaModelo(id=1, nombre="Test", descripcion="Descripción")
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.nombre, "Test")
        self.assertEqual(obj.descripcion, "Descripción")
    
    def test_guardar(self):
        # Prueba de guardado en BD (usar BD temporal)
        pass


if __name__ == "__main__":
    unittest.main()
