"""
Domain-specific exceptions for Conciliator application.
"""


class ConciliatorBaseException(Exception):
    """Base exception for all Conciliator errors"""
    pass


class InvalidExcelSchemaError(ConciliatorBaseException):
    """Raised when Excel file doesn't match expected schema"""
    pass


class MissingColumnsError(ConciliatorBaseException):
    """Raised when required columns are missing from source file"""
    
    def __init__(self, missing_columns: list[str]):
        self.missing_columns = missing_columns
        super().__init__(f"Missing required columns: {', '.join(missing_columns)}")


class TransformationError(ConciliatorBaseException):
    """Raised when data transformation fails"""
    pass


class ValidationError(ConciliatorBaseException):
    """Raised when data validation fails"""
    pass


class FileProcessingError(ConciliatorBaseException):
    """Raised when file processing fails"""
    pass
