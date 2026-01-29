"""
Worker Threads - Background processing
"""
from PyQt6.QtCore import QThread, pyqtSignal
import sys
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
            
            # Import the transformer main module
            import main as transformer_main
            procesar_archivo = transformer_main.procesar_archivo
            
            self.progress.emit(30)
            
            # Process the file
            output_file = procesar_archivo(self.file_path)
            
            self.progress.emit(80)
            
            if output_file:
                message = f"Archivo transformado exitosamente"
                self.finished.emit(True, message, output_file)
            else:
                self.finished.emit(False, "No se pudo generar el archivo de salida", "")
                
            self.progress.emit(100)
            
        except Exception as e:
            error_msg = f"Error durante la transformación: {str(e)}"
            self.finished.emit(False, error_msg, "")


class ConciliatorWorker(QThread):
    """Worker thread for Allianz conciliation"""
    
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str, list)  # success, summary, output_files
    
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        
    def run(self):
        """Run the conciliation process"""
        try:
            # Add CONCILIATOR ALLIANZ path to sys.path
            conciliator_path = Path(__file__).parent.parent.parent / "CONCILIATOR ALLIANZ"
            if str(conciliator_path) not in sys.path:
                sys.path.insert(0, str(conciliator_path))
            
            self.progress.emit(10)
            
            # Import the conciliator main module
            import main as conciliator_main
            load_softseguros_data = conciliator_main.load_softseguros_data
            load_celer_data = conciliator_main.load_celer_data
            load_allianz_data = conciliator_main.load_allianz_data
            combine_data_sources = conciliator_main.combine_data_sources
            run_conciliation = conciliator_main.run_conciliation
            save_report_to_file = conciliator_main.save_report_to_file
            
            self.progress.emit(20)
            
            # Load data
            soft_df = load_softseguros_data(self.config['softseguros'])
            self.progress.emit(30)
            
            celer_df = load_celer_data(self.config['celer'])
            self.progress.emit(40)
            
            allianz_df = load_allianz_data(self.config['allianz'])
            self.progress.emit(50)
            
            # Combine data sources
            combined_df = combine_data_sources(soft_df, celer_df)
            self.progress.emit(60)
            
            # Run conciliation
            results = run_conciliation(combined_df, allianz_df)
            self.progress.emit(80)
            
            # Save reports
            output_files = []
            if self.config.get('export_txt', True):
                txt_file = save_report_to_file(results)
                if txt_file:
                    output_files.append(txt_file)
            
            self.progress.emit(90)
            
            # Generate summary
            summary = self.generate_summary(results)
            
            self.progress.emit(100)
            self.finished.emit(True, summary, output_files)
            
        except Exception as e:
            error_msg = f"Error durante la conciliación: {str(e)}"
            self.finished.emit(False, error_msg, [])
            
    def generate_summary(self, results: dict) -> str:
        """Generate results summary"""
        summary = []
        
        caso1 = results.get('caso_1', [])
        caso2_especial = results.get('caso_2_especial', [])
        caso2 = results.get('caso_2', [])
        caso3_allianz = results.get('caso_3_allianz', [])
        caso3_combined = results.get('caso_3_combined', [])
        
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
