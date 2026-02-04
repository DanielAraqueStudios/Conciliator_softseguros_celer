"""
Worker Threads - Background processing
"""
from PyQt6.QtCore import QThread, pyqtSignal
import sys
import importlib.util
from pathlib import Path


class TransformerWorker(QThread):
    """Worker thread for Celer transformation"""
    
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str, str)  # success, message, output_file
    
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        
    def run(self):
        """Run the transformation process"""
        try:
            # Add TRANSFORMER CELER path to sys.path
            transformer_path = Path(__file__).parent.parent.parent / "TRANSFORMER CELER"
            if str(transformer_path) not in sys.path:
                sys.path.insert(0, str(transformer_path))
            
            self.progress.emit(10)
            
            # Import the transformer module
            import transformer as transformer_main
            
            self.progress.emit(30)
            
            # Determine file type and call appropriate function
            file_path = Path(self.file_path)
            file_extension = file_path.suffix.lower()
            
            if file_extension == '.xml':
                # Process XML file
                output_file = transformer_main.transform_xml_format(file_path)
            else:
                # Process XLSX/XLSB file
                output_file = transformer_main.transform_xlsx_format(file_path)
            
            self.progress.emit(80)
            
            if output_file:
                message = f"Archivo transformado exitosamente"
                self.finished.emit(True, message, str(output_file.absolute()))
            else:
                self.finished.emit(False, "No se pudo generar el archivo de salida", "")
                
            self.progress.emit(100)
            
        except Exception as e:
            error_msg = f"Error durante la transformación: {str(e)}"
            self.finished.emit(False, error_msg, "")


class ConciliatorWorker(QThread):
    """Worker thread for Allianz conciliation"""
    
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str, list, dict)  # success, summary, output_files, results
    
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        
    def run(self):
        """Run the conciliation process"""
        try:
            # Store original sys.path
            original_sys_path = sys.path.copy()
            
            # Clear sys.path and add only necessary paths
            conciliator_path = Path(__file__).parent.parent.parent / "CONCILIATOR ALLIANZ"
            root_path = Path(__file__).parent.parent.parent
            
            # Reset sys.path with correct order
            sys.path = [str(root_path), str(conciliator_path)] + original_sys_path
            
            self.progress.emit(10)
            
            # Import the conciliator module using importlib
            import importlib.util
            spec = importlib.util.spec_from_file_location("conciliator_module", conciliator_path / "conciliator.py")
            conciliator_main = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(conciliator_main)
            
            self.progress.emit(20)
            
            # Create conciliator instance
            conciliator = conciliator_main.AllianzConciliator(
                allianz_personas_path=self.config['allianz_personas'],
                allianz_colectivas_path=self.config['allianz_colectivas'],
                data_source=self.config['allianz_source'],
                data_source_type='both',
                softseguros_file_path=self.config['softseguros'],
                celer_file_path=self.config['celer']
            )
            
            self.progress.emit(40)
            
            # Run conciliation
            conciliator.run()
            
            self.progress.emit(80)
            
            # Generate summary
            summary = self.generate_summary_from_conciliator(conciliator)
            
            # Get output files
            output_files = []
            if self.config.get('export_txt', True):
                output_path = conciliator_path / "output"
                if output_path.exists():
                    txt_files = sorted(output_path.glob("Reporte_Conciliacion_*.txt"))
                    if txt_files:
                        output_files.append(str(txt_files[-1]))
            
            self.progress.emit(100)
            
            # Restore original sys.path
            sys.path = original_sys_path
            
            # Pass results to dashboard
            self.finished.emit(True, summary, output_files, conciliator.results)
            
        except Exception as e:
            error_msg = f"Error durante la conciliación: {str(e)}"
            self.finished.emit(False, error_msg, [], {})
            
    def generate_summary_from_conciliator(self, conciliator) -> str:
        """Generate results summary from conciliator instance"""
        summary = []
        
        # Map the correct keys from conciliator.results
        caso1 = conciliator.results.get('no_pagado', [])
        caso2_especial = conciliator.results.get('actualizar_recibo_softseguros', [])
        caso2 = conciliator.results.get('actualizar_sistema', [])
        caso3_allianz = conciliator.results.get('only_allianz', [])
        caso3_combined = conciliator.results.get('only_combined', [])
        
        summary.append(f"CASO 1 - Coincidencias exactas: {len(caso1)} pólizas")
        summary.append(f"CASO 2 ESPECIAL - Recibos Allianz en Softseguros: {len(caso2_especial)} pólizas")
        summary.append(f"CASO 2 - Recibos sin procesar: {len(caso2)} pólizas")
        summary.append(f"CASO 3 - Saldos pendientes Allianz: {len(caso3_allianz)} pólizas")
        summary.append(f"CASO 3 - Saldos pendientes Combined: {len(caso3_combined)} pólizas")
        summary.append("")
        summary.append(f"Total pólizas procesadas: {sum([len(caso1), len(caso2_especial), len(caso2), len(caso3_allianz), len(caso3_combined)])}")
        
        # Count CELER records that need Softseguros update
        needs_update = sum(1 for item in caso1 if item.get('necesita_actualizar_softseguros', False))
        if needs_update > 0:
            summary.append("")
            summary.append(f"⚠️ {needs_update} registros de CELER necesitan actualización en Softseguros")
        
        return "\n".join(summary)
