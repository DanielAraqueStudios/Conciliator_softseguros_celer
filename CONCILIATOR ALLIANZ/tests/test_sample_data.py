"""
Test to verify that documented sample data exists in the input Excel files
"""

import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path to import main module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main import read_allianz_file
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)  # Reduce noise during tests


class TestSampleData:
    """
    Verify that the three sample records documented in README exist in the actual files
    """
    
    # Sample data from README documentation
    SAMPLES = [
        {
            "name": "Sample 1: Automóviles - AGUDELO DIEZ",
            "Cliente - Tomador": "AGUDELO DIEZ,GLORIA LUCIA",
            "Póliza": 23537654,
            "MATRICULA": "LZX371",
            "Nombre Macroramo": "Automóviles",
            "expected_file": "PERSONAS"
        },
        {
            "name": "Sample 2: Multirriesgo - AMUNORTE",
            "Cliente - Tomador": "AMUNORTE ANTIOQUEÐO",
            "Póliza": 23729799,
            "MATRICULA": "",  # Empty for multirriesgo
            "Nombre Macroramo": "Multirriesgo",
            "expected_file": "PERSONAS"
        },
        {
            "name": "Sample 3: Automóviles - MONTOYA MARTINEZ",
            "Cliente - Tomador": "MONTOYA MARTINEZ, MONICA MARIA",
            "Póliza": 23357554,
            "MATRICULA": "MOM665",
            "Nombre Macroramo": "Automóviles",
            "expected_file": "PERSONAS"
        }
    ]
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.input_dir = self.base_dir / "INPUT"
        self.results = []
        
    def find_record(self, df, sample):
        """
        Search for a record in the DataFrame based on policy number
        
        Args:
            df: DataFrame to search
            sample: Sample data dictionary
            
        Returns:
            Tuple of (found: bool, row_data: dict or None)
        """
        # Search by policy number (most unique identifier)
        matching_rows = df[df['Póliza'] == sample['Póliza']]
        
        if len(matching_rows) == 0:
            return False, None
        
        # Get the first matching row
        row = matching_rows.iloc[0]
        
        return True, {
            'Cliente - Tomador': row['Cliente - Tomador'],
            'Póliza': row['Póliza'],
            'MATRICULA': row['MATRICULA'] if not pd.isna(row['MATRICULA']) else "",
            'Nombre Macroramo': row['Nombre Macroramo'],
            'Comisión': row['Comisión'],
            'Cartera Total': row['Cartera Total'],
            'Vencida': row['Vencida'],
            'No Vencida': row['No Vencida']
        }
    
    def verify_match(self, expected, actual):
        """
        Verify if actual data matches expected sample
        
        Args:
            expected: Expected sample data
            actual: Actual row data from Excel
            
        Returns:
            Tuple of (matches: bool, differences: list)
        """
        differences = []
        
        # Check each field
        for field in ['Cliente - Tomador', 'Póliza', 'MATRICULA', 'Nombre Macroramo']:
            expected_value = str(expected[field]).strip()
            actual_value = str(actual[field]).strip()
            
            if expected_value != actual_value:
                differences.append({
                    'field': field,
                    'expected': expected_value,
                    'actual': actual_value
                })
        
        return len(differences) == 0, differences
    
    def run_tests(self):
        """
        Run all sample data verification tests
        """
        print("=" * 80)
        print("ALLIANZ SAMPLE DATA VERIFICATION TEST")
        print("=" * 80)
        print(f"\nBase directory: {self.base_dir}")
        print(f"Input directory: {self.input_dir}\n")
        
        # Load the PERSONAS file (all samples are expected here)
        personas_file = self.input_dir / "PERSONAS" / "Informe Intermediario UNION AGENCIA DE SEGUROS LTDA_1701932_11_Jan_2026 (2).xlsb"
        
        print(f"Loading file: {personas_file.name}")
        print("-" * 80)
        
        try:
            df = read_allianz_file(str(personas_file))
            print(f"\n✓ File loaded successfully: {len(df)} rows\n")
            
        except Exception as e:
            print(f"\n✗ Error loading file: {e}\n")
            return False
        
        # Test each sample
        all_passed = True
        
        for i, sample in enumerate(self.SAMPLES, 1):
            print(f"\nTest {i}: {sample['name']}")
            print("-" * 80)
            
            # Find the record
            found, row_data = self.find_record(df, sample)
            
            if not found:
                print(f"✗ FAILED: Policy {sample['Póliza']} not found in file")
                all_passed = False
                self.results.append({
                    'sample': sample['name'],
                    'status': 'NOT FOUND',
                    'policy': sample['Póliza']
                })
                continue
            
            print(f"✓ Policy {sample['Póliza']} found")
            
            # Verify the data matches
            matches, differences = self.verify_match(sample, row_data)
            
            if matches:
                print(f"✓ PASSED: All fields match")
                print(f"  - Cliente: {row_data['Cliente - Tomador']}")
                print(f"  - Matrícula: {row_data['MATRICULA']}")
                print(f"  - Macroramo: {row_data['Nombre Macroramo']}")
                print(f"  - Cartera Total: ${row_data['Cartera Total']:,}")
                print(f"  - Comisión: ${row_data['Comisión']:,.2f}")
                
                self.results.append({
                    'sample': sample['name'],
                    'status': 'PASSED',
                    'policy': sample['Póliza'],
                    'data': row_data
                })
            else:
                print(f"✗ FAILED: Data mismatch")
                for diff in differences:
                    print(f"  - {diff['field']}:")
                    print(f"    Expected: '{diff['expected']}'")
                    print(f"    Actual:   '{diff['actual']}'")
                
                all_passed = False
                self.results.append({
                    'sample': sample['name'],
                    'status': 'MISMATCH',
                    'policy': sample['Póliza'],
                    'differences': differences
                })
        
        # Print summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for r in self.results if r['status'] == 'PASSED')
        failed = len(self.results) - passed
        
        print(f"\nTotal tests: {len(self.results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        
        if all_passed:
            print("\n✓ ALL TESTS PASSED - Documentation samples verified in input files")
        else:
            print("\n✗ SOME TESTS FAILED - Check differences above")
        
        print("=" * 80)
        
        return all_passed


def main():
    """
    Main test entry point
    """
    # Run tests
    tester = TestSampleData()
    success = tester.run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
