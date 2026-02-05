# Construcción del Ejecutable

## Opción 1: Usando el script .bat (Recomendado)

Simplemente haz doble clic en:
```
build_exe.bat
```

## Opción 2: Manual

1. Activar el entorno virtual:
```bash
.venv\Scripts\activate
```

2. Instalar PyInstaller:
```bash
pip install pyinstaller
```

3. Ejecutar el script de construcción:
```bash
python build_exe.py
```

## Resultado

El ejecutable se generará en:
```
dist/Conciliador_Seguros_Union.exe
```

## Características del Ejecutable

- ✅ Un solo archivo .exe (portable)
- ✅ Sin consola (solo ventana GUI)
- ✅ Incluye todas las dependencias
- ✅ Tamaño aproximado: 100-150 MB

## Distribución

Para distribuir la aplicación:
1. Copia el archivo `Conciliador_Seguros_Union.exe` de la carpeta `dist`
2. Envíalo a los usuarios finales
3. Los usuarios pueden ejecutarlo directamente sin instalar Python

## Notas

- La primera ejecución puede tardar unos segundos en iniciar
- El ejecutable incluye Python, PyQt6, Pandas y todas las librerías necesarias
- No requiere instalación, es completamente portable
