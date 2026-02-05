@echo off
echo ============================================================
echo    Construyendo ejecutable de Conciliador Seguros Union
echo ============================================================
echo.

REM Activar el entorno virtual
call .venv\Scripts\activate.bat

REM Instalar PyInstaller si no está instalado
pip install pyinstaller

REM Ejecutar el script de construcción
python build_exe.py

echo.
echo ============================================================
echo    Proceso completado
echo ============================================================
pause
