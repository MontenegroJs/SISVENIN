-- ============================================
-- SISVENIN - Esquema de Base de Datos (Modelo Físico)
-- Basado en TO-BE v1.1, Arquitectura y HU
-- Fecha: 20 de mayo de 2026
-- Motor: SQLite 3.x
-- ============================================

-- ============================================
-- 1. TABLA: productos
-- ============================================
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio_venta REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    precio_compra REAL,
    margen REAL DEFAULT 30.0,
    vencimiento TEXT,  -- DATE format: YYYY-MM-DD
    activo INTEGER DEFAULT 1
);

-- ============================================
-- 2. TABLA: ventas
-- ============================================
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT DEFAULT CURRENT_TIMESTAMP,  -- DATETIME format: YYYY-MM-DD HH:MM:SS
    total REAL NOT NULL
);

-- ============================================
-- 3. TABLA: venta_detalles
-- ============================================
CREATE TABLE IF NOT EXISTS venta_detalles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- ============================================
-- 4. ÍNDICES (para mejorar el rendimiento - RNF-01)
-- ============================================
-- Búsqueda de productos por nombre (HU-09)
CREATE INDEX IF NOT EXISTS idx_productos_nombre ON productos(nombre);

-- Reportes por fecha (HU-06, HU-10)
CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas(fecha);

-- Consultas de detalles de venta
CREATE INDEX IF NOT EXISTS idx_venta_detalles_venta_id ON venta_detalles(venta_id);
CREATE INDEX IF NOT EXISTS idx_venta_detalles_producto_id ON venta_detalles(producto_id);