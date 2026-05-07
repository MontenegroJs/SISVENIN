"""
Módulo Cliente
Exporta las clases principales
"""
from .cliente_modelo import Cliente
from .cliente_controller import ClienteController
from .cliente_repository import ClienteRepository
from .cliente_vista import ClienteVista

__all__ = [
    'Cliente',
    'ClienteController',
    'ClienteRepository',
    'ClienteVista',
]
