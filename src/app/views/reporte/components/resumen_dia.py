from PySide6.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel, QVBoxLayout, QSizePolicy, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class ResumenDia(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        self.card_total = self._crear_tarjeta(
            "TOTAL INGRESOS",
            "S/ 0.00",
            "Ventas realizadas: 0",
            "#2E7D32",
            "💰",
        )
        self.card_ganancia = self._crear_tarjeta(
            "GANANCIA ESTIMADA",
            "S/ 0.00",
            "Margen promedio: 0%",
            "#FF9800",
            "📈",
        )

        self.card_total.setMinimumWidth(440)
        self.card_total.setMinimumHeight(240)
        self.card_ganancia.setMinimumWidth(440)
        self.card_ganancia.setMinimumHeight(240)

        layout.addWidget(self.card_total)
        layout.addWidget(self.card_ganancia)
        layout.addStretch()

    def _crear_tarjeta(
        self,
        titulo: str,
        valor: str,
        subtitulo: str,
        color: str,
        icono: str,
    ) -> QFrame:
        frame = QFrame()
        frame.setObjectName("ResumenCard")
        frame.setStyleSheet(
            "QFrame#ResumenCard { background-color: white; border: 1px solid #E0E0E0; border-radius: 16px; }"
        )
        frame.setMinimumHeight(210)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 25))
        frame.setGraphicsEffect(shadow)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(16)
        frame_layout.setContentsMargins(24, 24, 24, 24)

        top_row = QHBoxLayout()
        icon = QLabel(icono)
        icon.setStyleSheet(f"font-size: 22px; color: {color};")
        top_row.addWidget(icon)
        top_row.addStretch()

        title = QLabel(titulo)
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #1A237E;")
        value = QLabel(valor)
        value.setStyleSheet(f"font-size: 42px; font-weight: 800; color: {color};")
        subtitle = QLabel(subtitulo)
        subtitle.setStyleSheet("font-size: 14px; color: #757575;")

        frame_layout.addLayout(top_row)
        frame_layout.addWidget(title)
        frame_layout.addWidget(value)
        frame_layout.addStretch()
        frame_layout.addWidget(subtitle)

        frame._value_label = value
        frame._subtitle_label = subtitle
        return frame

    def actualizar(self, total_ingresos: float, total_ventas: int, ganancia: float, margen: float) -> None:
        self.card_total._value_label.setText(f"S/ {total_ingresos:,.2f}")
        self.card_total._subtitle_label.setText(f"Ventas realizadas: {total_ventas}")
        self.card_ganancia._value_label.setText(f"S/ {ganancia:,.2f}")
        self.card_ganancia._subtitle_label.setText(f"Margen promedio: {margen:.0f}%")
