"""
Pruebas para el repositorio de Cliente
"""
import pytest
import tempfile
import os


@pytest.fixture
def temp_db_cliente():
    """Crea una base de datos temporal para pruebas"""
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)


def test_repository_con_temp_db(temp_db_cliente):
    """Prueba básica del repositorio con BD temporal"""
    from src.app.modules.cliente.cliente_repository import ClienteRepository
    from src.app.modules.cliente.cliente_modelo import Cliente
    
    # Guardar ruta original
    original_path = ClienteRepository.DB_PATH
    
    try:
        # Usar BD temporal
        ClienteRepository.DB_PATH = temp_db_cliente
        ClienteRepository.crear_tabla()
        
        # Guardar
        obj = Cliente(nombre="Test Repository", descripcion="Probando")
        ClienteRepository.guardar(obj)
        
        assert obj.id is not None
        assert obj.id > 0
        
        # Recuperar
        todos = ClienteRepository.obtener_todos()
        assert len(todos) >= 1
        assert todos[0].nombre == "Test Repository"
        
    finally:
        # Restaurar ruta original
        ClienteRepository.DB_PATH = original_path
