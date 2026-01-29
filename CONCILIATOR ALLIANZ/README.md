# CONCILIATOR ALLIANZ

## 📋 Descripción del Proyecto

Sistema automatizado de conciliación multi-fuente para reportes de cartera de la compañía de seguros **Allianz**. Este sistema integra datos de **Softseguros** (2025-2026) y **Celer** (2000-2026) con los informes de intermediario de Allianz, aplicando lógica de priorización y normalización inteligente para identificar cartera pendiente, discrepancias y pólizas que requieren actualización.

## 🎯 Objetivo

Automatizar el proceso de conciliación de la cartera de seguros Allianz mediante:
- **Integración dual-source**: Combina datos de Softseguros y Celer con priorización inteligente
- **Normalización avanzada**: Tolerancia de 9 dígitos en números de recibo
- **Detección de casos especiales**: Identifica registros sin NÚMERO ANEXO en Softseguros
- **Clasificación automática**: 3 casos de conciliación con alertas específicas
- **Reportes completos**: Consola y archivos TXT con todos los detalles de pólizas

## 📊 Estructura de Datos de Entrada

### Carpetas y Archivos de Entrada

```
DATA SOFTSEGUROS/
└── produccion_total.xlsx           # Excel con 62 columnas, 3,434 registros totales
    ├── NÚMERO PÓLIZA               # 648 registros Allianz (filtrados)
    ├── NÚMERO ANEXO                # Solo 38 registros tienen anexo (5.9%)
    ├── FECHA INICIO                # Para matching
    ├── ASEGURADORA                 # Filtro: "ALLIANZ"
    └── TOTAL                       # Saldo

TRANSFORMER CELER/output/
└── Cartera_Transformada_XML_*.xlsx # Celer transformado, 847 registros totales
    ├── Poliza                      # 94 registros Allianz (filtrados)
    ├── Documento                   # Recibo/anexo
    ├── F_Inicio                    # Para matching
    ├── Aseguradora                 # Filtro: contiene "ALLIANZ"
    └── Saldo                       # Saldo pendiente

ALLIANZ PERSONAS/
└── Informe Intermediario*.xlsb    # 60 registros
    ├── Póliza                      # Número de póliza
    ├── Recibo                      # Número de recibo
    ├── F.INI VIG                   # Fecha inicio vigencia
    ├── Cliente - Tomador           # Nombre cliente
    └── Cartera Total               # Monto total

ALLIANZ COLECTIVAS/
└── Informe Intermediario*.xlsb    # Seguros colectivos (disponible)
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

### ✅ Sprint 1: Lectura y Validación de Allianz (COMPLETADO)
- [x] Lector de archivos `.xlsb` con `pyxlsb`
- [x] Validación de estructura de columnas (23 columnas esperadas)
- [x] Detección automática de hojas "Detalle"
- [x] Auto-detección de fila de encabezados (maneja 2-20 filas vacías)
- [x] Manejo de caracteres especiales (Ð, Ñ, acentos, &)
- [x] Validación de tipos de datos
- [x] Logs de errores y advertencias
- [x] Normalización de números de póliza (elimina ceros a la izquierda)
- [x] Tests automatizados: 3/3 muestras verificadas

### ✅ Sprint 2: Sistema de Conciliación Multi-Fuente (COMPLETADO)
- [x] **Integración Softseguros + Celer**:
  - Carga y normalización de produccion_total.xlsx (Softseguros)
  - Carga de Cartera_Transformada XML (Celer)
  - Filtro automático: solo registros "ALLIANZ"
  - Priorización: Softseguros > Celer (período 2025-2026)
  - Eliminación de duplicados: 6 registros removidos de Celer

- [x] **Sistema de Matching Inteligente**:
  - Match key completo: `{poliza}_{recibo}_{fecha}`
  - Match key parcial: `{poliza}_{fecha}`
  - Normalización de recibos: últimos 9 dígitos (tolerancia Allianz)
  - Normalización de pólizas: elimina ceros a la izquierda

- [x] **Clasificación en 3 Casos**:
  - **CASO 1 - No han pagado**: Match completo (poliza + recibo + fecha)
    - Marca registros de CELER para actualizar en Softseguros
    - Muestra ambos recibos cuando coinciden
  - **CASO 2 ESPECIAL - Actualizar recibo en Softseguros**: 
    - Poliza + fecha coinciden, pero Softseguros NO tiene NÚMERO ANEXO
    - Sugiere recibo de Allianz para actualización
  - **CASO 2 - Actualizar sistema**: Match parcial (poliza + fecha, recibo diferente)
  - **CASO 3 - Corregir póliza**: 
    - Solo en Allianz (no en Softseguros/Celer)
    - Solo en Softseguros/Celer (no en Allianz)

- [x] **Menú Interactivo**:
  - Selección de fuente de datos: Softseguros / Celer / Ambos
  - Selección de Allianz: PERSONAS / COLECTIVAS / Ambos
  - Auto-detección de archivos con selección manual

- [x] **Reportes Completos**:
  - Consola: TODAS las pólizas de cada caso con detalles
  - Archivo TXT: Reporte completo con timestamp
  - Información: Tomador, Cliente Allianz, Saldos, Source

### 🔜 Sprint 3: Análisis de Cartera y Automatización (PLANEADO)
- [ ] Exportación a Excel con hojas separadas por caso
- [ ] Actualización automática de NÚMERO ANEXO en Softseguros
- [ ] Dashboard con métricas visuales
- [ ] Cálculo de totales por aging (1-30, 31-90, etc.)
- [ ] Resumen por macroramo y regional
- [ ] Identificación de pólizas críticas (180+ días)
- [ ] Sistema de alertas por email

### 📅 Sprint 4: Reportes Avanzados y Exportación (FUTURO)
- [ ] Exportación de resultados a Excel multi-hoja
- [ ] Generación de archivo consolidado
- [ ] Dashboard interactivo de métricas clave
- [ ] Resumen ejecutivo PDF
- [ ] Alertas automáticas para pólizas críticas
- [ ] Integración con API de Softseguros

## 📈 Métricas Clave

### Resultados de Conciliación Actual (Enero 29, 2026)

**Datos procesados:**
- **Softseguros**: 648 registros Allianz (de 3,434 totales)
  - Con NÚMERO ANEXO: 38 registros (5.9%)
  - Sin NÚMERO ANEXO: 610 registros (94.1%)
- **Celer**: 94 registros Allianz (de 847 totales)
- **Combined**: 736 registros únicos (6 duplicados removidos con prioridad Softseguros)
- **Allianz PERSONAS**: 60 registros

**Clasificación de Conciliación:**
1. **CASO 1 - No han pagado** (17 pólizas): 
   - Match completo: poliza + recibo + fecha coinciden
   - 11 de CELER → requieren actualización en Softseguros
   - 6 de SOFTSEGUROS → ya actualizados

2. **CASO 2 ESPECIAL** (8 pólizas):
   - Poliza + fecha coinciden en Softseguros y Allianz
   - Softseguros NO tiene NÚMERO ANEXO registrado
   - Sistema sugiere recibo de Allianz para actualización

3. **CASO 2 - Actualizar sistema** (10 pólizas):
   - Poliza + fecha coinciden
   - Recibo diferente entre sistemas
   - Requiere investigación y actualización

4. **CASO 3 - Solo en Allianz** (32 pólizas):
   - Pólizas reportadas por Allianz no encontradas en Softseguros/Celer
   - Posibles pagos directos o nuevas pólizas

5. **CASO 3 - Solo en Combined** (98 pólizas):
   - Pólizas en Softseguros/Celer no reportadas por Allianz
   - Posibles pagos completados o pólizas de otras fechas

**Tasas de coincidencia:**
- **Match Rate**: 4.90% (35 de 736 registros combinados)
- **Desglose de matches**:
  - Full match (CASO 1): 17 pólizas (2.31%)
  - Partial match (CASO 2): 10 pólizas (1.36%)
  - Special case (CASO 2 ESPECIAL): 8 pólizas (1.09%)

**Calidad de Datos Softseguros:**
- **NÚMERO ANEXO presente**: 5.9% (38/648)
- **NÚMERO ANEXO ausente**: 94.1% (610/648)
- **Impacto**: Mayor tasa de CASO 2 ESPECIAL por datos incompletos

### Resumen de Duplicados Removidos

| Período | Registros Softseguros | Registros Celer | Duplicados | Combined Final |
|---------|----------------------|-----------------|------------|----------------|
| 2025-2026 | 648 | 94 | 6 | 736 |

**Lógica de priorización**: Softseguros > Celer para período de overlap (2025-2026)

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

### Menú Interactivo - Nivel 1: Selección de Fuente de Datos

Al ejecutar, aparecerá el primer menú:

```
================================================================================
CONCILIADOR ALLIANZ - SELECCIÓN DE FUENTE DE DATOS
================================================================================

¿De dónde desea obtener los datos para conciliar?

  1. SOFTSEGUROS solamente
  2. CELER solamente
  3. AMBOS (SOFTSEGUROS + CELER con prioridad a Softseguros)

================================================================================

Ingrese su opcion (1-3): _
```

**Opciones:**
- **Opción 1**: Conciliar solo con datos de Softseguros (produccion_total.xlsx)
- **Opción 2**: Conciliar solo con datos de Celer (Cartera_Transformada XML)
- **Opción 3**: Conciliar con ambas fuentes (recomendado - prioriza Softseguros)

### Menú Interactivo - Nivel 2: Selección de Datos Allianz

Después de seleccionar la fuente, aparece el segundo menú:

```
================================================================================
CONCILIADOR ALLIANZ - SELECCIÓN DE DATOS ALLIANZ
================================================================================

Seleccione que datos de Allianz desea procesar:

  1. PERSONAS solamente
  2. COLECTIVAS solamente
  3. AMBOS (PERSONAS + COLECTIVAS)

================================================================================

Ingrese su opcion (1-3): _
```

**Opciones:**
- **Opción 1**: Procesar solo seguros de PERSONAS (60 registros)
- **Opción 2**: Procesar solo seguros COLECTIVAS
- **Opción 3**: Procesar ambos tipos de seguros

### Selección de Archivos

El sistema detecta automáticamente los archivos disponibles en cada carpeta y permite seleccionarlos:

1. **Archivo Softseguros** (si aplica): produccion_total.xlsx
2. **Archivo Celer** (si aplica): Cartera_Transformada_XML_*.xlsx
3. **Archivo Allianz PERSONAS** (si aplica): Informe Intermediario*.xlsb
4. **Archivo Allianz COLECTIVAS** (si aplica): Informe Intermediario*.xlsb

### Ejemplo de Ejecución Completa

```bash
$ python main.py

# Seleccionar: 3 (AMBOS - Softseguros + Celer)
# Seleccionar: 1 (PERSONAS solamente)
# Seleccionar archivos automáticamente detectados

# Output:
================================================================================
INICIANDO CONCILIACIÓN ALLIANZ (BOTH)
================================================================================
✓ Softseguros: 648 registros Allianz (38 con anexo, 610 sin anexo)
✓ Celer: 94 registros Allianz
✓ Combined: 736 registros (6 duplicados removidos)
✓ Allianz PERSONAS: 60 registros

================================================================================
REPORTE DE CONCILIACION ALLIANZ (BOTH)
================================================================================
[CASO 1] NO HAN PAGADO - CARTERA PENDIENTE: 17 pólizas
[CASO 2 ESPECIAL] ACTUALIZAR RECIBO EN SOFTSEGUROS: 8 pólizas
[CASO 2] ACTUALIZAR EN SISTEMA: 10 pólizas
[CASO 3] SOLO EN ALLIANZ: 32 pólizas
[CASO 3] SOLO EN SOFTSEGUROS/CELER: 98 pólizas

Tasa de coincidencia: 4.90%

✅ Reporte guardado en: output\Reporte_Conciliacion_20260129_093107.txt
```

## 📞 Contacto y Soporte

- **Empresa**: SEGUROS UNIÓN
- **Proyecto**: Automatizaciones de Conciliación
- **Última actualización**: Enero 29, 2026

---

**Última actualización**: 29 de enero de 2026  
**Estado**: Sprint 2 completado ✅ | Sistema dual-source operativo ✅  
**Versión**: 2.0.0 - Conciliador Multi-Fuente con Alertas Inteligentes

### 🎉 Logros del Sprint 2

✅ **Integración Dual-Source** - Softseguros + Celer con priorización automática  
✅ **Matching Inteligente** - 3 casos de conciliación con lógica avanzada  
✅ **Normalización Avanzada** - Tolerancia de 9 dígitos en recibos  
✅ **Detección Especial** - Identifica registros sin NÚMERO ANEXO  
✅ **Reportes Completos** - Consola + TXT con todas las pólizas listadas  
✅ **Alertas Inteligentes** - Marca CELER para actualizar en Softseguros  
✅ **Sistema de Menús** - Selección interactiva de fuentes y archivos  

**Sistema**: ✅ Producción - Conciliador funcional con 165 pólizas procesadas (Ene 29, 2026)
