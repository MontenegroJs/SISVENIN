@echo off
title SISVENIN - Eliminador de Módulos
cd /d "%~dp0"

:: Activar entorno virtual
call venv\Scripts\activate

:: Verificar si se pasó un argumento
if "%1"=="" (
    echo ========================================
    echo    SISVENIN - Eliminador de Módulos
    echo ========================================
    echo.
    echo Uso: delModu ^<nombre_modulo^>
    echo.
    echo Ejemplos:
    echo   delModu cliente
    echo   delModu producto
    echo.
    echo Para listar módulos:
    echo   delModu --list
    echo.
    pause
    exit /b 1
)

:: Ejecutar el script
python delModu.py %1 %2

:: Pausar para ver el resultado
echo.
pause