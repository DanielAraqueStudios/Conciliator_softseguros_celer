"""
Unit tests for ColumnTransformer service.
"""

import pytest
import pandas as pd
from services.column_transformer import ColumnTransformer
from schemas.celer_mapping import CELER_MAPPING


class TestColumnTransformer:
    """Test suite for ColumnTransformer"""
    
    @pytest.fixture
    def transformer(self):
        """Create transformer instance"""
        return ColumnTransformer()
    
    @pytest.fixture
    def valid_source_df(self):
        """Create a valid source DataFrame with all required columns"""
        # Get all required source columns
        required_cols = CELER_MAPPING.get_required_source_columns()
        
        # Create sample data
        data = {col: [f"value_{col}_1", f"value_{col}_2", f"value_{col}_3"] 
                for col in required_cols}
        
        return pd.DataFrame(data)
    
    def test_initialization(self, transformer):
        """Test transformer initializes correctly"""
        assert transformer.mapping is not None
        assert len(transformer.mapping.output_to_original) == 23  # A-W
    
    def test_transform_valid_input(self, transformer, valid_source_df):
        """Test transformation with valid input"""
        result = transformer.transform(valid_source_df)
        
        # Check output has correct number of columns
        assert len(result.columns) == 23
        
        # Check output columns are A-W
        assert list(result.columns) == [chr(65 + i) for i in range(23)]
        
        # Check same number of rows
        assert len(result) == len(valid_source_df)
    
    def test_transform_missing_columns(self, transformer):
        """Test transformation fails with missing columns"""
        # Create DataFrame with only some columns
        incomplete_df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        
        with pytest.raises(ValueError) as exc_info:
            transformer.transform(incomplete_df)
        
        assert "Missing required columns" in str(exc_info.value)
    
    def test_transform_preserves_data(self, transformer, valid_source_df):
        """Test that mapped data is correctly transferred"""
        result = transformer.transform(valid_source_df)
        
        # Check a few mappings (B←D, C←X, N←A)
        assert result["B"][0] == valid_source_df["D"][0]
        assert result["C"][0] == valid_source_df["X"][0]
        assert result["N"][0] == valid_source_df["A"][0]
    
    def test_column_order_is_deterministic(self, transformer, valid_source_df):
        """Test that output columns are always in A-W order"""
        result1 = transformer.transform(valid_source_df)
        result2 = transformer.transform(valid_source_df)
        
        assert list(result1.columns) == list(result2.columns)
        assert list(result1.columns) == [chr(65 + i) for i in range(23)]
    
    def test_validate_source_columns(self, transformer):
        """Test source column validation"""
        required = CELER_MAPPING.get_required_source_columns()
        
        # Valid case
        is_valid, missing = transformer.mapping.validate_source_columns(required)
        assert is_valid
        assert len(missing) == 0
        
        # Missing columns case
        incomplete = {"A", "B", "C"}
        is_valid, missing = transformer.mapping.validate_source_columns(incomplete)
        assert not is_valid
        assert len(missing) > 0


class TestCelerMapping:
    """Test suite for CelerMappingConfig"""
    
    def test_mapping_completeness(self):
        """Test that all 23 output columns are defined"""
        assert len(CELER_MAPPING.output_to_original) == 23
    
    def test_generated_columns_identified(self):
        """Test that generated columns are correctly identified"""
        generated = CELER_MAPPING.generated_columns
        assert "A" in [col.value for col in generated]
    
    def test_mapped_columns_excludes_generated(self):
        """Test that mapped_columns only returns non-generated columns"""
        mapped = CELER_MAPPING.mapped_columns
        
        # Column A should not be in mapped (it's generated)
        assert all(col.value != "A" for col in mapped.keys())
        
        # All mapped columns should have source values
        assert all(source is not None for source in mapped.values())
    
    def test_get_source_column(self):
        """Test getting source column for output column"""
        assert CELER_MAPPING.get_source_column("B") == "D"
        assert CELER_MAPPING.get_source_column("A") is None  # Generated
    
    def test_required_source_columns_count(self):
        """Test that we have the expected number of source columns"""
        required = CELER_MAPPING.get_required_source_columns()
        
        # Should be 22 (23 output columns - 1 generated)
        assert len(required) == 22
        
        # Should not contain None
        assert None not in required
