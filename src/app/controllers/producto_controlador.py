"""
Controlador del módulo Producto - SISVENIN
HU-08: CRUD de productos con precio sugerido

Responsabilidades:
- Validaciones de datos
- Lógica de negocio
- Orquestación entre vista y modelo
- No accede directamente a la base de datos (usa el modelo)
"""

from typing import List, Optional
from datetime import date
from src.app.models.producto_modelo import ProductoModelo


class ProductoControlador:
    """
    Controlador para la gestión de productos.
    Implementa validaciones y lógica de negocio.
    """
    
    # ==================== MÉTODOS DE VALIDACIÓN ====================
    
    @staticmethod
    def validar_nombre(nombre: str) -> bool:
        """
        Valida que el nombre no esté vacío ni sea solo espacios.
        
        Args:
            nombre: Nombre del producto
            
        Returns:
            True si es válido
            
        Raises:
            ValueError: Si el nombre está vacío o es solo espacios
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        return True
    
    @staticmethod
    def validar_precio_compra(precio_compra: float) -> bool:
        """
        Valida que el precio de compra sea mayor a 0.
        
        Args:
            precio_compra: Precio de compra del producto
            
        Returns:
            True si es válido
            
        Raises:
            ValueError: Si el precio es <= 0
        """
        if precio_compra <= 0:
            raise ValueError("El precio de compra debe ser mayor a 0")
        return True
    
    @staticmethod
    def validar_margen(margen: float) -> bool:
        """
        Valida que el margen no sea negativo.
        
        Args:
            margen: Porcentaje de margen de ganancia
            
        Returns:
            True si es válido
            
        Raises:
            ValueError: Si el margen es negativo
        """
        if margen < 0:
            raise ValueError("El margen no puede ser negativo")
        return True
    
    @staticmethod
    def validar_stock(stock: int) -> bool:
        """
        Valida que el stock no sea negativo.
        
        Args:
            stock: Cantidad disponible
            
        Returns:
            True si es válido
            
        Raises:
            ValueError: Si el stock es negativo
        """
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        return True
    
    # ==================== MÉTODOS DE CÁLCULO ====================
    
    @staticmethod
    def calcular_precio_sugerido(precio_compra: float, margen: float) -> float:
        """
        Calcula el precio de venta sugerido.
        
        Fórmula: Precio Venta = Precio Compra × (1 + Margen/100)
        
        Args:
            precio_compra: Precio de compra del producto
            margen: Porcentaje de margen de ganancia
            
        Returns:
            Precio sugerido redondeado a 2 decimales
        """
        precio = precio_compra * (1 + margen / 100)
        return round(precio, 2)
    
    # ==================== MÉTODOS DE CRUD ====================
    
    @staticmethod
    def crear_producto(
        nombre: str,
        precio_compra: float,
        margen: float,
        stock: int = 0,
        precio_venta: Optional[float] = None,
        vencimiento: Optional[date] = None
    ) -> int:
        """
        Crea un nuevo producto en el sistema.
        
        Args:
            nombre: Nombre del producto
            precio_compra: Precio de compra
            margen: Porcentaje de margen
            stock: Cantidad disponible
            precio_venta: Precio de venta (si es None, se calcula automáticamente)
            vencimiento: Fecha de vencimiento (opcional)
            
        Returns:
            ID del producto creado
            
        Raises:
            ValueError: Si alguna validación falla
        """
        # Validaciones
        ProductoControlador.validar_nombre(nombre)
        ProductoControlador.validar_precio_compra(precio_compra)
        ProductoControlador.validar_margen(margen)
        ProductoControlador.validar_stock(stock)
        
        # Calcular precio de venta si no se proporcionó
        if precio_venta is None or precio_venta <= 0:
            precio_venta = ProductoControlador.calcular_precio_sugerido(precio_compra, margen)
        
        # Crear modelo (sin descripcion)
        producto = ProductoModelo(
            nombre=nombre,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            margen=margen,
            stock=stock,
            vencimiento=vencimiento,
            activo=True
        )
        
        # Guardar en base de datos
        producto.guardar()
        
        return producto.id
    
    @staticmethod
    def actualizar_producto(
        id: int,
        nombre: str,
        precio_compra: float,
        margen: float,
        stock: int,
        precio_venta: Optional[float] = None,
        vencimiento: Optional[date] = None
    ) -> bool:
        """
        Actualiza un producto existente.
        
        Args:
            id: ID del producto a actualizar
            nombre: Nuevo nombre
            precio_compra: Nuevo precio de compra
            margen: Nuevo margen
            stock: Nuevo stock
            precio_venta: Nuevo precio de venta (si es None, se recalcula)
            vencimiento: Nueva fecha de vencimiento
            
        Returns:
            True si la actualización fue exitosa
            
        Raises:
            ValueError: Si el producto no existe o las validaciones fallan
        """
        # Verificar que el producto existe
        producto = ProductoModelo.obtener_por_id(id)
        if producto is None:
            raise ValueError("Producto no encontrado")
        
        # Validaciones
        ProductoControlador.validar_nombre(nombre)
        ProductoControlador.validar_precio_compra(precio_compra)
        ProductoControlador.validar_margen(margen)
        ProductoControlador.validar_stock(stock)
        
        # Calcular precio de venta si no se proporcionó
        if precio_venta is None or precio_venta <= 0:
            precio_venta = ProductoControlador.calcular_precio_sugerido(precio_compra, margen)
        
        # Actualizar atributos (sin descripcion)
        producto.nombre = nombre
        producto.precio_compra = precio_compra
        producto.precio_venta = precio_venta
        producto.margen = margen
        producto.stock = stock
        producto.vencimiento = vencimiento
        
        # Guardar cambios
        producto.guardar()
        
        return True
    
    @staticmethod
    def eliminar_producto(id: int) -> bool:
        """
        Elimina un producto del sistema (borrado físico).
        
        Args:
            id: ID del producto a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existía
        """
        producto = ProductoModelo.obtener_por_id(id)
        if producto is None:
            return False
        
        producto.eliminar()
        return True
    
    @staticmethod
    def obtener_producto(id: int) -> Optional[ProductoModelo]:
        """
        Obtiene un producto por su ID.
        
        Args:
            id: ID del producto
            
        Returns:
            ProductoModelo o None si no existe
        """
        return ProductoModelo.obtener_por_id(id)
    
    @staticmethod
    def obtener_todos_productos(solo_activos: bool = True) -> List[ProductoModelo]:
        """
        Obtiene la lista de todos los productos.
        
        Args:
            solo_activos: Si es True, solo productos activos
            
        Returns:
            Lista de productos
        """
        return ProductoModelo.obtener_todos(solo_activos=solo_activos)
    
    @staticmethod
    def buscar_productos(termino: str) -> List[ProductoModelo]:
        """
        Busca productos por nombre (coincidencia parcial).
        
        Args:
            termino: Texto a buscar
            
        Returns:
            Lista de productos que coinciden
        """
        if not termino or len(termino.strip()) < 2:
            return []
        return ProductoModelo.buscar_por_nombre(termino.strip())
    
    @staticmethod
    def buscar_por_codigo(codigo: str) -> Optional[ProductoModelo]:
        """
        Busca un producto por código de barras.
        
        Args:
            codigo: Código de barras del producto.
        
        Returns:
            Producto encontrado o None.
        """
        if not codigo or not codigo.strip():
            return None
        
        return ProductoModelo.buscar_por_codigo_barras(codigo.strip())

    @staticmethod
    def buscar_rapido_pos(termino: str, limite: int = 10) -> List[ProductoModelo]:
        """
        Búsqueda rápida optimizada para el POS.
        
        Args:
            termino: Texto a buscar (nombre o código).
            limite: Número máximo de resultados.
        
        Returns:
            Lista de productos encontrados.
        """
        if not termino or not termino.strip():
            return []
        
        return ProductoModelo.buscar_rapido(termino.strip(), limite)

    @staticmethod
    def validar_codigo_barras(codigo: str) -> bool:
        """
        Valida que el código de barras sea numérico y tenga entre 8 y 13 dígitos.
        
        Args:
            codigo: Código de barras a validar.
        
        Returns:
            True si es válido, False en caso contrario.
        """
        if not codigo or not codigo.strip():
            return False
        
        codigo_limpio = codigo.strip()
        
        if not codigo_limpio.isdigit():
            return False
        
        return 8 <= len(codigo_limpio) <= 13
    
    # ==================== MÉTODOS PARA ALERTAS (HU-04) ====================
    
    @staticmethod
    def obtener_productos_stock_bajo(limite: int = 5) -> List[ProductoModelo]:
        """
        Obtiene productos con stock menor al límite.
        
        Args:
            limite: Valor límite de stock (default 5)
            
        Returns:
            Lista de productos con stock bajo
        """
        return ProductoModelo.obtener_stock_bajo(limite=limite)
    
    @staticmethod
    def obtener_productos_por_vencer(dias: int = 7) -> List[ProductoModelo]:
        """
        Obtiene productos próximos a vencer dentro de X días.
        
        Args:
            dias: Número de días para considerar (default 7)
            
        Returns:
            Lista de productos próximos a vencer
        """
        return ProductoModelo.obtener_por_vencer(dias=dias)
    
    # ==================== MÉTODO LEGACY (compatibilidad) ====================
    
    @staticmethod
    def listar_ejemplo() -> List[ProductoModelo]:
        """
        Método legacy para compatibilidad con código existente.
        Retorna una lista de ejemplo de productos.
        
        Returns:
            Lista de productos de ejemplo
        """
        return [
            ProductoModelo(id=1, nombre="Producto 1"),
            ProductoModelo(id=2, nombre="Producto 2"),
        ]