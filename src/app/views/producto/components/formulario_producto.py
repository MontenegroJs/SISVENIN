"""
FormularioProducto - Componente de formulario para productos
Equivalente al modal de formulario en productos-page.tsx de React

Características:
- Modal con campos: nombre, precio compra, margen, stock, vencimiento
- Cálculo automático de precio sugerido: Precio Venta = Precio Compra × (1 + Margen/100)
- Opción "Modificar" para cambiar precio manualmente
- Opción "Aceptar sugerido" para volver al precio calculado
- Validaciones en tiempo real
- Botones: GUARDAR PRODUCTO (primario), CANCELAR (secundario)
"""

from typing import Optional, Callable
from datetime import date
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QDoubleSpinBox, QDateEdit, QFrame, QScrollArea, QDialog
)
from PySide6.QtCore import Qt, Signal, QDate

from src.app.shared.components.sis_button import SisButton
from src.app.shared.components.sis_modal import SisModal
from src.app.base_layout import BaseLayout
from src.app.models.producto_modelo import ProductoModelo
from src.app.controllers.producto_controlador import ProductoControlador


class FormularioProducto(SisModal):
    """
    Modal de formulario para crear o editar productos.
    Sigue el diseño del Prompt 0 de Figma (igual al React).
    
    Características:
    - Cálculo automático de precio sugerido
    - Opción de modificar precio manualmente
    - Validaciones de campos
    - Soporte para edición de productos existentes
    
    Señales:
        productoGuardado: Emitida cuando se guarda un producto (nuevo o editado)
    
    Ejemplo:
        # Crear nuevo producto
        formulario = FormularioProducto()
        formulario.productoGuardado.connect(lambda p: print(f"Guardado: {p.nombre}"))
        formulario.open()
        
        # Editar producto existente
        formulario = FormularioProducto(producto=producto_existente)
        formulario.open()
    """
    
    # Señales
    productoGuardado = Signal(ProductoModelo)  # Emitido cuando se guarda
    
    def __init__(
        self,
        producto: Optional[ProductoModelo] = None,
        parent=None
    ):
        """
        Inicializa el formulario.
        
        Args:
            producto: Producto a editar (None para crear nuevo)
            parent: Widget padre
        """
        titulo = "Editar Producto" if producto else "Nuevo Producto"
        super().__init__(title=titulo, size="lg", parent=parent)
        
        self._producto = producto
        self._controlador = ProductoControlador()
        self._editando = producto is not None
        self._modo_manual = False
        
        self._setup_form()
        
        if producto:
            self._cargar_datos_producto(producto)
        
        self._setup_footer()
    
    def _setup_form(self):
        """Configura el formulario con todos los campos"""
        # Crear contenido del modal
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(16)
        
        # ==================== CAMPO: NOMBRE ====================
        layout.addLayout(self._crear_campo_nombre())
        
        # ==================== CAMPOS: PRECIO COMPRA + MARGEN ====================
        layout.addLayout(self._crear_campos_precio_margen())
        
        # ==================== SECCIÓN: PRECIO SUGERIDO ====================
        layout.addWidget(self._crear_seccion_precio_sugerido())
        
        # ==================== CAMPOS: STOCK + VENCIMIENTO ====================
        layout.addLayout(self._crear_campos_stock_vencimiento())
        
        # ==================== CAMPO: DESCRIPCIÓN (opcional) ====================
        layout.addLayout(self._crear_campo_descripcion())
        
        # Scroll para formularios largos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        scroll.setWidget(content)
        
        self.set_content(scroll)
    
    def _crear_campo_nombre(self) -> QHBoxLayout:
        """Crea el campo de nombre del producto"""
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        label = QLabel("📝 Nombre del producto *")
        label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #212121;
        """)
        layout.addWidget(label)
        
        self._input_nombre = QLineEdit()
        self._input_nombre.setPlaceholderText("Ej: Leche evaporada Gloria")
        self._input_nombre.setMinimumHeight(48)
        self._input_nombre.setStyleSheet(self._estilo_input())
        layout.addWidget(self._input_nombre)
        
        # Label de error
        self._error_nombre = QLabel("")
        self._error_nombre.setStyleSheet("font-size: 12px; color: #D32F2F;")
        self._error_nombre.hide()
        layout.addWidget(self._error_nombre)
        
        return layout
    
    def _crear_campos_precio_margen(self) -> QHBoxLayout:
        """Crea los campos de precio compra y margen (lado a lado)"""
        layout = QHBoxLayout()
        layout.setSpacing(16)
        
        # Precio Compra
        precio_layout = QVBoxLayout()
        precio_layout.setSpacing(8)
        
        label_precio = QLabel("💰 Precio de compra (S/) *")
        label_precio.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #212121;
        """)
        precio_layout.addWidget(label_precio)
        
        self._input_precio_compra = QDoubleSpinBox()
        self._input_precio_compra.setMinimum(0)
        self._input_precio_compra.setMaximum(999999.99)
        self._input_precio_compra.setPrefix("S/ ")
        self._input_precio_compra.setAlignment(Qt.AlignRight)
        self._input_precio_compra.setMinimumHeight(48)
        self._input_precio_compra.setStyleSheet(self._estilo_input())
        self._input_precio_compra.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self._input_precio_compra.valueChanged.connect(self._actualizar_precio_sugerido)
        precio_layout.addWidget(self._input_precio_compra)
        
        self._error_precio = QLabel("")
        self._error_precio.setStyleSheet("font-size: 12px; color: #D32F2F;")
        self._error_precio.hide()
        precio_layout.addWidget(self._error_precio)
        
        # Margen
        margen_layout = QVBoxLayout()
        margen_layout.setSpacing(8)
        
        label_margen = QLabel("📈 Margen de ganancia (%) *")
        label_margen.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #212121;
        """)
        margen_layout.addWidget(label_margen)
        
        self._input_margen = QDoubleSpinBox()
        self._input_margen.setMinimum(0)
        self._input_margen.setMaximum(1000)
        self._input_margen.setSuffix(" %")
        self._input_margen.setAlignment(Qt.AlignRight)
        self._input_margen.setMinimumHeight(48)
        self._input_margen.setStyleSheet(self._estilo_input())
        self._input_margen.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self._input_margen.setValue(30.0)
        self._input_margen.valueChanged.connect(self._actualizar_precio_sugerido)
        margen_layout.addWidget(self._input_margen)
        
        self._error_margen = QLabel("")
        self._error_margen.setStyleSheet("font-size: 12px; color: #D32F2F;")
        self._error_margen.hide()
        margen_layout.addWidget(self._error_margen)
        
        layout.addLayout(precio_layout, 1)
        layout.addLayout(margen_layout, 1)
        
        return layout
    
    def _crear_seccion_precio_sugerido(self) -> QFrame:
        """Crea la sección del precio sugerido (con fondo verde claro)"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #E8F5E9;
                border-radius: 8px;
                border: 1px solid #A5D6A7;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(12)
        
        # Fila superior: texto y botones
        top_layout = QHBoxLayout()
        
        texto = QLabel("💵 Precio de venta sugerido (calculado automáticamente)")
        texto.setStyleSheet("""
            font-size: 13px;
            color: #757575;
        """)
        top_layout.addWidget(texto)
        top_layout.addStretch()
        
        self._btn_aceptar = SisButton("Aceptar sugerido", variant="secondary")
        self._btn_aceptar.setMinimumHeight(36)
        self._btn_aceptar.clicked.connect(self._aceptar_precio_sugerido)
        top_layout.addWidget(self._btn_aceptar)
        
        self._btn_modificar = SisButton("Modificar", variant="secondary")
        self._btn_modificar.setMinimumHeight(36)
        self._btn_modificar.clicked.connect(self._modificar_precio_manual)
        top_layout.addWidget(self._btn_modificar)
        
        layout.addLayout(top_layout)
        
        # Valor sugerido
        self._label_precio_sugerido = QLabel("S/ 0.00")
        self._label_precio_sugerido.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #2E7D32;
        """)
        layout.addWidget(self._label_precio_sugerido)
        
        # Fórmula mostrada
        self._label_formula = QLabel("")
        self._label_formula.setStyleSheet("""
            font-size: 12px;
            color: #757575;
        """)
        layout.addWidget(self._label_formula)
        
        # Input manual (oculto inicialmente)
        self._manual_container = QFrame()
        self._manual_container.setVisible(False)
        manual_layout = QHBoxLayout(self._manual_container)
        manual_layout.setContentsMargins(0, 8, 0, 0)
        manual_layout.setSpacing(12)
        
        label_manual = QLabel("Precio de venta final:")
        label_manual.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #212121;
        """)
        manual_layout.addWidget(label_manual)
        
        self._input_precio_manual = QDoubleSpinBox()
        self._input_precio_manual.setMinimum(0)
        self._input_precio_manual.setMaximum(999999.99)
        self._input_precio_manual.setPrefix("S/ ")
        self._input_precio_manual.setAlignment(Qt.AlignRight)
        self._input_precio_manual.setMinimumHeight(40)
        self._input_precio_manual.setStyleSheet(self._estilo_input())
        self._input_precio_manual.setButtonSymbols(QDoubleSpinBox.NoButtons)
        manual_layout.addWidget(self._input_precio_manual)
        
        self._btn_volver = SisButton("Volver al sugerido", variant="secondary")
        self._btn_volver.setMinimumHeight(36)
        self._btn_volver.clicked.connect(self._volver_al_sugerido)
        manual_layout.addWidget(self._btn_volver)
        
        manual_layout.addStretch()
        layout.addWidget(self._manual_container)
        
        return container
    
    def _crear_campos_stock_vencimiento(self) -> QHBoxLayout:
        """Crea los campos de stock y vencimiento (lado a lado)"""
        layout = QHBoxLayout()
        layout.setSpacing(16)
        
        # Stock
        stock_layout = QVBoxLayout()
        stock_layout.setSpacing(8)
        
        label_stock = QLabel("📦 Stock disponible *")
        label_stock.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #212121;
        """)
        stock_layout.addWidget(label_stock)
        
        self._input_stock = QDoubleSpinBox()
        self._input_stock.setMinimum(0)
        self._input_stock.setMaximum(999999)
        self._input_stock.setDecimals(0)
        self._input_stock.setAlignment(Qt.AlignRight)
        self._input_stock.setMinimumHeight(48)
        self._input_stock.setStyleSheet(self._estilo_input())
        self._input_stock.setButtonSymbols(QDoubleSpinBox.NoButtons)
        stock_layout.addWidget(self._input_stock)
        
        self._error_stock = QLabel("")
        self._error_stock.setStyleSheet("font-size: 12px; color: #D32F2F;")
        self._error_stock.hide()
        stock_layout.addWidget(self._error_stock)
        
        # Vencimiento
        vence_layout = QVBoxLayout()
        vence_layout.setSpacing(8)
        
        label_vence = QLabel("⏰ Fecha de vencimiento")
        label_vence.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #212121;
        """)
        vence_layout.addWidget(label_vence)
        
        self._input_vencimiento = QDateEdit()
        self._input_vencimiento.setCalendarPopup(True)
        self._input_vencimiento.setDate(QDate.currentDate())
        self._input_vencimiento.setDisplayFormat("dd/MM/yyyy")
        self._input_vencimiento.setMinimumHeight(48)
        self._input_vencimiento.setStyleSheet(self._estilo_input())
        self._input_vencimiento.setSpecialValueText("Sin vencimiento")
        vence_layout.addWidget(self._input_vencimiento)
        
        layout.addLayout(stock_layout, 1)
        layout.addLayout(vence_layout, 1)
        
        return layout
    
    def _crear_campo_descripcion(self) -> QVBoxLayout:
        """Crea el campo de descripción (opcional)"""
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        label = QLabel("📝 Descripción (opcional)")
        label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #212121;
        """)
        layout.addWidget(label)
        
        self._input_descripcion = QLineEdit()
        self._input_descripcion.setPlaceholderText("Información adicional del producto...")
        self._input_descripcion.setMinimumHeight(48)
        self._input_descripcion.setStyleSheet(self._estilo_input())
        layout.addWidget(self._input_descripcion)
        
        return layout
    
    def _estilo_input(self) -> str:
        """Estilo de input (con focus verde)"""
        return f"""
            QLineEdit, QDoubleSpinBox, QDateEdit {{
                font-size: 14px;
                padding: 12px;
                border: 1px solid {BaseLayout.COLOR_BORDE};
                border-radius: {BaseLayout.BORDER_RADIUS_INPUT}px;
                background-color: white;
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
            }}
            QLineEdit:focus, QDoubleSpinBox:focus, QDateEdit:focus {{
                border: 2px solid {BaseLayout.COLOR_PRIMARIO};
                outline: none;
            }}
        """
    
    def _setup_footer(self):
        """Configura los botones del footer"""
        btn_cancelar = SisButton("CANCELAR", variant="secondary")
        btn_cancelar.clicked.connect(self.close)
        
        btn_guardar = SisButton("GUARDAR PRODUCTO", variant="primary")
        btn_guardar.clicked.connect(self._guardar_producto)
        
        self.set_footer([btn_cancelar, btn_guardar])
    
    def _actualizar_precio_sugerido(self):
        """Actualiza el precio sugerido cuando cambia precio_compra o margen"""
        precio_compra = self._input_precio_compra.value()
        margen = self._input_margen.value()
        precio_sugerido = self._controlador.calcular_precio_sugerido(precio_compra, margen)
        
        self._label_precio_sugerido.setText(f"S/ {precio_sugerido:.2f}")
        self._label_formula.setText(
            f"{precio_compra:.2f} × (1 + {margen:.0f}/100) = {precio_sugerido:.4f}"
        )
        
        # Si no está en modo manual, actualizar el valor manual
        if not self._modo_manual:
            self._input_precio_manual.setValue(precio_sugerido)
    
    def _aceptar_precio_sugerido(self):
        """Acepta el precio sugerido y oculta el input manual"""
        self._modo_manual = False
        self._manual_container.setVisible(False)
        self._btn_aceptar.setVisible(True)
        self._btn_modificar.setVisible(True)
        self._actualizar_precio_sugerido()
    
    def _modificar_precio_manual(self):
        """Muestra el input para modificar el precio manualmente"""
        self._modo_manual = True
        self._manual_container.setVisible(True)
        self._input_precio_manual.setFocus()
    
    def _volver_al_sugerido(self):
        """Vuelve al precio sugerido"""
        self._aceptar_precio_sugerido()
    
    def _cargar_datos_producto(self, producto: ProductoModelo):
        """Carga los datos de un producto existente en el formulario"""
        self._input_nombre.setText(producto.nombre)
        self._input_precio_compra.setValue(producto.precio_compra)
        self._input_margen.setValue(producto.margen)
        self._input_precio_manual.setValue(producto.precio_venta)
        self._input_stock.setValue(producto.stock)
        
        if producto.vencimiento:
            self._input_vencimiento.setDate(QDate(
                producto.vencimiento.year,
                producto.vencimiento.month,
                producto.vencimiento.day
            ))
        
        self._aceptar_precio_sugerido()
    
    def _validar(self) -> bool:
        """
        Valida todos los campos del formulario.
        
        Returns:
            bool: True si todos los campos son válidos
        """
        valido = True
        
        # Validar nombre
        nombre = self._input_nombre.text().strip()
        if not nombre:
            self._error_nombre.setText("El nombre es obligatorio")
            self._error_nombre.show()
            valido = False
        else:
            self._error_nombre.hide()
        
        # Validar precio compra
        precio_compra = self._input_precio_compra.value()
        if precio_compra <= 0:
            self._error_precio.setText("El precio de compra debe ser mayor a 0")
            self._error_precio.show()
            valido = False
        else:
            self._error_precio.hide()
        
        # Validar margen
        margen = self._input_margen.value()
        if margen < 0:
            self._error_margen.setText("El margen no puede ser negativo")
            self._error_margen.show()
            valido = False
        else:
            self._error_margen.hide()
        
        # Validar stock
        stock = int(self._input_stock.value())
        if stock < 0:
            self._error_stock.setText("El stock no puede ser negativo")
            self._error_stock.show()
            valido = False
        else:
            self._error_stock.hide()
        
        return valido
    
    def _guardar_producto(self):
        """Guarda el producto (nuevo o editado)"""
        if not self._validar():
            return
        
        try:
            nombre = self._input_nombre.text().strip()
            precio_compra = self._input_precio_compra.value()
            margen = self._input_margen.value()
            stock = int(self._input_stock.value())
            
            # Determinar precio de venta
            if self._modo_manual:
                precio_venta = self._input_precio_manual.value()
            else:
                precio_venta = self._controlador.calcular_precio_sugerido(precio_compra, margen)
            
            # Fecha de vencimiento
            fecha_qdate = self._input_vencimiento.date()
            vencimiento = date(fecha_qdate.year(), fecha_qdate.month(), fecha_qdate.day())
            
            if self._editando and self._producto:
                # Actualizar producto existente
                self._controlador.actualizar_producto(
                    id=self._producto.id,
                    nombre=nombre,
                    precio_compra=precio_compra,
                    margen=margen,
                    stock=stock,
                    precio_venta=precio_venta,
                    vencimiento=vencimiento
                )
                # Actualizar el objeto producto
                self._producto.nombre = nombre
                self._producto.precio_compra = precio_compra
                self._producto.margen = margen
                self._producto.stock = stock
                self._producto.precio_venta = precio_venta
                self._producto.vencimiento = vencimiento
                self.productoGuardado.emit(self._producto)
            else:
                # Crear nuevo producto
                nuevo_id = self._controlador.crear_producto(
                    nombre=nombre,
                    precio_compra=precio_compra,
                    margen=margen,
                    stock=stock,
                    precio_venta=precio_venta,
                    vencimiento=vencimiento
                )
                # Obtener el producto creado
                nuevo_producto = self._controlador.obtener_producto(nuevo_id)
                if nuevo_producto:
                    self.productoGuardado.emit(nuevo_producto)
            
            self.close()
            
        except ValueError as e:
            # Mostrar error en el campo correspondiente
            error_msg = str(e)
            if "nombre" in error_msg.lower():
                self._error_nombre.setText(error_msg)
                self._error_nombre.show()
            elif "precio de compra" in error_msg.lower():
                self._error_precio.setText(error_msg)
                self._error_precio.show()
            elif "margen" in error_msg.lower():
                self._error_margen.setText(error_msg)
                self._error_margen.show()
            elif "stock" in error_msg.lower():
                self._error_stock.setText(error_msg)
                self._error_stock.show()
    
    def set_producto(self, producto: ProductoModelo):
        """
        Cambia el producto a editar.
        
        Args:
            producto: Producto a editar (None para nuevo)
        """
        self._producto = producto
        self._editando = producto is not None
        self.set_title("Editar Producto" if producto else "Nuevo Producto")
        
        if producto:
            self._cargar_datos_producto(producto)
        else:
            self._limpiar_formulario()
    
    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self._input_nombre.clear()
        self._input_precio_compra.setValue(0)
        self._input_margen.setValue(30.0)
        self._input_stock.setValue(0)
        self._input_vencimiento.setDate(QDate.currentDate())
        self._input_descripcion.clear()
        self._aceptar_precio_sugerido()
        self._actualizar_precio_sugerido()
        
        # Ocultar errores
        self._error_nombre.hide()
        self._error_precio.hide()
        self._error_margen.hide()
        self._error_stock.hide()