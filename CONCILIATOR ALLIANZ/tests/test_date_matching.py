"""
Test de Coincidencia con Fechas de Vigencia
Verifica si los samples del README coincidirían correctamente cuando incluimos F_Inicio
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def normalize_number(value):
    """Normalize numbers removing leading zeros"""
    try:
        return str(int(str(value)))
    except:
        return str(value)

def test_sample_data_with_dates():
    """
    Test usando los 3 samples del README con fechas incluidas
    Verifica si coinciden correctamente con la lógica de 3 casos
    """
    
    print("\n" + "=" * 80)
    print("TEST: COINCIDENCIA CON FECHAS DE VIGENCIA")
    print("=" * 80)
    
    # ============================================================================
    # SAMPLE 1: AGUDELO DIEZ,GLORIA LUCIA - Póliza 23537654
    # ============================================================================
    print("\n" + "-" * 80)
    print("SAMPLE 1: Póliza 23537654 (AGUDELO DIEZ,GLORIA LUCIA)")
    print("-" * 80)
    
    # Datos Celer (con leading zero como mencionado en README)
    celer_sample1 = {
        'Poliza': '023537654',  # Con leading zero
        'Documento': '347252144',
        'F_Inicio': '2025-12-11',  # Convertido de "12/11/2025"
        'Tomador': 'GLORIA LUCIA AGUDELO DIEZ'
    }
    
    # Datos Allianz
    allianz_sample1 = {
        'Póliza': '23537654',  # Sin leading zero
        'Recibo': '347252144',
        'F.INI VIG': 46002,  # Serial Excel para 12/11/2025
        'Cliente - Tomador': 'AGUDELO DIEZ,GLORIA LUCIA'
    }
    
    # Convertir fecha Excel a string
    excel_origin = pd.to_datetime('1899-12-30')
    allianz_fecha1 = (excel_origin + pd.to_timedelta(allianz_sample1['F.INI VIG'], unit='D')).strftime('%Y-%m-%d')
    
    # Normalizar y crear keys
    celer_poliza1 = normalize_number(celer_sample1['Poliza'])
    celer_recibo1 = normalize_number(celer_sample1['Documento'])
    celer_fecha1 = celer_sample1['F_Inicio']
    
    allianz_poliza1 = normalize_number(allianz_sample1['Póliza'])
    allianz_recibo1 = normalize_number(allianz_sample1['Recibo'])
    
    celer_key_full1 = f"{celer_poliza1}_{celer_recibo1}_{celer_fecha1}"
    allianz_key_full1 = f"{allianz_poliza1}_{allianz_recibo1}_{allianz_fecha1}"
    
    print(f"\nCeler:")
    print(f"  Poliza: {celer_sample1['Poliza']} → Normalizado: {celer_poliza1}")
    print(f"  Documento: {celer_recibo1}")
    print(f"  F_Inicio: {celer_fecha1}")
    print(f"  Key Full: {celer_key_full1}")
    
    print(f"\nAllianz:")
    print(f"  Póliza: {allianz_sample1['Póliza']} → Normalizado: {allianz_poliza1}")
    print(f"  Recibo: {allianz_recibo1}")
    print(f"  F.INI VIG: {allianz_sample1['F.INI VIG']} → {allianz_fecha1}")
    print(f"  Key Full: {allianz_key_full1}")
    
    match1 = celer_key_full1 == allianz_key_full1
    print(f"\n✅ RESULTADO: {'COINCIDE (CASO 1 - NO HAN PAGADO)' if match1 else '❌ NO COINCIDE'}")
    
    if match1:
        print(f"  → Esta póliza aparecería en 'CARTERA PENDIENTE'")
        print(f"  → Cartera vencida 1-30 días: $4,123,617")
        print(f"  → Cliente debe pagar esta póliza")
    
    # ============================================================================
    # SAMPLE 2: AMUNORTE ANTIOQUEÑO - Póliza 23729799
    # ============================================================================
    print("\n" + "-" * 80)
    print("SAMPLE 2: Póliza 23729799 (AMUNORTE ANTIOQUEÑO)")
    print("-" * 80)
    
    celer_sample2 = {
        'Poliza': '23729799',
        'Documento': '110616186',
        'F_Inicio': '2025-11-28',  # Convertido de "11/28/2025"
        'Tomador': 'ASOCIACION DE MUNICIPIOS DEL NORTE ANTIOQUEÑO - AMUNORTE'
    }
    
    allianz_sample2 = {
        'Póliza': '23729799',
        'Recibo': '110616186',
        'F.INI VIG': 45989,  # Serial Excel para 11/28/2025
        'Cliente - Tomador': 'AMUNORTE ANTIOQUEÐO'
    }
    
    allianz_fecha2 = (excel_origin + pd.to_timedelta(allianz_sample2['F.INI VIG'], unit='D')).strftime('%Y-%m-%d')
    
    celer_poliza2 = normalize_number(celer_sample2['Poliza'])
    celer_recibo2 = normalize_number(celer_sample2['Documento'])
    celer_fecha2 = celer_sample2['F_Inicio']
    
    allianz_poliza2 = normalize_number(allianz_sample2['Póliza'])
    allianz_recibo2 = normalize_number(allianz_sample2['Recibo'])
    
    celer_key_full2 = f"{celer_poliza2}_{celer_recibo2}_{celer_fecha2}"
    allianz_key_full2 = f"{allianz_poliza2}_{allianz_recibo2}_{allianz_fecha2}"
    
    print(f"\nCeler:")
    print(f"  Poliza: {celer_poliza2}")
    print(f"  Documento: {celer_recibo2}")
    print(f"  F_Inicio: {celer_fecha2}")
    print(f"  Key Full: {celer_key_full2}")
    
    print(f"\nAllianz:")
    print(f"  Póliza: {allianz_poliza2}")
    print(f"  Recibo: {allianz_recibo2}")
    print(f"  F.INI VIG: {allianz_sample2['F.INI VIG']} → {allianz_fecha2}")
    print(f"  Key Full: {allianz_key_full2}")
    
    match2 = celer_key_full2 == allianz_key_full2
    print(f"\n✅ RESULTADO: {'COINCIDE (CASO 1 - NO HAN PAGADO)' if match2 else '❌ NO COINCIDE'}")
    
    if match2:
        print(f"  → Esta póliza aparecería en 'CARTERA PENDIENTE'")
        print(f"  → Cartera vencida 1-30 días: $832,223")
        print(f"  → Cliente debe pagar esta póliza")
    
    # ============================================================================
    # SAMPLE 3: MONTOYA MARTINEZ, MONICA MARIA - Póliza 23357554
    # ============================================================================
    print("\n" + "-" * 80)
    print("SAMPLE 3: Póliza 23357554 (MONTOYA MARTINEZ, MONICA MARIA)")
    print("-" * 80)
    
    celer_sample3 = {
        'Poliza': '23357554',
        'Documento': '347178265',
        'F_Inicio': '2025-12-22',  # Convertido de "12/22/2025"
        'Tomador': 'MONICA MARIA MONTOYA MARTINEZ'
    }
    
    allianz_sample3 = {
        'Póliza': '23357554',
        'Recibo': '347178265',
        'F.INI VIG': 46013,  # Serial Excel para 12/22/2025
        'Cliente - Tomador': 'MONTOYA MARTINEZ, MONICA MARIA'
    }
    
    allianz_fecha3 = (excel_origin + pd.to_timedelta(allianz_sample3['F.INI VIG'], unit='D')).strftime('%Y-%m-%d')
    
    celer_poliza3 = normalize_number(celer_sample3['Poliza'])
    celer_recibo3 = normalize_number(celer_sample3['Documento'])
    celer_fecha3 = celer_sample3['F_Inicio']
    
    allianz_poliza3 = normalize_number(allianz_sample3['Póliza'])
    allianz_recibo3 = normalize_number(allianz_sample3['Recibo'])
    
    celer_key_full3 = f"{celer_poliza3}_{celer_recibo3}_{celer_fecha3}"
    allianz_key_full3 = f"{allianz_poliza3}_{allianz_recibo3}_{allianz_fecha3}"
    
    print(f"\nCeler:")
    print(f"  Poliza: {celer_poliza3}")
    print(f"  Documento: {celer_recibo3}")
    print(f"  F_Inicio: {celer_fecha3}")
    print(f"  Key Full: {celer_key_full3}")
    
    print(f"\nAllianz:")
    print(f"  Póliza: {allianz_poliza3}")
    print(f"  Recibo: {allianz_recibo3}")
    print(f"  F.INI VIG: {allianz_sample3['F.INI VIG']} → {allianz_fecha3}")
    print(f"  Key Full: {allianz_key_full3}")
    
    match3 = celer_key_full3 == allianz_key_full3
    print(f"\n✅ RESULTADO: {'COINCIDE (CASO 1 - NO HAN PAGADO)' if match3 else '❌ NO COINCIDE'}")
    
    if match3:
        print(f"  → Esta póliza aparecería en 'CARTERA PENDIENTE'")
        print(f"  → Cartera NO vencida: $1,834,871")
        print(f"  → Cliente debe pagar esta póliza")
    
    # ============================================================================
    # RESUMEN FINAL
    # ============================================================================
    print("\n" + "=" * 80)
    print("RESUMEN DE COINCIDENCIAS CON FECHAS")
    print("=" * 80)
    
    total_samples = 3
    total_matches = sum([match1, match2, match3])
    
    print(f"\nTotal muestras probadas: {total_samples}")
    print(f"Coincidencias con fecha: {total_matches}")
    print(f"No coincidencias: {total_samples - total_matches}")
    print(f"Tasa de éxito: {(total_matches/total_samples)*100:.1f}%")
    
    print(f"\n📊 CLASIFICACION:")
    print(f"  CASO 1 (No han pagado - Match completo): {total_matches} pólizas")
    print(f"  CASO 2 (Actualizar sistema): 0 pólizas")
    print(f"  CASO 3 (Corregir póliza): {total_samples - total_matches} pólizas")
    
    print("\n✅ CONCLUSION:")
    if total_matches == total_samples:
        print("  ¡TODAS LAS MUESTRAS COINCIDEN CORRECTAMENTE!")
        print("  Las 3 pólizas del README aparecerían en 'CARTERA PENDIENTE' (CASO 1)")
        print("  El matching con fecha funciona perfectamente para estos ejemplos.")
    else:
        print(f"  {total_matches} de {total_samples} coinciden correctamente")
        print(f"  {total_samples - total_matches} no coinciden - revisar datos")
    
    # Test assertion
    assert total_matches == total_samples, f"Expected all {total_samples} samples to match, but only {total_matches} matched"
    
    print("\n" + "=" * 80)
    print("TEST PASSED ✅")
    print("=" * 80)


if __name__ == "__main__":
    test_sample_data_with_dates()
