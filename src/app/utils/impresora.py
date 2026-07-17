"""
Utilidad de impresión de tickets - SISVENIN
HU-05: Ticket de venta obligatorio

Soporta:
- Impresión en impresoras térmicas (por defecto)
- Vista previa en pantalla (fallback)
- Formato de ticket estilo POS
"""

import os
import tempfile
from typing import List, Optional
from datetime import datetime
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QTextDocument, QFont
from PySide6.QtCore import Qt

from src.app.models.producto_modelo import ProductoModelo


class ImpresoraTicket:
    """
    Clase para manejar la impresión de tickets de venta.
    """
    
    def __init__(self):
        """Inicializa la impresora"""
        self.printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        self.printer.setPageSize(QPrinter.PageSize.Custom)
        self.printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter)
    
    def imprimir(
        self,
        productos: List[ProductoModelo],
        total: float,
        pago: float,
        vuelto: float
    ) -> bool:
        """
        Imprime el ticket de venta.
        
        Args:
            productos: Lista de productos vendidos
            total: Monto total
            pago: Monto recibido
            vuelto: Vuelto a devolver
            
        Returns:
            True si se imprimió correctamente, False en caso contrario
        """
        try:
            # Generar el texto del ticket
            texto_ticket = self._generar_texto_ticket(productos, total, pago, vuelto)
            
            # Crear un documento HTML para la impresión
            html = self._generar_html_ticket(productos, total, pago, vuelto)
            
            # Opción 1: Intentar imprimir con QPrinter
            if self._intentar_imprimir_html(html):
                return True
            
            # Opción 2: Fallback - Guardar como texto
            self._guardar_como_texto(texto_ticket)
            return False
            
        except Exception as e:
            print(f"❌ Error al imprimir ticket: {e}")
            return False
    
    def _intentar_imprimir_html(self, html: str) -> bool:
        """
        Intenta imprimir el ticket usando QPrinter.
        
        Returns:
            True si el usuario confirmó la impresión
        """
        try:
            doc = QTextDocument()
            doc.setHtml(html)
            doc.setPageSize(self.printer.pageRect().size())
            
            dialog = QPrintDialog(self.printer)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                doc.print_(self.printer)
                return True
            return False
        except Exception as e:
            print(f"⚠️ Error en impresión: {e}")
            return False
    
    def _generar_html_ticket(
        self,
        productos: List[ProductoModelo],
        total: float,
        pago: float,
        vuelto: float
    ) -> str:
        """Genera el ticket en formato HTML para impresión"""
        
        # Agrupar productos por ID
        agrupados = {}
        for p in productos:
            if p.id not in agrupados:
                agrupados[p.id] = {"producto": p, "cantidad": 0}
            agrupados[p.id]["cantidad"] += 1
        
        # Generar filas de productos
        filas = ""
        for data in agrupados.values():
            producto = data["producto"]
            cantidad = data["cantidad"]
            subtotal = producto.precio_venta * cantidad
            filas += f"""
                <tr>
                    <td style="padding: 4px 0;">{producto.nombre} x{cantidad}</td>
                    <td style="padding: 4px 0; text-align: right;">S/ {subtotal:.2f}</td>
                </tr>
            """
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    width: 280px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 1px dashed #000;
                    padding-bottom: 10px;
                    margin-bottom: 10px;
                }}
                .negocio {{
                    font-size: 18px;
                    font-weight: bold;
                    color: #2E7D32;
                }}
                .subtitulo {{
                    font-size: 11px;
                    color: #666;
                }}
                .fecha {{
                    text-align: center;
                    font-size: 11px;
                    margin-bottom: 10px;
                }}
                .productos {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                .productos th {{
                    font-size: 11px;
                    border-bottom: 1px dashed #000;
                    padding: 4px 0;
                    text-align: left;
                }}
                .productos td {{
                    padding: 4px 0;
                }}
                .total {{
                    font-size: 16px;
                    font-weight: bold;
                    border-top: 1px dashed #000;
                    padding-top: 10px;
                    margin-top: 10px;
                }}
                .pago {{
                    font-size: 12px;
                    color: #666;
                }}
                .vuelto {{
                    font-size: 14px;
                    font-weight: bold;
                    color: #2E7D32;
                }}
                .footer {{
                    text-align: center;
                    font-size: 11px;
                    color: #666;
                    border-top: 1px dashed #000;
                    padding-top: 10px;
                    margin-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="negocio">🛒 SISVENIN</div>
                <div class="subtitulo">Minimarket Villa Carrion</div>
            </div>
            
            <div class="fecha">📅 {fecha_actual}</div>
            
            <table class="productos">
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th style="text-align: right;">Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {filas}
                </tbody>
            </table>
            
            <div class="total" style="text-align: right;">
                TOTAL: S/ {total:.2f}
            </div>
            
            <div style="margin-top: 10px;">
                <div class="pago">PAGO CON: S/ {pago:.2f}</div>
                <div class="vuelto">VUELTO: S/ {vuelto:.2f}</div>
            </div>
            
            <div class="footer">
                ¡Gracias por su compra!
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generar_texto_ticket(
        self,
        productos: List[ProductoModelo],
        total: float,
        pago: float,
        vuelto: float
    ) -> str:
        """Genera el ticket en texto plano (fallback)"""
        
        agrupados = {}
        for p in productos:
            if p.id not in agrupados:
                agrupados[p.id] = {"producto": p, "cantidad": 0}
            agrupados[p.id]["cantidad"] += 1
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        lineas = []
        lineas.append("=" * 40)
        lineas.append("🛒 SISVENIN")
        lineas.append("Minimarket Villa Carrion")
        lineas.append("=" * 40)
        lineas.append(f"Fecha: {fecha_actual}")
        lineas.append("=" * 40)
        lineas.append("")
        lineas.append("PRODUCTOS")
        lineas.append("-" * 40)
        
        for data in agrupados.values():
            producto = data["producto"]
            cantidad = data["cantidad"]
            subtotal = producto.precio_venta * cantidad
            lineas.append(f"{producto.nombre} x{cantidad}  S/ {subtotal:.2f}")
        
        lineas.append("-" * 40)
        lineas.append(f"TOTAL: S/ {total:.2f}")
        lineas.append("")
        lineas.append(f"PAGO CON: S/ {pago:.2f}")
        lineas.append(f"VUELTO: S/ {vuelto:.2f}")
        lineas.append("")
        lineas.append("=" * 40)
        lineas.append("¡Gracias por su compra!")
        lineas.append("=" * 40)
        
        return "\n".join(lineas)
    
    def _guardar_como_texto(self, texto: str) -> None:
        """Guarda el ticket como archivo de texto (fallback)"""
        try:
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.txt',
                delete=False,
                encoding='utf-8'
            ) as f:
                f.write(texto)
                print(f"📄 Ticket guardado en: {f.name}")
        except Exception as e:
            print(f"❌ Error al guardar ticket:ññññññññ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,bh  ,mm{e}")