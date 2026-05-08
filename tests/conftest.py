# tests/conftest.py
"""
Configuración global de pytest para SISVENIN
Fixtures y configuración compartida para todos los módulos
"""
import sys
import os
import pytest
import tempfile

# Agregar la carpeta RAIZ del proyecto al path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))


# ========== CONFIGURACIÓN GENERAL ==========

def pytest_configure(config):
    """Configuración adicional de pytest"""
    # Marcar pruebas que requieren base de datos
    config.addinivalue_line(
        "markers", "db: marca pruebas que necesitan base de datos real"
    )
    # Marcar pruebas lentas
    config.addinivalue_line(
        "markers", "slow: marca pruebas que son lentas"
    )


# ========== FIXTURES COMPARTIDOS ==========

@pytest.fixture
def temp_db_base():
    """Crea una base de datos temporal para pruebas (usar en cada módulo)"""
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    yield temp_path
    
    # Limpiar al final
    if os.path.exists(temp_path):
        os.unlink(temp_path)


# ========== FIXTURES PARA MÓDULO PRODUCTO ==========

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


@pytest.fixture
def repo_producto_temp(temp_db_base):
    """
    Retorna un ProductoRepositorio que usa una BD temporal
    """
    from src.app.modules.producto.producto_repositorio import ProductoRepositorio
    
    # Guardar ruta original
    original_path = ProductoRepositorio.DB_PATH
    
    # Usar ruta temporal
    ProductoRepositorio.DB_PATH = temp_db_base
    
    # Crear tabla
    ProductoRepositorio.crear_tabla()
    
    yield ProductoRepositorio
    
    # Restaurar ruta original
    ProductoRepositorio.DB_PATH = original_path


# ========== FIXTURES GENÉRICOS (para módulos futuros) ==========

@pytest.fixture
def temp_db_modular(request):
    """
    Fixture genérico para crear BD temporal para cualquier repositorio
    
    Uso:
        def test_algo(temp_db_modular):
            from src.app.modules.mimodulo.mimodulo_repositorio import MiModuloRepositorio
            original = MiModuloRepositorio.DB_PATH
            MiModuloRepositorio.DB_PATH = temp_db_modular
            MiModuloRepositorio.crear_tabla()
            yield MiModuloRepositorio
            MiModuloRepositorio.DB_PATH = original
    """
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    yield temp_path
    
    if os.path.exists(temp_path):
        os.unlink(temp_path)