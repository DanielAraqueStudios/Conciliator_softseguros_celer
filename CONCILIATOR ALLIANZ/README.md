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

## 📦 Estructura del Proyecto (Propuesta)

```
CONCILIATOR ALLIANZ/
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias
├── main.py                      # Punto de entrada
├── INPUT/                       # Datos de entrada
│   ├── COLECTIVAS/             # Seguros colectivos
│   └── PERSONAS/               # Seguros individuales
├── OUTPUT/                      # Archivos procesados
├── schemas/                     # Modelos de datos
│   └── allianz_schema.py
├── services/                    # Lógica de negocio
│   ├── reader.py               # Lectura de .xlsb
│   ├── validator.py            # Validaciones
│   └── transformer.py          # Transformaciones
└── tests/                       # Pruebas unitarias
```

## 🚀 Funcionalidades Propuestas

### Sprint 1: Lectura y Validación
- [ ] Lector de archivos `.xlsb`
- [ ] Validación de estructura de columnas
- [ ] Detección automática de hojas "Detalle"
- [ ] Manejo de caracteres especiales (Ð, Ñ, acentos, &)
- [ ] Validación de tipos de datos
- [ ] Logs de errores y advertencias

### Sprint 2: Análisis de Cartera
- [ ] Cálculo de totales por aging (1-30, 31-90, etc.)
- [ ] Resumen por macroramo
- [ ] Resumen por sucursal/regional
- [ ] Identificación de pólizas críticas (180+ días)
- [ ] Estadísticas de comisiones vencidas

### Sprint 3: Conciliación
- [ ] Comparación entre archivos COLECTIVAS vs PERSONAS
- [ ] Detección de duplicados
- [ ] Validación de sumas (Vencida + No Vencida = Cartera Total)
- [ ] Verificación de proporciones vencidas
- [ ] Reporte de inconsistencias

### Sprint 4: Reportes
- [ ] Generación de archivo consolidado
- [ ] Dashboard de métricas clave
- [ ] Exportación a formato estándar (.xlsx)
- [ ] Resumen ejecutivo
- [ ] Alertas automáticas para pólizas críticas

## 📈 Métricas Clave a Calcular

1. **Cartera Total**: Suma de todas las carteras
2. **% Cartera Vencida**: (Vencida / Cartera Total) × 100
3. **Aging Promedio**: Días promedio de vencimiento
4. **Comisión Total Vencida**: Suma de comisiones vencidas
5. **Top 10 Pólizas Vencidas**: Por monto
6. **Distribución por Ramo**: Automóviles vs Multirriesgo vs otros
7. **Distribución Geográfica**: Por regional/sucursal

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

## 🎓 Próximos Pasos

1. **Implementar lector de `.xlsb`**: Validar que `pyxlsb` puede leer correctamente los archivos
2. **Crear esquemas Pydantic**: Definir modelos de validación para las 23 columnas
3. **Desarrollar validadores**: Verificar tipos, rangos y consistencia
4. **Construir transformador**: Limpiar, normalizar y enriquecer datos
5. **Crear sistema de reportes**: Generar outputs consolidados

## 📞 Contacto y Soporte

- **Empresa**: SEGUROS UNIÓN
- **Proyecto**: Automatizaciones de Conciliación
- **Fecha de inicio**: Enero 2026

---

**Última actualización**: 19 de enero de 2026
