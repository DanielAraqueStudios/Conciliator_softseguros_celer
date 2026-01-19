,include de special caracteher support"""
Test: Compare outputs from XLSX and XML format processors
----------------------------------------------------------
Verifies that both Program 1 (XLSX) and Program 2 (XML) produce 
identical transformed output files.
"""

import pandas as pd
from pathlib import Path
import sys

def compare_excel_files(file1: Path, file2: Path) -> dict:
    """
    Compare two Excel files for equality.
    
    Args:
        file1: Path to first Excel file
        file2: Path to second Excel file
        
    Returns:
        Dictionary with comparison results
    """
    results = {
        'files_identical': False,
        'shape_match': False,
        'columns_match': False,
        'data_match': False,
        'differences': []
    }
    
    print(f"\n{'='*70}")
    print("EXCEL FILE COMPARISON TEST")
    print(f"{'='*70}")
    print(f"\nFile 1 (XLSX): {file1.name}")
    print(f"File 2 (XML):  {file2.name}")
    print()
    
    # Check if files exist
    if not file1.exists():
        results['differences'].append(f"❌ File 1 not found: {file1}")
        return results
    
    if not file2.exists():
        results['differences'].append(f"❌ File 2 not found: {file2}")
        return results
    
    # Read both files
    print("📖 Reading files...")
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    print(f"   File 1: {len(df1)} rows × {len(df1.columns)} columns")
    print(f"   File 2: {len(df2)} rows × {len(df2.columns)} columns")
    
    # Compare shapes
    print(f"\n1️⃣  Comparing dimensions...")
    if df1.shape == df2.shape:
        print(f"   ✅ MATCH: Both files have {df1.shape[0]} rows × {df1.shape[1]} columns")
        results['shape_match'] = True
    else:
        msg = f"   ❌ MISMATCH: File 1 {df1.shape} vs File 2 {df2.shape}"
        print(msg)
        results['differences'].append(msg)
    
    # Compare column names
    print(f"\n2️⃣  Comparing column names...")
    if list(df1.columns) == list(df2.columns):
        print(f"   ✅ MATCH: Both files have identical {len(df1.columns)} columns")
        results['columns_match'] = True
    else:
        print(f"   ❌ MISMATCH: Column names differ")
        
        # Show differences
        cols1_only = set(df1.columns) - set(df2.columns)
        cols2_only = set(df2.columns) - set(df1.columns)
        
        if cols1_only:
            msg = f"   Columns only in File 1: {cols1_only}"
            print(msg)
            results['differences'].append(msg)
        
        if cols2_only:
            msg = f"   Columns only in File 2: {cols2_only}"
            print(msg)
            results['differences'].append(msg)
    
    # Compare data values
    print(f"\n3️⃣  Comparing data values...")
    
    if results['shape_match'] and results['columns_match']:
        # Compare each column
        differences_found = False
        
        for col in df1.columns:
            # Handle NaN values - they should be considered equal
            mask = (df1[col].isna() & df2[col].isna()) | (df1[col] == df2[col])
            
            if not mask.all():
                differences_found = True
                mismatch_count = (~mask).sum()
                msg = f"   ❌ Column '{col}': {mismatch_count} mismatched values"
                print(msg)
                results['differences'].append(msg)
                
                # Show first few differences
                diff_indices = df1[~mask].index[:3]
                for idx in diff_indices:
                    val1 = df1.loc[idx, col]
                    val2 = df2.loc[idx, col]
                    print(f"      Row {idx}: '{val1}' vs '{val2}'")
        
        if not differences_found:
            print(f"   ✅ MATCH: All {len(df1) * len(df1.columns):,} data values are identical")
            results['data_match'] = True
    else:
        msg = "   ⚠️  Cannot compare data - shapes or columns don't match"
        print(msg)
        results['differences'].append(msg)
    
    # Overall result
    results['files_identical'] = (
        results['shape_match'] and 
        results['columns_match'] and 
        results['data_match']
    )
    
    print(f"\n{'='*70}")
    if results['files_identical']:
        print("🎉 RESULT: FILES ARE IDENTICAL")
        print("✅ Both XLSX and XML processors produce the same output!")
    else:
        print("❌ RESULT: FILES HAVE DIFFERENCES")
        print(f"   Found {len(results['differences'])} differences")
    print(f"{'='*70}\n")
    
    return results


def find_latest_output_files(output_dir: Path) -> tuple:
    """
    Find the latest XLSX and XML output files.
    
    Args:
        output_dir: Path to output directory
        
    Returns:
        Tuple of (xlsx_file, xml_file)
    """
    xlsx_files = sorted(output_dir.glob('Cartera_Transformada_XLSX_*.xlsx'), 
                       key=lambda x: x.stat().st_mtime, reverse=True)
    xml_files = sorted(output_dir.glob('Cartera_Transformada_XML_*.xlsx'), 
                      key=lambda x: x.stat().st_mtime, reverse=True)
    
    xlsx_file = xlsx_files[0] if xlsx_files else None
    xml_file = xml_files[0] if xml_files else None
    
    return xlsx_file, xml_file


def main():
    """Main test execution"""
    output_dir = Path('output')
    
    # Check if output directory exists
    if not output_dir.exists():
        print(f"❌ Output directory not found: {output_dir}")
        sys.exit(1)
    
    # Find latest files
    print("🔍 Searching for output files...")
    xlsx_file, xml_file = find_latest_output_files(output_dir)
    
    if xlsx_file is None:
        print("\n❌ No XLSX output file found!")
        print("   Please run Program 1 (XLSX format) first:")
        print("   python main.py  →  Choose option 1  →  Press Enter")
        sys.exit(1)
    
    if xml_file is None:
        print("\n❌ No XML output file found!")
        print("   Please run Program 2 (XML format) first:")
        print("   python main.py  →  Choose option 2  →  Press Enter")
        sys.exit(1)
    
    print(f"   Found XLSX file: {xlsx_file.name}")
    print(f"   Found XML file:  {xml_file.name}")
    
    # Compare files
    results = compare_excel_files(xlsx_file, xml_file)
    
    # Exit with appropriate code
    if results['files_identical']:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
