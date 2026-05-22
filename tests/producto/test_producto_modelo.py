"""
Pruebas unitarias para el modelo Producto
"""
import unittest
from src.app.models.producto_modelo import ProductoModelo


class TestProductoModelo(unittest.TestCase):
    
    def test_crear_producto(self):
        obj = ProductoModelo(id=1, nombre="Test", descripcion="Descripción")
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.nombre, "Test")
        self.assertEqual(obj.descripcion, "Descripción")
    
    def test_guardar(self):
        # Prueba de guardado en BD (usar BD temporal)
        pass


if __name__ == "__main__":
    unittest.main()
