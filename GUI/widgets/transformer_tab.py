"""
Transformer Tab - Interface for TRANSFORMER CELER system
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTextEdit, QProgressBar, QGroupBox, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from widgets.file_drop_widget import FileDropWidget


class TransformerTab(QWidget):
    """Tab for Celer transformation operations"""
    
    processStarted = pyqtSignal(str)  # Emits file path to process
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI components"""
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        # Create content widget
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title = QLabel("TRANSFORMER CELER")
        title.setProperty("heading", True)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        description = QLabel(
            "Transforma archivos de Celer al formato requerido para conciliación"
        )
        description.setProperty("secondary", True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)
        
        # File drop zone
        file_group = QGroupBox("Cargar Archivo")
        file_layout = QVBoxLayout()
        
        self.drop_widget = FileDropWidget(accepted_extensions=['.xlsb', '.xlsx', '.xml'])
        self.drop_widget.fileDropped.connect(self.on_file_dropped)
        file_layout.addWidget(self.drop_widget)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Options group (placeholder for future options)
        options_group = QGroupBox("Opciones de Transformación")
        options_layout = QVBoxLayout()
        
        self.info_label = QLabel("• Soporta archivos XLSX, XLSB y XML")
        self.info_label.setProperty("secondary", True)
        options_layout.addWidget(self.info_label)
        
        self.info_label2 = QLabel("• Normalización de números de recibo (últimos 9 dígitos)")
        self.info_label2.setProperty("secondary", True)
        options_layout.addWidget(self.info_label2)
        
        self.info_label3 = QLabel("• Limpieza y formateo de datos")
        self.info_label3.setProperty("secondary", True)
        options_layout.addWidget(self.info_label3)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.process_button = QPushButton("🚀 Procesar Archivo")
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
        self.results_text.setMaximumHeight(200)
        self.results_text.setPlaceholderText("Los resultados de la transformación aparecerán aquí...")
        results_layout.addWidget(self.results_text)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        layout.addStretch()
        content_widget.setLayout(layout)
        
        # Set content widget to scroll area
        scroll.setWidget(content_widget)
        
        # Set scroll area as main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
    def on_file_dropped(self, file_path: str):
        """Handle file drop event"""
        self.current_file = file_path
        self.process_button.setEnabled(True)
        self.results_text.append(f"✓ Archivo cargado: {file_path}\n")
        
    def on_process_clicked(self):
        """Handle process button click"""
        if self.current_file:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.process_button.setEnabled(False)
            self.processStarted.emit(self.current_file)
            
    def update_progress(self, value: int):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        
    def show_results(self, success: bool, message: str, output_file: str = None):
        """Show processing results"""
        self.progress_bar.setVisible(False)
        self.process_button.setEnabled(True)
        
        if success:
            self.results_text.append(f"\n✅ Transformación completada exitosamente\n")
            if output_file:
                self.results_text.append(f"📄 Archivo generado: {output_file}\n")
            self.results_text.append(f"{message}\n")
        else:
            self.results_text.append(f"\n❌ Error en la transformación\n")
            self.results_text.append(f"{message}\n")
            
    def clear_all(self):
        """Clear all inputs and results"""
        self.current_file = None
        self.drop_widget.reset()
        self.results_text.clear()
        self.process_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
