"""
Verificar póliza específica 23537654 en archivos Celer y Allianz
"""

import pandas as pd
from pathlib import Path

def normalize_number(value):
    """Normalize numbers removing leading zeros"""
    try:
        return str(int(str(value).strip()))
    except (ValueError, TypeError):
        return str(value).strip()

# Archivos
base_dir = Path(__file__).parent.parent
celer_file = base_dir.parent / "TRANSFORMER CELER" / "output" / "Cartera_Transformada_XML_20260123_143400.xlsx"

print("=" * 80)
print("VERIFICACION DE POLIZA 23537654")
print("=" * 80)

# Leer Celer
print(f"\nCargando Celer: {celer_file.name}")
celer_df = pd.read_excel(celer_file)

# Primero, mostrar todas las pólizas que empiecen con "023" o "23537"
print(f"\nBuscando pólizas que contengan '23537'...")
celer_df['Poliza_str'] = celer_df['Poliza'].astype(str).str.strip()
matching = celer_df[celer_df['Poliza_str'].str.contains('23537', na=False)]

if len(matching) > 0:
    print(f"\n✓ ENCONTRADAS {len(matching)} pólizas que contienen '23537':")
    for idx, row in matching.iterrows():
        print(f"\n  Registro {idx}:")
        print(f"  - Poliza (original): '{row['Poliza']}'")
        print(f"  - Documento: {row['Documento']}")
        print(f"  - F_Inicio: {row['F_Inicio']}")
        print(f"  - Tomador: {row.get('Tomador', 'N/A')[:50]}")
        
        poliza_norm = normalize_number(row['Poliza'])
        recibo_norm = normalize_number(row['Documento'])
        fecha_str = pd.to_datetime(row['F_Inicio'], errors='coerce').strftime('%Y-%m-%d')
        
        print(f"  Normalizado:")
        print(f"  - Poliza: {poliza_norm}")
        print(f"  - Recibo: {recibo_norm}")
        print(f"  - Fecha: {fecha_str}")
        print(f"  - Match Key: {poliza_norm}_{recibo_norm}_{fecha_str}")
else:
    print(f"\n✗ NO encontradas pólizas que contengan '23537'")

# Buscar póliza con diferentes variantes
print("\n" + "-" * 80)
poliza_variants = ['23537654', '023537654', '0023537654', '00023537654']

print(f"\nBuscando variantes exactas...")
print(f"Variantes: {poliza_variants}")

for variant in poliza_variants:
    # Buscar sin normalizar
    found = celer_df[celer_df['Poliza_str'] == variant]
    if len(found) > 0:
        print(f"\n✓ ENCONTRADA con formato '{variant}':")
        for idx, row in found.iterrows():
            print(f"  - Poliza: '{row['Poliza']}'")
            print(f"  - Documento: {row['Documento']}")
            print(f"  - F_Inicio: {row['F_Inicio']}")
            print(f"  - Tomador: {row.get('Tomador', 'N/A')}")
            
            # Normalizar y crear key
            poliza_norm = normalize_number(row['Poliza'])
            recibo_norm = normalize_number(row['Documento'])
            fecha_str = pd.to_datetime(row['F_Inicio'], errors='coerce').strftime('%Y-%m-%d')
            
            print(f"\n  Normalizado:")
            print(f"  - Poliza: {poliza_norm}")
            print(f"  - Recibo: {recibo_norm}")
            print(f"  - Fecha: {fecha_str}")
            print(f"  - Match Key: {poliza_norm}_{recibo_norm}_{fecha_str}")
    else:
        print(f"  ✗ No encontrada con formato '{variant}'")

# Buscar con normalización
print(f"\n\nBuscando con normalización automática...")
celer_df['_poliza_norm'] = celer_df['Poliza'].apply(normalize_number)
found_normalized = celer_df[celer_df['_poliza_norm'] == '23537654']

if len(found_normalized) > 0:
    print(f"\n✓ ENCONTRADAS {len(found_normalized)} pólizas normalizadas a '23537654':")
    for idx, row in found_normalized.iterrows():
        print(f"\n  Registro {idx}:")
        print(f"  - Poliza (original): {row['Poliza']}")
        print(f"  - Poliza (normalizada): {row['_poliza_norm']}")
        print(f"  - Documento: {row['Documento']}")
        print(f"  - F_Inicio: {row['F_Inicio']}")
        print(f"  - Tomador: {row.get('Tomador', 'N/A')}")
        
        recibo_norm = normalize_number(row['Documento'])
        fecha_str = pd.to_datetime(row['F_Inicio'], errors='coerce').strftime('%Y-%m-%d')
        
        print(f"  - Match Key: {row['_poliza_norm']}_{recibo_norm}_{fecha_str}")
else:
    print(f"\n✗ NO ENCONTRADA con póliza normalizada '23537654'")

# Información esperada de Allianz
print("\n" + "=" * 80)
print("DATOS ESPERADOS DE ALLIANZ")
print("=" * 80)
print("  - Poliza: 23537654")
print("  - Recibo: 347252144")
print("  - Fecha: 2025-12-11")
print("  - Match Key: 23537654_347252144_2025-12-11")

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)

if len(found_normalized) > 0:
    print("\n✓ La póliza SÍ existe en Celer")
    print("  Si aparece en CASO 3, es porque:")
    print("  - El recibo no coincide, O")
    print("  - La fecha no coincide, O")
    print("  - El registro está duplicado con fechas diferentes")
else:
    print("\n✗ La póliza NO existe en Celer")
    print("  Por eso aparece en CASO 3 - Solo en Allianz")

print("\n" + "=" * 80)
