# Sistema de Conciliación - GUI

Interfaz gráfica moderna para los sistemas **TRANSFORMER CELER** y **CONCILIATOR ALLIANZ**.

## 🎨 Características

- **Interfaz moderna** con tema oscuro
- **Tres pestañas principales**:
  - 🔄 **Transformador Celer**: Transforma archivos Celer al formato requerido
  - 🔍 **Conciliador Allianz**: Concilia datos de Softseguros, Celer y Allianz
  - 📊 **Dashboard**: Métricas y visualizaciones en tiempo real

- **Drag & Drop**: Arrastra y suelta archivos para cargarlos
- **Procesamiento asíncrono**: No bloquea la interfaz durante operaciones largas
- **Reportes automáticos**: Generación de reportes TXT y visualizaciones
- **Métricas en tiempo real**: Dashboard con gráficos interactivos

## 📦 Instalación

### Requisitos
- Python 3.8 o superior
- PyQt6
- matplotlib
- pandas
- openpyxl
- pyxlsb

### Instalar dependencias

```bash
cd GUI
pip install -r requirements.txt
```

## 🚀 Uso

### Ejecutar la aplicación

```bash
cd GUI
python app.py
```

### Pestaña Transformador Celer

1. Arrastra y suelta un archivo Celer (.xlsb o .xlsx)
2. Haz clic en "🚀 Procesar Archivo"
3. Espera a que se complete la transformación
4. El archivo transformado se guardará automáticamente

### Pestaña Conciliador Allianz

1. Carga los tres archivos requeridos:
   - Archivo Softseguros (.xlsx o .xlsb)
   - Archivo Celer (.xlsx o .xlsb)
   - Archivo Allianz (.xml)
2. Selecciona las opciones de exportación
3. Haz clic en "🔍 Iniciar Conciliación"
4. Revisa los resultados en el área de texto
5. Los reportes se guardarán en la carpeta `output/`

### Dashboard

- Visualiza métricas generales:
  - Total de registros procesados
  - Número de coincidencias
  - Registros pendientes
  - Tasa de coincidencia
- Gráficos de distribución:
  - Distribución por casos
  - Distribución de montos
- Actualiza los datos con el botón "🔄 Actualizar Datos"

## 🎨 Tema Oscuro

La aplicación utiliza una paleta de colores oscura personalizada:

- **Background**: #1e1e2e
- **Surface**: #2a2a3e
- **Accent**: #3b82f6 (azul)
- **Success**: #10b981 (verde)
- **Warning**: #f59e0b (amarillo)
- **Error**: #ef4444 (rojo)
- **Text**: #e5e7eb

## 📁 Estructura del Proyecto

```
GUI/
├── app.py                      # Punto de entrada
├── main_window.py              # Ventana principal
├── requirements.txt            # Dependencias
├── styles/
│   └── dark_theme.py          # Tema oscuro
├── widgets/
│   ├── __init__.py
│   ├── file_drop_widget.py    # Widget de drag & drop
│   ├── transformer_tab.py     # Pestaña transformador
│   ├── conciliator_tab.py     # Pestaña conciliador
│   └── dashboard_tab.py       # Pestaña dashboard
└── workers/
    ├── __init__.py
    └── background_workers.py  # Hilos de procesamiento
```

## 🔧 Integración con Backend

La GUI se integra automáticamente con los sistemas existentes:

- **TRANSFORMER CELER**: Utiliza `TRANSFORMER CELER/main.py`
- **CONCILIATOR ALLIANZ**: Utiliza `CONCILIATOR ALLIANZ/main.py`

Los workers de procesamiento en segundo plano (`TransformerWorker`, `ConciliatorWorker`) manejan la comunicación con estos sistemas sin bloquear la interfaz.

## 📊 Reportes

Los reportes se generan automáticamente en la carpeta `output/`:

- **Transformador**: `output/TRANSFORMADO_CELER_[fecha].xlsx`
- **Conciliador**: `output/Reporte_Conciliacion_[fecha].txt`

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verifica que Python 3.8+ esté instalado
- Asegúrate de haber instalado todas las dependencias: `pip install -r requirements.txt`

### Los archivos no se cargan
- Verifica que los archivos tengan las extensiones correctas (.xlsx, .xlsb, .xml)
- Asegúrate de que los archivos no estén dañados o bloqueados

### El procesamiento se congela
- Los procesos largos se ejecutan en segundo plano
- Verifica la barra de progreso para ver el estado
- Revisa la consola para mensajes de error

## 📝 Versión

**v2.0.0** - Interfaz gráfica completa con integración de sistemas

## 👥 Autor

Desarrollado para **Seguros Unión**
