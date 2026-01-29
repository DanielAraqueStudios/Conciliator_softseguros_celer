"""
File Drop Widget - Drag and drop zone for file selection
"""
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from pathlib import Path


class FileDropWidget(QFrame):
    """Drag and drop widget for file selection"""
    
    fileDropped = pyqtSignal(str)  # Emits file path when dropped
    
    def __init__(self, accepted_extensions=None, parent=None):
        super().__init__(parent)
        self.accepted_extensions = accepted_extensions or ['.xlsx', '.xlsb', '.xml']
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI components"""
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(150)
        self.setStyleSheet("""
            FileDropWidget {
                border: 2px dashed #4b5563;
                border-radius: 8px;
                background-color: #2a2a3e;
            }
            FileDropWidget:hover {
                border-color: #3b82f6;
                background-color: #363654;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icon label (you can add an icon here)
        self.icon_label = QLabel("📁")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 48pt; background: transparent;")
        
        # Text label
        self.text_label = QLabel("Arrastra y suelta archivos aquí")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setProperty("subheading", True)
        
        # Supported formats label
        formats_text = ", ".join(self.accepted_extensions)
        self.formats_label = QLabel(f"Formatos aceptados: {formats_text}")
        self.formats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.formats_label.setProperty("secondary", True)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addWidget(self.formats_label)
        
        self.setLayout(layout)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            # Check if at least one file has valid extension
            for url in event.mimeData().urls():
                file_path = Path(url.toLocalFile())
                if file_path.suffix.lower() in self.accepted_extensions:
                    event.acceptProposedAction()
                    self.setStyleSheet("""
                        FileDropWidget {
                            border: 2px solid #3b82f6;
                            border-radius: 8px;
                            background-color: #363654;
                        }
                    """)
                    return
                    
    def dragLeaveEvent(self, event):
        """Handle drag leave event"""
        self.setStyleSheet("""
            FileDropWidget {
                border: 2px dashed #4b5563;
                border-radius: 8px;
                background-color: #2a2a3e;
            }
            FileDropWidget:hover {
                border-color: #3b82f6;
                background-color: #363654;
            }
        """)
        
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        
        for file_path in files:
            path = Path(file_path)
            if path.suffix.lower() in self.accepted_extensions:
                self.fileDropped.emit(str(path))
                self.text_label.setText(f"✓ Archivo cargado: {path.name}")
                self.text_label.setStyleSheet("color: #10b981; font-weight: bold;")
                break
        
        # Reset style
        self.setStyleSheet("""
            FileDropWidget {
                border: 2px dashed #4b5563;
                border-radius: 8px;
                background-color: #2a2a3e;
            }
            FileDropWidget:hover {
                border-color: #3b82f6;
                background-color: #363654;
            }
        """)
        
    def reset(self):
        """Reset the widget to initial state"""
        self.text_label.setText("Arrastra y suelta archivos aquí")
        self.text_label.setStyleSheet("")
