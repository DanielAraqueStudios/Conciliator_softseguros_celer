import pandas as pd
import sys

sys.path.insert(0, '.')

# Read both files
xlsx = pd.read_excel('output/TEST_XLSX_output.xlsx')
xml = pd.read_excel('output/TEST_XML_output_FINAL.xlsx')

print("\n" + "="*70)
print("DETAILED ANALYSIS OF REMAINING DIFFERENCES")
print("="*70)

# Check 'Tomador' column
print("\n\nTOMADOR COLUMN DIFFERENCES (13 remaining):")
print("-" * 70)
col = 'Tomador'
mask = (xlsx[col].isna() & xml[col].isna()) | (xlsx[col] == xml[col])
diff_indices = xlsx[~mask].index[:3]

for idx in diff_indices:
    xlsx_val = xlsx.loc[idx, col]
    xml_val = xml.loc[idx, col]
    
    print(f"\nRow {idx}:")
    print(f"  XLSX: '{xlsx_val}'")
    print(f"  XML:  '{xml_val}'")
    
    if pd.notna(xlsx_val) and pd.notna(xml_val):
        if str(xlsx_val).strip() == str(xml_val).strip():
            print(f"  DIFFERENCE: Whitespace only")
        else:
            print(f"  DIFFERENCE: Content")
            # Show which characters differ
            xlsx_str = str(xlsx_val)
            xml_str = str(xml_val)
            if len(xlsx_str) != len(xml_str):
                print(f"    Length: {len(xlsx_str)} vs {len(xml_str)}")
            # Show as bytes
            print(f"    XLSX bytes: {xlsx_str.encode('utf-8')[:50]}")
            print(f"    XML bytes:  {xml_str.encode('utf-8')[:50]}")
