@echo off
title SISVENIN - Configuración del entorno
echo ========================================
echo    SISVENIN - Configuración inicial
echo ========================================
echo.

:: Verificar si Python está instalado
echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo    Descargar desde: https://python.org
    pause
    exit /b 1
)
echo ✅ Python encontrado
python --version
echo.

:: Verificar si Git está instalado (opcional)
echo 🔍 Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Git no está instalado (opcional, solo para clonar)
) else (
    echo ✅ Git encontrado
    git --version
)
echo.

:: Verificar si ya existe el entorno virtual
if exist "venv\" (
    echo ⚠️ El entorno virtual ya existe
    choice /C SN /M "¿Deseas recrearlo? (S/N)"
    if errorlevel 2 (
        echo Usando entorno virtual existente
        goto :activar
    ) else (
        echo Eliminando entorno virtual antiguo...
        rmdir /s /q venv
    )
)
echo.

:: 1. Crear entorno virtual
echo 📦 Paso 1/4: Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo ❌ Error al crear el entorno virtual
    pause
    exit /b 1
)
echo ✅ Entorno virtual creado
echo.

:: 2. Activar entorno virtual
:activar
echo 🔧 Paso 2/4: Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error al activar el entorno virtual
    pause
    exit /b 1
)
echo ✅ Entorno virtual activado
echo.

:: 3. Actualizar pip
echo 🔄 Actualizando pip...
python -m pip install --upgrade pip >nul 2>&1
echo ✅ Pip actualizado
echo.

:: 4. Instalar dependencias
echo 📚 Paso 3/4: Instalando dependencias...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
) else (
    echo ⚠️ No se encontró requirements.txt
    echo    Instalando dependencias básicas...
    pip install PySide6 pytest pytest-cov pytest-qt
)
echo ✅ Dependencias instaladas
echo.

:: 5. Crear estructura de carpetas si no existe
echo 📁 Paso 4/4: Verificando estructura de carpetas...
if not exist "database\" mkdir database
if not exist "docs\" mkdir docs
if not exist "src\app\modules" mkdir src\app\modules
if not exist "tests\" mkdir tests
echo ✅ Estructura verificada
echo.

:: 6. Inicializar base de datos
echo 🗄️ Inicializando base de datos...
python -c "from src.app.modules.producto.producto_repository import ProductoRepository; ProductoRepository.inicializar()" 2>nul
if errorlevel 1 (
    echo ⚠️ No se pudo inicializar la BD (se creará al ejecutar la app)
) else (
    echo ✅ Base de datos inicializada
)
echo.

:: Resumen final
echo ========================================
echo    ✅ CONFIGURACIÓN COMPLETADA ✅
echo ========================================
echo.
echo 📌 Comandos útiles:
echo    run        - Ejecutar la aplicación
echo    newModu    - Crear un nuevo módulo
echo    test       - Ejecutar pruebas
echo.
echo 🚀 Para empezar, ejecuta: run
echo.

pause   