# Celer Column Mapping Documentation

**Last Updated:** January 16, 2026  
**Source File:** `DATA CELER/CarteraPendiente.xlsx`

---

## 📋 File Structure

- **Header Row:** Row 5 (index 4 in pandas)
- **Data Starts:** Row 6
- **Total Columns:** 49 named columns
- **Encoding:** UTF-8 with Excel XML format

---

## 🔄 Complete Column Mapping

### Output Format: 23 Columns (A-W)

| Output Col | Celer Column Name | Position | Data Type | Description |
|------------|-------------------|----------|-----------|-------------|
| **A** | *Generated* | N/A | String/Int | Sequential ID or calculated identifier |
| **B** | Días | D (4) | Integer | Days pending/overdue |
| **C** | Tomador | X (24) | String | Policyholder/customer name |
| **D** | Tipo_Doc | Z (26) | String | Document type (C.C., NIT, etc.) |
| **E** | Identificacion | AA (27) | String | Identification number |
| **F** | Poliza | U (21) | String | Policy number |
| **G** | Documento | E (5) | String | Document/receipt number |
| **H** | Cuota | F (6) | Integer | Installment/quota number |
| **I** | Placa | AO (41) | String | Vehicle license plate |
| **J** | Saldo | G (7) | Decimal | Outstanding balance amount |
| **K** | Aseguradora | V (22) | String | Insurance company name |
| **L** | Ramo | W (23) | String | Insurance line/branch type |
| **M** | Carta_Cobro | AL (38) | String | Collection letter reference |
| **N** | F_Inicio | A (1) | Date | Start/effective date |
| **O** | F_Expedicion | B (2) | Date | Issue/expedition date |
| **P** | F_Creacion | C (3) | DateTime | Creation date with timestamp |
| **Q** | Ejecutivo | AM (39) | String | Account executive name |
| **R** | Unidad | AV (48) | String | Business unit/department |
| **S** | Descripcion_Riesgo | AT (46) | String | Risk description/details |
| **T** | Celular_Pers | AD (30) | String | Personal cell phone |
| **U** | Celular_Lab | AE (31) | String | Work/office cell phone |
| **V** | Mail_Lab | AF (32) | String | Work email address |
| **W** | Mail_Pers | AG (33) | String | Personal email address |

---

## 📊 All Celer Source Columns (49 Total)

| Position | Excel Letter | Column Name | Used in Output | Description |
|----------|--------------|-------------|----------------|-------------|
| 0 | A | F_Inicio | ✅ Output N | Start date |
| 1 | B | F_Expedicion | ✅ Output O | Issue date |
| 2 | C | F_Creacion | ✅ Output P | Creation date |
| 3 | D | Días | ✅ Output B | Days pending |
| 4 | E | Documento | ✅ Output G | Document number |
| 5 | F | Cuota | ✅ Output H | Installment number |
| 6 | G | Saldo | ✅ Output J | Balance |
| 7 | H | Estado | ❌ | Payment status |
| 8 | I | Operacion | ❌ | Operation type |
| 9 | J | Descripcion | ❌ | Operation description |
| 10 | K | Prima | ❌ | Premium amount |
| 11 | L | Prima_Participacion | ❌ | Participation premium |
| 12 | M | Imp_Documento | ❌ | Document tax |
| 13 | N | Imp_Valor_Documento | ❌ | Document value tax |
| 14 | O | Otros_Rubros_Documento | ❌ | Other document items |
| 15 | P | Valores_Externos_Documento | ❌ | External document values |
| 16 | Q | Valor_Total | ❌ | Total value |
| 17 | R | Valor_Total_Cobro | ❌ | Total collection value |
| 18 | S | Valor_Comision | ❌ | Commission value |
| 19 | T | F_Plazo | ❌ | Due date |
| 20 | U | Poliza | ✅ Output F | Policy number |
| 21 | V | Aseguradora | ✅ Output K | Insurance company |
| 22 | W | Ramo | ✅ Output L | Insurance branch |
| 23 | X | Tomador | ✅ Output C | Policyholder |
| 24 | Y | Tipo_Persona | ❌ | Person type (Natural/Juridica) |
| 25 | Z | Tipo_Doc | ✅ Output D | Document type |
| 26 | AA | Identificacion | ✅ Output E | ID number |
| 27 | AB | Telefono_Of | ❌ | Office phone |
| 28 | AC | Telefono_Pers | ❌ | Personal phone |
| 29 | AD | Celular_Pers | ✅ Output T | Personal cell |
| 30 | AE | Celular_Lab | ✅ Output U | Work cell |
| 31 | AF | Mail_Lab | ✅ Output V | Work email |
| 32 | AG | Mail_Pers | ✅ Output W | Personal email |
| 33 | AH | Observacion_A | ❌ | Observation A |
| 34 | AI | Observacion_B | ❌ | Observation B |
| 35 | AJ | Observacion_C | ❌ | Observation C |
| 36 | AK | Recibo_Sin_Liberar | ❌ | Unreleased receipt |
| 37 | AL | Carta_Cobro | ✅ Output M | Collection letter |
| 38 | AM | Ejecutivo | ✅ Output Q | Executive name |
| 39 | AN | Ejecutivo_Cod | ❌ | Executive code |
| 40 | AO | Placa | ✅ Output I | License plate |
| 41 | AP | Linea_Vehiculo | ❌ | Vehicle line |
| 42 | AQ | Modelo_Vehiculo | ❌ | Vehicle model |
| 43 | AR | Tipo_Vehiculo | ❌ | Vehicle type |
| 44 | AS | Marca_Vehiculo | ❌ | Vehicle brand |
| 45 | AT | Descripcion_Riesgo | ✅ Output S | Risk description |
| 46 | AU | Fasecolda | ❌ | Fasecolda code |
| 47 | AV | Unidad | ✅ Output R | Business unit |
| 48 | AW | Forma_Recaudo_Poliza | ❌ | Policy collection method |

---

## 🎯 Transformation Summary

- **Total Celer Columns:** 49
- **Used in Output:** 22 (mapped directly)
- **Generated Columns:** 1 (Column A)
- **Output Columns:** 23 (A-W)
- **Unused Columns:** 27 (archived for potential future use)

---

## 📝 Data Quality Notes

### Date Fields
- `F_Inicio` (Output N): Date format, no time
- `F_Expedicion` (Output O): Date format, no time  
- `F_Creacion` (Output P): DateTime format with timestamp (e.g., "12/1/2025 12:25 PM")

### Numeric Fields
- `Días` (Output B): Integer, can be negative for early payments
- `Saldo` (Output J): Decimal/Float, can be negative for credits
- `Cuota` (Output H): Integer, installment number (0 = full payment)

### String Fields
- All name/text fields are trimmed and cleaned
- Email fields validated for format
- Phone fields stored as strings (preserve leading zeros)

### Empty/Null Handling
- `Placa` (Output I): Can be null for non-vehicle policies
- `Carta_Cobro` (Output M): Null if no collection letter issued
- Contact fields (T, U, V, W): At least one contact method should be present

---

## 🔐 Data Privacy

**Sensitive Fields** (handle with care):
- Output E: Identificacion (ID numbers)
- Output T, U: Phone numbers
- Output V, W: Email addresses

These fields must be:
- Encrypted at rest (if persisted)
- Masked in logs
- Access-controlled
- GDPR/data protection compliant

---

## 🔧 Configuration Location

Mapping configuration is maintained in:
```python
schemas/celer_mapping.py
```

Key constants:
- `CELER_MAPPING`: Main mapping configuration
- `CELER_COLUMN_NAMES`: Full list of 49 source columns
- `COLUMN_DESCRIPTIONS`: Human-readable descriptions
- `NAMED_COLUMN_MAPPING`: Direct name-to-output mapping
