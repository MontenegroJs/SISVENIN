"""
Pruebas unitarias para el modelo Venta_detalle
"""
import unittest
from src.app.models.venta_detalle_modelo import Venta_detalleModelo


class TestVenta_detalleModelo(unittest.TestCase):
    
    def test_crear_venta_detalle(self):
        obj = Venta_detalleModelo(id=1, nombre="Test", descripcion="Descripción")
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.nombre, "Test")
        self.assertEqual(obj.descripcion, "Descripción")
    
    def test_guardar(self):
        # Prueba de guardado en BD (usar BD temporal)
        pass


if __name__ == "__main__":
    unittest.main()
