"""
Column Transformation Service
------------------------------
Orchestrates the transformation of Celer exports to standardized format.
"""

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from schemas.celer_mapping import CELER_MAPPING, OutputColumn, COLUMN_DESCRIPTIONS

logger = logging.getLogger(__name__)


class ColumnTransformer:
    """
    Service responsible for transforming Celer export data to standardized output format.
    
    Responsibilities:
    - Validate source file has all required columns
    - Map columns according to CELER_MAPPING configuration
    - Generate calculated fields
    - Preserve data types and formats
    """
    
    def __init__(self):
        self.mapping = CELER_MAPPING
        logger.info("ColumnTransformer initialized with %d output columns", 
                   len(self.mapping.output_to_original))
    
    def transform(self, source_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform source DataFrame to standardized output format.
        
        Args:
            source_df: DataFrame from Celer export (with column letters as headers)
            
        Returns:
            Transformed DataFrame with columns A-W
            
        Raises:
            ValueError: If required source columns are missing
        """
        logger.info("Starting transformation for %d rows", len(source_df))
        
        # Validate source columns
        available_columns = set(source_df.columns)
        is_valid, missing = self.mapping.validate_source_columns(available_columns)
        
        if not is_valid:
            error_msg = f"Missing required columns from Celer export: {missing}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Create output DataFrame
        output_df = pd.DataFrame(index=source_df.index)
        
        # Map columns from source to output
        for output_col, source_col in self.mapping.mapped_columns.items():
            output_df[output_col.value] = source_df[source_col]
            logger.debug("Mapped %s ← %s", output_col.value, source_col)
        
        # Generate calculated fields
        for generated_col in self.mapping.generated_columns:
            output_df[generated_col.value] = self._generate_column(generated_col, source_df)
            logger.debug("Generated column %s", generated_col.value)
        
        # Ensure column order A-W
        output_df = output_df[[col.value for col in OutputColumn]]
        
        # Add descriptive column names
        column_headers = {col.value: COLUMN_DESCRIPTIONS[col] for col in OutputColumn}
        output_df.rename(columns=column_headers, inplace=True)
        
        logger.info("Transformation completed successfully for %d rows, %d columns", 
                   len(output_df), len(output_df.columns))
        
        return output_df
    
    def _generate_column(self, column: OutputColumn, source_df: pd.DataFrame) -> pd.Series:
        """
        Generate calculated/derived column values.
        
        Args:
            column: The output column to generate
            source_df: Source DataFrame for calculations
            
        Returns:
            Series with generated values
        """
        # Placeholder for generation logic
        # TODO: Implement specific generation logic based on business rules
        
        if column == OutputColumn.A:
            # Example: Could be a sequential ID, hash, or calculation
            logger.warning("Column A generation not yet implemented, using placeholder")
            return pd.Series([None] * len(source_df), index=source_df.index)
        
        # Default: return None for unknown generated columns
        logger.warning("No generation logic for column %s, using None", column.value)
        return pd.Series([None] * len(source_df), index=source_df.index)
    
    def validate_source_file(self, file_path: Path) -> tuple[bool, list[str]]:
        """
        Validate if a Celer export file has all required columns.
        
        Args:
            file_path: Path to Celer export Excel file
            
        Returns:
            Tuple of (is_valid, missing_columns)
        """
        try:
            # Read just the first row to check columns
            df = pd.read_excel(file_path, nrows=1)
            available_columns = set(df.columns)
            return self.mapping.validate_source_columns(available_columns)
        except Exception as e:
            logger.error("Failed to validate file %s: %s", file_path, str(e))
            return False, [f"Error reading file: {str(e)}"]
