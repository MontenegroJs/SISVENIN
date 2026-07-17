"""
Pruebas unitarias para el modelo Reporte
"""
import sqlite3
from datetime import datetime

from app.models.reporte_modelo import ReporteModelo

class TestReporteModelo:

    # Fixture auxiliar para insertar datos de prueba en la BD temporal
    def _insertar_datos_prueba(self, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        productos = [
            (1, "Leche evaporada", 2.50, 1.80, 30.0),
            (2, "Arroz 1kg", 3.50, 2.50, 30.0),
            (3, "Galletas soda", 2.50, 1.50, 30.0),
            (4, "Yogur fresa", 3.00, 2.10, 30.0),
        ]
        cursor.executemany(
            "INSERT INTO productos (id, nombre, precio_venta, precio_compra, margen) VALUES (?, ?, ?, ?, ?)",
            productos
        )

        fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO ventas (id, fecha, total) VALUES (1, ?, 10.50)", (fecha_hoy,))
        cursor.execute("INSERT INTO ventas (id, fecha, total) VALUES (2, ?, 20.00)", (fecha_hoy,))

        detalles_venta_1 = [
            (1, 1, 2, 2.50, 5.00),
            (1, 2, 1, 3.50, 3.50)
        ]
        cursor.executemany(
            "INSERT INTO venta_detalles (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?)",
            detalles_venta_1
        )

        detalles_venta_2 = [
            (2, 3, 5, 2.50, 12.50),
            (2, 4, 3, 3.00, 9.00)
        ]
        cursor.executemany(
            "INSERT INTO venta_detalles (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?)",
            detalles_venta_2
        )

        conn.commit()
        conn.close()

    # ==========================================
    # PRUEBAS UNITARIAS (TDD)
    # ==========================================

    def test_obtener_resumen_dia_con_ventas(self, db_real_clean):
        """
        HU-06: Verifica que el modelo calcule correctamente el resumen del día
        (Total Ingresos, Ganancia, Margen promedio y conteo de ventas).
        """
        self._insertar_datos_prueba(db_real_clean)

        modelo = ReporteModelo()
        modelo.base_datos = db_real_clean
        resumen = modelo.obtener_resumen_dia()

        assert resumen["total_ingresos"] == 30.00
        assert resumen["total_ventas"] == 2
        assert round(resumen["ganancia_estimada"], 2) == 10.10
        assert round(resumen["margen_promedio"], 1) == 33.7

    def test_obtener_productos_vendidos_dia(self, db_real_clean):
        """
        HU-06: Verifica que el modelo devuelva la lista de productos vendidos
        con sus cantidades, subtotales y el porcentaje de contribución.
        """
        self._insertar_datos_prueba(db_real_clean)

        modelo = ReporteModelo()
        modelo.base_datos = db_real_clean
        productos = modelo.obtener_productos_vendidos_dia()

        assert len(productos) == 4

        producto_top = productos[0]
        assert producto_top["nombre"] == "Galletas soda"
        assert producto_top["cantidad"] == 5
        assert producto_top["subtotal"] == 12.50
        assert round(producto_top["porcentaje"], 1) == 41.7

        producto_last = productos[-1]
        assert producto_last["nombre"] == "Arroz 1kg"
        assert producto_last["cantidad"] == 1
        assert producto_last["subtotal"] == 3.50
        assert round(producto_last["porcentaje"], 1) == 11.7

    def test_obtener_datos_sin_ventas(self, db_real_clean):
        """
        HU-06 (Caso borde): Verifica que el modelo retorne valores en cero 
        cuando no hay ventas registradas en el día.
        """
        modelo = ReporteModelo()
        modelo.base_datos = db_real_clean

        resumen = modelo.obtener_resumen_dia()
        productos = modelo.obtener_productos_vendidos_dia()

        assert resumen["total_ingresos"] == 0.0
        assert resumen["total_ventas"] == 0
        assert resumen["ganancia_estimada"] == 0.0
        assert resumen["margen_promedio"] == 0.0
        assert len(productos) == 0