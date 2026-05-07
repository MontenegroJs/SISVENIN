# tests/conftest.py
"""
Configuración global de pytest para SISVENIN
Solo para el módulo Producto (por ahora)
"""
import sys
import os
import pytest
import tempfile

# Agregar la carpeta RAIZ del proyecto al path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))


# ========== FIXTURES PARA PRODUCTO ==========

@pytest.fixture
def producto_ejemplo():
    """Retorna un producto de ejemplo para pruebas"""
    from src.app.modules.producto.producto_modelo import Producto
    return Producto(id=None, nombre="Producto Test", precio=10.5, stock=100)


@pytest.fixture
def producto_con_id():
    """Retorna un producto con ID (como si viniera de BD)"""
    from src.app.modules.producto.producto_modelo import Producto
    return Producto(id=1, nombre="Arroz", precio=3.50, stock=50)


@pytest.fixture
def lista_productos():
    """Retorna una lista de productos de ejemplo"""
    from src.app.modules.producto.producto_modelo import Producto
    return [
        Producto(id=1, nombre="Arroz", precio=3.50, stock=50),
        Producto(id=2, nombre="Leche", precio=2.00, stock=30),
        Producto(id=3, nombre="Pan", precio=1.00, stock=100),
    ]


# ========== FIXTURES PARA BASE DE DATOS TEMPORAL ==========

@pytest.fixture
def temp_db():
    """Crea una base de datos temporal para pruebas del repositorio"""
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    yield temp_path
    
    # Limpiar al final
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def repo_con_temp_db(temp_db):
    """
    Retorna un ProductoRepository que usa una BD temporal
    """
    from src.app.modules.producto import producto_repository
    from src.app.modules.producto.producto_repository import ProductoRepository
    
    # Guardar ruta original
    original_path = ProductoRepository.DB_PATH
    
    # Usar ruta temporal
    ProductoRepository.DB_PATH = temp_db
    
    # Crear tabla
    ProductoRepository.crear_tabla()
    
    yield ProductoRepository
    
    # Restaurar ruta original
    ProductoRepository.DB_PATH = original_path