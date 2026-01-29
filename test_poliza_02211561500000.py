"""
Test para buscar póliza 02211561500000 en Softseguros y Celer
"""
import pandas as pd
from pathlib import Path

def test_poliza_specific():
    """Buscar póliza 02211561500000 en ambos sistemas"""
    
    poliza_buscar = "02211561500000"
    
    print("="*80)
    print(f" BÚSQUEDA DE PÓLIZA: {poliza_buscar}")
    print("="*80)
    
    # === BUSCAR EN SOFTSEGUROS ===
    print("\n📊 BÚSQUEDA EN SOFTSEGUROS:")
    print("-"*80)
    
    softseguros_file = Path("DATA SOFTSEGUROS/produccion_total.xlsx")
    
    if softseguros_file.exists():
        df_soft = pd.read_excel(softseguros_file)
        
        # Buscar variantes de la póliza
        variantes = [
            poliza_buscar,
            str(int(poliza_buscar)),  # Sin ceros: 2211561500000
            poliza_buscar.lstrip('0'), # Sin ceros iniciales
        ]
        
        print(f"Buscando variantes: {variantes}\n")
        
        encontrados_soft = df_soft[df_soft['NÚMERO PÓLIZA'].astype(str).isin(variantes)]
        
        if len(encontrados_soft) > 0:
            print(f"✅ ENCONTRADO en Softseguros: {len(encontrados_soft)} registro(s)\n")
            
            for idx, row in encontrados_soft.iterrows():
                print(f"📋 Registro {idx}:")
                print(f"   NÚMERO PÓLIZA:    {row['NÚMERO PÓLIZA']}")
                print(f"   NÚMERO ANEXO:     {row['NÚMERO ANEXO']}")
                print(f"   ASEGURADORA:      {row['ASEGURADORA']}")
                print(f"   FECHA INICIO:     {row['FECHA INICIO']}")
                print(f"   FECHA FIN:        {row['FECHA FIN']}")
                print(f"   ESTADO:           {row['ESTADO']}")
                print(f"   ESTADO CARTERA:   {row['ESTADO CARTERA']}")
                print(f"   NOMBRES CLIENTE:  {row['NOMBRES CLIENTE']} {row['APELLIDOS CLIENTE']}")
                print(f"   CÉDULA CLIENTE:   {row['CÉDULA CLIENTE']}")
                print(f"   TOTAL:            ${row['TOTAL']:,.2f}")
                print(f"   PRIMA NETA:       ${row['PRIMA NETA']:,.2f}" if pd.notna(row['PRIMA NETA']) else "   PRIMA NETA:       NaN")
                print()
        else:
            print(f"❌ NO encontrado en Softseguros")
            print(f"\nBuscando pólizas similares (contiene '221156')...")
            similares = df_soft[df_soft['NÚMERO PÓLIZA'].astype(str).str.contains('221156', na=False)]
            if len(similares) > 0:
                print(f"Encontradas {len(similares)} pólizas similares:")
                for pol in similares['NÚMERO PÓLIZA'].head(10):
                    print(f"   - {pol}")
            else:
                print("No se encontraron pólizas similares")
    else:
        print(f"❌ Archivo no encontrado: {softseguros_file}")
    
    # === BUSCAR EN CELER ===
    print("\n" + "="*80)
    print("📊 BÚSQUEDA EN CELER:")
    print("-"*80)
    
    celer_dir = Path("TRANSFORMER CELER/output")
    celer_files = sorted(celer_dir.glob("Cartera_Transformada_XML_*.xlsx"))
    
    if celer_files:
        celer_file = celer_files[-1]  # Más reciente
        print(f"Archivo: {celer_file.name}\n")
        
        df_celer = pd.read_excel(celer_file)
        
        print(f"Buscando variantes: {variantes}\n")
        
        encontrados_celer = df_celer[df_celer['Poliza'].astype(str).isin(variantes)]
        
        if len(encontrados_celer) > 0:
            print(f"✅ ENCONTRADO en Celer: {len(encontrados_celer)} registro(s)\n")
            
            for idx, row in encontrados_celer.iterrows():
                print(f"📋 Registro {idx}:")
                print(f"   Poliza:           {row['Poliza']}")
                print(f"   Documento:        {row['Documento']}")
                print(f"   Aseguradora:      {row['Aseguradora']}")
                print(f"   F_Inicio:         {row['F_Inicio']}")
                print(f"   Saldo:            ${row['Saldo']:,.2f}" if pd.notna(row['Saldo']) else "   Saldo:            NaN")
                print(f"   Cliente:          {row.get('Nombre', 'N/A')} {row.get('Apellido', 'N/A')}")
                print(f"   Identificacion:   {row.get('Identificacion', 'N/A')}")
                print()
        else:
            print(f"❌ NO encontrado en Celer")
            print(f"\nBuscando pólizas similares (contiene '221156')...")
            similares = df_celer[df_celer['Poliza'].astype(str).str.contains('221156', na=False)]
            if len(similares) > 0:
                print(f"Encontradas {len(similares)} pólizas similares:")
                for pol in similares['Poliza'].head(10):
                    print(f"   - {pol}")
            else:
                print("No se encontraron pólizas similares")
    else:
        print(f"❌ No se encontraron archivos transformados en {celer_dir}")
    
    # === COMPARACIÓN ===
    print("\n" + "="*80)
    print("📊 ANÁLISIS COMPARATIVO:")
    print("="*80)
    
    if softseguros_file.exists() and celer_files:
        df_soft = pd.read_excel(softseguros_file)
        df_celer = pd.read_excel(celer_files[-1])
        
        encontrados_soft = df_soft[df_soft['NÚMERO PÓLIZA'].astype(str).isin(variantes)]
        encontrados_celer = df_celer[df_celer['Poliza'].astype(str).isin(variantes)]
        
        if len(encontrados_soft) > 0 and len(encontrados_celer) > 0:
            print("\n✅ Póliza existe en AMBOS sistemas")
            print("\n🔍 Diferencias clave:")
            
            soft_row = encontrados_soft.iloc[0]
            celer_row = encontrados_celer.iloc[0]
            
            print(f"\n   Póliza normalizada:")
            print(f"      Softseguros: '{soft_row['NÚMERO PÓLIZA']}'")
            print(f"      Celer:       '{celer_row['Poliza']}'")
            
            print(f"\n   Recibo/Anexo:")
            print(f"      Softseguros NÚMERO ANEXO: {soft_row['NÚMERO ANEXO']}")
            print(f"      Celer Documento:          {celer_row['Documento']}")
            
            print(f"\n   Fecha Inicio:")
            print(f"      Softseguros: {soft_row['FECHA INICIO']}")
            print(f"      Celer:       {celer_row['F_Inicio']}")
            
            print(f"\n   Aseguradora:")
            print(f"      Softseguros: {soft_row['ASEGURADORA']}")
            print(f"      Celer:       {celer_row['Aseguradora']}")
            
        elif len(encontrados_soft) > 0:
            print("\n⚠️  Póliza SOLO en Softseguros")
        elif len(encontrados_celer) > 0:
            print("\n⚠️  Póliza SOLO en Celer")
        else:
            print("\n❌ Póliza NO encontrada en ningún sistema")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    test_poliza_specific()
