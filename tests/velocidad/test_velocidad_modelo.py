"""
Pruebas unitarias para el modelo Velocidad
"""
import unittest
from src.app.models.velocidad_modelo import VelocidadModelo


class TestVelocidadModelo(unittest.TestCase):
    
    def test_crear_velocidad(self):
        obj = VelocidadModelo(id=1, nombre="Test", descripcion="Descripción")
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.nombre, "Test")
        self.assertEqual(obj.descripcion, "Descripción")
    
    def test_guardar(self):
        # Prueba de guardado en BD (usar BD temporal)
        pass


if __name__ == "__main__":
    unittest.main()
