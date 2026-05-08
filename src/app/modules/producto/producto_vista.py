"""
Módulo Producto - Vista
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QTableWidget,
                               QTableWidgetItem, QMessageBox, QHeaderView)
from .producto_controlador import ProductoControlador


class ProductoVista(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Título
        titulo = QLabel(f"📦 Gestión de Productos")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(titulo)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción"])
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.tabla)

        # Botones
        botones_layout = QHBoxLayout()
        
        btn_refrescar = QPushButton("🔄 Refrescar")
        btn_refrescar.clicked.connect(self.refrescar)
        botones_layout.addWidget(btn_refrescar)
        
        btn_nuevo = QPushButton("➕ Nuevo")
        btn_nuevo.clicked.connect(self.nuevo)
        botones_layout.addWidget(btn_nuevo)
        
        botones_layout.addStretch()
        layout.addLayout(botones_layout)

        # Cargar datos
        self.refrescar()

    def refrescar(self):
        """Carga los datos en la tabla"""
        try:
            datos = ProductoControlador.listar_ejemplo()
            self.tabla.setRowCount(len(datos))
            for i, item in enumerate(datos):
                self.tabla.setItem(i, 0, QTableWidgetItem(str(item.id)))
                self.tabla.setItem(i, 1, QTableWidgetItem(item.nombre))
                self.tabla.setItem(i, 2, QTableWidgetItem(item.descripcion))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron cargar los datos: {e}")

    def nuevo(self):
        """Abre diálogo para crear nuevo"""
        QMessageBox.information(self, "Nuevo", "Funcionalidad en desarrollo")
