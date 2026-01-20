"""
Test to verify if the documented sample policies from README exist in both:
1. Allianz input files
2. Celer transformed file
"""

import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main import read_allianz_file
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)


class ReadmeSamplesCrossCheck:
    """
    Verify README sample policies appear in both Celer and Allianz files
    """
    
    # Sample policies from README
    SAMPLES = [
        {
            "name": "Sample 1: AGUDELO DIEZ",
            "poliza": "23537654",
            "recibo": "347252144",
            "cliente": "AGUDELO DIEZ,GLORIA LUCIA"
        },
        {
            "name": "Sample 2: AMUNORTE",
            "poliza": "23729799",
            "recibo": "110616186",
            "cliente": "AMUNORTE ANTIOQUEÐO"
        },
        {
            "name": "Sample 3: MONTOYA MARTINEZ",
            "poliza": "23357554",
            "recibo": "347178265",
            "cliente": "MONTOYA MARTINEZ, MONICA MARIA"
        }
    ]
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.celer_file = Path(__file__).parent.parent.parent / "TRANSFORMER CELER" / "output" / "Cartera_Transformada_XML_20260119_110557.xlsx"
        self.allianz_input_dir = self.base_dir / "INPUT"
        
        self.celer_df = None
        self.allianz_df = None
        self.results = []
    
    def load_celer_data(self):
        """Load Celer transformed file"""
        if not self.celer_file.exists():
            raise FileNotFoundError(f"Celer file not found: {self.celer_file}")
        
        self.celer_df = pd.read_excel(self.celer_file)
        print(f"✓ Celer loaded: {len(self.celer_df)} rows")
        return self.celer_df
    
    def load_allianz_data(self):
        """Load Allianz PERSONAS file (where samples are documented)"""
        personas_file = self.allianz_input_dir / "PERSONAS" / "Informe Intermediario UNION AGENCIA DE SEGUROS LTDA_1701932_11_Jan_2026 (2).xlsb"
        self.allianz_df = read_allianz_file(str(personas_file))
        print(f"✓ Allianz PERSONAS loaded: {len(self.allianz_df)} rows\n")
        return self.allianz_df
    
    def normalize_number(self, value):
        """
        Normalize policy/recibo numbers by removing leading zeros
        Handles cases where Celer has '023537654' and Allianz has '23537654'
        """
        try:
            # Convert to int then back to string to remove leading zeros
            return str(int(str(value).strip()))
        except (ValueError, TypeError):
            # If conversion fails, return original stripped value
            return str(value).strip()
    
    def check_sample(self, sample):
        """
        Check if a sample exists in both Celer and Allianz
        
        Returns:
            dict with results
        """
        poliza = str(sample['poliza']).strip()
        recibo = str(sample['recibo']).strip()
        
        # Normalize for comparison (remove leading zeros)
        poliza_normalized = self.normalize_number(poliza)
        recibo_normalized = self.normalize_number(recibo)
        
        # Check in Allianz (normalize Allianz values)
        allianz_poliza_normalized = self.allianz_df['Póliza'].astype(str).str.strip().apply(self.normalize_number)
        allianz_recibo_normalized = self.allianz_df['Recibo'].astype(str).str.strip().apply(self.normalize_number)
        
        allianz_match = self.allianz_df[
            (allianz_poliza_normalized == poliza_normalized) &
            (allianz_recibo_normalized == recibo_normalized)
        ]
        in_allianz = len(allianz_match) > 0
        
        # Check in Celer (normalize Celer values)
        celer_poliza_normalized = self.celer_df['Poliza'].astype(str).str.strip().apply(self.normalize_number)
        celer_documento_normalized = self.celer_df['Documento'].astype(str).str.strip().apply(self.normalize_number)
        
        celer_match = self.celer_df[
            (celer_poliza_normalized == poliza_normalized) &
            (celer_documento_normalized == recibo_normalized)
        ]
        in_celer = len(celer_match) > 0
        
        result = {
            'sample': sample['name'],
            'poliza': poliza,
            'recibo': recibo,
            'in_allianz': in_allianz,
            'in_celer': in_celer,
            'in_both': in_allianz and in_celer
        }
        
        if in_allianz:
            result['allianz_cliente'] = allianz_match.iloc[0]['Cliente - Tomador']
        
        if in_celer:
            result['celer_tomador'] = celer_match.iloc[0]['Tomador']
        
        return result
    
    def run_test(self):
        """
        Execute the cross-check test
        """
        print("=" * 80)
        print("README SAMPLES CROSS-CHECK TEST")
        print("=" * 80)
        print("Checking if documented samples exist in BOTH Celer and Allianz files\n")
        
        # Load data
        self.load_celer_data()
        self.load_allianz_data()
        
        # Check each sample
        for sample in self.SAMPLES:
            result = self.check_sample(sample)
            self.results.append(result)
            
            print(f"📄 {result['sample']}")
            print(f"   Poliza: {result['poliza']} | Recibo/Documento: {result['recibo']}")
            print(f"   In Allianz: {'✓ YES' if result['in_allianz'] else '✗ NO'}")
            if result['in_allianz']:
                print(f"      └─ Cliente: {result['allianz_cliente']}")
            
            print(f"   In Celer:   {'✓ YES' if result['in_celer'] else '✗ NO'}")
            if result['in_celer']:
                print(f"      └─ Tomador: {result['celer_tomador']}")
            
            if result['in_both']:
                print(f"   ✅ FOUND IN BOTH SYSTEMS")
            else:
                print(f"   ⚠️ NOT IN BOTH SYSTEMS")
            
            print()
        
        # Summary
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        
        in_both = sum(1 for r in self.results if r['in_both'])
        in_allianz_only = sum(1 for r in self.results if r['in_allianz'] and not r['in_celer'])
        in_celer_only = sum(1 for r in self.results if r['in_celer'] and not r['in_allianz'])
        in_neither = sum(1 for r in self.results if not r['in_allianz'] and not r['in_celer'])
        
        print(f"✅ Found in BOTH systems: {in_both}/{len(self.SAMPLES)}")
        print(f"📋 Only in Allianz: {in_allianz_only}")
        print(f"📋 Only in Celer: {in_celer_only}")
        print(f"❌ In neither: {in_neither}")
        
        if in_both == len(self.SAMPLES):
            print("\n🎉 SUCCESS: All documented samples exist in both Celer and Allianz!")
        elif in_both > 0:
            print(f"\n⚠️ PARTIAL: {in_both} of {len(self.SAMPLES)} samples found in both systems")
        else:
            print("\n❌ NONE: No documented samples found in both systems")
        
        print("=" * 80)
        
        return in_both == len(self.SAMPLES)


def main():
    """
    Main test entry point
    """
    tester = ReadmeSamplesCrossCheck()
    success = tester.run_test()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
