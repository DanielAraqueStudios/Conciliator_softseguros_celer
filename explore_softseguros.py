"""
Script para explorar la estructura de archivos en DATA SOFTSEGUROS
"""
import pandas as pd
from pathlib import Path

def explore_softseguros_structure():
    """Explore and display structure of Softseguros data files"""
    
    data_dir = Path("DATA SOFTSEGUROS")
    
    print("="*80)
    print(" EXPLORACIÓN DE ESTRUCTURA - DATA SOFTSEGUROS")
    print("="*80)
    
    # Find all Excel files
    excel_files = list(data_dir.glob("*.xlsx")) + list(data_dir.glob("*.xls"))
    excel_files = [f for f in excel_files if not f.name.startswith('~$')]  # Exclude temp files
    
    if not excel_files:
        print("❌ No se encontraron archivos Excel en DATA SOFTSEGUROS")
        return
    
    print(f"\n📁 Archivos encontrados: {len(excel_files)}")
    for file in excel_files:
        print(f"   - {file.name}")
    
    # Analyze each file
    for file_path in excel_files:
        print("\n" + "="*80)
        print(f"📄 ARCHIVO: {file_path.name}")
        print("="*80)
        
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            print(f"\n📊 INFORMACIÓN GENERAL:")
            print(f"   Total de filas: {len(df)}")
            print(f"   Total de columnas: {len(df.columns)}")
            
            print(f"\n📋 COLUMNAS ({len(df.columns)} total):")
            for idx, col in enumerate(df.columns, 1):
                dtype = df[col].dtype
                non_null = df[col].notna().sum()
                print(f"   [{idx:2d}] {col:40s} | Tipo: {str(dtype):10s} | No nulos: {non_null:5d}/{len(df)}")
            
            print(f"\n🔍 PRIMERAS 5 FILAS:")
            print(df.head(5).to_string())
            
            print(f"\n📊 ESTADÍSTICAS DE COLUMNAS CLAVE:")
            # Look for common column names
            key_columns = []
            for col in df.columns:
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['poliza', 'póliza', 'recibo', 'documento', 
                                                              'fecha', 'aseguradora', 'saldo', 'cliente']):
                    key_columns.append(col)
            
            if key_columns:
                print(f"\n   Columnas identificadas como relevantes:")
                for col in key_columns:
                    unique_count = df[col].nunique()
                    sample_values = df[col].dropna().head(3).tolist()
                    print(f"\n   📌 {col}:")
                    print(f"      - Valores únicos: {unique_count}")
                    print(f"      - Ejemplos: {sample_values}")
            
            print(f"\n🔎 ANÁLISIS PARA CONCILIACIÓN:")
            print("\n   Buscar columnas equivalentes a:")
            print("   ✓ Poliza       → Número de póliza")
            print("   ✓ Documento    → Número de recibo/documento")
            print("   ✓ F_Inicio     → Fecha de inicio/vigencia")
            print("   ✓ Aseguradora  → Nombre de la aseguradora")
            print("   ✓ Saldo        → Saldo pendiente/cartera")
            
        except Exception as e:
            print(f"❌ Error al leer archivo: {e}")
    
    print("\n" + "="*80)
    print("✅ EXPLORACIÓN COMPLETADA")
    print("="*80)

if __name__ == "__main__":
    explore_softseguros_structure()
