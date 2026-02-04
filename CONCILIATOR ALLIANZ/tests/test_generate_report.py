"""
Test script to generate report with predefined selection
"""
import sys
from pathlib import Path

# Add parent directory
sys.path.insert(0, str(Path(__file__).parent))

from conciliator import AllianzConciliator

# File paths
base_dir = Path(__file__).parent
celer_file = base_dir.parent / "TRANSFORMER CELER" / "output" / "Cartera_Transformada_XML_20260123_143400.xlsx"
personas_file = base_dir / "INPUT" / "PERSONAS" / "Informe Intermediario UNION AGENCIA DE SEGUROS LTDA_1701932_11_Jan_2026 (2).xlsb"
colectivas_file = base_dir / "INPUT" / "COLECTIVAS" / "Informe Intermediario UNION AGENCIA DE SEGUROS LTDA_1701932_11_Jan_2026 (1).xlsb"

# Create conciliator with PERSONAS only
conciliator = AllianzConciliator(
    celer_file_path=celer_file,
    allianz_personas_path=personas_file,
    allianz_colectivas_path=colectivas_file,
    data_source='personas'  # PERSONAS only
)

# Run conciliation
print("\n" + "=" * 80)
print("TEST: GENERACION DE REPORTE TXT - PERSONAS ONLY")
print("=" * 80)

success = conciliator.run()

if success:
    print("\n✅ Conciliacion completada exitosamente!")
else:
    print("\n❌ Error en la conciliacion")
