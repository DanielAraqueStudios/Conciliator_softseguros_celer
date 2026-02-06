# Construcción del Ejecutable

## Método Rápido (Recomendado)

Simplemente ejecuta:
```bash
python build_exe.py
```

El script automáticamente:
- ✅ Verifica/Instala PyInstaller
- ✅ Limpia compilaciones anteriores
- ✅ Construye el ejecutable
- ✅ Muestra el resultado con emojis informativos

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
