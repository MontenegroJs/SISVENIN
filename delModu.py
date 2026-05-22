# delModu.py
"""
Script para eliminar un módulo completo de SISVENIN

Uso:
    python delModu.py <nombre_modulo>
    python delModu.py producto

Elimina:
    src/app/models/{nombre}_modelo.py
    src/app/controllers/{nombre}_controlador.py
    src/app/views/{nombre}_vista.py
    tests/{nombre}/ (carpeta completa con todos los tests)
"""

import argparse
import os
import shutil
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


def eliminar_carpeta(ruta):
    """Elimina una carpeta completa si existe"""
    if ruta.exists() and ruta.is_dir():
        shutil.rmtree(ruta)
        print(f"{GREEN}✓{RESET} Eliminada carpeta: {ruta.name}/")
        return True
    return False


def eliminar_modulo(nombre_modulo):
    nombre = nombre_modulo.lower().strip()
    
    if not nombre:
        print(f"{RED}❌ Debes especificar un nombre{RESET}")
        return False
    
    base = Path(__file__).parent.absolute()
    
    # Rutas de los archivos del módulo
    modelo = base / f"src/app/models/{nombre}_modelo.py"
    controlador = base / f"src/app/controllers/{nombre}_controlador.py"
    vista = base / f"src/app/views/{nombre}_vista.py"
    
    # Carpeta de tests del módulo
    tests_dir = base / f"tests/{nombre}"
    
    # Verificar si existe al menos un archivo o la carpeta de tests
    if not any([modelo.exists(), controlador.exists(), vista.exists(), tests_dir.exists()]):
        print(f"{YELLOW}⚠️ El módulo '{nombre}' no existe{RESET}")
        return False
    
    print(f"\n{RED}🗑️ Eliminando módulo '{nombre}'...{RESET}\n")
    
    # Lista de archivos a eliminar
    archivos = [
        ("Modelo", modelo),
        ("Controlador", controlador),
        ("Vista", vista),
    ]
    
    eliminados = []
    for nombre_archivo, ruta in archivos:
        if eliminar_archivo(ruta):
            eliminados.append(nombre_archivo)
    
    # Eliminar carpeta de tests
    if eliminar_carpeta(tests_dir):
        eliminados.append("Carpeta de tests")
    
    if eliminados:
        print(f"\n{GREEN}✅ Módulo '{nombre}' eliminado exitosamente!{RESET}")
        print(f"\n📁 Elementos eliminados:")
        for elemento in eliminados:
            print(f"   - {elemento}")
    else:
        print(f"{YELLOW}⚠️ No se encontraron archivos del módulo '{nombre}'{RESET}")
    
    return True


def listar_modulos():
    """Lista los módulos existentes (basado en modelos y carpetas de tests)"""
    base = Path(__file__).parent.absolute()
    models_dir = base / "src/app/models"
    tests_dir = base / "tests"
    
    modulos = set()
    
    # Buscar por archivos de modelo
    if models_dir.exists():
        for archivo in models_dir.glob("*_modelo.py"):
            nombre = archivo.stem.replace("_modelo", "")
            modulos.add(nombre)
    
    # Buscar por carpetas de tests
    if tests_dir.exists():
        for carpeta in tests_dir.iterdir():
            if carpeta.is_dir() and not carpeta.name.startswith("__"):
                modulos.add(carpeta.name)
    
    if modulos:
        print(f"\n{BLUE}📦 Módulos existentes:{RESET}")
        for i, mod in enumerate(sorted(modulos), 1):
            print(f"   {i}. {mod}")
    else:
        print(f"{YELLOW}⚠️ No hay módulos creados{RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Elimina un módulo completo de SISVENIN",
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
    print(f"   Se eliminarán:")
    print(f"   - src/app/models/{args.nombre}_modelo.py")
    print(f"   - src/app/controllers/{args.nombre}_controlador.py")
    print(f"   - src/app/views/{args.nombre}_vista.py")
    print(f"   - tests/{args.nombre}/ (carpeta completa)")
    
    confirmacion = input(f"\n¿Estás seguro? (s/N): ")
    
    if confirmacion.lower() != 's':
        print(f"{GREEN}✅ Eliminación cancelada{RESET}")
        return
    
    eliminar_modulo(args.nombre)


if __name__ == "__main__":
    main()