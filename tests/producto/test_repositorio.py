"""
Pruebas para el repositorio de Producto
"""
import pytest
import tempfile
import os


@pytest.fixture
def temp_db_producto():
    """Crea una base de datos temporal para pruebas"""
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)


def test_repositorio_con_temp_db(temp_db_producto):
    """Prueba básica del repositorio con BD temporal"""
    from src.app.modules.producto.producto_repositorio import ProductoRepositorio
    from src.app.modules.producto.producto_modelo import ProductoModelo
    
    # Guardar ruta original
    original_path = ProductoRepositorio.DB_PATH
    
    try:
        # Usar BD temporal
        ProductoRepositorio.DB_PATH = temp_db_producto
        ProductoRepositorio.crear_tabla()
        
        # Guardar
        obj = ProductoModelo(nombre="Test Repositorio", descripcion="Probando")
        ProductoRepositorio.guardar(obj)
        
        assert obj.id is not None
        assert obj.id > 0
        
        # Recuperar
        todos = ProductoRepositorio.obtener_todos()
        assert len(todos) >= 1
        assert todos[0].nombre == "Test Repositorio"
        
    finally:
        # Restaurar ruta original
        ProductoRepositorio.DB_PATH = original_path
