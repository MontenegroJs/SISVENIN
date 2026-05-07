# nuevo_modulo.py
"""
Script para crear automáticamente un nuevo módulo en SISVENIN

Uso:
    python nuevo_modulo.py <nombre_modulo>

Ejemplo:
    python nuevo_modulo.py cliente
    python nuevo_modulo.py proveedor

Estructura creada:
    src/app/modules/<nombre_modulo>/
        ├── components/
        ├── <nombre_modulo>_vista.py
        ├── <nombre_modulo>_controller.py
        ├── <nombre_modulo>_modelo.py
        ├── <nombre_modulo>_repository.py
        └── __init__.py

    tests/<nombre_modulo>/
        ├── test_modelo.py
        ├── test_controller.py
        ├── test_repository.py
        └── test_integracion.py
"""

import os
import sys
import argparse
from pathlib import Path

# Colores para la consola
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# Desactivar colores en Windows si hay problemas
if sys.platform == "win32":
    GREEN = YELLOW = RED = RESET = ""


def crear_carpeta(ruta):
    """Crea una carpeta si no existe"""
    os.makedirs(ruta, exist_ok=True)
    print(f"{GREEN}✓{RESET} Carpeta: {ruta}")


def crear_archivo(ruta, contenido):
    """Crea un archivo con el contenido dado"""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f"{GREEN}✓{RESET} Archivo: {ruta}")


def get_contenido_init(modulo):
    """Contenido para __init__.py del módulo"""
    class_name = modulo.capitalize()
    return f'''"""
Módulo {class_name}
Exporta las clases principales
"""
from .{modulo}_modelo import {class_name}
from .{modulo}_controller import {class_name}Controller
from .{modulo}_repository import {class_name}Repository
from .{modulo}_vista import {class_name}Vista

__all__ = [
    '{class_name}',
    '{class_name}Controller',
    '{class_name}Repository',
    '{class_name}Vista',
]
'''


def get_contenido_modelo(modulo):
    """Contenido para el archivo modelo"""
    class_name = modulo.capitalize()
    return f'''"""
Modelo del módulo {class_name}
"""
class {class_name}:
    def __init__(self, id=None, nombre="", descripcion=""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.activo = True

    def __str__(self):
        return f"{{self.nombre}} (ID: {{self.id}})"

    def to_dict(self):
        return {{
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "activo": self.activo,
        }}
'''


def get_contenido_controller(modulo):
    """Contenido para el archivo controller"""
    class_name = modulo.capitalize()
    return f'''"""
Controlador del módulo {class_name}
"""
from .{modulo}_modelo import {class_name}


class {class_name}Controller:
    
    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        return True

    @staticmethod
    def listar_ejemplo():
        """Retorna lista de ejemplo para pruebas"""
        return [
            {class_name}(id=1, nombre=f"{class_name} 1", descripcion="Descripción 1"),
            {class_name}(id=2, nombre=f"{class_name} 2", descripcion="Descripción 2"),
            {class_name}(id=3, nombre=f"{class_name} 3", descripcion="Descripción 3"),
        ]
'''


def get_contenido_repository(modulo):
    """Contenido para el archivo repository"""
    class_name = modulo.capitalize()
    return f'''"""
Repository del módulo {class_name} (Acceso a datos)
"""
import sqlite3
import os
from .{modulo}_modelo import {class_name}


class {class_name}Repository:
    # Ruta a la base de datos
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'database', 'sisvenin.db')
    DB_PATH = os.path.abspath(DB_PATH)

    @classmethod
    def _get_connection(cls):
        \"\"\"Obtiene conexión a la base de datos\"\"\"
        os.makedirs(os.path.dirname(cls.DB_PATH), exist_ok=True)
        return sqlite3.connect(cls.DB_PATH)

    @classmethod
    def inicializar(cls):
        \"\"\"Inicializa la base de datos\"\"\"
        cls.crear_tabla()

    @classmethod
    def crear_tabla(cls):
        \"\"\"Crea la tabla si no existe\"\"\"
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {modulo}s (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                activo INTEGER DEFAULT 1
            )
        """)
        conn.commit()
        conn.close()
        print(f"✓ Tabla '{modulo}s' creada/verificada")

    @classmethod
    def guardar(cls, obj):
        \"\"\"Guarda un objeto en la base de datos\"\"\"
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {modulo}s (nombre, descripcion, activo) VALUES (?, ?, ?)",
            (obj.nombre, obj.descripcion, 1 if obj.activo else 0)
        )
        conn.commit()
        obj.id = cursor.lastrowid
        conn.close()
        return obj

    @classmethod
    def obtener_todos(cls):
        \"\"\"Obtiene todos los objetos\"\"\"
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, nombre, descripcion, activo FROM {modulo}s WHERE activo = 1")
        rows = cursor.fetchall()
        conn.close()
        
        objetos = []
        for row in rows:
            obj = {class_name}(id=row[0], nombre=row[1], descripcion=row[2])
            obj.activo = bool(row[3])
            objetos.append(obj)
        return objetos

    @classmethod
    def obtener_por_id(cls, obj_id):
        \"\"\"Obtiene un objeto por su ID\"\"\"
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, nombre, descripcion, activo FROM {modulo}s WHERE id = ?", (obj_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            obj = {class_name}(id=row[0], nombre=row[1], descripcion=row[2])
            obj.activo = bool(row[3])
            return obj
        return None

    @classmethod
    def actualizar(cls, obj):
        \"\"\"Actualiza un objeto existente\"\"\"
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE {modulo}s SET nombre = ?, descripcion = ?, activo = ? WHERE id = ?",
            (obj.nombre, obj.descripcion, 1 if obj.activo else 0, obj.id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def eliminar(cls, obj_id):
        \"\"\"Elimina un objeto (borrado lógico)\"\"\"
        conn = cls._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {modulo}s SET activo = 0 WHERE id = ?", (obj_id,))
        conn.commit()
        conn.close()
'''


def get_contenido_vista(modulo):
    """Contenido para el archivo vista"""
    class_name = modulo.capitalize()
    return f'''"""
Módulo {class_name} - Vista
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QTableWidget,
                               QTableWidgetItem, QMessageBox, QHeaderView)
from .{modulo}_controller import {class_name}Controller


class {class_name}Vista(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Título
        titulo = QLabel(f"📦 Gestión de {class_name}s")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(titulo)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción"])
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.tabla)

        # Botones
        botones_layout = QHBoxLayout()
        
        btn_refrescar = QPushButton("🔄 Refrescar")
        btn_refrescar.clicked.connect(self.refrescar)
        botones_layout.addWidget(btn_refrescar)
        
        btn_nuevo = QPushButton("➕ Nuevo")
        btn_nuevo.clicked.connect(self.nuevo)
        botones_layout.addWidget(btn_nuevo)
        
        botones_layout.addStretch()
        layout.addLayout(botones_layout)

        # Cargar datos
        self.refrescar()

    def refrescar(self):
        \"\"\"Carga los datos en la tabla\"\"\"
        try:
            datos = {class_name}Controller.listar_ejemplo()
            self.tabla.setRowCount(len(datos))
            for i, item in enumerate(datos):
                self.tabla.setItem(i, 0, QTableWidgetItem(str(item.id)))
                self.tabla.setItem(i, 1, QTableWidgetItem(item.nombre))
                self.tabla.setItem(i, 2, QTableWidgetItem(item.descripcion))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron cargar los datos: {{e}}")

    def nuevo(self):
        \"\"\"Abre diálogo para crear nuevo\"\"\"
        QMessageBox.information(self, "Nuevo", "Funcionalidad en desarrollo")
'''


def get_contenido_componentes_init():
    """Contenido para components/__init__.py"""
    return '# Componentes específicos del módulo\n'


def get_contenido_test_modelo(modulo):
    """Contenido para test del modelo"""
    class_name = modulo.capitalize()
    return f'''"""
Pruebas unitarias para el modelo {class_name}
"""
import unittest
from src.app.modules.{modulo}.{modulo}_modelo import {class_name}


class Test{class_name}Modelo(unittest.TestCase):

    def test_crear_{modulo}(self):
        obj = {class_name}(id=1, nombre="Test", descripcion="Descripción")
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.nombre, "Test")
        self.assertEqual(obj.descripcion, "Descripción")

    def test_to_dict(self):
        obj = {class_name}(id=1, nombre="Test", descripcion="Desc")
        dic = obj.to_dict()
        self.assertEqual(dic["id"], 1)
        self.assertEqual(dic["nombre"], "Test")
        self.assertEqual(dic["descripcion"], "Desc")

    def test_str_representacion(self):
        obj = {class_name}(id=1, nombre="Test")
        self.assertIn("Test", str(obj))


if __name__ == "__main__":
    unittest.main()
'''


def get_contenido_test_controller(modulo):
    """Contenido para test del controller"""
    class_name = modulo.capitalize()
    return f'''"""
Pruebas unitarias para el controlador de {class_name}
"""
import unittest
from src.app.modules.{modulo}.{modulo}_controller import {class_name}Controller


class Test{class_name}Controller(unittest.TestCase):

    def test_validar_nombre_correcto(self):
        resultado = {class_name}Controller.validar_nombre("Válido")
        self.assertTrue(resultado)

    def test_validar_nombre_vacio(self):
        with self.assertRaises(ValueError):
            {class_name}Controller.validar_nombre("")

    def test_validar_nombre_espacios(self):
        with self.assertRaises(ValueError):
            {class_name}Controller.validar_nombre("   ")

    def test_listar_ejemplo(self):
        lista = {class_name}Controller.listar_ejemplo()
        self.assertGreater(len(lista), 0)
        self.assertTrue(hasattr(lista[0], 'id'))
        self.assertTrue(hasattr(lista[0], 'nombre'))


if __name__ == "__main__":
    unittest.main()
'''


def get_contenido_test_repository(modulo):
    """Contenido para test del repository"""
    class_name = modulo.capitalize()
    return f'''"""
Pruebas para el repositorio de {class_name}
"""
import pytest
import tempfile
import os


@pytest.fixture
def temp_db_{modulo}():
    \"\"\"Crea una base de datos temporal para pruebas\"\"\"
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)


def test_repository_con_temp_db(temp_db_{modulo}):
    \"\"\"Prueba básica del repositorio con BD temporal\"\"\"
    from src.app.modules.{modulo}.{modulo}_repository import {class_name}Repository
    from src.app.modules.{modulo}.{modulo}_modelo import {class_name}
    
    # Guardar ruta original
    original_path = {class_name}Repository.DB_PATH
    
    try:
        # Usar BD temporal
        {class_name}Repository.DB_PATH = temp_db_{modulo}
        {class_name}Repository.crear_tabla()
        
        # Guardar
        obj = {class_name}(nombre="Test Repository", descripcion="Probando")
        {class_name}Repository.guardar(obj)
        
        assert obj.id is not None
        assert obj.id > 0
        
        # Recuperar
        todos = {class_name}Repository.obtener_todos()
        assert len(todos) >= 1
        assert todos[0].nombre == "Test Repository"
        
    finally:
        # Restaurar ruta original
        {class_name}Repository.DB_PATH = original_path
'''


def get_contenido_test_integracion(modulo):
    """Contenido para test de integración"""
    class_name = modulo.capitalize()
    return f'''"""
Pruebas de integración para el módulo {class_name}
"""
import pytest
from src.app.modules.{modulo}.{modulo}_modelo import {class_name}
from src.app.modules.{modulo}.{modulo}_controller import {class_name}Controller


def test_crear_y_validar():
    \"\"\"Prueba integración entre modelo y controlador\"\"\"
    nombre = "Producto Integración"
    
    # Validar
    assert {class_name}Controller.validar_nombre(nombre) is True
    
    # Crear
    obj = {class_name}(nombre=nombre, descripcion="Test")
    assert obj.nombre == nombre
'''


def crear_modulo(nombre_modulo):
    """Función principal para crear el módulo"""
    nombre = nombre_modulo.lower().strip()
    
    if not nombre:
        print(f"{RED}❌ Error: Debes especificar un nombre para el módulo{RESET}")
        return False
    
    # Obtener la raíz del proyecto
    script_dir = Path(__file__).parent.absolute()
    base_path = script_dir / "src" / "app" / "modules" / nombre
    tests_path = script_dir / "tests" / nombre
    
    # Verificar si ya existe
    if base_path.exists():
        print(f"{YELLOW}⚠️ El módulo '{nombre}' ya existe en {base_path}{RESET}")
        return False
    
    print(f"\n{YELLOW}📦 Creando módulo '{nombre}'...{RESET}\n")
    
    try:
        # 1. Crear estructura de carpetas del módulo
        crear_carpeta(base_path)
        crear_carpeta(base_path / "components")
        
        # 2. Crear archivos del módulo
        crear_archivo(base_path / "__init__.py", get_contenido_init(nombre))
        crear_archivo(base_path / f"{nombre}_modelo.py", get_contenido_modelo(nombre))
        crear_archivo(base_path / f"{nombre}_controller.py", get_contenido_controller(nombre))
        crear_archivo(base_path / f"{nombre}_repository.py", get_contenido_repository(nombre))
        crear_archivo(base_path / f"{nombre}_vista.py", get_contenido_vista(nombre))
        crear_archivo(base_path / "components" / "__init__.py", get_contenido_componentes_init())
        
        # 3. Crear estructura de carpetas de tests para el módulo
        crear_carpeta(tests_path)
        
        # 4. Crear archivos de tests dentro de la carpeta del módulo
        crear_archivo(tests_path / "test_modelo.py", get_contenido_test_modelo(nombre))
        crear_archivo(tests_path / "test_controller.py", get_contenido_test_controller(nombre))
        crear_archivo(tests_path / "test_repository.py", get_contenido_test_repository(nombre))
        crear_archivo(tests_path / "test_integracion.py", get_contenido_test_integracion(nombre))
        
        # 5. Crear __init__.py en la carpeta de tests (para que sea un paquete)
        init_contenido = f'''"""
Tests para el módulo {nombre.capitalize()}
"""
'''
        crear_archivo(tests_path / "__init__.py", init_contenido)
        
        print(f"\n{GREEN}✅ Módulo '{nombre}' creado exitosamente!{RESET}")
        print(f"\n{YELLOW}📁 Estructura creada:{RESET}")
        print(f"   📂 src/app/modules/{nombre}/")
        print(f"   📂 tests/{nombre}/")
        print(f"\n{YELLOW}📝 Próximos pasos:{RESET}")
        print(f"   1. Revisa los archivos creados")
        print(f"   2. Ejecuta los tests: pytest tests/{nombre}/ -v")
        print(f"   3. Registra el módulo en src/app/app.py:")
        print(f"")
        print(f"      from src.app.modules.{nombre}.{nombre}_vista import {nombre.capitalize()}Vista")
        print(f"")
        print(f"      # En __init__ de App:")
        print(f"      self.modulo_{nombre} = {nombre.capitalize()}Vista()")
        print(f"      self.registrar_modulo('{nombre}', self.modulo_{nombre})")
        
        return True
        
    except Exception as e:
        print(f"{RED}❌ Error al crear el módulo: {e}{RESET}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Crea un nuevo módulo en SISVENIN con su estructura de tests",
        epilog="Ejemplo: python nuevo_modulo.py cliente"
    )
    parser.add_argument("nombre", help="Nombre del módulo (ej: cliente, proveedor, categoria)")
    args = parser.parse_args()
    
    crear_modulo(args.nombre)


if __name__ == "__main__":
    main()