import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

# Importamos el controlador y el modelo para el mock
from app.controllers.reporte_controlador import ReporteControlador
from app.models.reporte_modelo import ReporteModelo

class TestReporteControlador:
    
    # 1. PRUEBA: El controlador obtiene y estructura correctamente los datos
    def test_obtener_datos_para_reporte_con_ventas(self):
        """
        Verifica que el controlador orqueste correctamente la llamada al modelo
        y estructure los datos en el formato exacto que espera la Vista (UI).
        """
        # --- Setup (Preparar el escenario) ---
        
        # Creamos un Mock del Modelo. No queremos tocar la BD real en esta prueba.
        mock_modelo = MagicMock(spec=ReporteModelo)
        
        # Definimos qué devolverá el modelo cuando el controlador lo llame
        # Datos simulados que coinciden con nuestra prueba anterior del modelo
        mock_modelo.obtener_resumen_dia.return_value = {
            "total_ingresos": 30.00,
            "total_ventas": 2,
            "ganancia_estimada": 10.10,
            "margen_promedio": 33.7
        }
        
        mock_modelo.obtener_productos_vendidos_dia.return_value = [
            {"nombre": "Galletas soda", "cantidad": 5, "precio_unitario": 2.50, "subtotal": 12.50, "porcentaje": 41.7},
            {"nombre": "Yogur fresa", "cantidad": 3, "precio_unitario": 3.00, "subtotal": 9.00, "porcentaje": 30.0},
            {"nombre": "Leche evaporada", "cantidad": 2, "precio_unitario": 2.50, "subtotal": 5.00, "porcentaje": 16.6},
            {"nombre": "Arroz 1kg", "cantidad": 1, "precio_unitario": 3.50, "subtotal": 3.50, "porcentaje": 11.7}
        ]

        # Inyectamos el mock en el controlador
        controlador = ReporteControlador()
        controlador.modelo = mock_modelo
        
        # --- Ejecutar (Action) ---
        resultado = controlador.obtener_datos_para_reporte_dia()

        # --- Verificar (Assertions) ---
        
        # 1. El controlador debe haber llamado a los métodos del modelo exactamente una vez
        mock_modelo.obtener_resumen_dia.assert_called_once()
        mock_modelo.obtener_productos_vendidos_dia.assert_called_once()

        # 2. La estructura devuelta debe tener las claves que usará la interfaz
        assert "resumen" in resultado
        assert "productos" in resultado
        assert "fecha_formateada" in resultado

        # 3. Validar el resumen (El controlador debe validar y dejar los datos listos)
        resumen = resultado["resumen"]
        assert resumen["total_ingresos"] == 30.00
        assert resumen["total_ventas"] == 2
        assert resumen["ganancia_estimada"] == 10.10
        assert resumen["margen_promedio"] == 33.7
        
        # 4. Validar la lista de productos
        productos = resultado["productos"]
        assert len(productos) == 4
        assert productos[0]["nombre"] == "Galletas soda"
        assert productos[0]["porcentaje"] == 41.7

        # 5. Validar que la fecha esté formateada correctamente para la UI (ej: "04/07/2026")
        # Usamos un patrón regex simple para verificar formato DD/MM/YYYY
        import re
        assert re.match(r"\d{2}/\d{2}/\d{4}", resultado["fecha_formateada"])


    # 2. PRUEBA: El controlador maneja correctamente el escenario "Sin ventas"
    def test_obtener_datos_para_reporte_sin_ventas(self):
        """
        Verifica que el controlador maneje con gracia el caso de que no haya 
        ventas en el día (evitando que la vista reciba None o errores).
        """
        # --- Setup ---
        mock_modelo = MagicMock(spec=ReporteModelo)
        
        # El modelo devuelve datos en cero y lista vacía
        mock_modelo.obtener_resumen_dia.return_value = {
            "total_ingresos": 0.0,
            "total_ventas": 0,
            "ganancia_estimada": 0.0,
            "margen_promedio": 0.0
        }
        mock_modelo.obtener_productos_vendidos_dia.return_value = []

        controlador = ReporteControlador()
        controlador.modelo = mock_modelo

        # --- Ejecutar ---
        resultado = controlador.obtener_datos_para_reporte_dia()

        # --- Verificar ---
        resumen = resultado["resumen"]
        
        # Debe seguir siendo un diccionario con ceros, no None
        assert resumen["total_ingresos"] == 0.0
        assert resumen["total_ventas"] == 0
        
        # La lista de productos debe estar vacía, no None
        assert resultado["productos"] == []

        # La fecha debe formatearse igual, no importa que no haya datos
        assert resultado["fecha_formateada"] is not None


    # 3. PRUEBA: El controlador maneja errores inesperados del modelo
    def test_controlador_maneja_error_bd(self):
        """
        Verifica que si el modelo lanza una excepción (ej: BD corrupta), 
        el controlador la capture y devuelva un estado de error en lugar de 
        estrellar la aplicación.
        """
        # --- Setup ---
        mock_modelo = MagicMock(spec=ReporteModelo)
        # Simulamos un error grave al consultar la BD
        mock_modelo.obtener_resumen_dia.side_effect = Exception("Database disk image is malformed")

        controlador = ReporteControlador()
        controlador.modelo = mock_modelo

        # --- Ejecutar ---
        resultado = controlador.obtener_datos_para_reporte_dia()

        # --- Verificar ---
        # El controlador debe devolver un diccionario con una bandera de error y el mensaje
        assert resultado["error"] is True
        assert "No se pudo cargar el reporte" in resultado["mensaje_error"]
        # Los datos deben estar en cero para que la UI no se rompa
        assert resultado["resumen"]["total_ingresos"] == 0.0