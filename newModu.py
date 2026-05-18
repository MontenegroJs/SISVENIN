# newModu.py
"""
Script para crear un nuevo módulo en SISVENIN (sin __init__.py innecesarios)

Uso:
    python newModu.py <nombre_modulo>

Ejemplo:
    python newModu.py cliente

Estructura creada (sin __init__.py):
    src/app/models/{nombre}_modelo.py
    src/app/controllers/{nombre}_controlador.py
    src/app/views/{nombre}_vista.py
    tests/test_{nombre}.py
"""

import argparse
from pathlib import Path

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# Desactivar colores en Windows si hay problemas
try:
    import sys
    if sys.platform == "win32":
        GREEN = YELLOW = RED = RESET = ""
except ImportError:
    pass


def crear_archivo(ruta, contenido):
    """Crea un archivo con el contenido dado"""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f"{GREEN}✓{RESET} {ruta.name}")


def crear_modulo(nombre_modulo):
    nombre = nombre_modulo.lower().strip()
    
    if not nombre:
        print(f"{RED}❌ Debes especificar un nombre{RESET}")
        return False
    
    base = Path(__file__).parent.absolute()
    
    # Archivos a crear
    modelo = base / f"src/app/models/{nombre}_modelo.py"
    controlador = base / f"src/app/controllers/{nombre}_controlador.py"
    vista = base / f"src/app/views/{nombre}_vista.py"
    test = base / f"tests/test_{nombre}.py"
    
    # Verificar si ya existen
    if modelo.exists():
        print(f"{YELLOW}⚠️ El módulo '{nombre}' ya existe{RESET}")
        return False
    
    print(f"\n{YELLOW}📦 Creando módulo '{nombre}'...{RESET}\n")
    
    # Contenido del modelo
    modelo_contenido = f'''"""
Modelo del módulo {nombre.capitalize()}
"""
class {nombre.capitalize()}Modelo:
    def __init__(self, id=None, nombre="", descripcion=""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.activo = True

    def __str__(self):
        return f"{{self.nombre}} (ID: {{self.id}})"
'''
    
    # Contenido del controlador
    controlador_contenido = f'''"""
Controlador del módulo {nombre.capitalize()}
"""
from src.app.models.{nombre}_modelo import {nombre.capitalize()}Modelo


class {nombre.capitalize()}Controlador:
    
    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        return True

    @staticmethod
    def listar_ejemplo():
        return [
            {nombre.capitalize()}Modelo(id=1, nombre=f"{nombre.capitalize()} 1", descripcion="Descripción 1"),
            {nombre.capitalize()}Modelo(id=2, nombre=f"{nombre.capitalize()} 2", descripcion="Descripción 2"),
        ]
'''
    
    # Contenido de la vista
    vista_contenido = f'''"""
Módulo {nombre.capitalize()} - Vista
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from src.app.controllers.{nombre}_controlador import {nombre.capitalize()}Controlador


class {nombre.capitalize()}Vista(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        titulo = QLabel(f"📦 Gestión de {nombre.capitalize()}s")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titulo)
        
        self.btn = QPushButton("🔄 Refrescar")
        self.btn.clicked.connect(self.cargar_datos)
        layout.addWidget(self.btn)
        
        self.label = QLabel("")
        layout.addWidget(self.label)
    
    def cargar_datos(self):
        datos = {nombre.capitalize()}Controlador.listar_ejemplo()
        self.label.setText(f"Cargados {{len(datos)}} {nombre}s")
'''
    
    # Contenido del test
    test_contenido = f'''"""
Pruebas para el módulo {nombre.capitalize()}
"""
import unittest
from src.app.models.{nombre}_modelo import {nombre.capitalize()}Modelo
from src.app.controllers.{nombre}_controlador import {nombre.capitalize()}Controlador


class Test{nombre.capitalize()}Modelo(unittest.TestCase):
    def test_crear(self):
        obj = {nombre.capitalize()}Modelo(id=1, nombre="Test")
        self.assertEqual(obj.nombre, "Test")


if __name__ == "__main__":
    unittest.main()
'''
    
    # Crear archivos (sin __init__.py)
    crear_archivo(modelo, modelo_contenido)
    crear_archivo(controlador, controlador_contenido)
    crear_archivo(vista, vista_contenido)
    crear_archivo(test, test_contenido)
    
    print(f"\n{GREEN}✅ Módulo '{nombre}' creado exitosamente!{RESET}")
    print(f"\n📁 Archivos creados (sin __init__.py):")
    print(f"   src/app/models/{nombre}_modelo.py")
    print(f"   src/app/controllers/{nombre}_controlador.py")
    print(f"   src/app/views/{nombre}_vista.py")
    print(f"   tests/test_{nombre}.py")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Crea un nuevo módulo en SISVENIN (sin __init__.py innecesarios)",
        epilog="Ejemplo: python newModu.py cliente"
    )
    parser.add_argument("nombre", help="Nombre del módulo (ej: cliente, proveedor)")
    args = parser.parse_args()
    crear_modulo(args.nombre)


if __name__ == "__main__":
    main()