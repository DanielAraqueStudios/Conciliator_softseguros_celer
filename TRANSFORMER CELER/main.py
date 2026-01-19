"""
Main Transformation Script - Celer to Standardized Format
----------------------------------------------------------
Reads Celer export file and transforms it to standardized 23-column format (A-W).

Usage:
    python main.py [input_file] [output_file]
    
    If no arguments provided, uses default paths from .env
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

import pandas as pd
from dotenv import load_dotenv

from schemas.celer_mapping import CELER_MAPPING, OutputColumn
from services.column_transformer import ColumnTransformer
from domain.exceptions import (
    MissingColumnsError,
    TransformationError,
    FileProcessingError
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output/transformation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def setup_directories() -> None:
    """Ensure required directories exist"""
    for dir_path in ['output', 'logs', 'temp']:
        Path(dir_path).mkdir(exist_ok=True)
        logger.debug(f"Ensured directory exists: {dir_path}")


def read_celer_file(file_path: Path) -> pd.DataFrame:
    """
    Read Celer export Excel file.
    
    Args:
        file_path: Path to Celer Excel file
        
    Returns:
        DataFrame with Celer data
        
    Raises:
        FileProcessingError: If file cannot be read
    """
    try:
        logger.info(f"Reading Celer file: {file_path}")
        
        # Read Excel file starting at row 5 (header_row=4)
        df = pd.read_excel(file_path, header=CELER_MAPPING.header_row)
        
        logger.info(f"Successfully read {len(df)} rows, {len(df.columns)} columns")
        return df
        
    except FileNotFoundError:
        error_msg = f"File not found: {file_path}"
        logger.error(error_msg)
        raise FileProcessingError(error_msg)
    except Exception as e:
        error_msg = f"Error reading file {file_path}: {str(e)}"
        logger.error(error_msg)
        raise FileProcessingError(error_msg)


def write_output_file(df: pd.DataFrame, file_path: Path) -> None:
    """
    Write transformed DataFrame to Excel file.
    
    Args:
        df: Transformed DataFrame
        file_path: Output file path
    """
    try:
        logger.info(f"Writing output file: {file_path}")
        
        # Write to Excel with formatting
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Cartera_Transformada')
            
            # Get worksheet for formatting
            worksheet = writer.sheets['Cartera_Transformada']
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Format header row
            from openpyxl.styles import Font, PatternFill, Alignment
            
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")
            
            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")
        
        logger.info(f"Successfully wrote {len(df)} rows to {file_path}")
        
    except Exception as e:
        error_msg = f"Error writing output file {file_path}: {str(e)}"
        logger.error(error_msg)
        raise FileProcessingError(error_msg)


def transform_celer_data(
    input_file: Optional[Path] = None,
    output_file: Optional[Path] = None
) -> None:
    """
    Main transformation function.
    
    Args:
        input_file: Path to input Celer file (default: searches in input/ folder)
        output_file: Path to output file (default: output/Cartera_Transformada_YYYYMMDD.xlsx)
    """
    try:
        # Setup
        setup_directories()
        
        # Determine input file
        if input_file is None:
            # Look for Excel files in parent DATA CELER folder or current input folder
            data_celer_path = Path('../DATA CELER')
            if data_celer_path.exists():
                excel_files = list(data_celer_path.glob('*.xlsx'))
                if excel_files:
                    input_file = excel_files[0]
                    logger.info(f"Auto-detected input file: {input_file}")
            
            if input_file is None:
                raise FileProcessingError(
                    "No input file specified and no Excel file found in DATA CELER folder. "
                    "Please provide input file path."
                )
        
        input_file = Path(input_file)
        
        # Determine output file
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = Path(f'output/Cartera_Transformada_{timestamp}.xlsx')
        
        output_file = Path(output_file)
        
        logger.info("="*80)
        logger.info("STARTING CELER DATA TRANSFORMATION")
        logger.info("="*80)
        logger.info(f"Input file: {input_file}")
        logger.info(f"Output file: {output_file}")
        
        # Read input file
        source_df = read_celer_file(input_file)
        
        # Initialize transformer
        transformer = ColumnTransformer()
        
        # Perform transformation
        logger.info("Starting column transformation...")
        transformed_df = transformer.transform(source_df)
        
        # Write output file
        write_output_file(transformed_df, output_file)
        
        # Summary
        logger.info("="*80)
        logger.info("TRANSFORMATION COMPLETED SUCCESSFULLY")
        logger.info("="*80)
        logger.info(f"Input rows: {len(source_df)}")
        logger.info(f"Output rows: {len(transformed_df)}")
        logger.info(f"Output columns: {len(transformed_df.columns)} (A-W)")
        logger.info(f"Output file: {output_file.absolute()}")
        
    except MissingColumnsError as e:
        logger.error(f"Missing required columns: {e}")
        logger.error("Please check that the input file is a valid Celer export.")
        sys.exit(1)
        
    except TransformationError as e:
        logger.error(f"Transformation error: {e}")
        sys.exit(1)
        
    except FileProcessingError as e:
        logger.error(f"File processing error: {e}")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


def main() -> None:
    """CLI entry point"""
    input_file = None
    output_file = None
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    transform_celer_data(input_file, output_file)


if __name__ == "__main__":
    main()
