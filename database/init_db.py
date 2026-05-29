"""
Script para inicializar la base de datos SISVENIN con datos de ejemplo.
Ejecutar: python database/init_db.py
"""

import sqlite3
import os
from datetime import date, timedelta, datetime
import random

# Ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'sisvenin.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')


def ejecutar_schema(conn):
    """Ejecuta el schema.sql para crear las tablas e índices"""
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    print("✅ Tablas e índices creados")


def insertar_productos(conn):
    """Inserta productos de ejemplo (30 productos variados)"""
    cursor = conn.cursor()
    
    productos = [
        # Lácteos
        ("Leche evaporada", 2.50, 15, 1.92, 30.0, None),
        ("Leche light", 3.00, 8, 2.31, 30.0, None),
        ("Leche sin lactosa", 4.00, 5, 3.08, 30.0, None),
        ("Yogur fresa", 3.00, 12, 2.31, 30.0, (date.today() + timedelta(days=3)).isoformat()),
        ("Yogur natural", 3.00, 10, 2.31, 30.0, (date.today() + timedelta(days=5)).isoformat()),
        ("Queso fresco", 8.00, 6, 6.15, 30.0, (date.today() + timedelta(days=10)).isoformat()),
        ("Mantequilla", 5.50, 4, 4.23, 30.0, (date.today() + timedelta(days=20)).isoformat()),
        
        # Abarrotes
        ("Arroz 1kg", 3.50, 25, 2.69, 30.0, None),
        ("Arroz 5kg", 16.00, 10, 12.31, 30.0, None),
        ("Fideo espagueti", 2.80, 20, 2.15, 30.0, None),
        ("Fideo tallarín", 2.80, 18, 2.15, 30.0, None),
        ("Azúcar 1kg", 3.20, 15, 2.46, 30.0, None),
        ("Aceite 1L", 8.00, 12, 6.15, 30.0, None),
        ("Sal 500g", 1.50, 30, 1.15, 30.0, None),
        ("Menestra", 4.50, 8, 3.46, 30.0, None),
        ("Lentejas", 4.50, 7, 3.46, 30.0, None),
        
        # Conservas
        ("Atún en agua", 4.50, 15, 3.46, 30.0, (date.today() + timedelta(days=180)).isoformat()),
        ("Atún en aceite", 5.00, 12, 3.85, 30.0, (date.today() + timedelta(days=180)).isoformat()),
        ("Tomate triturado", 3.50, 10, 2.69, 30.0, (date.today() + timedelta(days=365)).isoformat()),
        
        # Bebidas
        ("Gaseosa 1.5L", 6.00, 20, 4.62, 30.0, None),
        ("Gaseosa 2.5L", 8.00, 15, 6.15, 30.0, None),
        ("Agua 2L", 3.00, 30, 2.31, 30.0, None),
        ("Cerveza 620ml", 7.00, 25, 5.38, 30.0, (date.today() + timedelta(days=90)).isoformat()),
        ("Jugo en caja", 2.50, 20, 1.92, 30.0, (date.today() + timedelta(days=60)).isoformat()),
        
        # Limpieza
        ("Jabón líquido", 4.00, 15, 3.08, 30.0, None),
        ("Detergente", 6.50, 10, 5.00, 30.0, None),
        ("Lejía 1L", 5.00, 8, 3.85, 30.0, None),
        ("Lavavajillas", 4.50, 12, 3.46, 30.0, None),
        
        # Snacks
        ("Galletas soda", 2.50, 20, 1.92, 30.0, (date.today() + timedelta(days=45)).isoformat()),
        ("Papas fritas", 3.50, 15, 2.69, 30.0, (date.today() + timedelta(days=30)).isoformat()),
    ]
    
    for producto in productos:
        cursor.execute("""
            INSERT INTO productos (nombre, precio_venta, stock, precio_compra, margen, vencimiento)
            VALUES (?, ?, ?, ?, ?, ?)
        """, producto)
    
    print(f"✅ Insertados {len(productos)} productos")


def insertar_ventas(conn):
    """Inserta ventas de los últimos 7 días (para pruebas de reportes)"""
    cursor = conn.cursor()
    
    # Obtener IDs de productos existentes
    cursor.execute("SELECT id, precio_venta FROM productos")
    productos = cursor.fetchall()
    if not productos:
        print("⚠️ No hay productos para crear ventas de ejemplo")
        return
    
    ventas_insertadas = 0
    detalles_insertados = 0
    
    # Generar ventas para los últimos 7 días
    for dia in range(7, -1, -1):
        fecha = date.today() - timedelta(days=dia)
        # Entre 3 y 10 ventas por día
        num_ventas_dia = random.randint(3, 10)
        
        for _ in range(num_ventas_dia):
            # Generar hora aleatoria entre 8:00 y 20:00
            hora = random.randint(8, 20)
            minuto = random.randint(0, 59)
            fecha_hora = datetime(fecha.year, fecha.month, fecha.day, hora, minuto, random.randint(0, 59))
            fecha_str = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
            
            # Total de la venta (se calculará sumando detalles)
            total = 0
            
            # Insertar venta
            cursor.execute("INSERT INTO ventas (fecha, total) VALUES (?, ?)", (fecha_str, 0))
            venta_id = cursor.lastrowid
            
            # Generar entre 1 y 5 productos por venta
            num_productos_venta = random.randint(1, 5)
            productos_seleccionados = random.sample(productos, min(num_productos_venta, len(productos)))
            
            for producto in productos_seleccionados:
                producto_id, precio_venta = producto
                cantidad = random.randint(1, 3)
                subtotal = precio_venta * cantidad
                total += subtotal
                
                cursor.execute("""
                    INSERT INTO venta_detalles (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (venta_id, producto_id, cantidad, precio_venta, subtotal))
                detalles_insertados += 1
            
            # Actualizar total de la venta
            cursor.execute("UPDATE ventas SET total = ? WHERE id = ?", (round(total, 2), venta_id))
            ventas_insertadas += 1
    
    print(f"✅ Insertadas {ventas_insertadas} ventas con {detalles_insertados} detalles")


def main():
    print(f"📁 Inicializando base de datos en: {DB_PATH}")
    
    # Verificar si el archivo ya existe
    if os.path.exists(DB_PATH):
        print("⚠️ La base de datos ya existe. Se eliminará y recreará.")
        # Opcional: hacer backup
        # os.rename(DB_PATH, DB_PATH + ".backup")
        os.remove(DB_PATH)
    
    # Conectar a la BD (la crea si no existe)
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # 1. Crear esquema
        ejecutar_schema(conn)
        
        # 2. Insertar productos
        insertar_productos(conn)
        
        # 3. Insertar ventas de ejemplo
        insertar_ventas(conn)
        
        # 4. Confirmar todos los cambios
        conn.commit()
        
        # 5. Mostrar resumen
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM productos")
        total_productos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM ventas")
        total_ventas = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM venta_detalles")
        total_detalles = cursor.fetchone()[0]
        
        print("\n" + "="*50)
        print("🎉 BASE DE DATOS INICIALIZADA CORRECTAMENTE")
        print("="*50)
        print(f"📦 Productos: {total_productos}")
        print(f"🧾 Ventas: {total_ventas}")
        print(f"📋 Detalles de venta: {total_detalles}")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    main()