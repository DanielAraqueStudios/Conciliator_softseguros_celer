"""
Main Window - Application main interface
"""
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QStatusBar, QWidget, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from widgets.transformer_tab import TransformerTab
from widgets.conciliator_tab import ConciliatorTab
from widgets.dashboard_tab import DashboardTab
from workers import TransformerWorker, ConciliatorWorker
from config import ConfigManager


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seguros Unión - Sistema de Conciliación v2.0")
        self.setMinimumSize(1200, 800)
        
        # Configuration manager
        self.config = ConfigManager()
        
        # Workers
        self.transformer_worker = None
        self.conciliator_worker = None
        
        self.setup_ui()
        
        # Check first run and setup output directory
        self.check_first_run()
        
    def check_first_run(self):
        """Check if this is the first run and setup configuration"""
        if self.config.is_first_run():
            success = self.config.setup_output_directory(self)
            if not success:
                # User cancelled, show warning and use default
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Configuración No Completada")
                msg.setText("No se configuró la carpeta de salida.")
                msg.setInformativeText(
                    "Se usará la carpeta predeterminada:\n"
                    f"{self.config.get_output_directory()}"
                )
                msg.exec()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Menu bar
        menubar = self.menuBar()
        
        # Settings menu
        settings_menu = menubar.addMenu("⚙️ Configuración")
        
        change_output_action = settings_menu.addAction("📁 Cambiar Carpeta de Salida")
        change_output_action.triggered.connect(self.change_output_directory)
        
        show_output_action = settings_menu.addAction("📂 Abrir Carpeta de Salida")
        show_output_action.triggered.connect(self.open_output_directory)
        
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
        
        # Set initial output directory in conciliator tab
        self.conciliator_tab.set_output_directory(str(self.config.get_output_directory()))
        
    def connect_signals(self):
        """Connect widget signals to handlers"""
        # Transformer tab
        self.transformer_tab.processStarted.connect(self.on_transformer_started)
        
        # Conciliator tab
        self.conciliator_tab.processStarted.connect(self.on_conciliator_started)
        self.conciliator_tab.outputDirectoryChanged.connect(self.on_output_directory_changed)
        
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
        
        # Add output directory to config
        config['output_directory'] = str(self.config.get_output_directory())
        
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
    
    def on_output_directory_changed(self, new_dir: str):
        """Handle output directory change from conciliator tab"""
        self.config.set('output_directory', new_dir)
        self.status_bar.showMessage(f"✓ Carpeta de salida actualizada: {new_dir}", 5000)
    
    def change_output_directory(self):
        """Allow user to change output directory"""
        from PyQt6.QtWidgets import QFileDialog
        from pathlib import Path
        
        current_dir = str(self.config.get_output_directory())
        
        new_dir = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar Nueva Carpeta de Salida",
            current_dir,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if new_dir:
            self.config.set('output_directory', new_dir)
            # Update the label in conciliator tab
            self.conciliator_tab.set_output_directory(new_dir)
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Configuración Actualizada")
            msg.setText("Carpeta de salida actualizada correctamente:")
            msg.setInformativeText(new_dir)
            msg.exec()
            self.status_bar.showMessage(f"✓ Carpeta de salida actualizada: {new_dir}", 5000)
    
    def open_output_directory(self):
        """Open output directory in file explorer"""
        import subprocess
        import platform
        
        output_dir = str(self.config.get_output_directory())
        
        try:
            if platform.system() == 'Windows':
                subprocess.Popen(['explorer', output_dir])
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', output_dir])
            else:  # Linux
                subprocess.Popen(['xdg-open', output_dir])
            
            self.status_bar.showMessage(f"✓ Carpeta abierta: {output_dir}", 3000)
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText("No se pudo abrir la carpeta")
            msg.setInformativeText(str(e))
            msg.exec()
        
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
