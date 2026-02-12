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

# 2. Verificar/Instalar dependencias críticas
print("\n📦 Verificando dependencias críticas...")
required_packages = [
    'pydantic',
    'python-dateutil',
    'pyxlsb',
    'openpyxl',
    'pandas',
    'matplotlib',
    'reportlab',
    'PyQt6',
    'numpy',
    'Pillow'
]

missing_packages = []
for package in required_packages:
    try:
        __import__(package.replace('-', '_').split('[')[0])
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ⚠️  {package} no encontrado")
        missing_packages.append(package)

if missing_packages:
    print(f"\n📥 Instalando {len(missing_packages)} paquetes faltantes...")
    for package in missing_packages:
        run_command([sys.executable, "-m", "pip", "install", package],
                   f"Instalación de {package}")
    print("✅ Todas las dependencias instaladas")
else:
    print("✅ Todas las dependencias ya están instaladas")

# 3. Limpiar compilaciones anteriores
print("\n🧹 Limpiando archivos anteriores...")
import shutil
for folder in ['build', 'dist']:
    folder_path = project_dir / folder
    if folder_path.exists():
        try:
            shutil.rmtree(folder_path)
            print(f"   Eliminado: {folder}")
        except PermissionError:
            print(f"   ⚠️  No se pudo eliminar {folder} (archivo en uso). Se sobrescribirá.")
        except Exception as e:
            print(f"   ⚠️  Error al eliminar {folder}: {e}")

# 4. Construir ejecutable
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
    
    # Añadir rutas de búsqueda para módulos
    '--paths', str(project_dir / 'GUI'),
    '--paths', str(project_dir / 'TRANSFORMER CELER'),
    '--paths', str(project_dir / 'CONCILIATOR ALLIANZ'),
    
    # Añadir datos necesarios
    '--add-data', f'{project_dir / "GUI" / "widgets"};widgets',
    '--add-data', f'{project_dir / "GUI" / "workers"};workers',
    '--add-data', f'{project_dir / "GUI" / "styles"};styles',
    '--add-data', f'{project_dir / "TRANSFORMER CELER"};TRANSFORMER CELER',
    '--add-data', f'{project_dir / "CONCILIATOR ALLIANZ"};CONCILIATOR ALLIANZ',
    
    # Importaciones ocultas necesarias - GUI
    '--hidden-import', 'PyQt6',
    '--hidden-import', 'PyQt6.QtCore',
    '--hidden-import', 'PyQt6.QtGui',
    '--hidden-import', 'PyQt6.QtWidgets',
    
    # Matplotlib y gráficos
    '--hidden-import', 'matplotlib',
    '--hidden-import', 'matplotlib.backends.backend_qt5agg',
    '--hidden-import', 'matplotlib.backends.backend_agg',
    '--hidden-import', 'matplotlib.figure',
    '--hidden-import', 'matplotlib.pyplot',
    '--hidden-import', 'PIL',
    '--hidden-import', 'PIL.Image',
    '--hidden-import', 'PIL._imaging',
    
    # Pandas y lectores de Excel
    '--hidden-import', 'pandas',
    '--hidden-import', 'pandas._libs',
    '--hidden-import', 'pandas._libs.tslibs',
    '--hidden-import', 'openpyxl',
    '--hidden-import', 'openpyxl.cell',
    '--hidden-import', 'openpyxl.cell._writer',
    '--hidden-import', 'openpyxl.styles',
    '--hidden-import', 'pyxlsb',
    '--hidden-import', 'pyxlsb.recordreader',
    '--hidden-import', 'xlrd',
    
    # Pydantic (requerido por TRANSFORMER CELER)
    '--hidden-import', 'pydantic',
    '--hidden-import', 'pydantic.fields',
    '--hidden-import', 'pydantic.main',
    '--hidden-import', 'pydantic.types',
    '--hidden-import', 'pydantic.validator',
    '--hidden-import', 'pydantic_core',
    
    # ReportLab (para generación de PDFs)
    '--hidden-import', 'reportlab',
    '--hidden-import', 'reportlab.pdfgen',
    '--hidden-import', 'reportlab.lib',
    
    # Python-dateutil
    '--hidden-import', 'dateutil',
    '--hidden-import', 'dateutil.parser',
    '--hidden-import', 'dateutil.tz',
    
    # Librerías estándar con importaciones dinámicas
    '--hidden-import', 'importlib',
    '--hidden-import', 'importlib.util',
    '--hidden-import', 'xml.etree.ElementTree',
    '--hidden-import', 'html',
    '--hidden-import', 're',
    '--hidden-import', 'enum',
    
    # Numpy (usado por pandas y matplotlib)
    '--hidden-import', 'numpy',
    '--hidden-import', 'numpy.core',
    '--hidden-import', 'numpy.core._methods',
    '--hidden-import', 'numpy.lib',
    '--hidden-import', 'numpy.lib.format',
    '--hidden-import', 'numpy._typing',
    
    # Excluir módulos innecesarios para hacer el ejecutable más pequeño
    '--exclude-module', 'torch',
    '--exclude-module', 'torchvision',
    '--exclude-module', 'tensorflow',
    '--exclude-module', 'scipy',
    '--exclude-module', 'IPython',
    '--exclude-module', 'notebook',
    '--exclude-module', 'jupyter',
    '--exclude-module', 'tkinter',
    '--exclude-module', 'pytest',
    '--exclude-module', 'setuptools',
    
    # Directorio de salida
    '--distpath', str(project_dir / 'dist'),
    '--workpath', str(project_dir / 'build'),
    '--specpath', str(project_dir),
    
    # Limpiar antes de construir
    '--clean',
    
    # Nivel de log
    '--log-level', 'INFO',
])

# 5. Verificar resultado
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

