"""
Repository del módulo Cliente (Acceso a datos)
"""
import sqlite3
import os
from .cliente_modelo import Cliente


class ClienteRepository:
    # Ruta a la base de datos
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'database', 'sisvenin.db')
    DB_PATH = os.path.abspath(DB_PATH)

    @classmethod
    def _get_connection(cls):
        """Obtiene conexión a la base de datos"""
        os.makedirs(os.path.dirname(cls.DB_PATH), exist_ok=True)
        return sqlite3.connect(cls.DB_PATH)

    @classmethod
    def inicializar(cls):
        """Inicializa la base de datos"""
        cls.crear_tabla()

    @classmethod
    def crear_tabla(cls):
        """Crea la tabla si no existe"""
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                activo INTEGER DEFAULT 1
            )
        """)
        conn.commit()
        conn.close()
        print(f"✓ Tabla 'clientes' creada/verificada")

    @classmethod
    def guardar(cls, obj):
        """Guarda un objeto en la base de datos"""
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO clientes (nombre, descripcion, activo) VALUES (?, ?, ?)",
            (obj.nombre, obj.descripcion, 1 if obj.activo else 0)
        )
        conn.commit()
        obj.id = cursor.lastrowid
        conn.close()
        return obj

    @classmethod
    def obtener_todos(cls):
        """Obtiene todos los objetos"""
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, nombre, descripcion, activo FROM clientes WHERE activo = 1")
        rows = cursor.fetchall()
        conn.close()
        
        objetos = []
        for row in rows:
            obj = Cliente(id=row[0], nombre=row[1], descripcion=row[2])
            obj.activo = bool(row[3])
            objetos.append(obj)
        return objetos

    @classmethod
    def obtener_por_id(cls, obj_id):
        """Obtiene un objeto por su ID"""
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, nombre, descripcion, activo FROM clientes WHERE id = ?", (obj_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            obj = Cliente(id=row[0], nombre=row[1], descripcion=row[2])
            obj.activo = bool(row[3])
            return obj
        return None

    @classmethod
    def actualizar(cls, obj):
        """Actualiza un objeto existente"""
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE clientes SET nombre = ?, descripcion = ?, activo = ? WHERE id = ?",
            (obj.nombre, obj.descripcion, 1 if obj.activo else 0, obj.id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def eliminar(cls, obj_id):
        """Elimina un objeto (borrado lógico)"""
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE clientes SET activo = 0 WHERE id = ?", (obj_id,))
        conn.commit()
        conn.close()
