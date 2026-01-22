# CONCILIATOR ALLIANZ

## 📋 Descripción del Proyecto

Sistema automatizado de conciliación para reportes de cartera de la compañía de seguros **Allianz**. Este sistema procesa los informes de intermediario para analizar la cartera pendiente, comisiones y vencimientos de pólizas.

## 🎯 Objetivo

Automatizar el proceso de conciliación de la cartera de seguros Allianz, procesando archivos `.xlsb` (Excel Binary Workbook) que contienen información detallada de pólizas, comisiones, antigüedad de cartera y vencimientos.

## 📊 Estructura de Datos de Entrada

### Carpetas de Entrada

```
INPUT/
├── COLECTIVAS/     # Seguros colectivos
│   └── Informe Intermediario UNION AGENCIA DE SEGUROS LTDA_1701932_11_Jan_2026 (1).xlsb
└── PERSONAS/       # Seguros de personas
    └── Informe Intermediario UNION AGENCIA DE SEGUROS LTDA_1701932_11_Jan_2026 (2).xlsb
```

### Formato de Archivo

- **Formato**: Excel Binary Workbook (`.xlsb`)
- **Hoja de trabajo**: `Detalle`
- **Nombre del intermediario**: UNION AGENCIA DE SEGUROS LTDA_1701932
- **Fecha de reporte**: Generado mensualmente (formato: DD_MMM_YYYY)

## 📑 Especificación de Columnas

La hoja "Detalle" contiene **23 columnas** (A-W) con la siguiente estructura:

| Columna | Nombre | Tipo | Descripción |
|---------|--------|------|-------------|
| **A** | Cliente - Tomador | string | Nombre del cliente titular de la póliza |
| **B** | Póliza | string | Número de póliza |
| **C** | MATRICULA | string | Matrícula del vehículo (cuando aplica) |
| **D** | F.INI VIG | date | Fecha de inicio de vigencia |
| **E** | F.FIN VIG | date | Fecha de fin de vigencia |
| **F** | Nombre Macroramo | string | Categoría de seguro (Automóviles, Multirriesgo, etc.) |
| **G** | Número Ramo | number | Código numérico del ramo |
| **H** | Recibo | string | Número de recibo |
| **I** | Nombre Sucursal | string | Sucursal donde se emitió la póliza |
| **J** | Regional | string | Región geográfica (Antioquia, etc.) |
| **K** | Nombre Asesor | string | Nombre del asesor/intermediario |
| **L** | Aplicación | number | Monto de aplicación |
| **M** | Comisión | number | Monto de comisión |
| **N** | 1-30 | number | Cartera vencida de 1 a 30 días |
| **O** | 31-90 | number | Cartera vencida de 31 a 90 días |
| **P** | 91-180 | number | Cartera vencida de 91 a 180 días |
| **Q** | 180+ | number | Cartera vencida mayor a 180 días |
| **R** | Vencida | number | Total cartera vencida |
| **S** | No Vencida | number | Total cartera no vencida |
| **T** | F. Límite Pago | date | Fecha límite de pago |
| **U** | Comisión Vencida | number | Monto de comisión vencida |
| **V** | Proporción Vencida | number | Proporción de cartera vencida (0-1) |
| **W** | Cartera Total | number | Suma total de cartera |

## 📝 Muestras de Datos

### Muestra 1: Seguro de Automóviles

```json
{
  "sheet": "Detalle",
  "rowNumber": "Ejemplo",
  "data": {
    "Cliente - Tomador": "AGUDELO DIEZ,GLORIA LUCIA",
    "Póliza": "23537654",
    "MATRICULA": "LZX371",
    "F.INI VIG": "12/11/2025",
    "F.FIN VIG": "12/11/2026",
    "Nombre Macroramo": "Automóviles",
    "Número Ramo": 1243,
    "Recibo": "347252144",
    "Nombre Sucursal": "Medellin 2",
    "Regional": "Antioquia",
    "Nombre Asesor": "UNION AGENCIA DE SEGUROS LTDA_1701932",
    "Aplicación": 0,
    "Comisión": 433153.13,
    "1-30": 4123617,
    "31-90": 0,
    "91-180": 0,
    "180+": 0,
    "Vencida": 4123617,
    "No Vencida": 0,
    "F. Límite Pago": "1/10/2026",
    "Comisión Vencida": 433153.13,
    "Proporción Vencida": 1,
    "Cartera Total": 4123617
  },
  "analysis": {
    "cartera_status": "Totalmente vencida (1-30 días)",
    "comision_status": "Comisión vencida 100%",
    "vigencia": "Vigente hasta 12/11/2026",
    "tipo_seguro": "Automóvil con matrícula"
  }
}
```

### Muestra 2: Multirriesgo con Caracteres Especiales

```json
{
  "sheet": "Detalle",
  "rowNumber": 2,
  "data": {
    "Cliente - Tomador": "AMUNORTE ANTIOQUEÐO",
    "Póliza": "23729799",
    "MATRICULA": "",
    "F.INI VIG": "11/28/2025",
    "F.FIN VIG": "11/28/2026",
    "Nombre Macroramo": "Multirriesgo",
    "Número Ramo": 2032,
    "Recibo": "110616186",
    "Nombre Sucursal": "Medellin 2",
    "Regional": "Antioquia",
    "Nombre Asesor": "UNION AGENCIA DE SEGUROS LTDA_1701932",
    "Aplicación": 0,
    "Comisión": 139869.6,
    "1-30": 832223,
    "31-90": 0,
    "91-180": 0,
    "180+": 0,
    "Vencida": 832223,
    "No Vencida": 0,
    "F. Límite Pago": "12/28/2025",
    "Comisión Vencida": 139869.6,
    "Proporción Vencida": 1,
    "Cartera Total": 832223
  },
  "analysis": {
    "cartera_status": "Totalmente vencida (1-30 días)",
    "comision_status": "Comisión vencida 100%",
    "vigencia": "Vigente hasta 11/28/2026",
    "tipo_seguro": "Multirriesgo (sin matrícula)",
    "special_chars": "Contiene carácter especial Ð"
  }
}
```

### Muestra 3: Póliza No Vencida

```json
{
  "sheet": "Detalle",
  "rowNumber": 2,
  "data": {
    "Cliente - Tomador": "MONTOYA MARTINEZ, MONICA MARIA",
    "Póliza": "23357554",
    "MATRICULA": "MOM665",
    "F.INI VIG": "12/22/2025",
    "F.FIN VIG": "12/22/2026",
    "Nombre Macroramo": "Automóviles",
    "Número Ramo": 1243,
    "Recibo": "347178265",
    "Nombre Sucursal": "Medellin 2",
    "Regional": "Antioquia",
    "Nombre Asesor": "UNION AGENCIA DE SEGUROS LTDA_1701932",
    "Aplicación": 0,
    "Comisión": 192738.63,
    "1-30": 0,
    "31-90": 0,
    "91-180": 0,
    "180+": 0,
    "Vencida": 0,
    "No Vencida": 1834871,
    "F. Límite Pago": "1/21/2026",
    "Comisión Vencida": 0,
    "Proporción Vencida": 0,
    "Cartera Total": 1834871
  },
  "analysis": {
    "cartera_status": "Cartera al día (No vencida)",
    "comision_status": "Sin comisión vencida",
    "vigencia": "Vigente hasta 12/22/2026",
    "tipo_seguro": "Automóvil con matrícula",
    "dias_para_vencimiento": "2 días (desde 19/01/2026)"
  }
}
```

## 🔍 Análisis de Patrones de Datos

### Patrones Identificados

1. **Formato de Nombres de Cliente**:
   - `APELLIDO1 APELLIDO2, NOMBRE1 NOMBRE2`
   - Algunos nombres pueden contener caracteres especiales (Ð, Ñ, acentos)

2. **Números de Póliza**:
   - 8 dígitos numéricos
   - Formato: `########`
   - ⚠️ **Importante**: Pueden tener ceros a la izquierda en Celer (ej: `023537654`) que deben normalizarse para comparación con Allianz (`23537654`)

3. **Matrículas**:
   - Formato alfanumérico: 3 letras + 3 números (`AAA###`)
   - Puede estar vacía para seguros sin vehículo

4. **Fechas**:
   - Formato: `MM/DD/YYYY` o `M/DD/YYYY`
   - Formatos detectados: `12/11/2025`, `1/10/2026`

5. **Ramos Identificados**:
   - `1243`: Automóviles
   - `2032`: Multirriesgo

6. **Sucursales y Regionales**:
   - Sucursal: "Medellin 2"
   - Regional: "Antioquia"

7. **Aging de Cartera**:
   - Columnas separadas por rangos de días: 1-30, 31-90, 91-180, 180+
   - Total consolidado en columna "Vencida"

8. **Proporciones**:
   - `Proporción Vencida`: 0 (al día) o 1 (totalmente vencida)
   - Valores intermedios pueden indicar vencimientos parciales

## ⚙️ Requisitos Técnicos

### Dependencias de Python

```python
# requirements.txt
pandas>=2.1.0           # Lectura de archivos Excel
openpyxl>=3.1.0        # Soporte para .xlsx
pyxlsb>=1.0.10         # Soporte para .xlsb (Excel Binary)
pydantic>=2.5.0        # Validación de datos
python-dateutil>=2.8.0 # Manejo de fechas
numpy>=1.24.0          # Operaciones numéricas
```

### Versiones

- **Python**: 3.9 o superior
- **Sistema Operativo**: Windows (desarrollo)
- **Encoding**: UTF-8 para manejar caracteres especiales

## 📦 Estructura del Proyecto

```
CONCILIATOR ALLIANZ/
├── README.md                    # Este archivo
├── main.py                      # Programa principal de conciliación
├── INPUT/                       # Datos de entrada
│   ├── COLECTIVAS/             # Seguros colectivos (953 registros)
│   └── PERSONAS/               # Seguros individuales (77 registros)
└── tests/                       # Pruebas automatizadas
    ├── test_sample_data.py     # Validación de muestras del README
    ├── test_readme_samples.py  # Cross-check Celer ↔ Allianz
    └── test_reconciliation.py  # Reconciliación completa

MAIN PROJECT/
├── main.py                      # Lector de archivos .xlsb con auto-detección
└── TRANSFORMER CELER/
    └── output/                  # Archivos transformados de Celer
```

## 🚀 Funcionalidades Implementadas

### Sprint 1: Lectura y Validación ✅
- [x] Lector de archivos `.xlsb` con `pyxlsb`
- [x] Validación de estructura de columnas (23 columnas esperadas)
- [x] Detección automática de hojas "Detalle"
- [x] Auto-detección de fila de encabezados (maneja 2-20 filas vacías)
- [x] Manejo de caracteres especiales (Ð, Ñ, acentos, &)
- [x] Validación de tipos de datos
- [x] Logs de errores y advertencias
- [x] Normalización de números de póliza (elimina ceros a la izquierda)
- [x] Tests automatizados: 3/3 muestras verificadas en ambos sistemas

### Sprint 2: Sistema de Conciliación ✅
- [x] Programa principal `main.py` con clase `AllianzConciliator`
- [x] Menú interactivo para seleccionar origen de datos (PERSONAS/COLECTIVAS/AMBOS)
- [x] Carga y normalización automática de archivos Celer y Allianz
- [x] Sistema de match key: `{poliza_normalizada}_{recibo_normalizado}`
- [x] Clasificación en 3 categorías:
  - **Cartera Pendiente**: Pólizas en ambos sistemas (20 registros)
  - **[ALERTA] Pagadas - Faltan en sistema**: En Allianz pero no en Celer (1010 registros)
  - **[INFO] Solo en Celer**: En Celer pero no en Allianz (1024 registros)
- [x] Reporte detallado en consola con información de cliente, cartera y comisiones
- [x] Estadísticas de coincidencia y tasas de match

### Sprint 3: Análisis de Cartera (Pendiente)
- [ ] Cálculo de totales por aging (1-30, 31-90, etc.)
- [ ] Resumen por macroramo
- [ ] Resumen por sucursal/regional
- [ ] Identificación de pólizas críticas (180+ días)
- [ ] Estadísticas de comisiones vencidas

### Sprint 4: Reportes y Exportación (Pendiente)
- [ ] Exportación de resultados a Excel (.xlsx)
- [ ] Generación de archivo consolidado
- [ ] Dashboard de métricas clave
- [ ] Resumen ejecutivo
- [ ] Alertas automáticas para pólizas críticas

## 📈 Métricas Clave

### Resultados de Conciliación Actual (Enero 2026)

**Datos procesados:**
- Total Celer: 1,044 registros
- Total Allianz: 1,030 registros (77 PERSONAS + 953 COLECTIVAS)

**Clasificación:**
1. **Cartera Pendiente** (20 pólizas): Existen en ambos sistemas, requieren conciliación
2. **[ALERTA] Pagadas - Faltan en sistema** (1,010 pólizas): Clientes pagaron a Allianz pero no están actualizados en Celer
3. **Solo en Celer** (1,024 pólizas): No encontradas en reporte Allianz

**Tasas de coincidencia:**
- Allianz: 1.94% (20/1030)
- Celer: 1.92% (20/1044)

### Métricas por Origen de Datos

| Origen | Registros | Cartera Pendiente | Alertas | Solo en Celer | Match Rate |
|--------|-----------|-------------------|---------|---------------|------------|
| PERSONAS | 77 | 20 | 57 | 1,024 | 25.97% |
| COLECTIVAS | 953 | 0 | 953 | 1,044 | 0.00% |
| AMBOS | 1,030 | 20 | 1,010 | 1,024 | 1.94% |

## ⚠️ Consideraciones Especiales

### Caracteres Especiales
El sistema debe manejar correctamente:
- **Ð** (eth islandesa) en nombres como "AMUNORTE ANTIOQUEÐO"
- **Ñ** y acentos españoles (á, é, í, ó, ú)
- **&** (ampersand) en nombres de empresas
- Espacios y comas en nombres

### Fechas
- Detectar automáticamente el formato de fecha
- Validar coherencia: F.INI VIG < F.FIN VIG
- Calcular días para vencimiento desde la fecha actual

### Validaciones Numéricas
```python
# Validación de integridad
assert row["Vencida"] + row["No Vencida"] == row["Cartera Total"]
assert row["1-30"] + row["31-90"] + row["91-180"] + row["180+"] == row["Vencida"]
```

### Formato de Archivo
- Los archivos `.xlsb` requieren la librería `pyxlsb`
- Pueden ser más eficientes que `.xlsx` pero menos compatibles
- Considerar conversión a `.xlsx` si es necesario
✅ 20 coincidencias, 1,010 solo en Allianz, 1,024 solo en Celer
- **Match Rate**: 1.94% (Celer contiene múltiples aseguradoras)

## 🎯 Uso del Sistema

### Ejecución del Programa Principal

```bash
# Navegar a la carpeta del proyecto
cd "CONCILIATOR ALLIANZ"

# Ejecutar el conciliador
python main.py
```

### Menú Interactivo

Al ejecutar, aparecerá un menú de selección:

```
================================================================================
CON~~**Sistema de conciliación completo**~~: ✅ Completado
3. ~~**Normalización de números de póliza**~~: ✅ Completado
4. ~~**Menú interactivo de selección**~~: ✅ Completado
5. **Exportación a Excel**: Guardar resultados en archivo .xlsx
6. **Sistema de filtros**: Filtrar por monto, fecha, o estado
7. **Dashboard visual**: Gráficos de distribución y aging
8. **Automatización**: Programar ejecución mensual
9. **Notificaciones**: Email alerts para pólizas críticas
  1. PERSONAS solamente
  2. COLECTIVAS solamente
  3. AMBOS (PERSONAS + COLECTIVAS)

================================================================================

Ingrese su opcion (1-3): _
```Sprint 2 completado ✅ | Tests pasando 3/3 ✅  
**Sistema**: Producción - Conciliador funcional con menú interactivo

### Salida del Programa

El programa genera un reporte detallado que incluye:

1. **Resumen**: Totales de registros Celer y Allianz
2. **Cartera Pendiente**: Listado de pólizas en ambos sistemas con:
   - Número de póliza y recibo
   - Nombre del cliente (Celer vs Allianz)
   - Montos de cartera total, vencida y comisión
3. **[ALERTA] Pagadas - Faltan en sistema**: Pólizas que requieren actualización
4. **[INFO] Solo en Celer**: Pólizas no encontradas en Allianz
5. **Estadísticas**: Totales y tasas de coincidencia

### 1. test_sample_data.py
- **Objetivo**: Verificar que las 3 muestras del README existen en los archivos de entrada
- **Resultado**: ✅ 3/3 muestras encontradas en PERSONAS
- **Cobertura**: Validación de datos documentados

### 2. test_readme_samples.py
- **Objetivo**: Cross-check entre archivos Celer y Allianz
- **Resultado**: ✅ 3/3 muestras encontradas en AMBOS sistemas
- **Features**: Normalización de números con ceros a la izquierda

### 3. test_reconciliation.py
- **Objetivo**: Reconciliación completa Celer ↔ Allianz
- **Resultado**: 2 coincidencias directas, 1042 solo en Celer, 1028 solo en Allianz
- **Match Rate**: 0.19% (indica que Celer contiene múltiples aseguradoras)

## 🎓 Próximos Pasos

1. ~~**Implementar lector de `.xlsb`**~~: ✅ Completado
2. **Crear esquemas Pydantic**: Definir modelos de validación para las 23 columnas
3. **Desarrollar validadores**: Verificar tipos, rangos y consistencia
4. **Construir transformador**: Limpiar, normalizar y enriquecer datos
5. **Crear sistema de reportes**: Generar outputs consolidados
6. **GUI para carga de archivos**: Interfaz para seleccionar archivos dinámicamente

## 📞 Contacto y Soporte

- **Empresa**: SEGUROS UNIÓN
- **Proyecto**: Automatizaciones de Conciliación
- **Fecha de inicio**: Enero 2026

---

**Última actualización**: 20 de enero de 2026  
**Estado**: Sprint 1 completado ✅ | Tests pasando 3/3 ✅
