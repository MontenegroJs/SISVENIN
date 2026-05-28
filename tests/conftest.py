# tests/conftest.py
import sys
import os
import pytest
import sqlite3
import shutil
import tempfile
import importlib  # ← Agregar esta importación

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))


def ejecutar_schema(db_path):
    """Ejecuta el schema.sql en la base de datos"""
    schema_path = os.path.join(PROJECT_ROOT, 'database', 'schema.sql')
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql)
        conn.commit()


@pytest.fixture
def db_real():
    """
    Usa una COPIA temporal de la base de datos real.
    Así no afectamos los datos originales y cada prueba tiene su propia BD.
    """
    from app.models.producto_modelo import ProductoModelo
    
    original_db_path = os.path.join(PROJECT_ROOT, 'database', 'sisvenin.db')
    
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    if os.path.exists(original_db_path):
        shutil.copy2(original_db_path, temp_path)
    else:
        ejecutar_schema(temp_path)
    
    original_db = ProductoModelo.base_datos
    ProductoModelo.base_datos = temp_path
    
    yield temp_path
    
    ProductoModelo.base_datos = original_db
    try:
        os.unlink(temp_path)
    except PermissionError:
        pass


@pytest.fixture
def db_real_clean():
    """
    Crea una base de datos NUEVA y VACÍA (no copia la original).
    Útil para pruebas que necesitan empezar desde cero.
    """
    # 🔧 FORZAR RECARGA DEL MÓDULO para evitar la caché
    import app.models.producto_modelo
    importlib.reload(app.models.producto_modelo)
    
    from app.models.producto_modelo import ProductoModelo
    
    # Crear BD temporal vacía
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Ejecutar schema para crear tablas vacías
    ejecutar_schema(temp_path)
    
    # Guardar ruta original del modelo
    original_db = ProductoModelo.base_datos
    
    # Configurar el modelo para usar la BD temporal
    ProductoModelo.base_datos = temp_path
    
    yield temp_path
    
    # Restaurar ruta original
    ProductoModelo.base_datos = original_db
    
    # Eliminar archivo temporal
    try:
        os.unlink(temp_path)
    except PermissionError:
        pass


@pytest.fixture
def temp_db():
    """
    Fixture para pruebas del modelo.
    Crea una base de datos temporal con el esquema completo.
    """
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    ejecutar_schema(temp_path)
    
    from app.models.producto_modelo import ProductoModelo
    original_db = ProductoModelo.base_datos
    ProductoModelo.base_datos = temp_path
    
    yield temp_path
    
    ProductoModelo.base_datos = original_db
    try:
        os.unlink(temp_path)
    except PermissionError:
        pass