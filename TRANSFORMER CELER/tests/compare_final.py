import pandas as pd
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Read both files
xlsx = pd.read_excel('output/TEST_XLSX_output.xlsx')
xml = pd.read_excel('output/TEST_XML_output_FINAL.xlsx')

print("\n" + "="*70)
print("FINAL COMPARISON TEST RESULTS")
print("="*70)

print(f"\nXLSX output: {xlsx.shape[0]} rows × {xlsx.shape[1]} columns")
print(f"XML output:  {xml.shape[0]} rows × {xml.shape[1]} columns")

# Check shapes
shape_match = xlsx.shape == xml.shape
print(f"\n[OK] Shapes match" if shape_match else f"\n[ERROR] Shapes don't match")

# Check columns
cols_match = list(xlsx.columns) == list(xml.columns)
print(f"[OK] Column names match" if cols_match else f"[ERROR] Column names don't match")

# Check data
if shape_match and cols_match:
    all_match = True
    diff_count = 0
    for col in xlsx.columns:
        mask = (xlsx[col].isna() & xml[col].isna()) | (xlsx[col] == xml[col])
        if not mask.all():
            mismatches = (~mask).sum()
            diff_count += mismatches
            print(f"[ERROR] Column '{col}': {mismatches} differences")
            all_match = False
    
    if all_match:
        print(f"[OK] All data values match")
        print("\n" + "="*70)
        print("SUCCESS: Both XLSX and XML produce IDENTICAL output!")
        print("="*70 + "\n")
    else:
        print(f"\n[INFO] Total differences: {diff_count}")
        print("\n" + "="*70)
        print("[ERROR] Data values differ")
        print("="*70 + "\n")
else:
    print("\n" + "="*70)
    print("[ERROR] Cannot compare data - different structure")
    print("="*70 + "\n")
