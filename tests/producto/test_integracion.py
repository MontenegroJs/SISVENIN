"""
Pruebas de integración para el módulo Producto
"""
import pytest
from src.app.modules.producto.producto_modelo import ProductoModelo
from src.app.modules.producto.producto_controlador import ProductoControlador


def test_crear_y_validar():
    """Prueba integración entre modelo y controlador"""
    nombre = "Producto Integración"
    
    # Validar
    assert ProductoControlador.validar_nombre(nombre) is True
    
    # Crear
    obj = ProductoModelo(nombre=nombre, descripcion="Test Integración")
    assert obj.nombre == nombre


def test_listar_ejemplo_integracion():
    """Prueba que listar_ejemplo retorne datos"""
    lista = ProductoControlador.listar_ejemplo()
    assert len(lista) > 0
    assert hasattr(lista[0], 'id')
    assert hasattr(lista[0], 'nombre')
