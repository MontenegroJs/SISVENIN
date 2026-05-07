# src/app/modules/producto/producto_repository.py
"""
Repository del módulo Producto (Acceso a datos)
Simplificado para la prueba inicial
"""
import sqlite3
import os
from .producto_modelo import Producto


class ProductoRepository:
    # Ruta a la base de datos
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'database', 'sisvenin.db')
    DB_PATH = os.path.abspath(DB_PATH)
    
    @classmethod
    def inicializar(cls):
        """Inicializa la base de datos (crea tablas si no existen)"""
        cls.crear_tabla()
    
    @classmethod
    def _get_connection(cls):
        """Obtiene conexión a la base de datos"""
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(cls.DB_PATH), exist_ok=True)
        return sqlite3.connect(cls.DB_PATH)
    
    @classmethod
    def crear_tabla(cls):
        """Crea la tabla de productos si no existe"""
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print(f"✅ Tabla 'productos' creada/verificada en {cls.DB_PATH}")
    
    @classmethod
    def guardar(cls, producto):
        """Guarda un producto en la base de datos"""
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            (producto.nombre, producto.precio, producto.stock)
        )
        conn.commit()
        producto.id = cursor.lastrowid
        conn.close()
        return producto
    
    @classmethod
    def obtener_todos(cls):
        """Obtiene todos los productos"""
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM productos")
        rows = cursor.fetchall()
        conn.close()
        
        productos = []
        for row in rows:
            productos.append(Producto(id=row[0], nombre=row[1], precio=row[2], stock=row[3]))
        return productos