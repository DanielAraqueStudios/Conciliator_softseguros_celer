"""
CONCILIATOR ALLIANZ - Main Program
Sistema de conciliación entre archivos Celer y Allianz
Identifica pólizas que requieren conciliación
"""

import sys
from pathlib import Path
import pandas as pd
import logging

# Add parent directory to import main reader
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import read_allianz_file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def select_file_from_folder(folder_path, extension, description):
    """
    List files in folder and let user select one
    If only one file exists, returns it automatically
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    
    # Find all files with extension
    files = list(folder.glob(f"*{extension}"))
    
    if len(files) == 0:
        raise FileNotFoundError(f"No {extension} files found in {folder}")
    
    if len(files) == 1:
        # Only one file, use it automatically
        print(f"\n[INFO] Archivo encontrado - {description}: {files[0].name}")
        return files[0]
    
    # Multiple files, show menu
    print(f"\n{description.upper()}")
    print("=" * 80)
    print(f"Se encontraron {len(files)} archivos. Seleccione uno:")
    print()
    
    for i, file in enumerate(files, 1):
        file_size = file.stat().st_size / 1024  # KB
        print(f"  {i}. {file.name} ({file_size:.2f} KB)")
    
    print("=" * 80)
    
    while True:
        try:
            selection = input(f"\nIngrese su opcion (1-{len(files)}): ").strip()
            index = int(selection) - 1
            
            if 0 <= index < len(files):
                selected_file = files[index]
                print(f"[OK] Seleccionado: {selected_file.name}")
                return selected_file
            else:
                print(f"[ERROR] Opcion invalida. Por favor ingrese un numero entre 1 y {len(files)}.")
        except ValueError:
            print("[ERROR] Por favor ingrese un numero valido.")
        except KeyboardInterrupt:
            print("\n\n[INFO] Proceso cancelado por el usuario.")
            sys.exit(0)


class AllianzConciliator:
    """
    Sistema de conciliación entre Celer y Allianz
    Identifica pólizas que requieren conciliación basándose en coincidencias
    """
    
    def __init__(self, celer_file_path, allianz_personas_path, allianz_colectivas_path, data_source='both'):
        self.celer_file = Path(celer_file_path)
        self.allianz_personas_file = Path(allianz_personas_path)
        self.allianz_colectivas_file = Path(allianz_colectivas_path)
        self.data_source = data_source.lower()  # 'personas', 'colectivas', or 'both'
        
        self.celer_df = None
        self.allianz_df = None
        
        self.results = {
            'to_reconcile': [],      # Exist in both - NEED RECONCILIATION
            'only_allianz': [],      # Only in Allianz - NOT IN CELER
            'only_celer': []         # Only in Celer - NOT IN ALLIANZ
        }
    
    def normalize_number(self, value):
        """
        Normalize policy/recibo numbers by removing leading zeros
        Handles: '023537654' -> '23537654'
        """
        try:
            return str(int(str(value).strip()))
        except (ValueError, TypeError):
            return str(value).strip()
    
    def load_celer_data(self):
        """Load and prepare Celer transformed data"""
        logger.info(f"Loading Celer file: {self.celer_file.name}")
        
        if not self.celer_file.exists():
            raise FileNotFoundError(f"Celer file not found: {self.celer_file}")
        
        self.celer_df = pd.read_excel(self.celer_file)
        
        # Verify columns
        if 'Poliza' not in self.celer_df.columns or 'Documento' not in self.celer_df.columns:
            raise ValueError(f"Required columns missing. Found: {list(self.celer_df.columns)}")
        
        # Normalize and create match key
        self.celer_df['_poliza_norm'] = self.celer_df['Poliza'].apply(self.normalize_number)
        self.celer_df['_documento_norm'] = self.celer_df['Documento'].apply(self.normalize_number)
        self.celer_df['_match_key'] = self.celer_df['_poliza_norm'] + "_" + self.celer_df['_documento_norm']
        
        logger.info(f"✓ Celer loaded: {len(self.celer_df)} records")
        return self.celer_df
    
    def load_allianz_data(self):
        """Load and prepare Allianz data based on data_source setting"""
        logger.info(f"Loading Allianz files ({self.data_source.upper()})...")
        
        dataframes = []
        
        # Load PERSONAS if requested
        if self.data_source in ['personas', 'both']:
            personas_df = read_allianz_file(str(self.allianz_personas_file))
            personas_df['_source'] = 'PERSONAS'
            logger.info(f"✓ PERSONAS: {len(personas_df)} records")
            dataframes.append(personas_df)
        
        # Load COLECTIVAS if requested
        if self.data_source in ['colectivas', 'both']:
            colectivas_df = read_allianz_file(str(self.allianz_colectivas_file))
            colectivas_df['_source'] = 'COLECTIVAS'
            logger.info(f"✓ COLECTIVAS: {len(colectivas_df)} records")
            dataframes.append(colectivas_df)
        
        # Combine loaded dataframes
        if not dataframes:
            raise ValueError(f"Invalid data_source: {self.data_source}. Must be 'personas', 'colectivas', or 'both'")
        
        self.allianz_df = pd.concat(dataframes, ignore_index=True)
        
        # Normalize and create match key
        self.allianz_df['_poliza_norm'] = self.allianz_df['Póliza'].apply(self.normalize_number)
        self.allianz_df['_recibo_norm'] = self.allianz_df['Recibo'].apply(self.normalize_number)
        self.allianz_df['_match_key'] = self.allianz_df['_poliza_norm'] + "_" + self.allianz_df['_recibo_norm']
        
        logger.info(f"✓ Allianz TOTAL: {len(self.allianz_df)} records")
        return self.allianz_df
    
    def perform_conciliation(self):
        """
        Perform conciliation analysis
        Identifies which policies need reconciliation
        """
        logger.info("Starting conciliation analysis...")
        
        # Get unique keys
        celer_keys = set(self.celer_df['_match_key'].unique())
        allianz_keys = set(self.allianz_df['_match_key'].unique())
        
        # Find matches
        matched_keys = celer_keys & allianz_keys
        only_allianz_keys = allianz_keys - celer_keys
        only_celer_keys = celer_keys - allianz_keys
        
        # Process records that NEED RECONCILIATION (in both systems)
        for key in matched_keys:
            celer_row = self.celer_df[self.celer_df['_match_key'] == key].iloc[0]
            allianz_row = self.allianz_df[self.allianz_df['_match_key'] == key].iloc[0]
            
            self.results['to_reconcile'].append({
                'poliza': celer_row['_poliza_norm'],
                'recibo': celer_row['_documento_norm'],
                'tomador_celer': celer_row.get('Tomador', 'N/A'),
                'cliente_allianz': allianz_row['Cliente - Tomador'],
                'source': allianz_row['_source'],
                'cartera_total_allianz': allianz_row.get('Cartera Total', 0),
                'vencida_allianz': allianz_row.get('Vencida', 0),
                'comision_allianz': allianz_row.get('Comisión', 0)
            })
        
        # Process records ONLY IN ALLIANZ (not in Celer)
        for key in only_allianz_keys:
            allianz_row = self.allianz_df[self.allianz_df['_match_key'] == key].iloc[0]
            
            self.results['only_allianz'].append({
                'poliza': allianz_row['_poliza_norm'],
                'recibo': allianz_row['_recibo_norm'],
                'cliente': allianz_row['Cliente - Tomador'],
                'source': allianz_row['_source'],
                'cartera_total': allianz_row.get('Cartera Total', 0)
            })
        
        # Process records ONLY IN CELER (not in Allianz)
        for key in only_celer_keys:
            celer_row = self.celer_df[self.celer_df['_match_key'] == key].iloc[0]
            
            self.results['only_celer'].append({
                'poliza': celer_row['_poliza_norm'],
                'documento': celer_row['_documento_norm'],
                'tomador': celer_row.get('Tomador', 'N/A'),
                'saldo': celer_row.get('Saldo', 0)
            })
        
        logger.info("Conciliation analysis completed")
    
    def print_report(self):
        """Print detailed conciliation report"""
        print("\n" + "=" * 80)
        print("REPORTE DE CONCILIACION ALLIANZ")
        print("=" * 80)
        
        # Summary
        print(f"\nRESUMEN:")
        print(f"  - Total Celer: {len(self.celer_df)} registros")
        print(f"  - Total Allianz: {len(self.allianz_df)} registros")
        print(f"  - Polizas unicas Celer: {len(set(self.celer_df['_match_key']))}")
        print(f"  - Polizas unicas Allianz: {len(set(self.allianz_df['_match_key']))}")
        
        # Policies that NEED RECONCILIATION
        print("\n" + "=" * 80)
        print("[OK] CARTERA PENDIENTE (Existen en ambos sistemas)")
        print("=" * 80)
        print(f"Total: {len(self.results['to_reconcile'])} polizas")
        
        if self.results['to_reconcile']:
            print("\nDetalle:")
            for i, record in enumerate(self.results['to_reconcile'], 1):
                print(f"\n  {i}. Poliza: {record['poliza']} | Recibo: {record['recibo']}")
                print(f"     Celer:   {record['tomador_celer']}")
                print(f"     Allianz: {record['cliente_allianz']} ({record['source']})")
                print(f"     Cartera: ${record['cartera_total_allianz']:,.0f} | Vencida: ${record['vencida_allianz']:,.0f}")
                print(f"     Comision: ${record['comision_allianz']:,.2f}")
        else:
            print("\n  ⚠️ No hay pólizas para conciliar")
        
        # Policies ONLY IN ALLIANZ (not in Celer)
        print("\n" + "=" * 80)
        print("[ALERTA] POLIZAS PAGADAS - FALTAN EN SISTEMA CELER")
        print("(Estas polizas fueron pagadas por el cliente pero no estan actualizadas en su sistema)")
        print("=" * 80)
        print(f"Total: {len(self.results['only_allianz'])} polizas")
        
        if len(self.results['only_allianz']) > 0:
            print(f"\nPrimeras 10 polizas:")
            for i, record in enumerate(self.results['only_allianz'][:10], 1):
                print(f"  {i}. Poliza: {record['poliza']} | Recibo: {record['recibo']}")
                print(f"     Cliente: {record['cliente']} ({record['source']})")
                print(f"     Cartera Total: ${record['cartera_total']:,.0f}")
        
        # Policies ONLY IN CELER (not in Allianz)
        print("\n" + "=" * 80)
        print("[INFO] POLIZAS SOLO EN CELER (No encontradas en Allianz)")
        print("=" * 80)
        print(f"Total: {len(self.results['only_celer'])} polizas")
        
        if len(self.results['only_celer']) > 0:
            print(f"\nPrimeras 10 polizas:")
            for i, record in enumerate(self.results['only_celer'][:10], 1):
                print(f"  {i}. Poliza: {record['poliza']} | Documento: {record['documento']}")
                print(f"     Tomador: {record['tomador']}")
                print(f"     Saldo: ${record['saldo']:,.0f}")
        
        # Statistics
        print("\n" + "=" * 80)
        print("ESTADISTICAS DE CONCILIACION")
        print("=" * 80)
        
        total_to_reconcile = len(self.results['to_reconcile'])
        total_only_allianz = len(self.results['only_allianz'])
        total_only_celer = len(self.results['only_celer'])
        
        print(f"\n[OK] Cartera pendiente: {total_to_reconcile}")
        print(f"[ALERTA] Pagadas - Faltan en sistema: {total_only_allianz}")
        print(f"[INFO]   Solo en Celer: {total_only_celer}")
        
        if len(self.allianz_df) > 0:
            match_rate = (total_to_reconcile / len(set(self.allianz_df['_match_key']))) * 100
            print(f"\nTasa de coincidencia Allianz: {match_rate:.2f}%")
        
        if len(self.celer_df) > 0:
            match_rate = (total_to_reconcile / len(set(self.celer_df['_match_key']))) * 100
            print(f"Tasa de coincidencia Celer: {match_rate:.2f}%")
        
        print("\n" + "=" * 80)
    
    def run(self):
        """Execute conciliation workflow"""
        try:
            print("\n" + "=" * 80)
            print("INICIANDO CONCILIACIÓN ALLIANZ")
            print("=" * 80)
            
            # Load data
            self.load_celer_data()
            self.load_allianz_data()
            
            # Perform conciliation
            self.perform_conciliation()
            
            # Print report
            self.print_report()
            
            return True
            
        except Exception as e:
            logger.error(f"Conciliation failed: {e}", exc_info=True)
            print(f"\n[ERROR]: {e}")
            return False


def main():
    """Main entry point"""
    # Display menu and get user selection
    print("\n" + "=" * 80)
    print("CONCILIADOR ALLIANZ - SELECCION DE DATOS")
    print("=" * 80)
    print("\nSeleccione que datos de Allianz desea procesar:")
    print("\n  1. PERSONAS solamente")
    print("  2. COLECTIVAS solamente")
    print("  3. AMBOS (PERSONAS + COLECTIVAS)")
    print("\n" + "=" * 80)
    
    # Get user input
    while True:
        try:
            selection = input("\nIngrese su opcion (1-3): ").strip()
            
            if selection == '1':
                data_source = 'personas'
                break
            elif selection == '2':
                data_source = 'colectivas'
                break
            elif selection == '3':
                data_source = 'both'
                break
            else:
                print("[ERROR] Opcion invalida. Por favor ingrese 1, 2 o 3.")
        except KeyboardInterrupt:
            print("\n\n[INFO] Proceso cancelado por el usuario.")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Error al leer entrada: {e}")
    
    # Define folder paths
    base_dir = Path(__file__).parent
    celer_folder = base_dir.parent / "TRANSFORMER CELER" / "output"
    personas_folder = base_dir / "INPUT" / "PERSONAS"
    colectivas_folder = base_dir / "INPUT" / "COLECTIVAS"
    
    # Select files from folders
    print("\n" + "=" * 80)
    print("SELECCION DE ARCHIVOS")
    print("=" * 80)
    
    celer_file = select_file_from_folder(celer_folder, ".xlsx", "Archivo Celer Transformado")
    allianz_personas = select_file_from_folder(personas_folder, ".xlsb", "Archivo Allianz PERSONAS")
    allianz_colectivas = select_file_from_folder(colectivas_folder, ".xlsb", "Archivo Allianz COLECTIVAS")
    
    # Create conciliator
    conciliator = AllianzConciliator(
        celer_file_path=celer_file,
        allianz_personas_path=allianz_personas,
        allianz_colectivas_path=allianz_colectivas,
        data_source=data_source
    )
    
    # Run conciliation
    success = conciliator.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
