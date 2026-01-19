"""
Main Transformation Script - Celer to Standardized Format
----------------------------------------------------------
Reads Celer export file and transforms it to standardized 23-column format (A-W).
Two separate programs: one for XLSX format, another for XML format.

Usage:
    python main.py
    
    Program will prompt you to choose:
    1. Process XLSX format
    2. Process XML format
    
    Then enter the input file path.
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


def read_celer_xlsx(file_path: Path) -> pd.DataFrame:
    """
    PROGRAM 1: Read Celer XLSX format.
    
    Args:
        file_path: Path to Celer XLSX file
        
    Returns:
        DataFrame with Celer data
        
    Raises:
        FileProcessingError: If file cannot be read
    """
    try:
        logger.info(f"[PROGRAM 1 - XLSX] Reading file: {file_path}")
        
        # Read Excel file starting at row 5 (header_row=4)
        df = pd.read_excel(file_path, header=CELER_MAPPING.header_row)
        logger.info(f"[PROGRAM 1 - XLSX] Successfully read {len(df)} rows, {len(df.columns)} columns")
        
        return df
        
    except FileNotFoundError:
        error_msg = f"[PROGRAM 1 - XLSX] File not found: {file_path}"
        logger.error(error_msg)
        raise FileProcessingError(error_msg)
    except Exception as e:
        error_msg = f"[PROGRAM 1 - XLSX] Error reading file: {str(e)}"
        logger.error(error_msg)
        raise FileProcessingError(error_msg)


def read_celer_xml(file_path: Path) -> pd.DataFrame:
    """
    PROGRAM 2: Read Celer XML format.
    
    Args:
        file_path: Path to Celer XML file
        
    Returns:
        DataFrame with Celer data
        
    Raises:
        FileProcessingError: If file cannot be read
    """
    try:
        logger.info(f"[PROGRAM 2 - XML] Reading file: {file_path}")
        
        # Read Excel XML format
        from adapters.xml_reader import read_celer_xml as xml_reader
        df = xml_reader(file_path, header_row=CELER_MAPPING.header_row)
        logger.info(f"[PROGRAM 2 - XML] Successfully read {len(df)} rows, {len(df.columns)} columns")
        
        return df
        
    except FileNotFoundError:
        error_msg = f"[PROGRAM 2 - XML] File not found: {file_path}"
        logger.error(error_msg)
        raise FileProcessingError(error_msg)
    except Exception as e:
        error_msg = f"[PROGRAM 2 - XML] Error reading file: {str(e)}"
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


def transform_xlsx_format(
    input_file: Path,
    output_file: Optional[Path] = None
) -> None:
    """
    PROGRAM 1: Transform XLSX format files.
    
    Args:
        input_file: Path to input XLSX file
        output_file: Path to output file (optional)
    """
    try:
        # Setup
        setup_directories()
        
        # Determine output file
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = Path(f'output/Cartera_Transformada_XLSX_{timestamp}.xlsx')
        
        logger.info("="*80)
        logger.info("PROGRAM 1: XLSX FORMAT TRANSFORMATION")
        logger.info("="*80)
        logger.info(f"Input file: {input_file}")
        logger.info(f"Output file: {output_file}")
        
        # Read XLSX file
        source_df = read_celer_xlsx(input_file)
        
        # Initialize transformer
        transformer = ColumnTransformer()
        
        # Perform transformation
        logger.info("[PROGRAM 1 - XLSX] Starting column transformation...")
        transformed_df = transformer.transform(source_df)
        
        # Write output file
        write_output_file(transformed_df, output_file)
        
        # Summary
        logger.info("="*80)
        logger.info("PROGRAM 1: TRANSFORMATION COMPLETED SUCCESSFULLY")
        logger.info("="*80)
        logger.info(f"Input rows: {len(source_df)}")
        logger.info(f"Output rows: {len(transformed_df)}")
        logger.info(f"Output columns: {len(transformed_df.columns)}")
        logger.info(f"Output file: {output_file.absolute()}")
        
    except Exception as e:
        logger.error(f"[PROGRAM 1 - XLSX] Error: {e}", exc_info=True)
        raise


def transform_xml_format(
    input_file: Path,
    output_file: Optional[Path] = None
) -> None:
    """
    PROGRAM 2: Transform XML format files.
    
    Args:
        input_file: Path to input XML file
        output_file: Path to output file (optional)
    """
    try:
        # Setup
        setup_directories()
        
        # Determine output file
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = Path(f'output/Cartera_Transformada_XML_{timestamp}.xlsx')
        
        logger.info("="*80)
        logger.info("PROGRAM 2: XML FORMAT TRANSFORMATION")
        logger.info("="*80)
        logger.info(f"Input file: {input_file}")
        logger.info(f"Output file: {output_file}")
        
        # Read XML file
        source_df = read_celer_xml(input_file)
        
        # Initialize transformer
        transformer = ColumnTransformer()
        
        # Perform transformation
        logger.info("[PROGRAM 2 - XML] Starting column transformation...")
        transformed_df = transformer.transform(source_df)
        
        # Write output file
        write_output_file(transformed_df, output_file)
        
        # Summary
        logger.info("="*80)
        logger.info("PROGRAM 2: TRANSFORMATION COMPLETED SUCCESSFULLY")
        logger.info("="*80)
        logger.info(f"Input rows: {len(source_df)}")
        logger.info(f"Output rows: {len(transformed_df)}")
        logger.info(f"Output columns: {len(transformed_df.columns)}")
        logger.info(f"Output file: {output_file.absolute()}")
        
    except Exception as e:
        logger.error(f"[PROGRAM 2 - XML] Error: {e}", exc_info=True)
        raise


def show_menu() -> int:
    """
    Display console menu and get user choice.
    
    Returns:
        User's choice (1 or 2)
    """
    print("\n" + "="*60)
    print(" CELER DATA TRANSFORMATION - CHOOSE INPUT FORMAT")
    print("="*60)
    print()
    print("  1. Process XLSX format (Excel .xlsx files)")
    print("  2. Process XML format (Excel 2003 XML files)")
    print()
    print("="*60)
    
    while True:
        try:
            choice = input("\nEnter your choice (1 or 2): ").strip()
            if choice in ['1', '2']:
                return int(choice)
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            sys.exit(0)
        except Exception:
            print("❌ Invalid input. Please enter 1 or 2.")


def get_input_file(format_name: str, extension: str) -> Path:
    """
    Get input file path from user.
    
    Args:
        format_name: Name of format (e.g., "XLSX", "XML")
        extension: Expected file extension (e.g., ".xlsx", ".xml")
        
    Returns:
        Path to input file
    """
    print(f"\n📁 Enter path to {format_name} file:")
    print(f"   Example: ../DATA CELER/CarteraPendiente{extension}")
    print(f"   (Press Enter for auto-detection)")
    
    while True:
        try:
            file_path = input("\nFile path: ").strip().strip('"').strip("'")
            
            if not file_path:
                # Try auto-detection
                data_celer_path = Path('../DATA CELER')
                if data_celer_path.exists():
                    files = list(data_celer_path.glob(f'*{extension}'))
                    files = [f for f in files if not f.name.startswith('~$')]
                    
                    if files:
                        file_path = str(files[0])
                        print(f"✅ Auto-detected file: {file_path}")
                    else:
                        print(f"❌ No {extension} files found in DATA CELER folder.")
                        continue
            
            path = Path(file_path)
            
            if not path.exists():
                print(f"❌ File not found: {file_path}")
                print("   Please check the path and try again.")
                continue
            
            if path.suffix.lower() != extension:
                print(f"❌ File must have {extension} extension.")
                print(f"   Your file has: {path.suffix}")
                continue
            
            return path
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("   Please try again.")


def main() -> None:
    """CLI entry point - Interactive console menu"""
    try:
        # Show menu and get choice
        choice = show_menu()
        
        if choice == 1:
            # PROGRAM 1: XLSX Format
            print("\n✅ Selected: PROGRAM 1 - XLSX FORMAT")
            input_file = get_input_file("XLSX", ".xlsx")
            transform_xlsx_format(input_file)
            
        elif choice == 2:
            # PROGRAM 2: XML Format
            print("\n✅ Selected: PROGRAM 2 - XML FORMAT")
            input_file = get_input_file("XML", ".xml")
            transform_xml_format(input_file)
        
        print("\n" + "="*60)
        print("✅ Process completed successfully!")
        print("="*60 + "\n")
        
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


if __name__ == "__main__":
    main()
