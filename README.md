# SISVENIN - Sistema de Ventas e Inventario para Minimarket Villa Carrion

Sistema de escritorio para gestionar ventas, inventario y cierre de caja de un minimarket.  

Desarrollado bajo la metodología ágil **Extreme Programming (XP)**.

## 👨‍💻 Autores
Fiorela Torres Herrera	        Desarrolladora
Gina Quispe Solano	            Desarrolladora
Lenin Erick Lancho Peña	        Líder del Equipo
Roy Eder Huarhuachi Pillaca	    Desarrollador
Lincoln Stip Soto Lira	        Desarrollador


## 📁 Estructura del proyecto
SISVENIN/
│
├── 📁 database/ # Base de datos SQLite
│ ├── .gitkeep
│ └── sisvenin.db
│
├── 📁 src/ # Código fuente
│ ├── 📁 app/ # Aplicación principal
│ │ ├── 📁 layout/ # Layouts genéricos
│ │ │ └── base_layout.py
│ │ │
│ │ ├── 📁 modules/ # Módulos de la aplicación
│ │ │ │
│ │ │ ├── 📁 producto/ # Módulo Producto
│ │ │ │ ├── 📁 components/
│ │ │ │ ├── producto_controlador.py
│ │ │ │ ├── producto_modelo.py
│ │ │ │ ├── producto_repositorio.py
│ │ │ │ ├── producto_vista.py
│ │ │ │ └── init.py
│ │ │ │
│ │ │ └── 📁 shared/ # Componentes compartidos
│ │ │ ├── 📁 components/
│ │ │ │ ├── boton_primario.py
│ │ │ │ └── input_busqueda.py
│ │ │ └── 📁 utils/
│ │ │ ├── validadores.py
│ │ │ └── init.py
│ │ │
│ │ └── app.py
│ │
│ ├── main.py
│ └── init.py
│
├── 📁 tests/ # Pruebas unitarias
│ ├── 📁 cliente/ # Tests del módulo Cliente
│ │ ├── test_controlador.py
│ │ ├── test_integracion.py
│ │ ├── test_modelo.py
│ │ ├── test_repositorio.py
│ │ └── init.py
│ ├── conftest.py
│
├── .gitignore
├── newModu.bat # Script para crear módulos
├── newModu.py
├── README.md
├── requirements.txt
├── run.bat # Ejecutar la aplicación
├── setup.bat # Configuración inicial
└── test.bat # Ejecutar pruebas


## 🔧 Instalación paso a paso

### 1. Clonar el repositorio

### 2. Crear entorno virtual
Ejecutar setup en consola

### 3. Verificar que todo funciona
test
run


## 🧪 Comandos útiles
Comando	                        ¿Qué hace?
test                        	Ejecuta todas las pruebas
run	                            Inicia el programa
newModu nombre_del_modulo       Crear un nuevo módulo


## 📝 Convenciones de nomenclatura
Tipo de archivo	                Formato	                Ejemplo
Modelo (datos)	                nombre_modelo.py	    producto_modelo.py
Vista (pantalla)	            nombre_vista.py	        producto_vista.py
Controlador (lógica)	        nombre_controlador.py	producto_controlador.py
Repositorio (base de datos)     nombre_repositorio.py   producto_repositorio.py

## Indexar archivos y carpetas
dir /s /b > indice.txt