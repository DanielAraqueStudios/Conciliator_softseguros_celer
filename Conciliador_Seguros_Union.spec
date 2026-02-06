# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\GUI\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\GUI\\widgets', 'widgets'), ('C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\GUI\\workers', 'workers'), ('C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\GUI\\styles', 'styles'), ('C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\TRANSFORMER CELER', 'TRANSFORMER CELER'), ('C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\CONCILIATOR ALLIANZ', 'CONCILIATOR ALLIANZ')],
    hiddenimports=['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'matplotlib', 'matplotlib.backends.backend_qt5agg', 'PIL', 'PIL.Image', 'pandas', 'openpyxl', 'pyxlsb', 'xlrd', 'importlib', 'importlib.util'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'torchvision', 'tensorflow', 'scipy', 'IPython', 'notebook', 'jupyter', 'tkinter', 'pytest', 'setuptools'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Conciliador_Seguros_Union',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
