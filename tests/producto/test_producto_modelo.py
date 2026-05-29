"""
Pruebas unitarias para el modelo ProductoModelo (HU-08)
Sprint 1 - Gestión de Productos

Convenciones:
- snake_case para nombres de prueba
- Docstrings explicando qué se prueba
- Usa pytest (no unittest)
"""

import pytest
import sys
import os
from datetime import date, timedelta

# Asegurar que podemos importar desde src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app.models.producto_modelo import ProductoModelo


class TestProductoModelo:
    """Pruebas unitarias para el modelo ProductoModelo"""

    # ==================== TEST DE CÁLCULO DE PRECIO SUGERIDO ====================

    def test_calcular_precio_sugerido_con_margen_30(self):
        """
        HU-08: El sistema calcula automáticamente el precio de venta
        usando la fórmula: Precio Venta = Precio Compra × (1 + Margen/100)
        
        Caso: precio_compra = 10.00, margen = 30%
        Resultado esperado: 13.00
        """
        producto = ProductoModelo(
            nombre="Producto Test",
            precio_compra=10.00,
            margen=30.0
        )
        
        precio_sugerido = producto.calcular_precio_sugerido()
        
        assert precio_sugerido == 13.00, f"Esperado 13.00, obtuve {precio_sugerido}"

    def test_calcular_precio_sugerido_con_margen_50(self):
        """
        HU-08: Cálculo con margen del 50%
        precio_compra = 20.00, margen = 50%
        Resultado esperado: 30.00
        """
        producto = ProductoModelo(
            nombre="Producto Test",
            precio_compra=20.00,
            margen=50.0
        )
        
        precio_sugerido = producto.calcular_precio_sugerido()
        
        assert precio_sugerido == 30.00

    def test_calcular_precio_sugerido_con_margen_0(self):
        """
        HU-08: Margen 0% -> precio_venta = precio_compra
        """
        producto = ProductoModelo(
            nombre="Producto Test",
            precio_compra=15.00,
            margen=0.0
        )
        
        precio_sugerido = producto.calcular_precio_sugerido()
        
        assert precio_sugerido == 15.00

    def test_calcular_precio_sugerido_con_margen_100(self):
        """
        HU-08: Margen 100% -> precio_venta = precio_compra × 2
        """
        producto = ProductoModelo(
            nombre="Producto Test",
            precio_compra=25.00,
            margen=100.0
        )
        
        precio_sugerido = producto.calcular_precio_sugerido()
        
        assert precio_sugerido == 50.00

    def test_calcular_precio_sugerido_redondeo_dos_decimales(self):
        """
        HU-08: El precio debe redondearse a 2 decimales (formato moneda)
        Caso: precio_compra = 1.92, margen = 30% -> 1.92 * 1.30 = 2.496 -> 2.50
        """
        producto = ProductoModelo(
            nombre="Leche evaporada",
            precio_compra=1.92,
            margen=30.0
        )
        
        precio_sugerido = producto.calcular_precio_sugerido()
        
        assert precio_sugerido == 2.50, f"Esperado 2.50, obtuve {precio_sugerido}"

    # ==================== TEST DE VALIDACIONES ====================

    def test_validar_nombre_no_vacio(self):
        """HU-08: El nombre del producto no puede estar vacío"""
        producto = ProductoModelo(nombre="")
        
        with pytest.raises(ValueError, match="El nombre es obligatorio"):
            producto.validar()

    def test_validar_nombre_solo_espacios(self):
        """HU-08: El nombre no puede ser solo espacios"""
        producto = ProductoModelo(nombre="   ")
        
        with pytest.raises(ValueError, match="El nombre es obligatorio"):
            producto.validar()

    def test_validar_precio_compra_mayor_a_cero(self):
        """HU-08: El precio de compra debe ser mayor a 0"""
        producto = ProductoModelo(
            nombre="Producto Test",
            precio_compra=0.0
        )
        
        with pytest.raises(ValueError, match="El precio de compra debe ser mayor a 0"):
            producto.validar()

    def test_validar_precio_compra_negativo(self):
        """HU-08: El precio de compra no puede ser negativo"""
        producto = ProductoModelo(
            nombre="Producto Test",
            precio_compra=-5.00
        )
        
        with pytest.raises(ValueError, match="El precio de compra debe ser mayor a 0"):
            producto.validar()

    def test_validar_margen_no_negativo(self):
        """HU-08: El margen no puede ser negativo"""
        producto = ProductoModelo(
            nombre="Producto Test",
            precio_compra=10.00,
            margen=-10.0
        )
        
        with pytest.raises(ValueError, match="El margen no puede ser negativo"):
            producto.validar()

    def test_validar_stock_no_negativo(self):
        """HU-08: El stock no puede ser negativo"""
        producto = ProductoModelo(
            nombre="Producto Test",
            precio_compra=10.00,
            stock=-5
        )
        
        with pytest.raises(ValueError, match="El stock no puede ser negativo"):
            producto.validar()

    def test_producto_valido_pasa_validacion(self):
        """HU-08: Un producto con datos correctos no lanza excepciones"""
        producto = ProductoModelo(
            nombre="Producto Válido",
            precio_compra=10.00,
            margen=30.0,
            stock=5,
            vencimiento=date(2026, 12, 31)
        )
        
        # No debe lanzar excepción
        producto.validar()
        assert True

    # ==================== TEST DE CRUD (base de datos) ====================

    def test_guardar_producto_nuevo(self, temp_db):
        """HU-08: Guardar un producto nuevo en la base de datos"""
        ProductoModelo.base_datos = temp_db
        ProductoModelo.inicializar_tabla()
        
        producto = ProductoModelo(
            nombre="Producto Test",
            precio_compra=10.00,
            precio_venta=13.00,
            margen=30.0,
            stock=5
        )
        
        producto.guardar()
        
        assert producto.id is not None
        assert producto.id > 0

    def test_obtener_todos_los_productos(self, temp_db):
        """HU-08: Obtener lista de todos los productos"""
        ProductoModelo.base_datos = temp_db
        ProductoModelo.inicializar_tabla()
        
        p1 = ProductoModelo(nombre="Producto A", precio_compra=10.00, precio_venta=13.00, margen=30.0, stock=5)
        p2 = ProductoModelo(nombre="Producto B", precio_compra=20.00, precio_venta=26.00, margen=30.0, stock=3)
        p1.guardar()
        p2.guardar()
        
        productos = ProductoModelo.obtener_todos()
        
        assert len(productos) == 2
        assert productos[0].nombre == "Producto A"
        assert productos[1].nombre == "Producto B"

    def test_obtener_producto_por_id(self, temp_db):
        """HU-08: Buscar un producto específico por su ID"""
        ProductoModelo.base_datos = temp_db
        ProductoModelo.inicializar_tabla()
        
        producto = ProductoModelo(nombre="Producto Test", precio_compra=10.00, precio_venta=13.00, margen=30.0, stock=5)
        producto.guardar()
        
        encontrado = ProductoModelo.obtener_por_id(producto.id)
        
        assert encontrado is not None
        assert encontrado.id == producto.id
        assert encontrado.nombre == "Producto Test"

    def test_obtener_por_id_inexistente(self, temp_db):
        """HU-08: Buscar un ID que no existe debe retornar None"""
        ProductoModelo.base_datos = temp_db
        ProductoModelo.inicializar_tabla()
        
        encontrado = ProductoModelo.obtener_por_id(999)
        
        assert encontrado is None

    def test_actualizar_producto(self, temp_db):
        """HU-08: Actualizar los datos de un producto existente"""
        ProductoModelo.base_datos = temp_db
        ProductoModelo.inicializar_tabla()
        
        producto = ProductoModelo(nombre="Original", precio_compra=10.00, precio_venta=13.00, margen=30.0, stock=5)
        producto.guardar()
        
        producto.nombre = "Modificado"
        producto.stock = 10
        producto.guardar()
        
        actualizado = ProductoModelo.obtener_por_id(producto.id)
        assert actualizado.nombre == "Modificado"
        assert actualizado.stock == 10

    def test_eliminar_producto(self, temp_db):
        """HU-08: Eliminar un producto (borrado físico)"""
        ProductoModelo.base_datos = temp_db
        ProductoModelo.inicializar_tabla()
        
        producto = ProductoModelo(nombre="A eliminar", precio_compra=10.00, precio_venta=13.00, margen=30.0, stock=5)
        producto.guardar()
        producto_id = producto.id
        
        producto.eliminar()
        
        eliminado = ProductoModelo.obtener_por_id(producto_id)
        assert eliminado is None

    def test_buscar_productos_por_nombre(self, temp_db):
        """HU-08/HU-09: Búsqueda de productos por nombre (coincidencia parcial)"""
        ProductoModelo.base_datos = temp_db
        ProductoModelo.inicializar_tabla()
        
        ProductoModelo(nombre="Leche evaporada", precio_compra=10.00, precio_venta=13.00, margen=30.0, stock=5).guardar()
        ProductoModelo(nombre="Leche light", precio_compra=10.00, precio_venta=13.00, margen=30.0, stock=5).guardar()
        ProductoModelo(nombre="Arroz 1kg", precio_compra=10.00, precio_venta=13.00, margen=30.0, stock=5).guardar()
        
        resultados = ProductoModelo.buscar_por_nombre("Leche")
        
        assert len(resultados) == 2
        assert "Leche" in resultados[0].nombre
        assert "Leche" in resultados[1].nombre

    def test_buscar_por_nombre_sin_resultados(self, temp_db):
        """HU-08/HU-09: Búsqueda sin coincidencias retorna lista vacía"""
        ProductoModelo.base_datos = temp_db
        ProductoModelo.inicializar_tabla()
        
        resultados = ProductoModelo.buscar_por_nombre("Inexistente")
        
        assert len(resultados) == 0

    # ==================== TEST DE ALERTAS (HU-04) ====================

    def test_obtener_productos_con_stock_bajo(self, temp_db):
        """HU-04: Productos con stock < 5 unidades"""
        ProductoModelo.base_datos = temp_db
        ProductoModelo.inicializar_tabla()
        
        ProductoModelo(nombre="Stock alto", precio_compra=10.00, precio_venta=13.00, margen=30.0, stock=10).guardar()
        ProductoModelo(nombre="Stock bajo 1", precio_compra=10.00, precio_venta=13.00, margen=30.0, stock=4).guardar()
        ProductoModelo(nombre="Stock bajo 2", precio_compra=10.00, precio_venta=13.00, margen=30.0, stock=2).guardar()
        
        stock_bajo = ProductoModelo.obtener_stock_bajo(limite=5)
        
        assert len(stock_bajo) == 2
        nombres = [p.nombre for p in stock_bajo]
        assert "Stock bajo 1" in nombres
        assert "Stock bajo 2" in nombres

    def test_obtener_productos_por_vencer(self, temp_db):
        """HU-04: Productos con vencimiento < X días desde hoy"""
        ProductoModelo.base_datos = temp_db
        ProductoModelo.inicializar_tabla()
        
        hoy = date.today()
        
        ProductoModelo(
            nombre="Vence pronto",
            precio_compra=10.00,
            precio_venta=13.00,
            margen=30.0,
            stock=5,
            vencimiento=hoy + timedelta(days=3)
        ).guardar()
        
        ProductoModelo(
            nombre="Vence lejos",
            precio_compra=10.00,
            precio_venta=13.00,
            margen=30.0,
            stock=5,
            vencimiento=hoy + timedelta(days=10)
        ).guardar()
        
        por_vencer = ProductoModelo.obtener_por_vencer(dias=7)
        
        assert len(por_vencer) == 1
        assert por_vencer[0].nombre == "Vence pronto"