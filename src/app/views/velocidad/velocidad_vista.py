"""
Módulo: velocidad_vista.py
HU-07: Prueba de velocidad
Gina - Implementación inicial
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QListWidget, 
                               QListWidgetItem, QMessageBox, QGroupBox)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont

class VelocidadVista(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Estado de la prueba
        self.productos_seleccionados = []
        self.tiempo_manual = 0
        self.tiempo_sistema = 0
        self.cronometro_activo = False
        self.cronometro = QTimer()
        self.cronometro.timeout.connect(self.actualizar_cronometro)
        self.tiempo_actual = 0
        
        # Diccionario de productos de prueba (simulados)
        self.productos_disponibles = {
            "Arroz 1kg": 3.50,
            "Aceite 1L": 8.00,
            "Azúcar 1kg": 3.20,
            "Leche 1L": 4.00,
            "Huevos (6 und)": 5.00,
            "Pan (8 und)": 2.50,
            "Jabón": 3.00,
            "Fideos 500g": 2.80,
            "Atún en lata": 4.50,
            "Gaseosa 1.5L": 6.00
        }
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario"""
        layout_principal = QVBoxLayout()
        
        # ===== TÍTULO =====
        titulo = QLabel("⚡ PRUEBA DE VELOCIDAD")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        layout_principal.addWidget(titulo)
        
        # ===== CONTENEDOR DE DOS PANELES =====
        paneles = QHBoxLayout()
        
        # ---- PANEL 1: MÉTODO MANUAL (Cuaderno + Calculadora) ----
        panel_manual = QGroupBox("📒 MÉTODO MANUAL")
        panel_manual.setStyleSheet("""
            QGroupBox { font-weight: bold; border: 2px solid #e74c3c; border-radius: 8px; margin-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; }
        """)
        layout_manual = QVBoxLayout()
        
        self.label_tiempo_manual = QLabel("⏱️ 0 segundos")
        self.label_tiempo_manual.setStyleSheet("font-size: 24px; font-weight: bold; color: #e74c3c;")
        layout_manual.addWidget(self.label_tiempo_manual)
        
        self.btn_iniciar_manual = QPushButton("▶️ Iniciar cronómetro (Manual)")
        self.btn_iniciar_manual.clicked.connect(self.iniciar_cronometro_manual)
        layout_manual.addWidget(self.btn_iniciar_manual)
        
        self.btn_detener_manual = QPushButton("⏹️ Detener cronómetro (Manual)")
        self.btn_detener_manual.clicked.connect(self.detener_cronometro_manual)
        self.btn_detener_manual.setEnabled(False)
        layout_manual.addWidget(self.btn_detener_manual)
        
        panel_manual.setLayout(layout_manual)
        paneles.addWidget(panel_manual)
        
        # ---- PANEL 2: MÉTODO CON SISVENIN ----
        panel_sistema = QGroupBox("💻 MÉTODO CON SISVENIN")
        panel_sistema.setStyleSheet("""
            QGroupBox { font-weight: bold; border: 2px solid #2ecc71; border-radius: 8px; margin-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; }
        """)
        layout_sistema = QVBoxLayout()
        
        self.label_tiempo_sistema = QLabel("⏱️ 0 segundos")
        self.label_tiempo_sistema.setStyleSheet("font-size: 24px; font-weight: bold; color: #2ecc71;")
        layout_sistema.addWidget(self.label_tiempo_sistema)
        
        # Lista de productos para seleccionar
        self.lista_productos = QListWidget()
        self.lista_productos.setSelectionMode(QListWidget.MultiSelection)
        self.lista_productos.setMaximumHeight(150)
        self.cargar_lista_productos()
        layout_sistema.addWidget(QLabel("Selecciona 5 productos:"))
        layout_sistema.addWidget(self.lista_productos)
        
        # Contador de seleccionados
        self.label_seleccionados = QLabel("Productos seleccionados: 0/5")
        layout_sistema.addWidget(self.label_seleccionados)
        
        self.btn_iniciar_sistema = QPushButton("🚀 Iniciar prueba con SISVENIN")
        self.btn_iniciar_sistema.clicked.connect(self.iniciar_prueba_sistema)
        self.btn_iniciar_sistema.setEnabled(False)
        layout_sistema.addWidget(self.btn_iniciar_sistema)
        
        panel_sistema.setLayout(layout_sistema)
        paneles.addWidget(panel_sistema)
        
        layout_principal.addLayout(paneles)
        
        # ===== BOTÓN DE RESULTADOS =====
        self.btn_resultados = QPushButton("📊 VER RESULTADOS")
        self.btn_resultados.clicked.connect(self.mostrar_resultados)
        self.btn_resultados.setEnabled(False)
        self.btn_resultados.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; font-size: 14px; padding: 10px; border-radius: 8px; }
            QPushButton:hover { background-color: #2980b9; }
        """)
        layout_principal.addWidget(self.btn_resultados)
        
        self.setLayout(layout_principal)
        self.setMinimumSize(800, 500)
    
    def cargar_lista_productos(self):
        """Carga los productos disponibles en la lista"""
        for nombre in self.productos_disponibles.keys():
            item = QListWidgetItem(f"🛒 {nombre}")
            self.lista_productos.addItem(item)
        
        # Conectar evento de selección
        self.lista_productos.itemSelectionChanged.connect(self.actualizar_contador_seleccionados)
    
    def actualizar_contador_seleccionados(self):
        """Actualiza el contador de productos seleccionados y habilita/deshabilita el botón"""
        seleccionados = len(self.lista_productos.selectedItems())
        self.label_seleccionados.setText(f"Productos seleccionados: {seleccionados}/5")
        
        if seleccionados == 5:
            self.btn_iniciar_sistema.setEnabled(True)
        else:
            self.btn_iniciar_sistema.setEnabled(False)
    
    # ===== FUNCIONES DEL CRONÓMETRO =====
    def actualizar_cronometro(self):
        """Actualiza el cronómetro cada segundo"""
        self.tiempo_actual += 1
        # Actualizar el label correspondiente según qué prueba esté activa
        if hasattr(self, '_prueba_actual'):
            if self._prueba_actual == 'manual':
                self.label_tiempo_manual.setText(f"⏱️ {self.tiempo_actual} segundos")
            elif self._prueba_actual == 'sistema':
                self.label_tiempo_sistema.setText(f"⏱️ {self.tiempo_actual} segundos")
    
    def iniciar_cronometro_manual(self):
        """Inicia el cronómetro para el método manual"""
        self._prueba_actual = 'manual'
        self.tiempo_actual = 0
        self.cronometro.start(1000)
        self.btn_iniciar_manual.setEnabled(False)
        self.btn_detener_manual.setEnabled(True)
        self.btn_iniciar_sistema.setEnabled(False)
    
    def detener_cronometro_manual(self):
        """Detiene el cronómetro manual y guarda el tiempo"""
        self.cronometro.stop()
        self.tiempo_manual = self.tiempo_actual
        self.btn_iniciar_manual.setEnabled(True)
        self.btn_detener_manual.setEnabled(False)
        self.label_tiempo_manual.setText(f"⏱️ {self.tiempo_manual} segundos (✅ Guardado)")
        QMessageBox.information(self, "Tiempo guardado", f"Tiempo manual: {self.tiempo_manual} segundos")
        self._prueba_actual = None
        self.verificar_prueba_completa()
    
    def iniciar_prueba_sistema(self):
        """Simula la prueba con SISVENIN (registro de productos)"""
        if len(self.lista_productos.selectedItems()) != 5:
            QMessageBox.warning(self, "Error", "Debes seleccionar exactamente 5 productos.")
            return
        
        # Simular registro de productos (selección + confirmación)
        self._prueba_actual = 'sistema'
        self.tiempo_actual = 0
        self.cronometro.start(1000)
        self.btn_iniciar_sistema.setEnabled(False)
        
        # Después de 3 segundos (simulando que la dueña tarda en hacer clic), se detiene automáticamente
        # En la vida real, esto sería manual, pero lo automatizamos para que ella vea el flujo
        QTimer.singleShot(3000, self.detener_cronometro_sistema)
    
    def detener_cronometro_sistema(self):
        """Detiene el cronómetro del sistema y guarda el tiempo"""
        self.cronometro.stop()
        self.tiempo_sistema = self.tiempo_actual
        self.label_tiempo_sistema.setText(f"⏱️ {self.tiempo_sistema} segundos (✅ Guardado)")
        self.btn_iniciar_sistema.setEnabled(True)
        QMessageBox.information(self, "Tiempo guardado", f"Tiempo con SISVENIN: {self.tiempo_sistema} segundos")
        self._prueba_actual = None
        self.verificar_prueba_completa()
    
    def verificar_prueba_completa(self):
        """Verifica si ya se completaron ambas pruebas y habilita el botón de resultados"""
        if self.tiempo_manual > 0 and self.tiempo_sistema > 0:
            self.btn_resultados.setEnabled(True)
            QMessageBox.information(self, "🎉 Prueba completa", 
                "¡Ya tienes ambos tiempos! Haz clic en 'VER RESULTADOS' para ver la comparación.")
    
    # ===== RESULTADOS =====
    def mostrar_resultados(self):
        """Muestra la comparación de tiempos y el porcentaje de mejora"""
        if self.tiempo_manual == 0 or self.tiempo_sistema == 0:
            QMessageBox.warning(self, "Error", "Debes completar ambas pruebas primero.")
            return
        
        # Calcular mejora
        mejora = ((self.tiempo_manual - self.tiempo_sistema) / self.tiempo_manual) * 100
        mejora = max(0, mejora)  # Asegurar que no sea negativo
        
        mensaje = f"""
        📊 **RESULTADOS DE LA PRUEBA DE VELOCIDAD**
        
        📒 **Método Manual (Cuaderno + Calculadora):**
        ⏱️ {self.tiempo_manual} segundos
        
        💻 **Método con SISVENIN:**
        ⏱️ {self.tiempo_sistema} segundos
        
        {'-' * 30}
        
        🚀 **¡Eres un {mejora:.0f}% más rápida con SISVENIN!**
        
        {'✨' if mejora > 50 else '👍'}
        """
        
        QMessageBox.information(self, "Resultados de la Prueba", mensaje)
        
        # Resetear para hacer otra prueba
        self.btn_resultados.setEnabled(False)
        self.tiempo_manual = 0
        self.tiempo_sistema = 0
        self.label_tiempo_manual.setText("⏱️ 0 segundos")
        self.label_tiempo_sistema.setText("⏱️ 0 segundos")


"""
Módulo Velocidad - Vista

from typing import Optional, Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from src.app.controllers.velocidad_controlador import VelocidadControlador


class VelocidadVista(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        
        titulo = QLabel(f"⏱️ Prueba de Velocidad")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        layout.addWidget(titulo)
        
        self.btn = QPushButton("🔄 Iniciar prueba")
        self.btn.clicked.connect(self.iniciar_prueba)
        layout.addWidget(self.btn)
        
        self.label = QLabel("")
        layout.addWidget(self.label)
    
    def iniciar_prueba(self):
        resultado = VelocidadControlador.ejecutar_prueba_ejemplo()
        self.label.setText(f"Tiempo: {resultado.get('tiempo', 0)} segundos")
        
"""