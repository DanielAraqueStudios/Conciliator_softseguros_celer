"""
CONCILIATOR ALLIANZ - Main Entry Point
Sistema de conciliación para reportes de cartera Allianz
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Tuple
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class AllianzExcelReader:
    """
    Lector robusto de archivos Excel (.xlsb/.xlsx) de Allianz
    con auto-detección de columnas y manejo de filas vacías
    """
    
    # Expected column names for validation
    EXPECTED_COLUMNS = [
        "Cliente - Tomador", "Póliza", "MATRICULA", "F.INI VIG", "F.FIN VIG",
        "Nombre Macroramo", "Número Ramo", "Recibo", "Nombre Sucursal",
        "Regional", "Nombre Asesor", "Aplicación", "Comisión",
        "1-30", "31-90", "91-180", "180+", "Vencida", "No Vencida",
        "F. Límite Pago", "Comisión Vencida", "Proporción Vencida", "Cartera Total"
    ]
    
    def __init__(self, file_path: Path):
        """
        Initialize the Excel reader
        
        Args:
            file_path: Path to the Excel file (.xlsb or .xlsx)
        """
        self.file_path = file_path
        self.df: Optional[pd.DataFrame] = None
        self.sheet_name: Optional[str] = None
        self.header_row: Optional[int] = None
        
    def detect_sheet_name(self) -> str:
        """
        Detect the correct sheet name to read
        Priority: 'Detalle' > first sheet
        
        Returns:
            Sheet name to read
        """
        try:
            # Read all sheet names
            xl_file = pd.ExcelFile(self.file_path, engine='pyxlsb')
            sheet_names = xl_file.sheet_names
            
            logger.info(f"Available sheets: {sheet_names}")
            
            # Look for 'Detalle' sheet (case-insensitive)
            for sheet in sheet_names:
                if sheet.lower() == 'detalle':
                    logger.info(f"Found 'Detalle' sheet: {sheet}")
                    return sheet
            
            # If 'Detalle' not found, use first sheet
            logger.warning(f"'Detalle' sheet not found, using first sheet: {sheet_names[0]}")
            return sheet_names[0]
            
        except Exception as e:
            logger.error(f"Error detecting sheet name: {e}")
            raise
    
    def detect_header_row(self, df: pd.DataFrame, max_search_rows: int = 20) -> int:
        """
        Auto-detect which row contains the column headers
        Searches for key column names in the first N rows
        
        Args:
            df: DataFrame with potential headers in early rows
            max_search_rows: Maximum number of rows to search
            
        Returns:
            Row index where headers are found (0-indexed)
        """
        # Key columns to look for (most distinctive)
        key_columns = ["Cliente - Tomador", "Póliza", "Nombre Macroramo"]
        
        # Search in the first max_search_rows
        for row_idx in range(min(max_search_rows, len(df))):
            row_values = df.iloc[row_idx].astype(str).tolist()
            
            # Check how many key columns are present in this row
            matches = sum(1 for key in key_columns if key in row_values)
            
            if matches >= 2:  # At least 2 key columns found
                logger.info(f"Header row detected at index {row_idx} (row {row_idx + 1} in Excel)")
                return row_idx
        
        # If no clear header found, assume row 0
        logger.warning("Could not detect header row clearly, assuming row 0")
        return 0
    
    def read_excel_with_auto_detection(self) -> pd.DataFrame:
        """
        Read Excel file with automatic detection of:
        - Sheet name ('Detalle')
        - Header row (skipping empty rows)
        - Column names
        
        Returns:
            Cleaned DataFrame with proper headers
        """
        try:
            # Step 1: Detect sheet name
            self.sheet_name = self.detect_sheet_name()
            
            # Step 2: Read sheet without assuming header location
            logger.info(f"Reading sheet '{self.sheet_name}' to detect headers...")
            df_raw = pd.read_excel(
                self.file_path,
                sheet_name=self.sheet_name,
                header=None,  # Don't assume header location
                engine='pyxlsb'
            )
            
            logger.info(f"Raw data shape: {df_raw.shape}")
            
            # Step 3: Detect header row
            self.header_row = self.detect_header_row(df_raw)
            
            # Step 4: Re-read with correct header
            logger.info(f"Re-reading with header at row {self.header_row}...")
            self.df = pd.read_excel(
                self.file_path,
                sheet_name=self.sheet_name,
                header=self.header_row,
                engine='pyxlsb'
            )
            
            # Step 5: Clean column names (strip whitespace)
            self.df.columns = self.df.columns.str.strip()
            
            # Step 6: Remove completely empty rows
            initial_rows = len(self.df)
            self.df = self.df.dropna(how='all')
            removed_rows = initial_rows - len(self.df)
            
            if removed_rows > 0:
                logger.info(f"Removed {removed_rows} empty rows")
            
            logger.info(f"Final data shape: {self.df.shape}")
            logger.info(f"Columns: {list(self.df.columns)}")
            
            return self.df
            
        except Exception as e:
            logger.error(f"Error reading Excel file: {e}")
            raise
    
    def validate_columns(self) -> Tuple[bool, list]:
        """
        Validate that expected columns are present
        
        Returns:
            Tuple of (is_valid, missing_columns)
        """
        if self.df is None:
            raise ValueError("DataFrame not loaded. Call read_excel_with_auto_detection() first.")
        
        actual_columns = set(self.df.columns)
        expected_columns = set(self.EXPECTED_COLUMNS)
        
        missing_columns = expected_columns - actual_columns
        
        if missing_columns:
            logger.warning(f"Missing columns: {missing_columns}")
            return False, list(missing_columns)
        
        logger.info("✓ All expected columns are present")
        return True, []
    
    def get_summary(self) -> dict:
        """
        Get summary statistics of the loaded data
        
        Returns:
            Dictionary with summary information
        """
        if self.df is None:
            raise ValueError("DataFrame not loaded. Call read_excel_with_auto_detection() first.")
        
        summary = {
            "file_name": self.file_path.name,
            "sheet_name": self.sheet_name,
            "header_row": self.header_row,
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "column_names": list(self.df.columns),
            "cartera_total": self.df['Cartera Total'].sum() if 'Cartera Total' in self.df.columns else None,
            "cartera_vencida": self.df['Vencida'].sum() if 'Vencida' in self.df.columns else None,
            "comision_total": self.df['Comisión'].sum() if 'Comisión' in self.df.columns else None,
            "unique_polizas": self.df['Póliza'].nunique() if 'Póliza' in self.df.columns else None
        }
        
        return summary


def read_allianz_file(file_path: str) -> pd.DataFrame:
    """
    Main function to read an Allianz Excel file
    
    Args:
        file_path: Path to the Excel file (string or Path)
        
    Returns:
        Cleaned DataFrame with validated data
    """
    try:
        path = Path(file_path)
        
        # Validate file exists
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Validate file extension
        if path.suffix.lower() not in ['.xlsb', '.xlsx']:
            raise ValueError(f"Unsupported file format: {path.suffix}. Expected .xlsb or .xlsx")
        
        logger.info(f"Starting to read file: {path.name}")
        logger.info(f"File size: {path.stat().st_size / 1024:.2f} KB")
        
        # Create reader and load data
        reader = AllianzExcelReader(path)
        df = reader.read_excel_with_auto_detection()
        
        # Validate columns
        is_valid, missing_cols = reader.validate_columns()
        if not is_valid:
            logger.error(f"Column validation failed. Missing: {missing_cols}")
            # Continue anyway, but log the warning
        
        # Display summary
        summary = reader.get_summary()
        logger.info("=" * 60)
        logger.info("FILE SUMMARY")
        logger.info("=" * 60)
        for key, value in summary.items():
            if key == "column_names":
                continue  # Skip detailed column list
            logger.info(f"{key}: {value}")
        logger.info("=" * 60)
        
        return df
        
    except Exception as e:
        logger.error(f"Failed to read file: {e}")
        raise


def main():
    """
    Main entry point for testing
    """
    # Define input folders
    BASE_DIR = Path(__file__).parent
    INPUT_DIR = BASE_DIR / "CONCILIATOR ALLIANZ" / "INPUT"
    
    # Files to process
    files_to_read = [
        INPUT_DIR / "PERSONAS" / "Informe Intermediario UNION AGENCIA DE SEGUROS LTDA_1701932_11_Jan_2026 (2).xlsb",
        INPUT_DIR / "COLECTIVAS" / "Informe Intermediario UNION AGENCIA DE SEGUROS LTDA_1701932_11_Jan_2026 (1).xlsb"
    ]
    
    for file_path in files_to_read:
        print("\n" + "=" * 80)
        print(f"PROCESSING: {file_path.parent.name}/{file_path.name}")
        print("=" * 80)
        
        try:
            df = read_allianz_file(file_path)
            
            # Show first few rows
            print("\nFirst 3 rows:")
            print(df.head(3).to_string())
            
            # Show data types
            print("\nData types:")
            print(df.dtypes)
            
        except FileNotFoundError:
            logger.warning(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}")
            continue


if __name__ == "__main__":
    main()
