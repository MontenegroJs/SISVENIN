# src/main.py
"""
SISVENIN - Punto de entrada principal
"""
import sys
import os

# Agregar la carpeta src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication, QMessageBox
from src.app.app import App
from src.app.modules.producto.producto_repositorio import ProductoRepositorio


def main():
    """Función principal que inicia la aplicación"""
    
    try:
        # Inicializar base de datos
        print("🔄 Inicializando base de datos...")
        ProductoRepositorio.inicializar()
        print("✅ Base de datos lista")
        
        # Crear aplicación Qt
        app = QApplication(sys.argv)
        app.setApplicationName("SISVENIN")
        app.setOrganizationName("Minimarket Villa Carrion")
        
        # Mostrar ventana principal
        ventana = App()
        ventana.show()
        
        # Ejecutar
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Error al iniciar: {e}")
        # Si hay error crítico, mostrar mensaje
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "Error", f"No se pudo iniciar SISVENIN:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()