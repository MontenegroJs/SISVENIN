"""
Controlador del módulo Reporte
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from app.models.reporte_modelo import ReporteModelo
from app.utils.pdf_generador import guardar_html_reporte, guardar_texto_como_pdf


class ReporteControlador:
    """
    Controlador responsable de orquestar la lógica de negocio para el módulo de Reportes.
    Coordina la comunicación entre el Modelo (datos) y la Vista (interfaz).
    """

    def __init__(self):
        self.modelo = ReporteModelo()

    def _formatear_fecha(self, fecha: Optional[str] = None) -> str:
        if fecha is None:
            return datetime.now().strftime("%d/%m/%Y")

        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            return fecha_obj.strftime("%d/%m/%Y")
        except ValueError:
            return fecha

    def obtener_datos_para_reporte_dia(self, fecha: Optional[str] = None) -> Dict[str, Any]:
        """
        Orquesta la obtención de datos del reporte diario.
        Si no hay ventas para el día actual, usa la última fecha disponible.
        """
        fecha_consulta = fecha or datetime.now().strftime("%Y-%m-%d")

        try:
            resumen = self.modelo.obtener_resumen_dia(fecha_consulta)
            productos = self.modelo.obtener_productos_vendidos_dia(fecha_consulta)

            if fecha is None and not productos and resumen["total_ingresos"] == 0:
                ultima_fecha = self.modelo.obtener_ultima_fecha_ventas()
                if ultima_fecha and ultima_fecha != fecha_consulta:
                    fecha_consulta = ultima_fecha
                    resumen = self.modelo.obtener_resumen_dia(fecha_consulta)
                    productos = self.modelo.obtener_productos_vendidos_dia(fecha_consulta)

            return {
                "resumen": resumen,
                "productos": productos,
                "fecha_formateada": self._formatear_fecha(fecha_consulta),
                "error": False,
                "mensaje_error": ""
            }

        except Exception:
            return {
                "resumen": {
                    "total_ingresos": 0.0,
                    "total_ventas": 0,
                    "ganancia_estimada": 0.0,
                    "margen_promedio": 0.0
                },
                "productos": [],
                "fecha_formateada": datetime.now().strftime("%d/%m/%Y"),
                "error": True,
                "mensaje_error": "No se pudo cargar el reporte. Verifique la base de datos."
            }

    def _armar_texto_reporte(self, datos: Dict[str, Any]) -> str:
        resumen = datos["resumen"]
        lines = [
            "MINIMARKET VILLA CARRION",
            "REPORTE DEL DÍA",
            f"Fecha: {datos['fecha_formateada']}",
            "",
            f"TOTAL INGRESOS: S/ {resumen['total_ingresos']:.2f}",
            f"GANANCIA ESTIMADA: S/ {resumen['ganancia_estimada']:.2f}",
            f"MARGEN PROMEDIO: {resumen['margen_promedio']:.1f}%",
            "",
            "PRODUCTOS VENDIDOS:",
        ]

        for producto in datos["productos"]:
            lines.append(
                f"- {producto['nombre']} | Cant: {producto['cantidad']} | P.Unit: S/ {producto['precio_unitario']:.2f} | Subtotal: S/ {producto['subtotal']:.2f} | %: {producto['porcentaje']:.1f}%"
            )

        return "\n".join(lines)

    def _armar_html_reporte(self, datos: Dict[str, Any]) -> str:
        resumen = datos["resumen"]
        producto_rows = "".join(
            f"<tr><td>{producto['nombre']}</td><td>{producto['cantidad']}</td><td>S/ {producto['precio_unitario']:.2f}</td><td>S/ {producto['subtotal']:.2f}</td><td>{producto['porcentaje']:.1f}%</td></tr>"
            for producto in datos["productos"]
        )

        return f"""
<html>
<head>
    <meta charset=\"utf-8\" />
    <title>Reporte del día</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 24px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #444; padding: 8px; text-align: left; }}
        th {{ background: #f3f3f3; }}
    </style>
</head>
<body>
    <h1>Minimarket Villa Carrion</h1>
    <h2>Reporte del día</h2>
    <p>Fecha: {datos['fecha_formateada']}</p>
    <p>Total ingresos: S/ {resumen['total_ingresos']:.2f}</p>
    <p>Ganancia estimada: S/ {resumen['ganancia_estimada']:.2f}</p>
    <p>Margen promedio: {resumen['margen_promedio']:.1f}%</p>
    <table>
        <thead>
            <tr>
                <th>Producto</th>
                <th>Cantidad</th>
                <th>Precio unitario</th>
                <th>Subtotal</th>
                <th>%</th>
            </tr>
        </thead>
        <tbody>
            {producto_rows}
        </tbody>
    </table>
</body>
</html>
"""

    def guardar_reporte_html(self, fecha: Optional[str] = None, ruta_salida: Optional[str] = None) -> Dict[str, Any]:
        datos = self.obtener_datos_para_reporte_dia(fecha)
        if datos["error"]:
            return {"error": True, "mensaje": datos["mensaje_error"], "ruta": None}

        ruta_salida = ruta_salida or f"reporte_del_dia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        html = self._armar_html_reporte(datos)
        ruta = guardar_html_reporte(html, ruta_salida)

        return {"error": False, "mensaje": "Reporte HTML generado correctamente.", "ruta": ruta}

    def exportar_reporte_pdf(self, fecha: Optional[str] = None, ruta_salida: Optional[str] = None) -> Dict[str, Any]:
        datos = self.obtener_datos_para_reporte_dia(fecha)
        if datos["error"]:
            return {"error": True, "mensaje": datos["mensaje_error"], "ruta_pdf": None}

        ruta_salida = ruta_salida or f"reporte_del_dia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        texto = self._armar_texto_reporte(datos)

        try:
            ruta_pdf = guardar_texto_como_pdf(texto, ruta_salida)
            return {"error": False, "mensaje": "Reporte PDF generado correctamente.", "ruta_pdf": ruta_pdf}
        except Exception as error:
            html_ruta = Path(ruta_salida).with_suffix(".html")
            guardar_html_reporte(self._armar_html_reporte(datos), str(html_ruta))
            return {
                "error": True,
                "mensaje": f"No se pudo generar PDF: {error}. Se creó HTML en {html_ruta}",
                "ruta_pdf": None,
                "ruta_html": str(html_ruta),
            }