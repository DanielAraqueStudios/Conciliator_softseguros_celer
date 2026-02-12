# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\GUI\\app.py'],
    pathex=['C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\GUI', 'C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\TRANSFORMER CELER', 'C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\CONCILIATOR ALLIANZ'],
    binaries=[],
    datas=[('C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\GUI\\widgets', 'widgets'), ('C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\GUI\\workers', 'workers'), ('C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\GUI\\styles', 'styles'), ('C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\TRANSFORMER CELER', 'TRANSFORMER CELER'), ('C:\\Users\\danie\\Documents\\EMPRESA\\SEGUROS UNIÓN\\AUTOMATIZACIONES\\Conciliator_softseguros_celer\\CONCILIATOR ALLIANZ', 'CONCILIATOR ALLIANZ')],
    hiddenimports=['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'matplotlib', 'matplotlib.backends.backend_qt5agg', 'matplotlib.backends.backend_agg', 'matplotlib.figure', 'matplotlib.pyplot', 'PIL', 'PIL.Image', 'PIL._imaging', 'pandas', 'pandas._libs', 'pandas._libs.tslibs', 'openpyxl', 'openpyxl.cell', 'openpyxl.cell._writer', 'openpyxl.styles', 'pyxlsb', 'pyxlsb.recordreader', 'xlrd', 'pydantic', 'pydantic.fields', 'pydantic.main', 'pydantic.types', 'pydantic.validator', 'pydantic_core', 'reportlab', 'reportlab.pdfgen', 'reportlab.lib', 'dateutil', 'dateutil.parser', 'dateutil.tz', 'importlib', 'importlib.util', 'xml.etree.ElementTree', 'html', 're', 'enum', 'numpy', 'numpy.core', 'numpy.core._methods', 'numpy.lib', 'numpy.lib.format', 'numpy._typing'],
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
