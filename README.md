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
│ ├── main.py # Punto de entrada
│ │
│ └── 📁 app/ # Aplicación principal
│ ├── app.py # Ventana principal
│ │
│ ├── 📁 models/ # Capa MODELO (datos)
│ │ └── producto_modelo.py
│ │
│ ├── 📁 controllers/ # Capa CONTROLADOR (lógica)
│ │ └── producto_controlador.py
│ │
│ └── 📁 views/ # Capa VISTA (interfaz)
│   └── producto_vista.py
│
├── 📁 tests/ # Pruebas unitarias
│ ├── conftest.py # Configuración de pytest
│ └── test_producto.py
│
├── .gitignore
├── newModu.bat # Crear nuevo módulo
├── newModu.py
├── delModu.bat # Eliminar módulo
├── delModu.py
├── README.md
├── requirements.txt
├── run.bat # Ejecutar aplicación
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
newModu <nombre>	            Crea un nuevo módulo (modelo, controlador, vista, tests)
delModu --list	                Lista los módulos existentes
delModu <nombre>	            Elimina un módulo completo


## 📝 Convenciones de nomenclatura
Tipo de archivo	        Formato	                    Ejemplo
Modelo (datos)	        nombre_modelo.py	        producto_modelo.py
Controlador (lógica)	nombre_controlador.py	    producto_controlador.py
Vista (pantalla)	    nombre_vista.py	            producto_vista.py
Pruebas	                test_nombre.py	            test_producto.py

## Indexar archivos y carpetas
git ls-files --cached --others --exclude-standard > indice.txt