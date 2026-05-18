# src/main.py
"""
SISVENIN - Punto de entrada principal
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication
from src.app.app import App


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SISVENIN")
    app.setOrganizationName("Minimarket Villa Carrion")
    
    ventana = App()
    ventana.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()