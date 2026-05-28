"""
Modelo del módulo Venta_detalle
"""
import sqlite3
import os

class Venta_detalleModelo:
    def __init__(self, id=None, nombre="", descripcion=""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.activo = True

    def __str__(self):
        return f"{self.nombre} (ID: {self.id})"
    
    def guardar(self):
        """Guarda el objeto en la base de datos (MVC puro - el modelo accede a BD)"""
        # Aquí iría la lógica de inserción/actualización en SQLite
        pass
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los registros de la base de datos"""
        # Aquí iría la consulta SELECT
        pass
