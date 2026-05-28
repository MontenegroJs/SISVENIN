"""
Pruebas unitarias para el modelo Dashboard
"""
import unittest
from src.app.models.dashboard_modelo import DashboardModelo


class TestDashboardModelo(unittest.TestCase):
    
    def test_crear_dashboard(self):
        obj = DashboardModelo(id=1, nombre="Test", descripcion="Descripción")
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.nombre, "Test")
        self.assertEqual(obj.descripcion, "Descripción")
    
    def test_guardar(self):
        # Prueba de guardado en BD (usar BD temporal)
        pass


if __name__ == "__main__":
    unittest.main()
