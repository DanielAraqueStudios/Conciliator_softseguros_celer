import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from adapters.xml_reader import read_celer_xml

# Test XML reader with special characters
df = read_celer_xml(Path('../DATA CELER/CarteraPendiente.xml'))

print(f"\nRead {len(df)} rows, {len(df.columns)} columns")
print(f"\nColumns: {list(df.columns[:5])}")
print(f"\nChecking row 40 - Tomador column (should have 'CONSTRUCCIONES B & Z S.A.S.'):")

# Find the Tomador column (it might have different name)
tomador_col = [col for col in df.columns if 'tomador' in col.lower() or 'raz' in col.lower()]
if tomador_col:
    col_name = tomador_col[0]
    print(f"Column name: '{col_name}'")
    print(f"Value: '{df[col_name].iloc[40]}'")
    print(f"Has ampersand: {'&' in str(df[col_name].iloc[40])}")
else:
    print("Tomador column not found")
    print(f"Available columns: {list(df.columns)}")
