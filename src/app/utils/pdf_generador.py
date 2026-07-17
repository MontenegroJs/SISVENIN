import os
from pathlib import Path
from typing import Optional


def guardar_html_reporte(html: str, ruta_salida: Optional[str] = None) -> str:
    ruta_salida = ruta_salida or "reporte_del_dia.html"
    ruta = Path(ruta_salida)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with ruta.open("w", encoding="utf-8") as archivo:
        archivo.write(html)

    return str(ruta.resolve())


def guardar_texto_como_pdf(texto: str, ruta_salida: Optional[str] = None) -> str:
    """
    Genera un PDF simple desde texto plano.
    Si no se dispone de una librería de PDF, guarda el texto en un archivo .txt
    renombrado a .pdf como fallback.
    """
    if ruta_salida is None:
        ruta_salida = "reporte_del_dia.pdf"

    ruta = Path(ruta_salida)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(str(ruta), pagesize=letter)
        width, height = letter

        y = height - 40
        for linea in texto.split("\n"):
            c.drawString(40, y, linea)
            y -= 14
            if y < 40:
                c.showPage()
                y = height - 40

        c.save()
        return str(ruta.resolve())
    except ImportError:
        fallback = ruta.with_suffix(".txt")
        with fallback.open("w", encoding="utf-8") as archivo:
            archivo.write(texto)
        return str(fallback.resolve())
