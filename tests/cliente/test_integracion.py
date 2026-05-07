"""
Pruebas de integración para el módulo Cliente
"""
import pytest
from src.app.modules.cliente.cliente_modelo import Cliente
from src.app.modules.cliente.cliente_controller import ClienteController


def test_crear_y_validar():
    """Prueba integración entre modelo y controlador"""
    nombre = "Producto Integración"
    
    # Validar
    assert ClienteController.validar_nombre(nombre) is True
    
    # Crear
    obj = Cliente(nombre=nombre, descripcion="Test")
    assert obj.nombre == nombre
