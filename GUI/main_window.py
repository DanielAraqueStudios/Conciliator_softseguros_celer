"""
Main Window - Application main interface
"""
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QStatusBar, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from widgets.transformer_tab import TransformerTab
from widgets.conciliator_tab import ConciliatorTab
from widgets.dashboard_tab import DashboardTab
from workers import TransformerWorker, ConciliatorWorker


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seguros Unión - Sistema de Conciliación v2.0")
        self.setMinimumSize(1200, 800)
        
        # Workers
        self.transformer_worker = None
        self.conciliator_worker = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        
        # Create tabs
        self.transformer_tab = TransformerTab()
        self.conciliator_tab = ConciliatorTab()
        self.dashboard_tab = DashboardTab()
        
        # Add tabs
        self.tabs.addTab(self.transformer_tab, "🔄 Transformador Celer")
        self.tabs.addTab(self.conciliator_tab, "🔍 Conciliador Allianz")
        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        
        layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo")
        
        # Connect signals
        self.connect_signals()
        
    def connect_signals(self):
        """Connect widget signals to handlers"""
        # Transformer tab
        self.transformer_tab.processStarted.connect(self.on_transformer_started)
        
        # Conciliator tab
        self.conciliator_tab.processStarted.connect(self.on_conciliator_started)
        
        # Dashboard tab
        self.dashboard_tab.refresh_button.clicked.connect(self.on_dashboard_refresh)
        
    def on_transformer_started(self, file_path: str):
        """Handle transformer process start"""
        self.status_bar.showMessage(f"Transformando archivo: {file_path}")
        
        # Create and start worker
        self.transformer_worker = TransformerWorker(file_path)
        self.transformer_worker.progress.connect(self.transformer_tab.update_progress)
        self.transformer_worker.finished.connect(self.on_transformer_finished)
        self.transformer_worker.start()
        
    def on_transformer_finished(self, success: bool, message: str, output_file: str):
        """Handle transformer process completion"""
        self.transformer_tab.show_results(success, message, output_file)
        
        if success:
            self.status_bar.showMessage("✓ Transformación completada exitosamente", 5000)
            
            # Auto-load transformed file into conciliator tab
            if output_file:
                self.conciliator_tab.load_celer_file(output_file)
                self.status_bar.showMessage("✓ Archivo Celer cargado automáticamente en Conciliador", 5000)
        else:
            self.status_bar.showMessage("✗ Error en la transformación", 5000)
            
        self.transformer_worker = None
        
    def on_conciliator_started(self, config: dict):
        """Handle conciliator process start"""
        self.status_bar.showMessage("Ejecutando conciliación...")
        
        # Create and start worker
        self.conciliator_worker = ConciliatorWorker(config)
        self.conciliator_worker.progress.connect(self.conciliator_tab.update_progress)
        self.conciliator_worker.finished.connect(self.on_conciliator_finished)
        self.conciliator_worker.start()
        
    def on_conciliator_finished(self, success: bool, summary: str, output_files: list, results: dict = None):
        """Handle conciliator process completion"""
        self.conciliator_tab.show_results(success, summary, output_files)
        
        if success:
            self.status_bar.showMessage("✓ Conciliación completada exitosamente", 5000)
            # Update dashboard with full results
            if results:
                self.dashboard_tab.update_results(results)
        else:
            self.status_bar.showMessage("✗ Error en la conciliación", 5000)
            
        self.conciliator_worker = None
            
    def on_dashboard_refresh(self):
        """Handle dashboard refresh"""
        self.status_bar.showMessage("Dashboard actualizado", 3000)
        
    def closeEvent(self, event):
        """Handle window close event"""
        # Stop any running workers
        if self.transformer_worker and self.transformer_worker.isRunning():
            self.transformer_worker.terminate()
            self.transformer_worker.wait()
            
        if self.conciliator_worker and self.conciliator_worker.isRunning():
            self.conciliator_worker.terminate()
            self.conciliator_worker.wait()
            
        event.accept()
