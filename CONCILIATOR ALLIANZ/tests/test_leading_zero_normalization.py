"""
Test: Normalización de Ceros Iniciales en Pólizas
Valida que pólizas con cero inicial (023178309) coincidan correctamente con pólizas sin cero (23178309)
"""

import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def normalize_number(value):
    """Normalize numbers removing leading zeros"""
    try:
        return str(int(str(value).strip()))
    except (ValueError, TypeError):
        return str(value).strip()


def test_poliza_23178309():
    """
    Test específico para póliza 23178309 que puede aparecer con cero inicial
    """
    
    print("\n" + "=" * 80)
    print("TEST: NORMALIZACION DE CERO INICIAL - POLIZA 23178309")
    print("=" * 80)
    
    # ============================================================================
    # ESCENARIO: Póliza con cero inicial en Celer, sin cero en Allianz
    # ============================================================================
    
    print("\n" + "-" * 80)
    print("ESCENARIO: Póliza 023178309 (Celer) vs 23178309 (Allianz)")
    print("-" * 80)
    
    # Datos Celer (CON cero inicial)
    celer_poliza_raw = '023178309'
    celer_recibo_raw = '349378509'
    celer_fecha = '2026-01-13'
    
    # Datos Allianz (SIN cero inicial)
    allianz_poliza_raw = '23178309'
    allianz_recibo_raw = '349378509'
    allianz_fecha = '2026-01-13'
    
    print(f"\n📋 DATOS ORIGINALES:")
    print(f"  Celer  - Poliza: '{celer_poliza_raw}' | Recibo: {celer_recibo_raw} | Fecha: {celer_fecha}")
    print(f"  Allianz - Poliza: '{allianz_poliza_raw}' | Recibo: {allianz_recibo_raw} | Fecha: {allianz_fecha}")
    
    # Normalizar
    celer_poliza_norm = normalize_number(celer_poliza_raw)
    celer_recibo_norm = normalize_number(celer_recibo_raw)
    
    allianz_poliza_norm = normalize_number(allianz_poliza_raw)
    allianz_recibo_norm = normalize_number(allianz_recibo_raw)
    
    print(f"\n🔧 DESPUÉS DE NORMALIZAR:")
    print(f"  Celer  - Poliza: '{celer_poliza_norm}' | Recibo: {celer_recibo_norm}")
    print(f"  Allianz - Poliza: '{allianz_poliza_norm}' | Recibo: {allianz_recibo_norm}")
    
    # Crear match keys
    celer_key_full = f"{celer_poliza_norm}_{celer_recibo_norm}_{celer_fecha}"
    allianz_key_full = f"{allianz_poliza_norm}_{allianz_recibo_norm}_{allianz_fecha}"
    
    print(f"\n🔑 MATCH KEYS GENERADOS:")
    print(f"  Celer:   {celer_key_full}")
    print(f"  Allianz: {allianz_key_full}")
    
    # Verificar coincidencia
    match_poliza = celer_poliza_norm == allianz_poliza_norm
    match_recibo = celer_recibo_norm == allianz_recibo_norm
    match_fecha = celer_fecha == allianz_fecha
    match_full = celer_key_full == allianz_key_full
    
    print(f"\n✅ RESULTADOS DE COMPARACIÓN:")
    print(f"  Póliza coincide:  {match_poliza} ({'✓' if match_poliza else '✗'})")
    print(f"  Recibo coincide:  {match_recibo} ({'✓' if match_recibo else '✗'})")
    print(f"  Fecha coincide:   {match_fecha} ({'✓' if match_fecha else '✗'})")
    print(f"  Match completo:   {match_full} ({'✓' if match_full else '✗'})")
    
    # Determinar clasificación
    print(f"\n📊 CLASIFICACIÓN:")
    if match_full:
        print("  → CASO 1: NO HAN PAGADO (Cartera Pendiente)")
        print("  → Esta póliza NO debería aparecer en CASO 3")
        print("  → La normalización funciona correctamente ✅")
    else:
        print("  → CASO 3: CORREGIR POLIZA")
        print("  → ERROR: Esta póliza NO debería estar aquí ❌")
        if not match_poliza:
            print(f"     Problema: Pólizas no coinciden ('{celer_poliza_norm}' vs '{allianz_poliza_norm}')")
        if not match_recibo:
            print(f"     Problema: Recibos no coinciden ('{celer_recibo_norm}' vs '{allianz_recibo_norm}')")
        if not match_fecha:
            print(f"     Problema: Fechas no coinciden ('{celer_fecha}' vs '{allianz_fecha}')")
    
    # ============================================================================
    # CASO ADICIONAL: Múltiples formatos con ceros
    # ============================================================================
    
    print("\n" + "-" * 80)
    print("CASOS ADICIONALES: Diferentes formatos con ceros")
    print("-" * 80)
    
    test_cases = [
        ('023178309', '23178309', 'Con 1 cero inicial'),
        ('0023178309', '23178309', 'Con 2 ceros iniciales'),
        ('00023178309', '23178309', 'Con 3 ceros iniciales'),
        ('23178309', '23178309', 'Ambos sin cero inicial'),
        ('023178309', '023178309', 'Ambos con cero inicial'),
    ]
    
    print("\nFormato | Celer → Normalizado | Allianz → Normalizado | ¿Coincide?")
    print("-" * 80)
    
    all_pass = True
    for celer_raw, allianz_raw, descripcion in test_cases:
        celer_norm = normalize_number(celer_raw)
        allianz_norm = normalize_number(allianz_raw)
        coincide = celer_norm == allianz_norm
        simbolo = '✓' if coincide else '✗'
        
        print(f"{descripcion:30} | {celer_raw:12} → {celer_norm:10} | {allianz_raw:12} → {allianz_norm:10} | {coincide} {simbolo}")
        
        if not coincide:
            all_pass = False
    
    # ============================================================================
    # RESULTADO FINAL
    # ============================================================================
    
    print("\n" + "=" * 80)
    print("RESULTADO DEL TEST")
    print("=" * 80)
    
    if match_full and all_pass:
        print("\n✅ TEST PASSED")
        print("  - La póliza 023178309 (Celer) coincide correctamente con 23178309 (Allianz)")
        print("  - Todos los formatos con ceros iniciales se normalizan correctamente")
        print("  - La póliza NO aparecerá en CASO 3 (solo si recibo y fecha también coinciden)")
    else:
        print("\n❌ TEST FAILED")
        if not match_full:
            print("  - ERROR: La póliza 023178309 NO coincide con 23178309")
        if not all_pass:
            print("  - ERROR: Algunos formatos no se normalizan correctamente")
    
    print("\n" + "=" * 80)
    
    # Assertions
    assert match_poliza, f"Las pólizas deberían coincidir después de normalizar: '{celer_poliza_norm}' vs '{allianz_poliza_norm}'"
    assert match_full, f"Los match keys completos deberían coincidir: '{celer_key_full}' vs '{allianz_key_full}'"
    assert all_pass, "Todos los casos de normalización deberían pasar"
    
    print("✅ Todas las aserciones pasaron correctamente\n")


if __name__ == "__main__":
    test_poliza_23178309()
