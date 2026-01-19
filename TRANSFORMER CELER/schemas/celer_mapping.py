"""
Celer Data Mapping Configuration
---------------------------------
Defines the column mapping from Celer program exports to standardized output format.

This mapping is the source of truth for all transformations.
"""

from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field


class OutputColumn(str, Enum):
    """Output column identifiers (A-W)"""
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"
    W = "W"


class CelerMappingConfig(BaseModel):
    """
    Mapping configuration from Celer original input to standardized output.
    
    Attributes:
        sheet_name: Sheet name in the mapping reference file
        header_row: Row index where data starts (0-indexed, row 5 = index 4)
        output_to_original: Dictionary mapping output columns to original input column names
        generated_columns: Columns that are calculated/generated (not from source)
    """
    sheet_name: str = Field(default="ARCHIVO", description="Sheet name for mapping reference")
    header_row: int = Field(default=4, description="Row index where headers are (0-indexed, row 5 = 4)")
    output_to_original: Dict[OutputColumn, Optional[str]] = Field(
        default={
            OutputColumn.A: None,  # Generated/Calculated field
            OutputColumn.B: "Días",
            OutputColumn.C: "Tomador",
            OutputColumn.D: "Tipo_Doc",
            OutputColumn.E: "Identificacion",
            OutputColumn.F: "Poliza",
            OutputColumn.G: "Documento",
            OutputColumn.H: "Cuota",
            OutputColumn.I: "Placa",
            OutputColumn.J: "Saldo",
            OutputColumn.K: "Aseguradora",
            OutputColumn.L: "Ramo",
            OutputColumn.M: "Carta_Cobro",
            OutputColumn.N: "F_Inicio",
            OutputColumn.O: "F_Expedicion",
            OutputColumn.P: "F_Creacion",
            OutputColumn.Q: "Ejecutivo",
            OutputColumn.R: "Unidad",
            OutputColumn.S: "Descripcion_Riesgo",
            OutputColumn.T: "Celular_Pers",
            OutputColumn.U: "Celular_Lab",
            OutputColumn.V: "Mail_Lab",
            OutputColumn.W: "Mail_Pers",
        },
        description="Mapping from output column to original Celer column name"
    )
    
    @property
    def generated_columns(self) -> list[OutputColumn]:
        """Returns list of columns that are generated (not from source)"""
        return [col for col, source in self.output_to_original.items() if source is None]
    
    @property
    def mapped_columns(self) -> Dict[OutputColumn, str]:
        """Returns only columns with direct source mapping (excludes generated)"""
        return {col: source for col, source in self.output_to_original.items() if source is not None}
    
    def get_source_column(self, output_col: OutputColumn) -> Optional[str]:
        """Get the source column for a given output column"""
        return self.output_to_original.get(output_col)
    
    def get_required_source_columns(self) -> set[str]:
        """Returns set of all required source columns from Celer export"""
        return {source for source in self.output_to_original.values() if source is not None}
    
    def validate_source_columns(self, available_columns: set[str]) -> tuple[bool, list[str]]:
        """
        Validate if all required source columns are available in the input file.
        names present in the source file
            
        Returns:
            Tuple of (is_valid, missing_columns)
        """
        required = self.get_required_source_columns()
        missing = required - available_columns
        return len(missing) == 0, sorted(list(missing))
    
    def get_output_headers(self) -> Dict[OutputColumn, str]:
        """Returns dictionary of output column letters to their descriptive names"""
        return COLUMN_DESCRIPTIONS
        missing = required - available_columns
        return len(missing) == 0, sorted(list(missing))


# Singleton instance - source of truth
CELER_MAPPING = CelerMappingConfig()


# Column name mapping from Celer export (named columns to letter positions)
# Celer exports with 49 named columns, we map them by their position (letter equivalent)
CELER_COLUMN_NAMES = [
    "F_Inicio",                    # A (index 0)
    "F_Expedicion",                # B (index 1)
    "F_Creacion",                  # C (index 2)
    "Días",                        # D (index 3)
    "Documento",                   # E (index 4)
    "Cuota",                       # F (index 5)
    "Saldo",                       # G (index 6)
    "Estado",                      # H (index 7)
    "Operacion",                   # I (index 8)
    "Descripcion",                 # J (index 9)
    "Prima",                       # K (index 10)
    "Prima_Participacion",         # L (index 11)
    "Imp_Documento",               # M (index 12)
    "Imp_Valor_Documento",         # N (index 13)
    "Otros_Rubros_Documento",      # O (index 14)
    "Valores_Externos_Documento",  # P (index 15)
    "Valor_Total",                 # Q (index 16)
    "Valor_Total_Cobro",           # R (index 17)
    "Valor_Comision",              # S (index 18)
    "F_Plazo",                     # T (index 19)
    "Poliza",                      # U (index 20)
    "Aseguradora",                 # V (index 21)
    "Ramo",                        # W (index 22)
    "Tomador",                     # X (index 23)
    "Tipo_Persona",                # Y (index 24)
    "Tipo_Doc",                    # Z (index 25)
    "Identificacion",              # AA (index 26)
    "Telefono_Of",                 # AB (index 27)
    "Telefono_Pers",               # AC (index 28)
    "Celular_Pers",                # AD (index 29)
    "Celular_Lab",                 # AE (index 30)
    "Mail_Lab",                    # AF (index 31)
    "Mail_Pers",                   # AG (index 32)
    "Observacion_A",               # AH (index 33)
    "Observacion_B",               # AI (index 34)
    "Observacion_C",               # AJ (index 35)
    "Recibo_Sin_Liberar",          # AK (index 36)
    "Carta_Cobro",                 # AL (index 37)
    "Ejecutivo",                   # AM (index 38)
    "Ejecutivo_Cod",               # AN (index 39)
    "Placa",                       # AO (index 40)
    "Linea_Vehiculo",              # AP (index 41)
    "Modelo_Vehiculo",             # AQ (index 42)
    "Tipo_Vehiculo",               # AR (index 43)
    "Marca_Vehiculo",              # AS (index 44)
    "Descripcion_Riesgo",          # AT (index 45)
    "Fasecolda",                   # AU (index 46)
    "Unidad",                      # AV (index 47)
    "Forma_Recaudo_Poliza",        # AW (index 48)
]


# Human-readable column descriptions with actual Celer column names
COLUMN_DESCRIPTIONS: Dict[OutputColumn, str] = {
    OutputColumn.A: "ID_Secuencial",
    OutputColumn.B: "Días",
    OutputColumn.C: "Tomador",
    OutputColumn.D: "Tipo_Doc",
    OutputColumn.E: "Identificacion",
    OutputColumn.F: "Poliza",
    OutputColumn.G: "Documento",
    OutputColumn.H: "Cuota",
    OutputColumn.I: "Placa",
    OutputColumn.J: "Saldo",
    OutputColumn.K: "Aseguradora",
    OutputColumn.L: "Ramo",
    OutputColumn.M: "Carta_Cobro",
    OutputColumn.N: "F_Inicio",
    OutputColumn.O: "F_Expedicion",
    OutputColumn.P: "F_Creacion",
    OutputColumn.Q: "Ejecutivo",
    OutputColumn.R: "Unidad",
    OutputColumn.S: "Descripcion_Riesgo",
    OutputColumn.T: "Celular_Pers",
    OutputColumn.U: "Celular_Lab",
    OutputColumn.V: "Mail_Lab",
    OutputColumn.W: "Mail_Pers",
}


# Named column mapping for transformation
NAMED_COLUMN_MAPPING: Dict[OutputColumn, Optional[str]] = {
    OutputColumn.A: None,  # Generated
    OutputColumn.B: "Días",
    OutputColumn.C: "Tomador",
    OutputColumn.D: "Tipo_Doc",
    OutputColumn.E: "Identificacion",
    OutputColumn.F: "Poliza",
    OutputColumn.G: "Documento",
    OutputColumn.H: "Cuota",
    OutputColumn.I: "Placa",
    OutputColumn.J: "Saldo",
    OutputColumn.K: "Aseguradora",
    OutputColumn.L: "Ramo",
    OutputColumn.M: "Carta_Cobro",
    OutputColumn.N: "F_Inicio",
    OutputColumn.O: "F_Expedicion",
    OutputColumn.P: "F_Creacion",
    OutputColumn.Q: "Ejecutivo",
    OutputColumn.R: "Unidad",
    OutputColumn.S: "Descripcion_Riesgo",
    OutputColumn.T: "Celular_Pers",
    OutputColumn.U: "Celular_Lab",
    OutputColumn.V: "Mail_Lab",
    OutputColumn.W: "Mail_Pers",
}
