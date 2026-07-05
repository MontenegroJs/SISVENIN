"""
Modelo del módulo Reporte
"""
import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional


class ReporteModelo:
    """
    Modelo responsable de la lógica de acceso a datos para el módulo de Reportes.
    Sigue el patrón MVC y maneja las consultas SQLite.
    """

    base_datos: str = "database/sisvenin.db"

    def _get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos SQLite."""
        db_path = getattr(self, "base_datos", ReporteModelo.base_datos)
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def obtener_resumen_dia(self, fecha: Optional[str] = None) -> Dict[str, Any]:
        """
        Calcula el resumen financiero del día.

        Args:
            fecha (str, optional): Fecha en formato YYYY-MM-DD.
                Si es None, usa la fecha actual del sistema.
        """
        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT
                    COUNT(DISTINCT v.id) AS total_ventas,
                    SUM(vd.subtotal) AS total_ingresos
                FROM ventas v
                JOIN venta_detalles vd ON v.id = vd.venta_id
                WHERE DATE(v.fecha) = ?
                """,
                (fecha,),
            )
            row = cursor.fetchone()
            total_ventas = int(row["total_ventas"] or 0)
            total_ingresos = float(row["total_ingresos"] or 0.0)

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
                JOIN productos p ON vd.producto_id = p.id
                JOIN ventas v ON vd.venta_id = v.id
                WHERE DATE(v.fecha) = ?
                """,
                (fecha,),
            )
            row = cursor.fetchone()
            ganancia_estimada = float(row["ganancia_estimada"] or 0.0)

        margen_promedio = 0.0
        if total_ingresos > 0:
            margen_promedio = (ganancia_estimada / total_ingresos) * 100

        return {
            "total_ingresos": round(total_ingresos, 2),
            "total_ventas": total_ventas,
            "ganancia_estimada": round(ganancia_estimada, 2),
            "margen_promedio": round(margen_promedio, 1),
        }

    def obtener_productos_vendidos_dia(self, fecha: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtiene la lista de productos vendidos en el día con sus métricas.
        """
        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT SUM(vd.subtotal) AS total_dia
                FROM venta_detalles vd
                JOIN ventas v ON vd.venta_id = v.id
                WHERE DATE(v.fecha) = ?
                """,
                (fecha,),
            )
            row = cursor.fetchone()
            total_dia = float(row["total_dia"] or 0.0)

            cursor.execute(
                """
                SELECT
                    p.nombre,
                    SUM(vd.cantidad) AS cantidad,
                    ROUND(SUM(vd.subtotal) / SUM(vd.cantidad), 2) AS precio_unitario,
                    SUM(vd.subtotal) AS subtotal
                FROM venta_detalles vd
                JOIN productos p ON vd.producto_id = p.id
                JOIN ventas v ON vd.venta_id = v.id
                WHERE DATE(v.fecha) = ?
                GROUP BY p.id, p.nombre
                ORDER BY subtotal DESC
                """,
                (fecha,),
            )
            rows = cursor.fetchall()

        productos = []
        for row in rows:
            subtotal = float(row["subtotal"] or 0.0)
            porcentaje = round((subtotal / total_dia) * 100, 1) if total_dia > 0 else 0.0
            productos.append({
                "nombre": row["nombre"],
                "cantidad": int(row["cantidad"] or 0),
                "precio_unitario": float(row["precio_unitario"] or 0.0),
                "subtotal": round(subtotal, 2),
                "porcentaje": porcentaje,
            })

        return productos

    def obtener_ultima_fecha_ventas(self) -> Optional[str]:
        """
        Devuelve la última fecha con ventas registradas en la base de datos.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT MAX(DATE(fecha)) AS ultima_fecha FROM ventas"
            )
            row = cursor.fetchone()
            return row["ultima_fecha"] if row and row["ultima_fecha"] else None

    def obtener_reporte_dia(self, fecha: Optional[str] = None) -> Dict[str, Any]:
        """
        Devuelve todos los datos necesarios para el reporte del día.
        """
        fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        return {
            "fecha": fecha,
            "resumen": self.obtener_resumen_dia(fecha),
            "productos": self.obtener_productos_vendidos_dia(fecha),
        }
