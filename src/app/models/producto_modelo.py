"""
Modelo del módulo Producto - SISVENIN
HU-08: CRUD de productos con precio sugerido

Convenciones:
- Type hints para todos los métodos públicos
- Docstrings en formato Google Style
- Snake_case para métodos y variables
- MVC puro: el modelo accede directamente a SQLite
"""

import sqlite3
import os
from typing import List, Optional
from datetime import date, timedelta


class ProductoModelo:
    """
    Modelo de datos para un producto del inventario.
    
    Attributes:
        id: Identificador único del producto (None si no está guardado)
        nombre: Nombre del producto
        precio_compra: Precio al que compró la dueña
        precio_venta: Precio de venta al público
        margen: Porcentaje de ganancia (default 30.0)
        stock: Cantidad disponible en inventario
        vencimiento: Fecha de caducidad (opcional)
        activo: Borrado lógico (1=activo, 0=eliminado)
    """
    
    # Variable de clase para la ruta de la base de datos
    base_datos: str = "database/sisvenin.db"
    
    def __init__(
        self,
        id: Optional[int] = None,
        nombre: str = "",
        precio_compra: float = 0.0,
        precio_venta: float = 0.0,
        margen: float = 30.0,
        stock: int = 0,
        vencimiento: Optional[date] = None,
        activo: bool = True
    ):
        """
        Inicializa un producto.
        
        Args:
            id: Identificador único (None para productos nuevos)
            nombre: Nombre del producto
            precio_compra: Precio de compra
            precio_venta: Precio de venta
            margen: Porcentaje de ganancia (default 30)
            stock: Cantidad disponible
            vencimiento: Fecha de caducidad
            activo: Estado activo/inactivo
        """
        self.id: Optional[int] = id
        self.nombre: str = nombre
        self.precio_compra: float = precio_compra
        self.precio_venta: float = precio_venta
        self.margen: float = margen
        self.stock: int = stock
        self.vencimiento: Optional[date] = vencimiento
        self.activo: bool = activo
    
    def __str__(self) -> str:
        """Representación en string del producto."""
        return f"{self.nombre} (ID: {self.id})"
    
    # ==================== MÉTODOS DE CÁLCULO ====================
    
    def calcular_precio_sugerido(self) -> float:
        """
        Calcula el precio de venta sugerido basado en precio_compra y margen.
        
        Fórmula: Precio Venta = Precio Compra × (1 + Margen/100)
        El resultado se redondea a 2 decimales.
        
        Returns:
            Precio sugerido redondeado a 2 decimales
        """
        precio_sugerido = self.precio_compra * (1 + self.margen / 100)
        return round(precio_sugerido, 2)
    
    # ==================== MÉTODOS DE VALIDACIÓN ====================
    
    def validar(self) -> None:
        """
        Valida que los datos del producto sean correctos.
        
        Raises:
            ValueError: Si algún campo no cumple las validaciones
        """
        # Validar nombre
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre es obligatorio")
        
        # Validar precio de compra
        if self.precio_compra <= 0:
            raise ValueError("El precio de compra debe ser mayor a 0")
        
        # Validar margen
        if self.margen < 0:
            raise ValueError("El margen no puede ser negativo")
        
        # Validar stock
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
    
    # ==================== MÉTODOS DE BASE DE DATOS ====================
    
    @classmethod
    def _get_connection(cls) -> sqlite3.Connection:
        """
        Obtiene una conexión a la base de datos.
        
        Returns:
            Conexión SQLite
        """
        # Asegurar que el directorio database existe
        db_dir = os.path.dirname(cls.base_datos)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        return sqlite3.connect(cls.base_datos)
    
    @classmethod
    def inicializar_tabla(cls) -> None:
        """
        Crea la tabla de productos si no existe.
        Basado en el schema.sql del proyecto.
        """
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio_venta REAL NOT NULL,
                    stock INTEGER NOT NULL DEFAULT 0,
                    precio_compra REAL,
                    margen REAL DEFAULT 30.0,
                    vencimiento TEXT,
                    activo INTEGER DEFAULT 1
                )
            """)
            conn.commit()
    
    def guardar(self) -> None:
        """
        Guarda el producto en la base de datos.
        Si tiene id, actualiza; si no, inserta un nuevo registro.
        """
        self.validar()
        
        # Si precio_venta no está definido, calcularlo automáticamente
        if self.precio_venta == 0.0:
            self.precio_venta = self.calcular_precio_sugerido()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if self.id is None:
                # INSERT
                cursor.execute("""
                    INSERT INTO productos 
                    (nombre, precio_compra, precio_venta, margen, stock, vencimiento, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.nombre,
                    self.precio_compra,
                    self.precio_venta,
                    self.margen,
                    self.stock,
                    self.vencimiento.isoformat() if self.vencimiento else None,
                    1 if self.activo else 0
                ))
                self.id = cursor.lastrowid
            else:
                # UPDATE
                cursor.execute("""
                    UPDATE productos 
                    SET nombre = ?, precio_compra = ?, precio_venta = ?,
                        margen = ?, stock = ?, vencimiento = ?, activo = ?
                    WHERE id = ?
                """, (
                    self.nombre,
                    self.precio_compra,
                    self.precio_venta,
                    self.margen,
                    self.stock,
                    self.vencimiento.isoformat() if self.vencimiento else None,
                    1 if self.activo else 0,
                    self.id
                ))
            
            conn.commit()
    
    def eliminar(self) -> None:
        """
        Elimina el producto de la base de datos (borrado físico).
        """
        if self.id is None:
            return
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (self.id,))
            conn.commit()
            self.id = None
    
    @classmethod
    def obtener_todos(cls, solo_activos: bool = True) -> List['ProductoModelo']:
        """
        Obtiene todos los productos de la base de datos.
        
        Args:
            solo_activos: Si es True, solo devuelve productos activos
            
        Returns:
            Lista de objetos ProductoModelo
        """
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            
            if solo_activos:
                cursor.execute("SELECT * FROM productos WHERE activo = 1 ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM productos ORDER BY nombre")
            
            rows = cursor.fetchall()
            return [cls._row_to_producto(row) for row in rows]
    
    @classmethod
    def obtener_por_id(cls, id: int) -> Optional['ProductoModelo']:
        """
        Obtiene un producto por su ID.
        
        Args:
            id: Identificador del producto
            
        Returns:
            ProductoModelo o None si no existe
        """
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
            row = cursor.fetchone()
            
            if row:
                return cls._row_to_producto(row)
            return None
    
    @classmethod
    def buscar_por_nombre(cls, termino: str) -> List['ProductoModelo']:
        """
        Busca productos por nombre (coincidencia parcial, case insensitive).
        
        Args:
            termino: Texto a buscar
            
        Returns:
            Lista de productos que coinciden
        """
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM productos 
                WHERE activo = 1 AND nombre LIKE ?
                ORDER BY nombre
            """, (f"%{termino}%",))
            
            rows = cursor.fetchall()
            return [cls._row_to_producto(row) for row in rows]
    
    @classmethod
    def buscar_por_codigo_barras(cls, codigo: str) -> Optional['ProductoModelo']:
        """
        Busca un producto por código de barras (coincidencia exacta).
        
        Args:
            codigo: Código de barras del producto.
        
        Returns:
            Producto encontrado o None si no existe.
        """
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM productos 
                WHERE activo = 1 AND codigo_barras = ?
                LIMIT 1
            """, (codigo,))
            row = cursor.fetchone()
            
            if row:
                return cls._row_to_producto(row)
            return None

    @classmethod
    def buscar_rapido(cls, termino: str, limite: int = 10) -> List['ProductoModelo']:
        """
        Búsqueda rápida unificada (nombre o código) para POS.
        
        Args:
            termino: Texto a buscar (puede ser nombre o código de barras).
            limite: Número máximo de resultados.
        
        Returns:
            Lista de productos que coinciden.
        """
        # Si el término es numérico, intentar búsqueda exacta por código primero
        if termino.isdigit():
            producto = cls.buscar_por_codigo_barras(termino)
            if producto:
                return [producto]
        
        # Búsqueda por nombre (coincidencia parcial)
        return cls.buscar_por_nombre(termino)
    
    @classmethod
    def obtener_stock_bajo(cls, limite: int = 5) -> List['ProductoModelo']:
        """
        Obtiene productos con stock menor al límite.
        
        Args:
            limite: Valor límite de stock (default 5)
            
        Returns:
            Lista de productos con stock bajo
        """
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM productos 
                WHERE activo = 1 AND stock < ?
                ORDER BY stock ASC
            """, (limite,))
            
            rows = cursor.fetchall()
            return [cls._row_to_producto(row) for row in rows]
    
    @classmethod
    def obtener_por_vencer(cls, dias: int = 7) -> List['ProductoModelo']:
        """
        Obtiene productos con fecha de vencimiento dentro de X días.
        
        Args:
            dias: Número de días para considerar "próximo a vencer"
            
        Returns:
            Lista de productos próximos a vencer
        """
        hoy = date.today()
        fecha_limite = hoy + timedelta(days=dias)
        
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM productos 
                WHERE activo = 1 
                  AND vencimiento IS NOT NULL 
                  AND vencimiento >= ? 
                  AND vencimiento <= ?
                ORDER BY vencimiento ASC
            """, (hoy.isoformat(), fecha_limite.isoformat()))
            
            rows = cursor.fetchall()
            return [cls._row_to_producto(row) for row in rows]
    
    @classmethod
    def _row_to_producto(cls, row: tuple) -> 'ProductoModelo':
        """
        Convierte una fila de la base de datos en un objeto ProductoModelo.
        
        Estructura esperada de la tabla (según schema.sql):
        0: id
        1: nombre
        2: precio_venta
        3: stock
        4: precio_compra
        5: margen
        6: vencimiento
        7: activo
        """
        vencimiento = None
        if len(row) > 6 and row[6]:
            try:
                vencimiento = date.fromisoformat(row[6])
            except ValueError:
                pass
        
        return cls(
            id=row[0],
            nombre=row[1],
            precio_compra=row[4] if len(row) > 4 and row[4] else 0.0,
            precio_venta=row[2] if len(row) > 2 and row[2] else 0.0,
            margen=row[5] if len(row) > 5 and row[5] else 30.0,
            stock=row[3] if len(row) > 3 and row[3] else 0,
            vencimiento=vencimiento,
            activo=bool(row[7]) if len(row) > 7 else True
        )