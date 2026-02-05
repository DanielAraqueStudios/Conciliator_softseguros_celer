"""
Configuration Manager - Handle application settings
"""
import json
from pathlib import Path
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class ConfigManager:
    """Manage application configuration"""
    
    def __init__(self):
        self.config_file = Path(__file__).parent.parent / "config.json"
        self.config = self.load_config()
        
    def load_config(self) -> dict:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return {}
        return {}
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
    
    def is_first_run(self) -> bool:
        """Check if this is the first run"""
        return not self.config_file.exists() or 'output_directory' not in self.config
    
    def setup_output_directory(self, parent_widget=None) -> bool:
        """
        Setup output directory with user dialog
        Returns True if successful, False if cancelled
        """
        # Show info dialog
        msg_box = QMessageBox(parent_widget)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Configuración Inicial")
        msg_box.setText("Bienvenido al Sistema de Conciliación")
        msg_box.setInformativeText(
            "Por favor, seleccione la carpeta donde se guardarán los reportes de conciliación.\n\n"
            "Esta carpeta se usará para guardar todos los archivos de salida del sistema."
        )
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        
        result = msg_box.exec()
        if result == QMessageBox.StandardButton.Cancel:
            return False
        
        # Select directory
        output_dir = QFileDialog.getExistingDirectory(
            parent_widget,
            "Seleccionar Carpeta de Salida para Reportes",
            str(Path.home() / "Documents"),
            QFileDialog.Option.ShowDirsOnly
        )
        
        if output_dir:
            self.set('output_directory', output_dir)
            
            # Show success message
            success_msg = QMessageBox(parent_widget)
            success_msg.setIcon(QMessageBox.Icon.Information)
            success_msg.setWindowTitle("Configuración Guardada")
            success_msg.setText(f"Carpeta de salida configurada correctamente:")
            success_msg.setInformativeText(output_dir)
            success_msg.exec()
            
            return True
        
        return False
    
    def get_output_directory(self) -> Path:
        """Get output directory path"""
        output_dir = self.get('output_directory')
        if output_dir:
            path = Path(output_dir)
            # Create if doesn't exist
            path.mkdir(parents=True, exist_ok=True)
            return path
        
        # Fallback to default
        default_path = Path(__file__).parent.parent / "CONCILIATOR ALLIANZ" / "output"
        default_path.mkdir(parents=True, exist_ok=True)
        return default_path
