"""
Quick Test: Generate XLSX output and compare with XML output
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import transform_xlsx_format, transform_xml_format

def main():
    print("\n" + "="*70)
    print("QUICK COMPARISON TEST")
    print("="*70)
    
    # Input files
    data_dir = Path('../DATA CELER')
    xlsx_input = data_dir / 'CarteraPendiente.xlsx'
    xml_input = data_dir / 'CarteraPendiente.xml'
    
    # Output files
    output_dir = Path('output')
    xlsx_output = output_dir / 'TEST_XLSX_output.xlsx'
    xml_output = output_dir / 'TEST_XML_output.xlsx'
    
    print("\n1️⃣  Processing XLSX format...")
    try:
        transform_xlsx_format(xlsx_input, xlsx_output)
        print("   ✅ XLSX processing complete")
    except Exception as e:
        print(f"   ❌ XLSX processing failed: {e}")
        return False
    
    print("\n2️⃣  Processing XML format...")
    try:
        transform_xml_format(xml_input, xml_output)
        print("   ✅ XML processing complete")
    except Exception as e:
        print(f"   ❌ XML processing failed: {e}")
        return False
    
    print("\n3️⃣  Comparing outputs...")
    
    # Now compare
    import pandas as pd
    
    df_xlsx = pd.read_excel(xlsx_output)
    df_xml = pd.read_excel(xml_output)
    
    print(f"\n   XLSX output: {len(df_xlsx)} rows × {len(df_xlsx.columns)} columns")
    print(f"   XML output:  {len(df_xml)} rows × {len(df_xml.columns)} columns")
    
    # Check shapes
    if df_xlsx.shape != df_xml.shape:
        print(f"\n   ❌ Shape mismatch!")
        return False
    
    print(f"   ✅ Shapes match")
    
    # Check columns
    if list(df_xlsx.columns) != list(df_xml.columns):
        print(f"\n   ❌ Column names mismatch!")
        return False
    
    print(f"   ✅ Column names match")
    
    # Check data
    differences = 0
    for col in df_xlsx.columns:
        mask = (df_xlsx[col].isna() & df_xml[col].isna()) | (df_xlsx[col] == df_xml[col])
        if not mask.all():
            diff_count = (~mask).sum()
            differences += diff_count
            print(f"   ❌ Column '{col}': {diff_count} differences")
    
    if differences == 0:
        print(f"   ✅ All data values match!")
        print(f"\n{'='*70}")
        print("🎉 SUCCESS: Both formats produce IDENTICAL output!")
        print(f"{'='*70}\n")
        return True
    else:
        print(f"\n   ❌ Found {differences} total differences")
        print(f"\n{'='*70}")
        print("❌ FAILURE: Outputs are different")
        print(f"{'='*70}\n")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
