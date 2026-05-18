# delModu.py
"""
Script para eliminar un módulo completo de SISVENIN (sin __init__.py)

Uso:
    python delModu.py <nombre_modulo>
    python delModu.py producto

Elimina:
    src/app/models/{nombre}_modelo.py
    src/app/controllers/{nombre}_controlador.py
    src/app/views/{nombre}_vista.py
    tests/test_{nombre}.py
"""

import argparse
import os
from pathlib import Path

# Colores
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Desactivar colores en Windows si hay problemas
try:
    import sys
    if sys.platform == "win32":
        GREEN = YELLOW = RED = BLUE = RESET = ""
except ImportError:
    pass


def eliminar_archivo(ruta):
    """Elimina un archivo si existe"""
    if ruta.exists():
        os.remove(ruta)
        print(f"{GREEN}✓{RESET} Eliminado: {ruta.name}")
        return True
    return False


def eliminar_modulo(nombre_modulo):
    nombre = nombre_modulo.lower().strip()
    
    if not nombre:
        print(f"{RED}❌ Debes especificar un nombre{RESET}")
        return False
    
    base = Path(__file__).parent.absolute()
    
    # Rutas de los archivos
    modelo = base / f"src/app/models/{nombre}_modelo.py"
    controlador = base / f"src/app/controllers/{nombre}_controlador.py"
    vista = base / f"src/app/views/{nombre}_vista.py"
    test = base / f"tests/test_{nombre}.py"
    
    # Verificar si existe al menos un archivo
    if not any([modelo.exists(), controlador.exists(), vista.exists(), test.exists()]):
        print(f"{YELLOW}⚠️ El módulo '{nombre}' no existe{RESET}")
        return False
    
    print(f"\n{RED}🗑️ Eliminando módulo '{nombre}'...{RESET}\n")
    
    # Lista de archivos a eliminar
    archivos = [
        ("Modelo", modelo),
        ("Controlador", controlador),
        ("Vista", vista),
        ("Test", test),
    ]
    
    eliminados = []
    for nombre_archivo, ruta in archivos:
        if eliminar_archivo(ruta):
            eliminados.append(nombre_archivo)
    
    if eliminados:
        print(f"\n{GREEN}✅ Módulo '{nombre}' eliminado exitosamente!{RESET}")
        print(f"\n📁 Archivos eliminados:")
        for archivo in eliminados:
            print(f"   - {archivo}")
    else:
        print(f"{YELLOW}⚠️ No se encontraron archivos del módulo '{nombre}'{RESET}")
    
    return True


def listar_modulos():
    """Lista los módulos existentes"""
    base = Path(__file__).parent.absolute()
    models_dir = base / "src/app/models"
    
    if not models_dir.exists():
        print(f"{YELLOW}⚠️ No hay módulos creados{RESET}")
        return
    
    modulos = []
    for archivo in models_dir.glob("*_modelo.py"):
        nombre = archivo.stem.replace("_modelo", "")
        modulos.append(nombre)
    
    if modulos:
        print(f"\n{BLUE}📦 Módulos existentes:{RESET}")
        for i, mod in enumerate(sorted(modulos), 1):
            print(f"   {i}. {mod}")
    else:
        print(f"{YELLOW}⚠️ No hay módulos creados{RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Elimina un módulo completo de SISVENIN (sin __init__.py)",
        epilog="Ejemplo: python delModu.py producto"
    )
    parser.add_argument("nombre", nargs="?", help="Nombre del módulo a eliminar")
    parser.add_argument("--list", "-l", action="store_true", help="Listar módulos existentes")
    
    args = parser.parse_args()
    
    if args.list:
        listar_modulos()
        return
    
    if not args.nombre:
        print(f"{YELLOW}💡 Uso: python delModu.py <nombre_modulo>{RESET}")
        print(f"   Para listar módulos: python delModu.py --list{RESET}")
        return
    
    # Confirmar eliminación
    print(f"\n{YELLOW}⚠️ ATENCIÓN: Vas a eliminar el módulo '{args.nombre}'{RESET}")
    confirmacion = input(f"¿Estás seguro? (s/N): ")
    
    if confirmacion.lower() != 's':
        print(f"{GREEN}✅ Eliminación cancelada{RESET}")
        return
    
    eliminar_modulo(args.nombre)


if __name__ == "__main__":
    main()