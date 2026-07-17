"""
Modelo del módulo Dashboard
"""
import sqlite3
from datetime import date


def calcular_ganancia_estimada_dia(
    conn: sqlite3.Connection, 
    fecha: str | None = None
) -> float:
    """
    Calcula la ganancia estimada para un día específico.
    
    Ganancia = Ventas del día - Costo de ventas
    
    Lógica de costo:
    - Si precio_compra IS NOT NULL AND > 0: usa precio_compra exacto
    - Si no: usa el margen del producto (predeterminado 30%)
    
    Args:
        conn: Conexión SQLite
        fecha: Fecha en formato YYYY-MM-DD. Si es None, usa el día actual.
    
    Returns:
        float: Ganancia estimada total del día (puede ser 0 si no hay ventas)
    """
    if fecha is None:
        fecha = date.today().isoformat()
    
    cursor = conn.cursor()
    
    # Calcula ganancia usando la misma lógica que ReporteModelo
    cursor.execute(
        """
        SELECT SUM(
            CASE
                WHEN p.precio_compra IS NOT NULL AND p.precio_compra > 0 THEN
                    vd.subtotal - (vd.cantidad * p.precio_compra)
                WHEN p.margen IS NOT NULL THEN
                    vd.subtotal * (p.margen / 100.0)
                ELSE
                    0
            END
        ) AS ganancia_estimada
        FROM venta_detalles vd
        JOIN ventas v ON vd.venta_id = v.id
        JOIN productos p ON vd.producto_id = p.id
        WHERE DATE(v.fecha) = ?
        """,
        (fecha,)
    )
    
    resultado = cursor.fetchone()
    ganancia_total = float(resultado[0] or 0.0) if resultado else 0.0
    
    return ganancia_total


def obtener_numero_ventas_dia(
    conn: sqlite3.Connection,
    fecha: str | None = None
) -> int:
    """
    Obtiene el número de ventas realizadas en un día específico.
    
    Args:
        conn: Conexión SQLite
        fecha: Fecha en formato YYYY-MM-DD. Si es None, usa el día actual.
    
    Returns:
        int: Número de ventas del día
    """
    if fecha is None:
        fecha = date.today().isoformat()
    
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT COUNT(DISTINCT v.id)
        FROM ventas v
        WHERE DATE(v.fecha) = ?
        """,
        (fecha,)
    )
    
    resultado = cursor.fetchone()
    return resultado[0] if resultado else 0


class DashboardModelo:
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
