# src/app/shared/components/__init__.py
"""
Componentes compartidos de SISVENIN
Equivalente a los componentes de React (sisvenin-button, sisvenin-card, etc.)

Uso:
    from src.app.shared.components import SisButton, SisCard, SisModal
"""

# Botones
from .sis_button import SisButton, SisIconButton

# Tarjetas
from .sis_card import SisCard, SisMetricCard

# Inputs
from .sis_input import SisInput, SisNumberInput

# Select
from .sis_select import SisSelect

# Modales
from .sis_modal import SisModal, SisConfirmModal

# Alertas
from .sis_alert import SisAlert, SisAlertList, SisEmptyState

# Tablas
from .sis_table import SisTable, SisPaginatedTable

# Paginación
from .sis_pagination import SisPagination, SisCompactPagination

# Exportar todo
__all__ = [
    # Botones
    "SisButton",
    "SisIconButton",
    # Tarjetas
    "SisCard",
    "SisMetricCard",
    # Inputs
    "SisInput",
    "SisNumberInput",
    # Select
    "SisSelect",
    # Modales
    "SisModal",
    "SisConfirmModal",
    # Alertas
    "SisAlert",
    "SisAlertList",
    "SisEmptyState",
    # Tablas
    "SisTable",
    "SisPaginatedTable",
    # Paginación
    "SisPagination",
    "SisCompactPagination",
]