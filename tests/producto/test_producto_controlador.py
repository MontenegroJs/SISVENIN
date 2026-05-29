"""
Pruebas unitarias para el controlador de Producto (HU-08)
Sprint 1 - Gestión de Productos
"""

import pytest
import sys
import os
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.app.controllers.producto_controlador import ProductoControlador
from src.app.models.producto_modelo import ProductoModelo


class TestProductoControlador:

    # ==================== TEST DE VALIDACIONES (sin BD) ====================

    def test_validar_nombre_correcto(self):
        resultado = ProductoControlador.validar_nombre("Producto Válido")
        assert resultado is True

    def test_validar_nombre_vacio(self):
        with pytest.raises(ValueError, match="El nombre es obligatorio"):
            ProductoControlador.validar_nombre("")

    def test_validar_nombre_solo_espacios(self):
        with pytest.raises(ValueError, match="El nombre es obligatorio"):
            ProductoControlador.validar_nombre("   ")

    def test_validar_precio_compra_correcto(self):
        resultado = ProductoControlador.validar_precio_compra(10.50)
        assert resultado is True

    def test_validar_precio_compra_cero(self):
        with pytest.raises(ValueError, match="El precio de compra debe ser mayor a 0"):
            ProductoControlador.validar_precio_compra(0.0)

    def test_validar_precio_compra_negativo(self):
        with pytest.raises(ValueError, match="El precio de compra debe ser mayor a 0"):
            ProductoControlador.validar_precio_compra(-5.0)

    def test_validar_margen_correcto(self):
        resultado = ProductoControlador.validar_margen(30.0)
        assert resultado is True

    def test_validar_margen_negativo(self):
        with pytest.raises(ValueError, match="El margen no puede ser negativo"):
            ProductoControlador.validar_margen(-10.0)

    def test_validar_stock_correcto(self):
        resultado = ProductoControlador.validar_stock(5)
        assert resultado is True

    def test_validar_stock_negativo(self):
        with pytest.raises(ValueError, match="El stock no puede ser negativo"):
            ProductoControlador.validar_stock(-1)

    # ==================== TEST DE CÁLCULO DE PRECIO ====================

    def test_calcular_precio_sugerido(self):
        resultado = ProductoControlador.calcular_precio_sugerido(10.00, 30.0)
        assert resultado == 13.00

    def test_calcular_precio_sugerido_redondeo(self):
        resultado = ProductoControlador.calcular_precio_sugerido(1.92, 30.0)
        assert resultado == 2.50

    # ==================== TEST DE CRUD (con BD real) ====================

    def test_crear_producto(self, db_real):
        producto_id = ProductoControlador.crear_producto(
            nombre="Producto Test",
            precio_compra=10.00,
            margen=30.0,
            stock=5
        )
        assert producto_id is not None
        assert producto_id > 0
        
        producto = ProductoModelo.obtener_por_id(producto_id)
        assert producto.nombre == "Producto Test"
        assert producto.precio_venta == 13.00

    def test_crear_producto_con_precio_manual(self, db_real):
        producto_id = ProductoControlador.crear_producto(
            nombre="Producto Manual",
            precio_compra=10.00,
            margen=30.0,
            stock=5,
            precio_venta=20.00
        )
        assert producto_id is not None
        producto = ProductoModelo.obtener_por_id(producto_id)
        assert producto.precio_venta == 20.00

    def test_crear_producto_con_vencimiento(self, db_real):
        fecha_vencimiento = date(2026, 12, 31)
        producto_id = ProductoControlador.crear_producto(
            nombre="Producto Vencimiento",
            precio_compra=10.00,
            margen=30.0,
            stock=5,
            vencimiento=fecha_vencimiento
        )
        producto = ProductoModelo.obtener_por_id(producto_id)
        assert producto.vencimiento == fecha_vencimiento

    def test_crear_producto_validacion_falla(self, db_real):
        with pytest.raises(ValueError, match="El nombre es obligatorio"):
            ProductoControlador.crear_producto(
                nombre="",
                precio_compra=10.00,
                margen=30.0,
                stock=5
            )

    def test_actualizar_producto(self, db_real):
        producto_id = ProductoControlador.crear_producto(
            nombre="Original",
            precio_compra=10.00,
            margen=30.0,
            stock=5
        )
        
        resultado = ProductoControlador.actualizar_producto(
            id=producto_id,
            nombre="Actualizado",
            precio_compra=20.00,
            margen=50.0,
            stock=10
        )
        assert resultado is True
        
        producto = ProductoModelo.obtener_por_id(producto_id)
        assert producto.nombre == "Actualizado"
        assert producto.precio_compra == 20.00
        assert producto.margen == 50.0
        assert producto.stock == 10
        assert producto.precio_venta == 30.00

    def test_actualizar_producto_inexistente(self, db_real):
        with pytest.raises(ValueError, match="Producto no encontrado"):
            ProductoControlador.actualizar_producto(
                id=999,
                nombre="No existe",
                precio_compra=10.00,
                margen=30.0,
                stock=5
            )

    def test_eliminar_producto(self, db_real):
        producto_id = ProductoControlador.crear_producto(
            nombre="A eliminar",
            precio_compra=10.00,
            margen=30.0,
            stock=5
        )
        assert ProductoModelo.obtener_por_id(producto_id) is not None
        
        resultado = ProductoControlador.eliminar_producto(producto_id)
        assert resultado is True
        assert ProductoModelo.obtener_por_id(producto_id) is None

    def test_eliminar_producto_inexistente(self, db_real):
        resultado = ProductoControlador.eliminar_producto(999)
        assert resultado is False

    def test_obtener_producto_por_id(self, db_real):
        producto_id = ProductoControlador.crear_producto(
            nombre="Para obtener",
            precio_compra=10.00,
            margen=30.0,
            stock=5
        )
        producto = ProductoControlador.obtener_producto(producto_id)
        assert producto is not None
        assert producto.id == producto_id
        assert producto.nombre == "Para obtener"

    # ==================== PRUEBAS QUE NECESITAN BD LIMPIA ====================

    def test_obtener_todos_los_productos(self, db_real_clean):
        ProductoModelo.base_datos = db_real_clean
        ProductoModelo.inicializar_tabla()
        
        ProductoControlador.crear_producto(nombre="Producto A", precio_compra=10.00, margen=30.0, stock=5)
        ProductoControlador.crear_producto(nombre="Producto B", precio_compra=20.00, margen=30.0, stock=3)
        
        productos = ProductoControlador.obtener_todos_productos()
        assert len(productos) == 2

    def test_buscar_productos_por_nombre(self, db_real_clean):
        ProductoModelo.base_datos = db_real_clean
        ProductoModelo.inicializar_tabla()
        
        ProductoControlador.crear_producto(nombre="Leche evaporada", precio_compra=10.00, margen=30.0, stock=5)
        ProductoControlador.crear_producto(nombre="Leche light", precio_compra=10.00, margen=30.0, stock=5)
        ProductoControlador.crear_producto(nombre="Arroz 1kg", precio_compra=10.00, margen=30.0, stock=5)
        
        resultados = ProductoControlador.buscar_productos("Leche")
        assert len(resultados) == 2

    def test_buscar_productos_sin_resultados(self, db_real_clean):
        ProductoModelo.base_datos = db_real_clean
        ProductoModelo.inicializar_tabla()
        
        resultados = ProductoControlador.buscar_productos("InexistenteXYZ")
        assert len(resultados) == 0

    def test_obtener_productos_stock_bajo(self, db_real_clean):
        ProductoModelo.base_datos = db_real_clean
        ProductoModelo.inicializar_tabla()
        
        ProductoControlador.crear_producto(nombre="Stock alto", precio_compra=10.00, margen=30.0, stock=10)
        ProductoControlador.crear_producto(nombre="Stock bajo 1", precio_compra=10.00, margen=30.0, stock=4)
        ProductoControlador.crear_producto(nombre="Stock bajo 2", precio_compra=10.00, margen=30.0, stock=2)
        
        stock_bajo = ProductoControlador.obtener_productos_stock_bajo()
        assert len(stock_bajo) == 2

    def test_obtener_productos_por_vencer(self, db_real_clean):
        from datetime import date, timedelta
        
        ProductoModelo.base_datos = db_real_clean
        ProductoModelo.inicializar_tabla()
        
        hoy = date.today()
        
        ProductoControlador.crear_producto(
            nombre="Vence pronto",
            precio_compra=10.00,
            margen=30.0,
            stock=5,
            vencimiento=hoy + timedelta(days=3)
        )
        ProductoControlador.crear_producto(
            nombre="Vence lejos",
            precio_compra=10.00,
            margen=30.0,
            stock=5,
            vencimiento=hoy + timedelta(days=10)
        )
        
        por_vencer = ProductoControlador.obtener_productos_por_vencer(dias=7)
        assert len(por_vencer) == 1
        assert por_vencer[0].nombre == "Vence pronto"