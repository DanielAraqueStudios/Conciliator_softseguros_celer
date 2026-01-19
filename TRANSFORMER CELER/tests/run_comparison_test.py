"""
Automated Test Runner: Compare XLSX vs XML Output
--------------------------------------------------
This script automates the process of:
1. Running Program 1 (XLSX format)
2. Running Program 2 (XML format)
3. Comparing the outputs

Run this to verify both programs produce identical results.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def run_transformation(format_choice: str, format_name: str) -> bool:
    """
    Run transformation program with specified format.
    
    Args:
        format_choice: "1" for XLSX, "2" for XML
        format_name: Name for display
        
    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*70}")
    print(f"Running PROGRAM {format_choice}: {format_name} Format")
    print(f"{'='*70}\n")
    
    # Prepare input: choice + empty line (auto-detect file)
    input_data = f"{format_choice}\n\n"
    
    try:
        result = subprocess.run(
            ['python', 'main.py'],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=30
        )
        
        # Show output
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"\n❌ Program {format_choice} failed!")
            print(result.stderr)
            return False
        
        print(f"\n✅ Program {format_choice} completed successfully!")
        return True
        
    except subprocess.TimeoutExpired:
        print(f"\n❌ Program {format_choice} timed out!")
        return False
    except Exception as e:
        print(f"\n❌ Program {format_choice} error: {e}")
        return False


def main():
    """Main execution"""
    start_time = datetime.now()
    
    print("\n" + "="*70)
    print("AUTOMATED TEST: XLSX vs XML OUTPUT COMPARISON")
    print("="*70)
    print("\nThis test will:")
    print("  1. Run PROGRAM 1 (XLSX format transformation)")
    print("  2. Run PROGRAM 2 (XML format transformation)")  
    print("  3. Compare both output files")
    print("\nUsing auto-detected input files from ../DATA CELER/")
    
    # Step 1: Run XLSX transformation
    if not run_transformation("1", "XLSX"):
        print("\n❌ TEST FAILED: XLSX transformation failed")
        sys.exit(1)
    
    # Step 2: Run XML transformation
    if not run_transformation("2", "XML"):
        print("\n❌ TEST FAILED: XML transformation failed")
        sys.exit(1)
    
    # Step 3: Compare outputs
    print(f"\n{'='*70}")
    print("Running Comparison Test")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            ['python', 'tests/test_format_comparison.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            print(f"\n{'='*70}")
            print("🎉 ALL TESTS PASSED!")
            print(f"{'='*70}")
            print(f"\n✅ Both XLSX and XML processors produce identical output")
            print(f"✅ Total execution time: {elapsed:.2f} seconds")
            print(f"\n{'='*70}\n")
            sys.exit(0)
        else:
            print(f"\n{'='*70}")
            print("❌ TEST FAILED: Files are not identical")
            print(f"{'='*70}\n")
            if result.stderr:
                print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Comparison test error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
