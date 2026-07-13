"""
Pruebas unitarias para el modelo Dashboard
"""

import sqlite3
from datetime import date, timedelta

import pytest

from src.app.models.dashboard_modelo import calcular_ganancia_estimada_dia, obtener_numero_ventas_dia


def _crear_producto(conn: sqlite3.Connection, nombre: str, precio_venta: float,
                     precio_compra: float | None, margen: float = 30.0, stock: int = 100) -> int:
    """Inserta un producto de prueba y retorna su id."""
    cursor = conn.execute(
        """
        INSERT INTO productos (nombre, precio_venta, precio_compra, margen, stock, activo)
        VALUES (?, ?, ?, ?, ?, 1)
        """,
        (nombre, precio_venta, precio_compra, margen, stock),
    )
    conn.commit()
    return cursor.lastrowid


def _crear_venta(conn: sqlite3.Connection, fecha: str, total: float) -> int:
    """Inserta una venta de prueba y retorna su id."""
    cursor = conn.execute(
        "INSERT INTO ventas (fecha, total) VALUES (?, ?)",
        (fecha, total),
    )
    conn.commit()
    return cursor.lastrowid


def _crear_detalle_venta(conn: sqlite3.Connection, venta_id: int, producto_id: int,
                          cantidad: int, precio_unitario: float, subtotal: float) -> None:
    """Inserta un detalle de venta de prueba."""
    conn.execute(
        """
        INSERT INTO venta_detalles
            (venta_id, producto_id, cantidad, precio_unitario, subtotal)
        VALUES (?, ?, ?, ?, ?)
      
        """,
        (venta_id, producto_id, cantidad, precio_unitario, subtotal),
    )
    conn.commit()


class TestCalcularGananciaEstimadaDia:
    """Pruebas para la función calcular_ganancia_estimada_dia."""

    def test_sin_ventas_ganancia_es_cero(self, db_connection):
        """Si no hay ventas registradas hoy, la ganancia estimada debe ser 0."""
        hoy = date.today().isoformat()

        ganancia = calcular_ganancia_estimada_dia(db_connection, fecha=hoy)

        assert ganancia == 0

    def test_venta_con_precio_compra_registrado(self, db_connection):
        """
        Un producto con precio_compra definido debe usar ese valor exacto
        para calcular el costo, sin aplicar el margen del producto.
        """
        hoy = date.today().isoformat()
        producto_id = _crear_producto(
            db_connection, "Arroz 1kg", precio_venta=5.00, precio_compra=3.50, margen=30.0
        )
        venta_id = _crear_venta(db_connection, fecha=hoy, total=10.00)
        _crear_detalle_venta(
            db_connection, venta_id, producto_id,
            cantidad=2, precio_unitario=5.00, subtotal=10.00
        )

        # Ventas: 10.00 | Costo: 2 * 3.50 = 7.00 | Ganancia esperada: 3.00
        ganancia = calcular_ganancia_estimada_dia(db_connection, fecha=hoy)

        assert ganancia == pytest.approx(3.00)

    def test_venta_sin_precio_compra_usa_margen_del_producto(self, db_connection):
        """
        Si el producto no tiene precio_compra, usa el margen del producto.
        Con margen=30%, la ganancia es subtotal * 0.30
        """
        hoy = date.today().isoformat()
        # Producto sin precio_compra, margen 30% (por defecto)
        producto_id = _crear_producto(
            db_connection, "Fideos 500g", precio_venta=4.00, precio_compra=None, margen=30.0
        )
        venta_id = _crear_venta(db_connection, fecha=hoy, total=4.00)
        _crear_detalle_venta(
            db_connection, venta_id, producto_id,
            cantidad=1, precio_unitario=4.00, subtotal=4.00
        )

        # Con margen 30%: ganancia = 4.00 * (30 / 100) = 1.20
        ganancia = calcular_ganancia_estimada_dia(db_connection, fecha=hoy)

        assert ganancia == pytest.approx(1.20)

    def test_multiples_ventas_del_dia_suma_ganancias(self, db_connection):
        """
        Si hay múltiples ventas en el mismo día, la ganancia debe ser
        la suma de todas las ganancias individuales.
        """
        hoy = date.today().isoformat()
        
        # Producto 1: con precio_compra
        prod1_id = _crear_producto(
            db_connection, "Arroz 1kg", precio_venta=5.00, precio_compra=3.50, margen=30.0
        )
        # Producto 2: sin precio_compra (usa margen 30%)
        prod2_id = _crear_producto(
            db_connection, "Fideos 500g", precio_venta=4.00, precio_compra=None, margen=30.0
        )
        
        # Venta 1
        venta1_id = _crear_venta(db_connection, fecha=hoy, total=10.00)
        _crear_detalle_venta(db_connection, venta1_id, prod1_id, 2, 5.00, 10.00)
        
        # Venta 2
        venta2_id = _crear_venta(db_connection, fecha=hoy, total=8.00)
        _crear_detalle_venta(db_connection, venta2_id, prod2_id, 2, 4.00, 8.00)
        
        # Ganancia esperada:
        # Venta 1 (con precio_compra): 10.00 - (2 * 3.50) = 3.00
        # Venta 2 (margen 30%): 8.00 * 0.30 = 2.40
        # Total: 3.00 + 2.40 = 5.40
        ganancia = calcular_ganancia_estimada_dia(db_connection, fecha=hoy)

        assert ganancia == pytest.approx(5.40)

    def test_ventas_de_otro_dia_no_se_incluyen(self, db_connection):
        """
        Las ventas de días anteriores no deben incluirse en el cálculo
        de la ganancia estimada del día actual.
        """
        hoy = date.today().isoformat()
        ayer = (date.today() - timedelta(days=1)).isoformat()
        
        producto_id = _crear_producto(
            db_connection, "Producto Test", precio_venta=10.00, precio_compra=6.00, margen=30.0
        )
        
        # Venta de ayer
        venta_ayer = _crear_venta(db_connection, fecha=ayer, total=10.00)
        _crear_detalle_venta(db_connection, venta_ayer, producto_id, 1, 10.00, 10.00)
        
        # Venta de hoy
        venta_hoy = _crear_venta(db_connection, fecha=hoy, total=10.00)
        _crear_detalle_venta(db_connection, venta_hoy, producto_id, 1, 10.00, 10.00)
        
        # Solo debe contar la ganancia de hoy: 10.00 - 6.00 = 4.00
        ganancia = calcular_ganancia_estimada_dia(db_connection, fecha=hoy)

        assert ganancia == pytest.approx(4.00)

    def test_mezcla_productos_con_y_sin_precio_compra(self, db_connection):
        """
        Valida que el cálculo funciona correctamente cuando hay una mezcla
        de productos con precio_compra definido y sin él.
        """
        hoy = date.today().isoformat()
        
        prod_con_precio = _crear_producto(
            db_connection, "Producto A", precio_venta=100.00, precio_compra=60.00, margen=30.0
        )
        prod_sin_precio = _crear_producto(
            db_connection, "Producto B", precio_venta=50.00, precio_compra=None, margen=30.0
        )
        
        venta_id = _crear_venta(db_connection, fecha=hoy, total=150.00)
        _crear_detalle_venta(db_connection, venta_id, prod_con_precio, 1, 100.00, 100.00)
        _crear_detalle_venta(db_connection, venta_id, prod_sin_precio, 1, 50.00, 50.00)
        
        # Ganancia esperada:
        # Producto A (con precio_compra): 100.00 - 60.00 = 40.00
        # Producto B (margen 30%): 50.00 * 0.30 = 15.00
        # Total: 40.00 + 15.00 = 55.00
        ganancia = calcular_ganancia_estimada_dia(db_connection, fecha=hoy)

        assert ganancia == pytest.approx(55.00)

    def test_venta_mixta_con_y_sin_precio_compra(self, db_connection):
        """
        Una venta con varios productos, algunos con precio_compra registrado
        y otros sin él, debe combinar ambas reglas correctamente.
        """
        hoy = date.today().isoformat()
        producto_con_costo = _crear_producto(
            db_connection, "Aceite 1L", precio_venta=8.00, precio_compra=6.00, margen=30.0
        )
        producto_sin_costo = _crear_producto(
            db_connection, "Azúcar 1kg", precio_venta=4.50, precio_compra=None, margen=30.0
        )
        venta_id = _crear_venta(db_connection, fecha=hoy, total=12.50)
        _crear_detalle_venta(
            db_connection, venta_id, producto_con_costo,
            cantidad=1, precio_unitario=8.00, subtotal=8.00
        )
        _crear_detalle_venta(
            db_connection, venta_id, producto_sin_costo,
            cantidad=1, precio_unitario=4.50, subtotal=4.50
        )

        # Ganancia por producto:
        # Con precio_compra: 8.00 - 6.00 = 2.00
        # Con margen 30%: 4.50 * 0.30 = 1.35
        # Total: 2.00 + 1.35 = 3.35
        ganancia = calcular_ganancia_estimada_dia(db_connection, fecha=hoy)

        assert ganancia == pytest.approx(3.35)

    def test_solo_considera_ventas_de_la_fecha_indicada(self, db_connection):
        """
        Las ventas de días distintos al consultado NO deben incluirse
        en el cálculo de la ganancia estimada.
        """
        hoy = date.today().isoformat()
        ayer = (date.today() - timedelta(days=1)).isoformat()

        producto_id = _crear_producto(
            db_connection, "Leche 1L", precio_venta=4.00, precio_compra=3.00, margen=30.0
        )

        # Venta de ayer (no debe contar)
        venta_ayer = _crear_venta(db_connection, fecha=ayer, total=4.00)
        _crear_detalle_venta(
            db_connection, venta_ayer, producto_id,
            cantidad=1, precio_unitario=4.00, subtotal=4.00
        )

        # Venta de hoy (sí debe contar)
        venta_hoy = _crear_venta(db_connection, fecha=hoy, total=8.00)
        _crear_detalle_venta(
            db_connection, venta_hoy, producto_id,
            cantidad=2, precio_unitario=4.00, subtotal=8.00
        )

        # Solo la venta de hoy: ventas 8.00 - costo (2 * 3.00 = 6.00) = 2.00
        ganancia = calcular_ganancia_estimada_dia(db_connection, fecha=hoy)

        assert ganancia == pytest.approx(2.00)

    def test_ganancia_puede_ser_negativa_si_se_vendio_a_perdida(self, db_connection):
        """
        Si el precio_compra es mayor al precio_unitario vendido (venta a
        pérdida o error de carga), la ganancia estimada debe reflejar
        un valor negativo, sin lanzar excepciones.
        """
        hoy = date.today().isoformat()
        producto_id = _crear_producto(
            db_connection, "Producto en oferta", precio_venta=3.00, precio_compra=5.00, margen=30.0
        )
        venta_id = _crear_venta(db_connection, fecha=hoy, total=3.00)
        _crear_detalle_venta(
            db_connection, venta_id, producto_id,
            cantidad=1, precio_unitario=3.00, subtotal=3.00
        )

        # Ganancia esperada: 3.00 - 5.00 = -2.00
        ganancia = calcular_ganancia_estimada_dia(db_connection, fecha=hoy)

        assert ganancia == pytest.approx(-2.00)

    def test_redondeo_a_dos_decimales(self, db_connection):
        """
        El resultado debe entregarse redondeado a 2 decimales, dado que
        se trabaja con soles (S/) y no tiene sentido mostrar más precisión.
        """
        hoy = date.today().isoformat()
        producto_id = _crear_producto(
            db_connection, "Producto con decimales", precio_venta=3.33, precio_compra=None, margen=30.0
        )
        venta_id = _crear_venta(db_connection, fecha=hoy, total=3.33)
        _crear_detalle_venta(
            db_connection, venta_id, producto_id,
            cantidad=1, precio_unitario=3.33, subtotal=3.33
        )

        ganancia = calcular_ganancia_estimada_dia(db_connection, fecha=hoy)

        # Con margen 30%: 3.33 * 0.30 = 0.999
        assert ganancia == pytest.approx(0.999, abs=0.001)


class TestObtenerNumeroVentasDia:
    """Pruebas para la función obtener_numero_ventas_dia."""

    def test_sin_ventas_retorna_cero(self, db_connection):
        """Si no hay ventas registradas hoy, debe retornar 0."""
        hoy = date.today().isoformat()
        
        numero_ventas = obtener_numero_ventas_dia(db_connection, fecha=hoy)
        
        assert numero_ventas == 0

    def test_una_venta_retorna_uno(self, db_connection):
        """Si hay una venta registrada, debe retornar 1."""
        hoy = date.today().isoformat()
        producto_id = _crear_producto(
            db_connection, "Leche 1L", precio_venta=4.00, precio_compra=3.00, margen=30.0
        )
        venta_id = _crear_venta(db_connection, fecha=hoy, total=4.00)
        _crear_detalle_venta(
            db_connection, venta_id, producto_id,
            cantidad=1, precio_unitario=4.00, subtotal=4.00
        )
        
        numero_ventas = obtener_numero_ventas_dia(db_connection, fecha=hoy)
        
        assert numero_ventas == 1

    def test_multiples_ventas_retorna_cantidad_correcta(self, db_connection):
        """Si hay múltiples ventas, debe retornar la cantidad exacta."""
        hoy = date.today().isoformat()
        producto_id = _crear_producto(
            db_connection, "Arroz 1kg", precio_venta=5.00, precio_compra=3.50, margen=30.0
        )
        
        # Crear 3 ventas
        for i in range(3):
            venta_id = _crear_venta(db_connection, fecha=hoy, total=5.00)
            _crear_detalle_venta(
                db_connection, venta_id, producto_id,
                cantidad=1, precio_unitario=5.00, subtotal=5.00
            )
        
        numero_ventas = obtener_numero_ventas_dia(db_connection, fecha=hoy)
        
        assert numero_ventas == 3

    def test_solo_cuenta_ventas_de_la_fecha_indicada(self, db_connection):
        """Las ventas de otros días no deben contar."""
        hoy = date.today().isoformat()
        ayer = (date.today() - timedelta(days=1)).isoformat()
        
        producto_id = _crear_producto(
            db_connection, "Producto A", precio_venta=10.00, precio_compra=5.00, margen=30.0
        )
        
        # Venta de ayer (no debe contar)
        venta_ayer = _crear_venta(db_connection, fecha=ayer, total=10.00)
        _crear_detalle_venta(
            db_connection, venta_ayer, producto_id,
            cantidad=1, precio_unitario=10.00, subtotal=10.00
        )
        
        # Venta de hoy (sí debe contar)
        venta_hoy = _crear_venta(db_connection, fecha=hoy, total=10.00)
        _crear_detalle_venta(
            db_connection, venta_hoy, producto_id,
            cantidad=1, precio_unitario=10.00, subtotal=10.00
        )
        
        numero_ventas = obtener_numero_ventas_dia(db_connection, fecha=hoy)
        
        assert numero_ventas == 1