"""
CONCILIATOR ALLIANZ - Main Program
Sistema de conciliación entre archivos Celer y Allianz
Identifica pólizas que requieren conciliación
"""

import sys
from pathlib import Path
import pandas as pd
import logging
from datetime import datetime

# Add parent directory to import main reader
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import read_allianz_file  # Import from root main.py

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
    Sistema de conciliación entre Softseguros, Celer y Allianz
    Identifica pólizas que requieren conciliación basándose en coincidencias
    Prioridad: Softseguros > Celer
    """
    
    def __init__(self, allianz_personas_path, allianz_colectivas_path, data_source='both', 
                 data_source_type='both', softseguros_file_path=None, celer_file_path=None):
        self.allianz_personas_file = Path(allianz_personas_path) if allianz_personas_path else None
        self.allianz_colectivas_file = Path(allianz_colectivas_path) if allianz_colectivas_path else None
        self.data_source = data_source.lower()  # 'personas', 'colectivas', or 'both'
        self.data_source_type = data_source_type.lower()  # 'softseguros', 'celer', or 'both'
        
        self.softseguros_file = Path(softseguros_file_path) if softseguros_file_path else None
        self.celer_file = Path(celer_file_path) if celer_file_path else None
        
        self.softseguros_df = None
        self.celer_df = None
        self.combined_df = None  # Softseguros + Celer combinados con prioridad
        self.allianz_df = None
        
        self.results = {
            'no_pagado': [],                    # Caso 1: Poliza + Recibo + Fecha coinciden - NO HAN PAGADO
            'actualizar_sistema': [],           # Caso 2: Poliza + Fecha coinciden, Recibo diferente - ACTUALIZAR SISTEMA
            'actualizar_recibo_softseguros': [], # Caso 2 especial: Sin anexo en Softseguros - ACTUALIZAR RECIBO EN SOFTSEGUROS
            'corregir_poliza': [],              # Caso 3: No coincide poliza - CORREGIR POLIZA
            'only_allianz': [],                 # Solo en Allianz
            'only_combined': []                 # Solo en Softseguros/Celer combinados
        }
    
    def normalize_number(self, value):
        """
        Normalize policy/recibo numbers by removing leading zeros
        Handles: '023537654' -> '23537654'
        Examples:
          - '023178309' -> '23178309' ✓
          - '0023178309' -> '23178309' ✓
          - '23178309' -> '23178309' ✓
        """
        try:
            # Convert to int to remove leading zeros, then back to string
            result = str(int(str(value).strip()))
            return result
        except (ValueError, TypeError):
            # If conversion fails, just strip spaces
            return str(value).strip()
    
    def normalize_recibo(self, value):
        """
        Normalize recibo numbers to last 9 significant digits for matching
        Allianz recibos are always 9 digits, but Celer may have 10+ digits
        
        Examples:
          - '1347216594' (10 digits) -> '347216594' (last 9)
          - '347216594' (9 digits) -> '347216594' (unchanged)
          - '023527545' (with leading zeros) -> '023527545' normalized to '23527545' -> '23527545' (last 9)
        
        Logic: First remove leading zeros, then take last 9 digits
        """
        try:
            # First normalize to remove leading zeros
            normalized = self.normalize_number(value)
            # Take last 9 digits for matching (Allianz standard)
            return normalized[-9:] if len(normalized) >= 9 else normalized
        except (ValueError, TypeError):
            return str(value).strip()
    
    def load_softseguros_data(self):
        """Load and prepare Softseguros data"""
        logger.info(f"Loading Softseguros file: {self.softseguros_file.name}")
        
        if not self.softseguros_file.exists():
            raise FileNotFoundError(f"Softseguros file not found: {self.softseguros_file}")
        
        self.softseguros_df = pd.read_excel(self.softseguros_file)
        
        # Verify columns
        required_cols = ['NÚMERO PÓLIZA', 'NÚMERO ANEXO', 'FECHA INICIO', 'ASEGURADORA']
        missing = [col for col in required_cols if col not in self.softseguros_df.columns]
        if missing:
            raise ValueError(f"Required columns missing: {missing}. Found: {list(self.softseguros_df.columns)}")
        
        # Filter: Only ALLIANZ
        total_before = len(self.softseguros_df)
        self.softseguros_df = self.softseguros_df[
            self.softseguros_df['ASEGURADORA'].str.upper().str.contains('ALLIANZ', na=False)
        ].copy()
        logger.info(f"✓ Filtered Softseguros by 'ALLIANZ': {len(self.softseguros_df)}/{total_before} records")
        
        # Normalize and create match keys
        self.softseguros_df['_poliza_norm'] = self.softseguros_df['NÚMERO PÓLIZA'].apply(self.normalize_number)
        self.softseguros_df['_anexo_norm'] = self.softseguros_df['NÚMERO ANEXO'].apply(self.normalize_recibo)
        self.softseguros_df['_fecha_inicio_str'] = pd.to_datetime(self.softseguros_df['FECHA INICIO'], errors='coerce').dt.strftime('%Y-%m-%d')
        
        # Mark records without anexo
        self.softseguros_df['_tiene_anexo'] = self.softseguros_df['NÚMERO ANEXO'].notna()
        
        # Match keys: completo (poliza+anexo+fecha) solo si tiene anexo, parcial (poliza+fecha) para todos
        self.softseguros_df['_match_key_full'] = self.softseguros_df.apply(
            lambda row: row['_poliza_norm'] + "_" + row['_anexo_norm'] + "_" + row['_fecha_inicio_str'] 
            if row['_tiene_anexo'] else None, axis=1
        )
        self.softseguros_df['_match_key_partial'] = self.softseguros_df['_poliza_norm'] + "_" + self.softseguros_df['_fecha_inicio_str']
        
        # Mark source
        self.softseguros_df['_source'] = 'SOFTSEGUROS'
        
        # Count records with/without anexo
        con_anexo = self.softseguros_df['_tiene_anexo'].sum()
        sin_anexo = len(self.softseguros_df) - con_anexo
        logger.info(f"✓ Softseguros: {con_anexo} con anexo, {sin_anexo} sin anexo")
        
        return self.softseguros_df
    
    def load_celer_data(self):
        """Load and prepare Celer transformed data"""
        logger.info(f"Loading Celer file: {self.celer_file.name}")
        
        if not self.celer_file.exists():
            raise FileNotFoundError(f"Celer file not found: {self.celer_file}")
        
        self.celer_df = pd.read_excel(self.celer_file)
        
        # Verify columns
        required_cols = ['Poliza', 'Documento', 'F_Inicio', 'Aseguradora']
        missing = [col for col in required_cols if col not in self.celer_df.columns]
        if missing:
            raise ValueError(f"Required columns missing: {missing}. Found: {list(self.celer_df.columns)}")
        
        # Filter: Only ALLIANZ SEGUROS S.A
        total_before = len(self.celer_df)
        self.celer_df = self.celer_df[
            self.celer_df['Aseguradora'].str.upper().str.contains('ALLIANZ', na=False)
        ].copy()
        logger.info(f"✓ Filtered by Aseguradora 'ALLIANZ': {len(self.celer_df)}/{total_before} records")
        
        # Normalize and create match keys
        self.celer_df['_poliza_norm'] = self.celer_df['Poliza'].apply(self.normalize_number)
        self.celer_df['_documento_norm'] = self.celer_df['Documento'].apply(self.normalize_recibo)  # Last 9 digits
        self.celer_df['_fecha_inicio_str'] = pd.to_datetime(self.celer_df['F_Inicio'], errors='coerce').dt.strftime('%Y-%m-%d')
        
        # Match keys: completo (poliza+recibo+fecha) y parcial (poliza+fecha)
        self.celer_df['_match_key_full'] = self.celer_df['_poliza_norm'] + "_" + self.celer_df['_documento_norm'] + "_" + self.celer_df['_fecha_inicio_str']
        self.celer_df['_match_key_partial'] = self.celer_df['_poliza_norm'] + "_" + self.celer_df['_fecha_inicio_str']
        
        # Mark source
        self.celer_df['_source'] = 'CELER'
        self.celer_df['_tiene_anexo'] = True  # Celer siempre tiene documento
        
        logger.info(f"✓ Celer loaded: {len(self.celer_df)} records")
        return self.celer_df
    
    def combine_data_sources(self):
        """
        Combine Softseguros and Celer data with priority to Softseguros
        Remove duplicates from Celer if they exist in Softseguros (same poliza+fecha)
        """
        logger.info("Combining Softseguros and Celer with prioritization...")
        
        if self.softseguros_df is None or self.celer_df is None:
            raise ValueError("Must load both Softseguros and Celer data first")
        
        # Create sets of partial keys from Softseguros (poliza+fecha)
        soft_partial_keys = set(self.softseguros_df['_match_key_partial'].dropna())
        
        # Filter Celer: Keep only records NOT in Softseguros
        celer_unique = self.celer_df[~self.celer_df['_match_key_partial'].isin(soft_partial_keys)].copy()
        
        removed_duplicates = len(self.celer_df) - len(celer_unique)
        logger.info(f"✓ Removed {removed_duplicates} duplicates from Celer (exist in Softseguros)")
        
        # Combine: Softseguros + Celer únicos
        self.combined_df = pd.concat([self.softseguros_df, celer_unique], ignore_index=True)
        
        logger.info(f"✓ Combined data: {len(self.combined_df)} records")
        logger.info(f"   - From Softseguros: {len(self.softseguros_df)}")
        logger.info(f"   - From Celer (unique): {len(celer_unique)}")
        
        return self.combined_df
        return self.celer_df
    
    def load_allianz_data(self):
        """Load and prepare Allianz data based on data_source setting"""
        logger.info(f"Loading Allianz files ({self.data_source.upper()})...")
        
        dataframes = []
        
        # Load PERSONAS if requested
        if self.data_source in ['personas', 'both']:
            if self.allianz_personas_file is None or not self.allianz_personas_file.exists():
                raise FileNotFoundError(f"Allianz Personas file is required but not provided or doesn't exist")
            personas_df = read_allianz_file(str(self.allianz_personas_file))
            personas_df['_source'] = 'PERSONAS'
            logger.info(f"✓ PERSONAS: {len(personas_df)} records")
            dataframes.append(personas_df)
        
        # Load COLECTIVAS if requested
        if self.data_source in ['colectivas', 'both']:
            if self.allianz_colectivas_file is None or not self.allianz_colectivas_file.exists():
                raise FileNotFoundError(f"Allianz Colectivas file is required but not provided or doesn't exist")
            colectivas_df = read_allianz_file(str(self.allianz_colectivas_file))
            colectivas_df['_source'] = 'COLECTIVAS'
            logger.info(f"✓ COLECTIVAS: {len(colectivas_df)} records")
            dataframes.append(colectivas_df)
        
        # Combine loaded dataframes
        if not dataframes:
            raise ValueError(f"Invalid data_source: {self.data_source}. Must be 'personas', 'colectivas', or 'both'")
        
        self.allianz_df = pd.concat(dataframes, ignore_index=True)
        
        # Normalize and create match keys
        self.allianz_df['_poliza_norm'] = self.allianz_df['Póliza'].apply(self.normalize_number)
        self.allianz_df['_recibo_norm'] = self.allianz_df['Recibo'].apply(self.normalize_recibo)  # Last 9 digits
        
        # Convert Excel serial dates to datetime
        # Excel dates are stored as integers (days since 1899-12-30)
        def convert_excel_date(serial_date):
            if pd.isna(serial_date):
                return 'NaT'
            try:
                # Excel origin is 1899-12-30 (not 1900-01-01 due to Excel bug)
                dt = pd.to_datetime('1899-12-30') + pd.to_timedelta(int(serial_date), unit='D')
                return dt.strftime('%Y-%m-%d')
            except:
                return 'NaT'
        
        self.allianz_df['_fecha_inicio_str'] = self.allianz_df['F.INI VIG'].apply(convert_excel_date)
        
        # Match keys: completo (poliza+recibo+fecha) y parcial (poliza+fecha)
        self.allianz_df['_match_key_full'] = self.allianz_df['_poliza_norm'] + "_" + self.allianz_df['_recibo_norm'] + "_" + self.allianz_df['_fecha_inicio_str']
        self.allianz_df['_match_key_partial'] = self.allianz_df['_poliza_norm'] + "_" + self.allianz_df['_fecha_inicio_str']
        
        logger.info(f"✓ Allianz TOTAL: {len(self.allianz_df)} records")
        return self.allianz_df
    
    def perform_conciliation(self):
        """
        Perform conciliation analysis with cases:
        1. Full match (poliza + recibo + fecha) - NO HAN PAGADO
        2. Partial match (poliza + fecha, diff recibo) - ACTUALIZAR SISTEMA
        2 especial. Softseguros sin anexo - ACTUALIZAR RECIBO EN SOFTSEGUROS
        3. No match on poliza - CORREGIR POLIZA
        """
        logger.info("Starting conciliation analysis...")
        
        if self.combined_df is None:
            raise ValueError("Must combine data sources first")
        
        # Get unique keys from combined data (Softseguros + Celer únicos)
        combined_keys_full = set(self.combined_df['_match_key_full'].dropna().unique())
        allianz_keys_full = set(self.allianz_df['_match_key_full'].unique())
        
        combined_keys_partial = set(self.combined_df['_match_key_partial'].unique())
        allianz_keys_partial = set(self.allianz_df['_match_key_partial'].unique())
        
        # CASO 1: Match completo (Poliza + Recibo + Fecha) - NO HAN PAGADO
        matched_full = combined_keys_full & allianz_keys_full
        for key in matched_full:
            combined_row = self.combined_df[self.combined_df['_match_key_full'] == key].iloc[0]
            allianz_row = self.allianz_df[self.allianz_df['_match_key_full'] == key].iloc[0]
            
            # Determine source-specific fields
            if combined_row['_source'] == 'SOFTSEGUROS':
                poliza_orig = combined_row['NÚMERO PÓLIZA']
                recibo_orig = combined_row['NÚMERO ANEXO']
                recibo_norm = combined_row['_anexo_norm']
                tomador = f"{combined_row.get('NOMBRES CLIENTE', '')} {combined_row.get('APELLIDOS CLIENTE', '')}".strip()
                saldo = combined_row.get('TOTAL', 0)
            else:  # CELER
                poliza_orig = combined_row['Poliza']
                recibo_orig = combined_row['Documento']
                recibo_norm = combined_row['_documento_norm']
                tomador = combined_row.get('Tomador', 'N/A')
                saldo = combined_row.get('Saldo', 0)
            
            self.results['no_pagado'].append({
                'poliza': combined_row['_poliza_norm'],
                'recibo': recibo_norm,
                'recibo_allianz': allianz_row['_recibo_norm'],
                'fecha_inicio': combined_row['_fecha_inicio_str'],
                'tomador': tomador,
                'cliente_allianz': allianz_row['Cliente - Tomador'],
                'source_data': combined_row['_source'],
                'source_allianz': allianz_row['_source'],
                'saldo': saldo,
                'cartera_total': allianz_row.get('Cartera Total', 0),
                'necesita_actualizar_softseguros': combined_row['_source'] == 'CELER'
            })
        
        # CASO 2 ESPECIAL: Softseguros sin anexo (Poliza + Fecha match, pero SIN anexo)
        # Estos deben reportarse como "Actualizar recibo en Softseguros"
        for key_partial in (combined_keys_partial & allianz_keys_partial):
            combined_rows = self.combined_df[self.combined_df['_match_key_partial'] == key_partial]
            
            for _, combined_row in combined_rows.iterrows():
                # Si es de Softseguros y NO tiene anexo
                if combined_row['_source'] == 'SOFTSEGUROS' and not combined_row['_tiene_anexo']:
                    # Buscar el match en Allianz
                    allianz_match = self.allianz_df[self.allianz_df['_match_key_partial'] == key_partial]
                    
                    if len(allianz_match) > 0:
                        allianz_row = allianz_match.iloc[0]
                        
                        self.results['actualizar_recibo_softseguros'].append({
                            'poliza': combined_row['_poliza_norm'],
                            'fecha_inicio': combined_row['_fecha_inicio_str'],
                            'recibo_allianz': allianz_row['_recibo_norm'],
                            'tomador': f"{combined_row.get('NOMBRES CLIENTE', '')} {combined_row.get('APELLIDOS CLIENTE', '')}".strip(),
                            'cliente_allianz': allianz_row['Cliente - Tomador'],
                            'source_allianz': allianz_row['_source'],
                            'saldo_softseguros': combined_row.get('TOTAL', 0),
                            'cartera_allianz': allianz_row.get('Cartera Total', 0),
                            'nota': 'Actualizar NÚMERO ANEXO en Softseguros'
                        })
        
        # CASO 2: Match parcial (Poliza + Fecha, diferente Recibo) - ACTUALIZAR SISTEMA
        # Solo para registros CON anexo/documento
        for key_partial in (combined_keys_partial & allianz_keys_partial):
            combined_rows = self.combined_df[self.combined_df['_match_key_partial'] == key_partial]
            allianz_rows = self.allianz_df[self.allianz_df['_match_key_partial'] == key_partial]
            
            for _, combined_row in combined_rows.iterrows():
                # Skip si es Softseguros sin anexo (ya procesado arriba)
                if combined_row['_source'] == 'SOFTSEGUROS' and not combined_row['_tiene_anexo']:
                    continue
                
                for _, allianz_row in allianz_rows.iterrows():
                    # Si la clave completa NO coincide = recibo diferente
                    if combined_row['_match_key_full'] != allianz_row['_match_key_full']:
                        
                        if combined_row['_source'] == 'SOFTSEGUROS':
                            recibo_combined = combined_row['_anexo_norm']
                            tomador = f"{combined_row.get('NOMBRES CLIENTE', '')} {combined_row.get('APELLIDOS CLIENTE', '')}".strip()
                            saldo = combined_row.get('TOTAL', 0)
                        else:  # CELER
                            recibo_combined = combined_row['_documento_norm']
                            tomador = combined_row.get('Tomador', 'N/A')
                            saldo = combined_row.get('Saldo', 0)
                        
                        self.results['actualizar_sistema'].append({
                            'poliza': combined_row['_poliza_norm'],
                            'fecha_inicio': combined_row['_fecha_inicio_str'],
                            'recibo_combinado': recibo_combined,
                            'recibo_allianz': allianz_row['_recibo_norm'],
                            'tomador': tomador,
                            'cliente_allianz': allianz_row['Cliente - Tomador'],
                            'source_data': combined_row['_source'],
                            'source_allianz': allianz_row['_source'],
                            'saldo_combinado': saldo,
                            'cartera_allianz': allianz_row.get('Cartera Total', 0)
                        })
        
        # CASO 3: CORREGIR POLIZA - Registros que no coinciden en póliza
        # Solo en Allianz (no en Combined)
        only_allianz_count = 0
        for key in allianz_keys_full:
            if key not in combined_keys_full:
                allianz_row = self.allianz_df[self.allianz_df['_match_key_full'] == key].iloc[0]
                # Verificar si al menos coincide parcialmente
                if allianz_row['_match_key_partial'] not in combined_keys_partial:
                    if only_allianz_count < 3:
                        logger.debug(f"Only Allianz #{only_allianz_count + 1}: Poliza='{allianz_row['_poliza_norm']}' | Key={key}")
                    
                    self.results['only_allianz'].append({
                        'poliza': allianz_row['_poliza_norm'],
                        'recibo': allianz_row['_recibo_norm'],
                        'fecha_inicio': allianz_row['_fecha_inicio_str'],
                        'cliente': allianz_row['Cliente - Tomador'],
                        'source': allianz_row['_source'],
                        'cartera_total': allianz_row.get('Cartera Total', 0)
                    })
                    only_allianz_count += 1
        
        # Solo en Combined (no en Allianz)
        only_combined_count = 0
        for key in combined_keys_full:
            if key not in allianz_keys_full:
                combined_row = self.combined_df[self.combined_df['_match_key_full'] == key].iloc[0]
                # Verificar si al menos coincide parcialmente
                if combined_row['_match_key_partial'] not in allianz_keys_partial:
                    if only_combined_count < 3:
                        logger.debug(f"Only Combined #{only_combined_count + 1}: Poliza='{combined_row['_poliza_norm']}' | Source={combined_row['_source']}")
                    
                    if combined_row['_source'] == 'SOFTSEGUROS':
                        tomador = f"{combined_row.get('NOMBRES CLIENTE', '')} {combined_row.get('APELLIDOS CLIENTE', '')}".strip()
                        saldo = combined_row.get('TOTAL', 0)
                    else:
                        tomador = combined_row.get('Tomador', 'N/A')
                        saldo = combined_row.get('Saldo', 0)
                    
                    self.results['only_combined'].append({
                        'poliza': combined_row['_poliza_norm'],
                        'recibo': combined_row.get('_anexo_norm', combined_row.get('_documento_norm', 'N/A')),
                        'fecha_inicio': combined_row['_fecha_inicio_str'],
                        'tomador': tomador,
                        'source': combined_row['_source'],
                        'saldo': saldo
                    })
                    only_combined_count += 1
        
        logger.info("Conciliation analysis completed")
    
    def save_report_to_file(self):
        """Save simplified conciliation report to text file"""
        # Create output directory if it doesn't exist
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"Reporte_Conciliacion_{timestamp}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write(f"REPORTE DE CONCILIACION ALLIANZ ({self.data_source_type.upper()})\n")
            f.write("=" * 80 + "\n")
            f.write(f"\nFecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Fuente de datos: {self.data_source_type.upper()}\n")
            f.write(f"Fuente de datos Allianz: {self.data_source.upper()}\n")
            
            # Summary
            f.write(f"\nRESUMEN:\n")
            if self.softseguros_df is not None and len(self.softseguros_df) > 0:
                f.write(f"  - Total Softseguros: {len(self.softseguros_df)} registros\n")
            if self.celer_df is not None and len(self.celer_df) > 0:
                f.write(f"  - Total Celer: {len(self.celer_df)} registros\n")
            if self.combined_df is not None:
                f.write(f"  - Total Combinado: {len(self.combined_df)} registros\n")
            f.write(f"  - Total Allianz: {len(self.allianz_df)} registros\n")
            
            # Results
            f.write(f"\nRESULTADOS:\n")
            f.write(f"  [CASO 1] No han pagado: {len(self.results['no_pagado'])}\n")
            f.write(f"  [CASO 2 ESPECIAL] Actualizar recibo en Softseguros: {len(self.results['actualizar_recibo_softseguros'])}\n")
            f.write(f"  [CASO 2] Actualizar sistema: {len(self.results['actualizar_sistema'])}\n")
            f.write(f"  [CASO 3] Solo en Allianz: {len(self.results['only_allianz'])}\n")
            f.write(f"  [CASO 3] Solo en Softseguros/Celer: {len(self.results['only_combined'])}\n")
            
            # CASO 1: NO HAN PAGADO - TODAS LAS POLIZAS
            f.write("\n" + "=" * 80 + "\n")
            f.write("[CASO 1] NO HAN PAGADO - CARTERA PENDIENTE\n")
            f.write("(Poliza + Recibo + Fecha coinciden en ambos sistemas)\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total: {len(self.results['no_pagado'])} polizas\n\n")
            
            if self.results['no_pagado']:
                for i, record in enumerate(self.results['no_pagado'], 1):
                    f.write(f"{i}. Poliza: {record['poliza']} | Recibo ({record['source_data']}): {record['recibo']} | Recibo Allianz: {record['recibo_allianz']} | Fecha: {record['fecha_inicio']}\n")
                    if record['necesita_actualizar_softseguros']:
                        f.write(f"   ⚠️  ACTUALIZAR RECIBO EN SOFTSEGUROS (actualmente solo en CELER)\n")
                    f.write(f"   Tomador ({record['source_data']}): {record['tomador']}\n")
                    f.write(f"   Cliente (Allianz): {record['cliente_allianz']}\n")
                    f.write(f"   Saldo ({record['source_data']}): ${record['saldo']:,.2f} | Cartera Allianz: ${record['cartera_total']:,.2f}\n\n")
            else:
                f.write("No hay polizas en este caso.\n\n")
            
            # CASO 2 ESPECIAL: ACTUALIZAR RECIBO EN SOFTSEGUROS - TODAS LAS POLIZAS
            f.write("\n" + "=" * 80 + "\n")
            f.write("[CASO 2 ESPECIAL] ACTUALIZAR RECIBO EN SOFTSEGUROS\n")
            f.write("(Poliza + Fecha coinciden, pero Softseguros NO tiene NÚMERO ANEXO)\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total: {len(self.results['actualizar_recibo_softseguros'])} polizas\n\n")
            
            if self.results['actualizar_recibo_softseguros']:
                for i, record in enumerate(self.results['actualizar_recibo_softseguros'], 1):
                    f.write(f"{i}. Poliza: {record['poliza']} | Fecha: {record['fecha_inicio']}\n")
                    f.write(f"   {record['nota']}\n")
                    f.write(f"   Recibo sugerido (Allianz): {record['recibo_allianz']}\n")
                    f.write(f"   Cliente: {record['tomador']}\n\n")
            else:
                f.write("No hay polizas en este caso.\n\n")
            
            # CASO 2: ACTUALIZAR SISTEMA - TODAS LAS POLIZAS
            f.write("\n" + "=" * 80 + "\n")
            f.write("[CASO 2] ACTUALIZAR EN SISTEMA\n")
            f.write("(Poliza + Fecha coinciden, pero DIFERENTE numero de recibo)\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total: {len(self.results['actualizar_sistema'])} polizas\n\n")
            
            if self.results['actualizar_sistema']:
                for i, record in enumerate(self.results['actualizar_sistema'], 1):
                    f.write(f"{i}. Poliza: {record['poliza']} | Fecha: {record['fecha_inicio']}\n")
                    f.write(f"   Recibo ({record['source_data']}): {record['recibo_combinado']} | Recibo Allianz: {record['recibo_allianz']}\n")
                    f.write(f"   Tomador ({record['source_data']}): {record['tomador']}\n")
                    f.write(f"   Cliente (Allianz): {record['cliente_allianz']}\n")
                    f.write(f"   Saldo ({record['source_data']}): ${record['saldo_combinado']:,.2f} | Cartera Allianz: ${record['cartera_allianz']:,.2f}\n\n")
            else:
                f.write("No hay polizas en este caso.\n\n")
            
            # CASO 3: SOLO EN ALLIANZ - TODAS LAS POLIZAS
            f.write("\n" + "=" * 80 + "\n")
            f.write("[CASO 3] CORREGIR POLIZA - Solo en Allianz\n")
            f.write("(Polizas en Allianz que NO coinciden con ninguna en Softseguros/Celer)\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total: {len(self.results['only_allianz'])} polizas\n\n")
            
            if self.results['only_allianz']:
                for i, record in enumerate(self.results['only_allianz'], 1):
                    f.write(f"{i}. Poliza: {record['poliza']} | Recibo: {record['recibo']} | Fecha: {record['fecha_inicio']}\n")
                    f.write(f"   Cliente: {record['cliente']}\n")
                    f.write(f"   Source: {record['source']} | Cartera Total: ${record['cartera_total']:,.2f}\n\n")
            else:
                f.write("No hay polizas en este caso.\n\n")
            
            # CASO 3: SOLO EN COMBINED - TODAS LAS POLIZAS
            f.write("\n" + "=" * 80 + "\n")
            f.write("[CASO 3] CORREGIR POLIZA - Solo en Softseguros/Celer\n")
            f.write("(Polizas en Softseguros/Celer que NO coinciden con ninguna en Allianz)\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total: {len(self.results['only_combined'])} polizas\n\n")
            
            if self.results['only_combined']:
                for i, record in enumerate(self.results['only_combined'], 1):
                    f.write(f"{i}. Poliza: {record['poliza']} | Recibo: {record['recibo']} | Fecha: {record['fecha_inicio']}\n")
                    f.write(f"   Tomador: {record['tomador']}\n")
                    f.write(f"   Source: {record['source']} | Saldo: ${record['saldo']:,.2f}\n\n")
            else:
                f.write("No hay polizas en este caso.\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("REPORTE COMPLETO GUARDADO\n")
            f.write("=" * 80 + "\n")
        
        return output_file
    
    def print_report(self):
        """Print simplified conciliation report"""
        print("\n" + "=" * 80)
        print(f"REPORTE DE CONCILIACION ALLIANZ ({self.data_source_type.upper()})")
        print("=" * 80)
        
        # Summary
        print(f"\nRESUMEN:")
        if self.softseguros_df is not None and len(self.softseguros_df) > 0:
            print(f"  - Total Softseguros: {len(self.softseguros_df)} registros")
        if self.celer_df is not None and len(self.celer_df) > 0:
            print(f"  - Total Celer: {len(self.celer_df)} registros")
        if self.combined_df is not None:
            print(f"  - Total Combinado (con prioridad Softseguros): {len(self.combined_df)} registros")
        print(f"  - Total Allianz: {len(self.allianz_df)} registros")
        
        # CASO 1: NO HAN PAGADO - TODAS LAS POLIZAS
        print("\n" + "=" * 80)
        print("[CASO 1] NO HAN PAGADO - CARTERA PENDIENTE")
        print("(Poliza + Recibo + Fecha coinciden en ambos sistemas)")
        print("=" * 80)
        print(f"Total: {len(self.results['no_pagado'])} polizas\n")
        
        if self.results['no_pagado']:
            for i, record in enumerate(self.results['no_pagado'], 1):
                print(f"{i}. Poliza: {record['poliza']} | Recibo ({record['source_data']}): {record['recibo']} | Recibo Allianz: {record['recibo_allianz']} | Fecha: {record['fecha_inicio']}")
                if record['necesita_actualizar_softseguros']:
                    print(f"   ⚠️  ACTUALIZAR RECIBO EN SOFTSEGUROS (actualmente solo en CELER)")
                print(f"   Tomador ({record['source_data']}): {record['tomador']}")
                print(f"   Cliente (Allianz): {record['cliente_allianz']}")
                print(f"   Saldo ({record['source_data']}): ${record['saldo']:,.2f} | Cartera Allianz: ${record['cartera_total']:,.2f}\n")
        else:
            print("No hay polizas en este caso.\n")
        
        # CASO 2 ESPECIAL: ACTUALIZAR RECIBO EN SOFTSEGUROS - TODAS LAS POLIZAS
        print("\n" + "=" * 80)
        print("[CASO 2 ESPECIAL] ACTUALIZAR RECIBO EN SOFTSEGUROS")
        print("(Poliza + Fecha coinciden, pero Softseguros NO tiene NÚMERO ANEXO)")
        print("=" * 80)
        print(f"Total: {len(self.results['actualizar_recibo_softseguros'])} polizas\n")
        
        if self.results['actualizar_recibo_softseguros']:
            for i, record in enumerate(self.results['actualizar_recibo_softseguros'], 1):
                print(f"{i}. Poliza: {record['poliza']} | Fecha: {record['fecha_inicio']}")
                print(f"   {record['nota']}")
                print(f"   Recibo sugerido (Allianz): {record['recibo_allianz']}")
                print(f"   Cliente: {record['tomador']}\n")
        else:
            print("No hay polizas en este caso.\n")
        
        # CASO 2: ACTUALIZAR SISTEMA - TODAS LAS POLIZAS
        print("\n" + "=" * 80)
        print("[CASO 2] ACTUALIZAR EN SISTEMA")
        print("(Poliza + Fecha coinciden, pero DIFERENTE numero de recibo)")
        print("=" * 80)
        print(f"Total: {len(self.results['actualizar_sistema'])} polizas\n")
        
        if self.results['actualizar_sistema']:
            for i, record in enumerate(self.results['actualizar_sistema'], 1):
                print(f"{i}. Poliza: {record['poliza']} | Fecha: {record['fecha_inicio']}")
                print(f"   Recibo ({record['source_data']}): {record['recibo_combinado']} | Recibo Allianz: {record['recibo_allianz']}")
                print(f"   Tomador ({record['source_data']}): {record['tomador']}")
                print(f"   Cliente (Allianz): {record['cliente_allianz']}")
                print(f"   Saldo ({record['source_data']}): ${record['saldo_combinado']:,.2f} | Cartera Allianz: ${record['cartera_allianz']:,.2f}\n")
        else:
            print("No hay polizas en este caso.\n")
        
        # CASO 3: CORREGIR POLIZA - Solo en Allianz - TODAS LAS POLIZAS
        print("\n" + "=" * 80)
        print("[CASO 3] CORREGIR POLIZA - Solo en Allianz")
        print("(Polizas en Allianz que NO coinciden con ninguna en Softseguros/Celer)")
        print("=" * 80)
        print(f"Total: {len(self.results['only_allianz'])} polizas\n")
        
        if self.results['only_allianz']:
            for i, record in enumerate(self.results['only_allianz'], 1):
                print(f"{i}. Poliza: {record['poliza']} | Recibo: {record['recibo']} | Fecha: {record['fecha_inicio']}")
                print(f"   Cliente: {record['cliente']}")
                print(f"   Source: {record['source']} | Cartera Total: ${record['cartera_total']:,.2f}\n")
        else:
            print("No hay polizas en este caso.\n")
        
        # CASO 3: CORREGIR POLIZA - Solo en Combined - TODAS LAS POLIZAS
        print("\n" + "=" * 80)
        print("[CASO 3] CORREGIR POLIZA - Solo en Softseguros/Celer")
        print("(Polizas en Softseguros/Celer que NO coinciden con ninguna en Allianz)")
        print("=" * 80)
        print(f"Total: {len(self.results['only_combined'])} polizas\n")
        
        if self.results['only_combined']:
            for i, record in enumerate(self.results['only_combined'], 1):
                print(f"{i}. Poliza: {record['poliza']} | Recibo: {record['recibo']} | Fecha: {record['fecha_inicio']}")
                print(f"   Tomador: {record['tomador']}")
                print(f"   Source: {record['source']} | Saldo: ${record['saldo']:,.2f}\n")
        else:
            print("No hay polizas en este caso.\n")
        
        # Match rate
        total_combined = len(set(self.combined_df['_match_key_partial']))
        total_allianz = len(set(self.allianz_df['_match_key_partial']))
        matched = len(self.results['no_pagado']) + len(self.results['actualizar_sistema']) + len(self.results['actualizar_recibo_softseguros'])
        
        if total_combined > 0:
            match_rate = (matched / total_combined) * 100
            print(f"\nTasa de coincidencia: {match_rate:.2f}%")
        
        print("\n" + "=" * 80)
    
    def run(self):
        """Execute conciliation workflow"""
        try:
            print("\n" + "=" * 80)
            print(f"INICIANDO CONCILIACIÓN ALLIANZ ({self.data_source_type.upper()})")
            print("=" * 80)
            
            # Load data sources based on selection
            if self.data_source_type == 'softseguros':
                self.load_softseguros_data()
                self.combined_df = self.softseguros_df.copy()
                self.celer_df = pd.DataFrame()  # Empty
                
            elif self.data_source_type == 'celer':
                self.load_celer_data()
                self.combined_df = self.celer_df.copy()
                self.softseguros_df = pd.DataFrame()  # Empty
                
            else:  # both
                self.load_softseguros_data()
                self.load_celer_data()
                self.combine_data_sources()
            
            # Load Allianz data
            self.load_allianz_data()
            
            # Perform conciliation
            self.perform_conciliation()
            
            # Print report to console
            self.print_report()
            
            # Save report to file
            output_file = self.save_report_to_file()
            print(f"\n✅ Reporte guardado en: {output_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"Conciliation failed: {e}", exc_info=True)
            print(f"\n[ERROR]: {e}")
            return False


def main():
    """Main entry point"""
    # Menu 1: Select data source type (Softseguros, Celer, or Both)
    print("\n" + "=" * 80)
    print("CONCILIADOR ALLIANZ - SELECCIÓN DE FUENTE DE DATOS")
    print("=" * 80)
    print("\n¿De dónde desea obtener los datos para conciliar?")
    print("\n  1. SOFTSEGUROS solamente")
    print("  2. CELER solamente")
    print("  3. AMBOS (SOFTSEGUROS + CELER con prioridad a Softseguros)")
    print("\n" + "=" * 80)
    
    # Get data source type
    while True:
        try:
            selection = input("\nIngrese su opcion (1-3): ").strip()
            
            if selection == '1':
                data_source_type = 'softseguros'
                break
            elif selection == '2':
                data_source_type = 'celer'
                break
            elif selection == '3':
                data_source_type = 'both'
                break
            else:
                print("[ERROR] Opcion invalida. Por favor ingrese 1, 2 o 3.")
        except KeyboardInterrupt:
            print("\n\n[INFO] Proceso cancelado por el usuario.")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Error al leer entrada: {e}")
    
    # Menu 2: Select Allianz data source (PERSONAS, COLECTIVAS, or BOTH)
    print("\n" + "=" * 80)
    print("CONCILIADOR ALLIANZ - SELECCIÓN DE DATOS ALLIANZ")
    print("=" * 80)
    print("\nSeleccione que datos de Allianz desea procesar:")
    print("\n  1. PERSONAS solamente")
    print("  2. COLECTIVAS solamente")
    print("  3. AMBOS (PERSONAS + COLECTIVAS)")
    print("\n" + "=" * 80)
    
    # Get Allianz data source
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
    softseguros_folder = base_dir.parent / "DATA SOFTSEGUROS"
    celer_folder = base_dir.parent / "TRANSFORMER CELER" / "output"
    personas_folder = base_dir / "INPUT" / "PERSONAS"
    colectivas_folder = base_dir / "INPUT" / "COLECTIVAS"
    
    # Select files from folders based on data source type
    print("\n" + "=" * 80)
    print("SELECCIÓN DE ARCHIVOS")
    print("=" * 80)
    
    softseguros_file = None
    celer_file = None
    
    if data_source_type in ['softseguros', 'both']:
        softseguros_file = select_file_from_folder(softseguros_folder, ".xlsx", "Archivo Softseguros")
    
    if data_source_type in ['celer', 'both']:
        celer_file = select_file_from_folder(celer_folder, ".xlsx", "Archivo Celer Transformado")
    
    allianz_personas = select_file_from_folder(personas_folder, ".xlsb", "Archivo Allianz PERSONAS")
    allianz_colectivas = select_file_from_folder(colectivas_folder, ".xlsb", "Archivo Allianz COLECTIVAS")
    
    # Create conciliator
    conciliator = AllianzConciliator(
        allianz_personas_path=allianz_personas,
        allianz_colectivas_path=allianz_colectivas,
        data_source=data_source,
        data_source_type=data_source_type,
        softseguros_file_path=softseguros_file,
        celer_file_path=celer_file
    )
    
    # Run conciliation
    success = conciliator.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
