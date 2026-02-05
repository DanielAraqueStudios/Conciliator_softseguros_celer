"""
Script para construir el ejecutable de la aplicación
Requiere: pip install pyinstaller
"""
import subprocess
import sys
from pathlib import Path

def print_header(message):
    """Imprimir encabezado formateado"""
    print("\n" + "="*60)
    print(f"  {message}")
    print("="*60 + "\n")

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}")
        print(e.stderr)
        return False

# Directorio del proyecto
project_dir = Path(__file__).parent

print_header("Construyendo Ejecutable - Conciliador Seguros Unión")

# 1. Verificar/Instalar PyInstaller
print("📦 Verificando PyInstaller...")
try:
    import PyInstaller
    print("✅ PyInstaller ya está instalado")
except ImportError:
    print("⚠️  PyInstaller no encontrado. Instalando...")
    if not run_command([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                      "Instalación de PyInstaller"):
        sys.exit(1)
    import PyInstaller

# 2. Limpiar compilaciones anteriores
print("\n🧹 Limpiando archivos anteriores...")
import shutil
for folder in ['build', 'dist']:
    folder_path = project_dir / folder
    if folder_path.exists():
        shutil.rmtree(folder_path)
        print(f"   Eliminado: {folder}")

# 3. Construir ejecutable
print_header("Iniciando Construcción del Ejecutable")

import PyInstaller.__main__

# Configuración de PyInstaller
PyInstaller.__main__.run([
    # Archivo principal
    str(project_dir / 'GUI' / 'app.py'),
    
    # Nombre del ejecutable
    '--name=Conciliador_Seguros_Union',
    
    # Un solo archivo ejecutable
    '--onefile',
    
    # Ventana (sin consola)
    '--windowed',
    
    # Añadir datos necesarios
    '--add-data', f'{project_dir / "GUI" / "widgets"};widgets',
    '--add-data', f'{project_dir / "GUI" / "workers.py"};.',
    '--add-data', f'{project_dir / "GUI" / "config.py"};.',
    '--add-data', f'{project_dir / "TRANSFORMER CELER"};TRANSFORMER CELER',
    '--add-data', f'{project_dir / "CONCILIATOR ALLIANZ"};CONCILIATOR ALLIANZ',
    '--add-data', f'{project_dir / "main.py"};.',
    
    # Importaciones ocultas necesarias
    '--hidden-import', 'PyQt6',
    '--hidden-import', 'PyQt6.QtCore',
    '--hidden-import', 'PyQt6.QtGui',
    '--hidden-import', 'PyQt6.QtWidgets',
    '--hidden-import', 'matplotlib',
    '--hidden-import', 'matplotlib.backends.backend_qt5agg',
    '--hidden-import', 'pandas',
    '--hidden-import', 'openpyxl',
    '--hidden-import', 'pyxlsb',
    '--hidden-import', 'xlrd',
    '--hidden-import', 'importlib',
    '--hidden-import', 'importlib.util',
    
    # Directorio de salida
    '--distpath', str(project_dir / 'dist'),
    '--workpath', str(project_dir / 'build'),
    '--specpath', str(project_dir),
    
    # Limpiar antes de construir
    '--clean',
    
    # Nivel de log
    '--log-level', 'INFO',
])

# 4. Verificar resultado
exe_path = project_dir / 'dist' / 'Conciliador_Seguros_Union.exe'
if exe_path.exists():
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    
    print_header("✅ Ejecutable Creado Exitosamente")
    print(f"📁 Ubicación: {exe_path}")
    print(f"📊 Tamaño: {size_mb:.2f} MB")
    print("\n💡 Instrucciones:")
    print("   1. Encuentra el archivo en la carpeta 'dist'")
    print("   2. Puedes copiar el .exe a cualquier computadora Windows")
    print("   3. No requiere Python instalado para ejecutarse")
    print("="*60 + "\n")
else:
    print_header("❌ Error: No se pudo crear el ejecutable")
    sys.exit(1)

