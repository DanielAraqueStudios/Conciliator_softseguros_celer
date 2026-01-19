import pandas as pd

# Read both files
xlsx = pd.read_excel('output/TEST_XLSX_output.xlsx')
xml = pd.read_excel('output/Cartera_Transformada_XML_20260119_110557.xlsx')

print("\n" + "="*70)
print("DETAILED DIFFERENCE ANALYSIS")
print("="*70)

# Check specific columns with differences
diff_columns = ['Tomador', 'Poliza', 'Descripcion_Riesgo', 'Mail_Lab', 'Mail_Pers']

for col in diff_columns:
    print(f"\n\n{col}")
    print("-" * 70)
    
    # Find rows with differences
    mask = (xlsx[col].isna() & xml[col].isna()) | (xlsx[col] == xml[col])
    diff_indices = xlsx[~mask].index[:5]  # Show first 5 differences
    
    for idx in diff_indices:
        xlsx_val = xlsx.loc[idx, col]
        xml_val = xml.loc[idx, col]
        
        print(f"\nRow {idx}:")
        print(f"  XLSX: '{xlsx_val}' (type: {type(xlsx_val).__name__}, len: {len(str(xlsx_val)) if pd.notna(xlsx_val) else 'NA'})")
        print(f"  XML:  '{xml_val}' (type: {type(xml_val).__name__}, len: {len(str(xml_val)) if pd.notna(xml_val) else 'NA'})")
        
        # Check if it's whitespace issue
        if pd.notna(xlsx_val) and pd.notna(xml_val):
            if str(xlsx_val).strip() == str(xml_val).strip():
                print(f"  → Difference is WHITESPACE only")
            else:
                print(f"  → Content is different")
                # Show repr to see hidden characters
                print(f"     XLSX repr: {repr(xlsx_val)}")
                print(f"     XML repr:  {repr(xml_val)}")
