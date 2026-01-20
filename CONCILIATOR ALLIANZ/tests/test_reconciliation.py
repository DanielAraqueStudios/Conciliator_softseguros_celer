"""
Reconciliation Test: Celer vs Allianz
Match policies and receipts between Celer transformed file and Allianz input files
"""

import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path to import main module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main import read_allianz_file
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class CelerAllianzReconciliation:
    """
    Reconcile Celer transformed data with Allianz input data
    
    Matching Logic:
    - Celer Column F (Poliza) ↔ Allianz Column B (Póliza)
    - Celer Column G (Documento) ↔ Allianz Column H (Recibo)
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.celer_file = Path(__file__).parent.parent.parent / "TRANSFORMER CELER" / "output" / "Cartera_Transformada_XML_20260119_110557.xlsx"
        self.allianz_input_dir = self.base_dir / "INPUT"
        
        self.celer_df = None
        self.allianz_personas_df = None
        self.allianz_colectivas_df = None
        self.allianz_combined_df = None
        
        self.results = {
            'matched': [],
            'celer_only': [],
            'allianz_only': [],
            'partial_match_poliza': [],
            'partial_match_recibo': []
        }
    
    def load_celer_data(self):
        """
        Load Celer transformed file
        Expected columns: F (Poliza), G (Documento)
        """
        logger.info(f"Loading Celer file: {self.celer_file}")
        
        if not self.celer_file.exists():
            raise FileNotFoundError(f"Celer file not found: {self.celer_file}")
        
        # Read Excel file
        self.celer_df = pd.read_excel(self.celer_file)
        
        logger.info(f"Celer data loaded: {len(self.celer_df)} rows, {len(self.celer_df.columns)} columns")
        logger.info(f"Celer columns: {list(self.celer_df.columns)}")
        
        # Verify required columns exist
        if 'Poliza' not in self.celer_df.columns:
            raise ValueError(f"Column 'Poliza' not found in Celer file. Available: {list(self.celer_df.columns)}")
        if 'Documento' not in self.celer_df.columns:
            raise ValueError(f"Column 'Documento' not found in Celer file. Available: {list(self.celer_df.columns)}")
        
        # Create unique key for matching (Poliza + Documento)
        self.celer_df['_match_key'] = (
            self.celer_df['Poliza'].astype(str).str.strip() + "_" + 
            self.celer_df['Documento'].astype(str).str.strip()
        )
        
        return self.celer_df
    
    def load_allianz_data(self):
        """
        Load both Allianz input files (PERSONAS and COLECTIVAS)
        Expected columns: B (Póliza), H (Recibo)
        """
        logger.info("Loading Allianz files...")
        
        # Load PERSONAS
        personas_file = self.allianz_input_dir / "PERSONAS" / "Informe Intermediario UNION AGENCIA DE SEGUROS LTDA_1701932_11_Jan_2026 (2).xlsb"
        self.allianz_personas_df = read_allianz_file(str(personas_file))
        self.allianz_personas_df['_source'] = 'PERSONAS'
        
        # Load COLECTIVAS
        colectivas_file = self.allianz_input_dir / "COLECTIVAS" / "Informe Intermediario UNION AGENCIA DE SEGUROS LTDA_1701932_11_Jan_2026 (1).xlsb"
        self.allianz_colectivas_df = read_allianz_file(str(colectivas_file))
        self.allianz_colectivas_df['_source'] = 'COLECTIVAS'
        
        # Combine both files
        self.allianz_combined_df = pd.concat([
            self.allianz_personas_df,
            self.allianz_colectivas_df
        ], ignore_index=True)
        
        logger.info(f"Allianz PERSONAS: {len(self.allianz_personas_df)} rows")
        logger.info(f"Allianz COLECTIVAS: {len(self.allianz_colectivas_df)} rows")
        logger.info(f"Allianz COMBINED: {len(self.allianz_combined_df)} rows")
        
        # Create unique key for matching (Póliza + Recibo)
        self.allianz_combined_df['_match_key'] = (
            self.allianz_combined_df['Póliza'].astype(str).str.strip() + "_" + 
            self.allianz_combined_df['Recibo'].astype(str).str.strip()
        )
        
        return self.allianz_combined_df
    
    def perform_reconciliation(self):
        """
        Perform reconciliation between Celer and Allianz data
        """
        logger.info("Starting reconciliation...")
        
        # Get unique keys from both datasets
        celer_keys = set(self.celer_df['_match_key'].unique())
        allianz_keys = set(self.allianz_combined_df['_match_key'].unique())
        
        # Find matches and differences
        matched_keys = celer_keys & allianz_keys
        celer_only_keys = celer_keys - allianz_keys
        allianz_only_keys = allianz_keys - celer_keys
        
        # Store matched records
        for key in matched_keys:
            celer_row = self.celer_df[self.celer_df['_match_key'] == key].iloc[0]
            allianz_row = self.allianz_combined_df[self.allianz_combined_df['_match_key'] == key].iloc[0]
            
            self.results['matched'].append({
                'poliza': celer_row['Poliza'],
                'documento': celer_row['Documento'],
                'tomador_celer': celer_row.get('Tomador', 'N/A'),
                'cliente_allianz': allianz_row['Cliente - Tomador'],
                'source': allianz_row['_source']
            })
        
        # Store Celer-only records
        for key in celer_only_keys:
            celer_row = self.celer_df[self.celer_df['_match_key'] == key].iloc[0]
            self.results['celer_only'].append({
                'poliza': celer_row['Poliza'],
                'documento': celer_row['Documento'],
                'tomador': celer_row.get('Tomador', 'N/A')
            })
        
        # Store Allianz-only records
        for key in allianz_only_keys:
            allianz_row = self.allianz_combined_df[self.allianz_combined_df['_match_key'] == key].iloc[0]
            self.results['allianz_only'].append({
                'poliza': allianz_row['Póliza'],
                'recibo': allianz_row['Recibo'],
                'cliente': allianz_row['Cliente - Tomador'],
                'source': allianz_row['_source']
            })
        
        # Find partial matches (same Poliza but different Recibo/Documento)
        celer_polizas = set(self.celer_df['Poliza'].astype(str).str.strip().unique())
        allianz_polizas = set(self.allianz_combined_df['Póliza'].astype(str).str.strip().unique())
        
        common_polizas = celer_polizas & allianz_polizas
        
        for poliza in common_polizas:
            celer_docs = set(self.celer_df[self.celer_df['Poliza'].astype(str).str.strip() == poliza]['Documento'].astype(str).str.strip().unique())
            allianz_recibos = set(self.allianz_combined_df[self.allianz_combined_df['Póliza'].astype(str).str.strip() == poliza]['Recibo'].astype(str).str.strip().unique())
            
            # Find documents that don't match
            only_in_celer = celer_docs - allianz_recibos
            only_in_allianz = allianz_recibos - celer_docs
            
            if only_in_celer or only_in_allianz:
                self.results['partial_match_poliza'].append({
                    'poliza': poliza,
                    'celer_documentos': list(celer_docs),
                    'allianz_recibos': list(allianz_recibos),
                    'only_in_celer': list(only_in_celer),
                    'only_in_allianz': list(only_in_allianz)
                })
        
        logger.info("Reconciliation completed")
    
    def print_report(self):
        """
        Print detailed reconciliation report
        """
        print("\n" + "=" * 80)
        print("CELER ↔ ALLIANZ RECONCILIATION REPORT")
        print("=" * 80)
        
        print(f"\n📊 DATA LOADED:")
        print(f"  - Celer records: {len(self.celer_df)}")
        print(f"  - Allianz PERSONAS: {len(self.allianz_personas_df)}")
        print(f"  - Allianz COLECTIVAS: {len(self.allianz_colectivas_df)}")
        print(f"  - Allianz TOTAL: {len(self.allianz_combined_df)}")
        
        print(f"\n✅ MATCHED RECORDS (Poliza + Documento/Recibo):")
        print(f"  Total: {len(self.results['matched'])}")
        
        if self.results['matched']:
            print(f"\n  First 5 matches:")
            for i, match in enumerate(self.results['matched'][:5], 1):
                print(f"    {i}. Poliza: {match['poliza']} | Documento: {match['documento']}")
                print(f"       Celer: {match['tomador_celer']}")
                print(f"       Allianz: {match['cliente_allianz']} ({match['source']})")
        
        print(f"\n⚠️ CELER ONLY (Not found in Allianz):")
        print(f"  Total: {len(self.results['celer_only'])}")
        
        if self.results['celer_only']:
            print(f"\n  First 5 Celer-only records:")
            for i, record in enumerate(self.results['celer_only'][:5], 1):
                print(f"    {i}. Poliza: {record['poliza']} | Documento: {record['documento']} | {record['tomador']}")
        
        print(f"\n⚠️ ALLIANZ ONLY (Not found in Celer):")
        print(f"  Total: {len(self.results['allianz_only'])}")
        
        if self.results['allianz_only']:
            print(f"\n  First 5 Allianz-only records:")
            for i, record in enumerate(self.results['allianz_only'][:5], 1):
                print(f"    {i}. Poliza: {record['poliza']} | Recibo: {record['recibo']} | {record['cliente']} ({record['source']})")
        
        print(f"\n🔍 PARTIAL MATCHES (Same Poliza, Different Documento/Recibo):")
        print(f"  Total: {len(self.results['partial_match_poliza'])}")
        
        if self.results['partial_match_poliza']:
            print(f"\n  First 3 partial matches:")
            for i, partial in enumerate(self.results['partial_match_poliza'][:3], 1):
                print(f"    {i}. Poliza: {partial['poliza']}")
                print(f"       Celer Documentos: {partial['celer_documentos']}")
                print(f"       Allianz Recibos: {partial['allianz_recibos']}")
                if partial['only_in_celer']:
                    print(f"       ⚠️ Only in Celer: {partial['only_in_celer']}")
                if partial['only_in_allianz']:
                    print(f"       ⚠️ Only in Allianz: {partial['only_in_allianz']}")
        
        # Calculate statistics
        print(f"\n📈 RECONCILIATION STATISTICS:")
        total_unique_celer = len(self.celer_df['_match_key'].unique())
        total_unique_allianz = len(self.allianz_combined_df['_match_key'].unique())
        matched_count = len(self.results['matched'])
        
        if total_unique_celer > 0:
            match_rate_celer = (matched_count / total_unique_celer) * 100
            print(f"  - Celer Match Rate: {match_rate_celer:.2f}% ({matched_count}/{total_unique_celer})")
        
        if total_unique_allianz > 0:
            match_rate_allianz = (matched_count / total_unique_allianz) * 100
            print(f"  - Allianz Match Rate: {match_rate_allianz:.2f}% ({matched_count}/{total_unique_allianz})")
        
        print("\n" + "=" * 80)
    
    def run(self):
        """
        Execute full reconciliation workflow
        """
        try:
            # Load data
            self.load_celer_data()
            self.load_allianz_data()
            
            # Perform reconciliation
            self.perform_reconciliation()
            
            # Print report
            self.print_report()
            
            return True
            
        except Exception as e:
            logger.error(f"Reconciliation failed: {e}", exc_info=True)
            print(f"\n❌ ERROR: {e}")
            return False


def main():
    """
    Main test entry point
    """
    print("\n" + "=" * 80)
    print("CELER-ALLIANZ RECONCILIATION TEST")
    print("=" * 80)
    print("\nMatching Logic:")
    print("  Celer Poliza (Column F) ↔ Allianz Póliza (Column B)")
    print("  Celer Documento (Column G) ↔ Allianz Recibo (Column H)")
    print("=" * 80)
    
    reconciler = CelerAllianzReconciliation()
    success = reconciler.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
