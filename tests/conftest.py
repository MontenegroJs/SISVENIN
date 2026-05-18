# tests/conftest.py
import sys
import os

# Agregar la carpeta RAIZ del proyecto al path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

# Agregar también la carpeta src directamente
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

# Opcional: imprimir para verificar
print(f"✅ PYTHONPATH configurado: {PROJECT_ROOT}")