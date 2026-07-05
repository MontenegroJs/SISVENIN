from typing import List
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from src.app.base_layout import BaseLayout


class TablaProductosVendidos(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._productos = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._table = QTableWidget()
        self._table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels([
            "Producto",
            "Cantidad",
            "Precio Unit.",
            "Subtotal",
            "% Ventas"
        ])
        self._table.verticalHeader().setVisible(False)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.setSelectionMode(QTableWidget.SingleSelection)
        self._table.setShowGrid(False)
        self._table.setAlternatingRowColors(True)
        self._table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._table.verticalHeader().setDefaultSectionSize(44)

        header = self._table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self._table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {BaseLayout.COLOR_TARJETA};
                border: 1px solid {BaseLayout.COLOR_BORDE};
                border-radius: {BaseLayout.BORDER_RADIUS_TARJETA}px;
            }}
            QTableWidget::item {{
                padding: 12px 16px;
                border-bottom: 1px solid {BaseLayout.COLOR_BORDE};
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
                background-color: white;
            }}
            QTableWidget::item:hover {{
                background-color: {BaseLayout.COLOR_HOVER_FILA};
            }}
            QTableWidget::item:selected {{
                background-color: rgba(46, 125, 50, 0.08);
            }}
            QHeaderView::section {{
                background-color: #F5F5F5;
                border-bottom: 1px solid {BaseLayout.COLOR_BORDE};
                padding: 14px 16px;
                font-size: 14px;
                font-weight: 600;
                color: {BaseLayout.COLOR_TEXTO_PRINCIPAL};
            }}
            QTableCornerButton::section {{
                background-color: #F5F5F5;
                border: none;
            }}
        """)

        layout.addWidget(self._table)

    def actualizar(self, productos: List[dict]) -> None:
        self._productos = productos
        self._table.setRowCount(len(productos))

        for row, item in enumerate(productos):
            producto_item = QTableWidgetItem(item.get("nombre", ""))
            cantidad_item = QTableWidgetItem(str(item.get("cantidad", 0)))
            precio_item = QTableWidgetItem(f"S/ {item.get('precio_unitario', 0.0):.2f}")
            total_item = QTableWidgetItem(f"S/ {item.get('subtotal', 0.0):.2f}")
            margen_item = QTableWidgetItem(f"{item.get('porcentaje', 0.0):.1f}%")

            for col, widget_item in enumerate([producto_item, cantidad_item, precio_item, total_item, margen_item]):
                widget_item.setTextAlignment(Qt.AlignVCenter | (Qt.AlignRight if col in (1, 2, 3, 4) else Qt.AlignLeft))
                self._table.setItem(row, col, widget_item)

            if item.get("porcentaje", 0.0) < 0:
                for col in range(5):
                    self._table.item(row, col).setForeground(QColor(BaseLayout.COLOR_PELIGRO))

        if productos:
            total_cantidad = sum(item.get("cantidad", 0) for item in productos)
            total_subtotal = sum(item.get("subtotal", 0.0) for item in productos)
            row = self._table.rowCount()
            self._table.insertRow(row)

            total_label = QTableWidgetItem("TOTALES")
            total_label.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            total_label.setFont(total_label.font())
            self._table.setItem(row, 0, total_label)

            cantidad_total = QTableWidgetItem(str(total_cantidad))
            cantidad_total.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self._table.setItem(row, 1, cantidad_total)

            subtotal_empty = QTableWidgetItem("")
            subtotal_empty.setFlags(subtotal_empty.flags() & ~Qt.ItemIsSelectable)
            self._table.setItem(row, 2, subtotal_empty)

            total_subtotal_item = QTableWidgetItem(f"S/ {total_subtotal:.2f}")
            total_subtotal_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            total_subtotal_item.setForeground(QColor("#2E7D32"))
            self._table.setItem(row, 3, total_subtotal_item)

            porcentaje_total = QTableWidgetItem("100%")
            porcentaje_total.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            porcentaje_total.setForeground(QColor("#2E7D32"))
            self._table.setItem(row, 4, porcentaje_total)

            for col in range(5):
                item = self._table.item(row, col)
                if item:
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                    item.setBackground(QColor("#F5F5F5"))
        else:
            self._table.setRowCount(1)
            empty_item = QTableWidgetItem("No hay productos vendidos")
            empty_item.setTextAlignment(Qt.AlignCenter)
            self._table.setSpan(0, 0, 1, 5)
            self._table.setItem(0, 0, empty_item)
