"""
Conciliator Tab - Interface for CONCILIATOR ALLIANZ system
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTextEdit, QProgressBar, QGroupBox, 
                             QComboBox, QCheckBox, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt, pyqtSignal
from widgets.file_drop_widget import FileDropWidget


class ConciliatorTab(QWidget):
    """Tab for Allianz conciliation operations"""
    
    processStarted = pyqtSignal(dict)  # Emits config dict with file paths
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.softseguros_file = None
        self.celer_file = None
        self.allianz_personas_file = None
        self.allianz_colectivas_file = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title = QLabel("CONCILIATOR ALLIANZ")
        title.setProperty("heading", True)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        description = QLabel(
            "Concilia datos de Softseguros, Celer y Allianz"
        )
        description.setProperty("secondary", True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)
        
        # File drop zones
        files_group = QGroupBox("Archivos de Entrada")
        files_layout = QVBoxLayout()
        
        # Softseguros
        soft_label = QLabel("1. Archivo Softseguros:")
        soft_label.setProperty("subheading", True)
        files_layout.addWidget(soft_label)
        
        self.soft_drop = FileDropWidget(accepted_extensions=['.xlsx', '.xlsb'])
        self.soft_drop.fileDropped.connect(self.on_soft_dropped)
        files_layout.addWidget(self.soft_drop)
        
        # Celer
        celer_label = QLabel("2. Archivo Celer:")
        celer_label.setProperty("subheading", True)
        files_layout.addWidget(celer_label)
        
        self.celer_drop = FileDropWidget(accepted_extensions=['.xlsx', '.xlsb'])
        self.celer_drop.fileDropped.connect(self.on_celer_dropped)
        files_layout.addWidget(self.celer_drop)
        
        # Allianz Personas
        allianz_personas_label = QLabel("3a. Archivo Allianz Personas:")
        allianz_personas_label.setProperty("subheading", True)
        files_layout.addWidget(allianz_personas_label)
        
        self.allianz_personas_drop = FileDropWidget(accepted_extensions=['.xlsb', '.xlsx'])
        self.allianz_personas_drop.fileDropped.connect(self.on_allianz_personas_dropped)
        files_layout.addWidget(self.allianz_personas_drop)
        
        # Allianz Colectivas
        allianz_colectivas_label = QLabel("3b. Archivo Allianz Colectivas:")
        allianz_colectivas_label.setProperty("subheading", True)
        files_layout.addWidget(allianz_colectivas_label)
        
        self.allianz_colectivas_drop = FileDropWidget(accepted_extensions=['.xlsb', '.xlsx'])
        self.allianz_colectivas_drop.fileDropped.connect(self.on_allianz_colectivas_dropped)
        files_layout.addWidget(self.allianz_colectivas_drop)
        
        files_group.setLayout(files_layout)
        layout.addWidget(files_group)
        
        # Options
        options_group = QGroupBox("Opciones de Conciliación")
        options_layout = QVBoxLayout()
        
        # Allianz data source selection
        allianz_source_layout = QHBoxLayout()
        allianz_source_label = QLabel("Procesar Allianz:")
        allianz_source_layout.addWidget(allianz_source_label)
        
        self.allianz_source_group = QButtonGroup()
        self.allianz_both_radio = QRadioButton("Ambos")
        self.allianz_personas_radio = QRadioButton("Solo Personas")
        self.allianz_colectivas_radio = QRadioButton("Solo Colectivas")
        self.allianz_both_radio.setChecked(True)
        
        self.allianz_source_group.addButton(self.allianz_both_radio, 0)
        self.allianz_source_group.addButton(self.allianz_personas_radio, 1)
        self.allianz_source_group.addButton(self.allianz_colectivas_radio, 2)
        
        # Connect radio buttons to check_ready
        self.allianz_both_radio.toggled.connect(self.check_ready)
        self.allianz_personas_radio.toggled.connect(self.check_ready)
        self.allianz_colectivas_radio.toggled.connect(self.check_ready)
        
        allianz_source_layout.addWidget(self.allianz_both_radio)
        allianz_source_layout.addWidget(self.allianz_personas_radio)
        allianz_source_layout.addWidget(self.allianz_colectivas_radio)
        allianz_source_layout.addStretch()
        options_layout.addLayout(allianz_source_layout)
        
        # Case selection
        case_layout = QHBoxLayout()
        case_label = QLabel("Mostrar casos:")
        self.case_combo = QComboBox()
        self.case_combo.addItems([
            "Todos los casos",
            "CASO 1 - Coincidencias exactas",
            "CASO 2 ESPECIAL - Recibos Allianz en Softseguros",
            "CASO 2 - Recibos sin procesar",
            "CASO 3 - Saldos pendientes"
        ])
        case_layout.addWidget(case_label)
        case_layout.addWidget(self.case_combo)
        case_layout.addStretch()
        options_layout.addLayout(case_layout)
        
        # Export options
        self.export_txt_check = QCheckBox("Exportar reporte TXT")
        self.export_txt_check.setChecked(True)
        options_layout.addWidget(self.export_txt_check)
        
        self.export_excel_check = QCheckBox("Exportar reporte Excel")
        self.export_excel_check.setChecked(False)
        options_layout.addWidget(self.export_excel_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.process_button = QPushButton("🔍 Iniciar Conciliación")
        self.process_button.setEnabled(False)
        self.process_button.setProperty("success", True)
        self.process_button.clicked.connect(self.on_process_clicked)
        
        self.clear_button = QPushButton("🗑️ Limpiar")
        self.clear_button.clicked.connect(self.clear_all)
        
        button_layout.addStretch()
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Results area
        results_group = QGroupBox("Resultados")
        results_layout = QVBoxLayout()
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("Los resultados de la conciliación aparecerán aquí...")
        results_layout.addWidget(self.results_text)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        self.setLayout(layout)
        
    def on_soft_dropped(self, file_path: str):
        """Handle Softseguros file drop"""
        self.softseguros_file = file_path
        self.check_ready()
        
    def on_celer_dropped(self, file_path: str):
        """Handle Celer file drop"""
        self.celer_file = file_path
        self.check_ready()
        
    def load_celer_file(self, file_path: str):
        """Load Celer file programmatically (from transformer)"""
        from pathlib import Path
        path = Path(file_path)
        
        self.celer_file = str(path)
        self.celer_drop.text_label.setText(f"✓ {path.name}")
        self.celer_drop.text_label.setStyleSheet("color: #10b981; font-weight: bold; background: transparent; border: none;")
        self.celer_drop.icon_label.setText("✅")
        self.results_text.append(f"\n✓ Archivo Celer cargado automáticamente: {path.name}\n")
        self.check_ready()
        
    def on_allianz_personas_dropped(self, file_path: str):
        """Handle Allianz Personas file drop"""
        self.allianz_personas_file = file_path
        self.check_ready()
        
    def on_allianz_colectivas_dropped(self, file_path: str):
        """Handle Allianz Colectivas file drop"""
        self.allianz_colectivas_file = file_path
        self.check_ready()
        
    def check_ready(self):
        """Check if required files are loaded based on Allianz selection"""
        allianz_ready = False
        
        # Check which Allianz files are needed
        if self.allianz_both_radio.isChecked():
            allianz_ready = self.allianz_personas_file and self.allianz_colectivas_file
        elif self.allianz_personas_radio.isChecked():
            allianz_ready = self.allianz_personas_file is not None
        elif self.allianz_colectivas_radio.isChecked():
            allianz_ready = self.allianz_colectivas_file is not None
        
        if self.softseguros_file and self.celer_file and allianz_ready:
            self.process_button.setEnabled(True)
            self.results_text.append("\n✓ Todos los archivos necesarios cargados. Listo para conciliar.\n")
        
    def on_process_clicked(self):
        """Handle process button click"""
        # Determine which Allianz source to use
        if self.allianz_both_radio.isChecked():
            allianz_source = 'both'
        elif self.allianz_personas_radio.isChecked():
            allianz_source = 'personas'
        else:
            allianz_source = 'colectivas'
        
        config = {
            'softseguros': self.softseguros_file,
            'celer': self.celer_file,
            'allianz_personas': self.allianz_personas_file,
            'allianz_colectivas': self.allianz_colectivas_file,
            'allianz_source': allianz_source,
            'case_filter': self.case_combo.currentIndex(),
            'export_txt': self.export_txt_check.isChecked(),
            'export_excel': self.export_excel_check.isChecked()
        }
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.process_button.setEnabled(False)
        self.processStarted.emit(config)
        
    def update_progress(self, value: int):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        
    def show_results(self, success: bool, results_summary: str, output_files: list = None):
        """Show conciliation results"""
        self.progress_bar.setVisible(False)
        self.process_button.setEnabled(True)
        
        if success:
            self.results_text.append(f"\n{'='*60}\n")
            self.results_text.append(f"✅ CONCILIACIÓN COMPLETADA\n")
            self.results_text.append(f"{'='*60}\n\n")
            self.results_text.append(results_summary)
            
            if output_files:
                self.results_text.append(f"\n📄 Archivos generados:\n")
                for file in output_files:
                    self.results_text.append(f"  • {file}\n")
        else:
            self.results_text.append(f"\n❌ Error en la conciliación\n")
            self.results_text.append(f"{results_summary}\n")
            
    def clear_all(self):
        """Clear all inputs and results"""
        self.softseguros_file = None
        self.celer_file = None
        self.allianz_personas_file = None
        self.allianz_colectivas_file = None
        
        self.soft_drop.reset()
        self.celer_drop.reset()
        self.allianz_personas_drop.reset()
        self.allianz_colectivas_drop.reset()
        
        self.results_text.clear()
        self.process_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
