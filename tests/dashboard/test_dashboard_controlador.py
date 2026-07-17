"""
Pruebas unitarias para el controlador de Dashboard
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import date

from src.app.controllers.dashboard_controlador import DashboardControlador


class TestDashboardControlador:
    """Pruebas para el controlador del Dashboard - HU-03."""

    def test_obtener_ganancia_estimada_dia_consulta_modelo(self):
        """
        El controlador debe llamar al modelo para obtener
        la ganancia estimada del día.
        """
        controlador = DashboardControlador(db_path='/tmp/test.db')
        
        mock_conn = MagicMock()
        with patch('src.app.controllers.dashboard_controlador.sqlite3.connect') as mock_sqlite:
            mock_sqlite.return_value = mock_conn
            with patch('src.app.controllers.dashboard_controlador.calcular_ganancia_estimada_dia') as mock_calcular:
                mock_calcular.return_value = 250.50
                
                ganancia = controlador.obtener_ganancia_estimada_dia()
                
                mock_calcular.assert_called_once()
                assert ganancia == 250.50

    def test_obtener_numero_ventas_dia_retorna_cantidad_correcta(self):
        """
        El controlador debe obtener el número de ventas del día del modelo.
        """
        controlador = DashboardControlador(db_path='/tmp/test.db')
        
        mock_conn = MagicMock()
        with patch('src.app.controllers.dashboard_controlador.sqlite3.connect') as mock_sqlite:
            mock_sqlite.return_value = mock_conn
            with patch('src.app.controllers.dashboard_controlador.obtener_numero_ventas_dia') as mock_ventas:
                mock_ventas.return_value = 5
                
                numero_ventas = controlador.obtener_numero_ventas_dia()
                
                mock_ventas.assert_called_once()
                assert numero_ventas == 5

    def test_obtener_ganancia_estimada_dia_retorna_cero_sin_ventas(self):
        """
        Si no hay ventas en el día, el controlador debe retornar 0.
        """
        controlador = DashboardControlador(db_path='/tmp/test.db')
        
        mock_conn = MagicMock()
        with patch('src.app.controllers.dashboard_controlador.sqlite3.connect') as mock_sqlite:
            mock_sqlite.return_value = mock_conn
            with patch('src.app.controllers.dashboard_controlador.calcular_ganancia_estimada_dia') as mock_calcular:
                mock_calcular.return_value = 0
                
                ganancia = controlador.obtener_ganancia_estimada_dia()
                
                assert ganancia == 0

    def test_actualizar_indicador_ganancia_obtiene_dato_y_actualiza_vista(self):
        """
        El controlador debe obtener la ganancia y número de ventas,
        y actualizar el indicador en la vista.
        """
        vista_mock = MagicMock()
        controlador = DashboardControlador(vista=vista_mock, db_path='/tmp/test.db')
        
        mock_conn = MagicMock()
        with patch('src.app.controllers.dashboard_controlador.sqlite3.connect') as mock_sqlite:
            mock_sqlite.return_value = mock_conn
            with patch('src.app.controllers.dashboard_controlador.calcular_ganancia_estimada_dia') as mock_calcular:
                with patch('src.app.controllers.dashboard_controlador.obtener_numero_ventas_dia') as mock_ventas:
                    mock_calcular.return_value = 347.75
                    mock_ventas.return_value = 3
                    
                    controlador.actualizar_indicador_ganancia()
                    
                    vista_mock.mostrar_ganancia.assert_called_once_with(347.75, 3)

    def test_actualizar_indicador_ganancia_formatea_moneda_correctamente(self):
        """
        El indicador debe mostrar la ganancia formateada
        con el símbolo de moneda S/ (nuevos soles) y número de ventas.
        """
        vista_mock = MagicMock()
        controlador = DashboardControlador(vista=vista_mock, db_path='/tmp/test.db')
        
        mock_conn = MagicMock()
        with patch('src.app.controllers.dashboard_controlador.sqlite3.connect') as mock_sqlite:
            mock_sqlite.return_value = mock_conn
            with patch('src.app.controllers.dashboard_controlador.calcular_ganancia_estimada_dia') as mock_calcular:
                with patch('src.app.controllers.dashboard_controlador.obtener_numero_ventas_dia') as mock_ventas:
                    mock_calcular.return_value = 500.00
                    mock_ventas.return_value = 2
                    
                    controlador.actualizar_indicador_ganancia()
                    
                    # Verifica que se llamó con el formato correcto
                    vista_mock.mostrar_ganancia.assert_called_once_with(500.00, 2)