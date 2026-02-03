"""
File Drop Widget - Drag and drop zone for file selection
"""
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QFileDialog
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
        
        # Icon label
        self.icon_label = QLabel("📁")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 48pt; background: transparent; border: none;")
        self.icon_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        
        # Text label
        self.text_label = QLabel("Arrastra y suelta archivos aquí")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setProperty("subheading", True)
        self.text_label.setStyleSheet("background: transparent; border: none;")
        self.text_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        
        # OR label
        or_label = QLabel("o")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        or_label.setProperty("secondary", True)
        or_label.setStyleSheet("background: transparent; border: none; margin: 5px;")
        or_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        
        # Browse button
        self.browse_button = QPushButton("📂 Seleccionar Archivo")
        self.browse_button.clicked.connect(self.browse_file)
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        
        # Supported formats label
        formats_text = ", ".join(self.accepted_extensions)
        self.formats_label = QLabel(f"Formatos: {formats_text}")
        self.formats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.formats_label.setProperty("secondary", True)
        self.formats_label.setStyleSheet("background: transparent; border: none;")
        self.formats_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addWidget(or_label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.formats_label)
        
        self.setLayout(layout)
        
    def browse_file(self):
        """Open file dialog to browse for file"""
        # Build filter string
        filter_parts = []
        for ext in self.accepted_extensions:
            filter_parts.append(f"*{ext}")
        filter_string = f"Archivos ({' '.join(filter_parts)})"
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            filter_string
        )
        
        if file_path:
            self.fileDropped.emit(file_path)
            file_name = Path(file_path).name
            self.text_label.setText(f"✓ {file_name}")
            self.text_label.setStyleSheet("color: #10b981; font-weight: bold; background: transparent; border: none;")
            self.icon_label.setText("✅")
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            # Check if at least one file has valid extension
            valid = False
            for url in event.mimeData().urls():
                file_path = Path(url.toLocalFile())
                if file_path.suffix.lower() in self.accepted_extensions:
                    valid = True
                    break
            
            if valid:
                event.acceptProposedAction()
                self.setStyleSheet("""
                    FileDropWidget {
                        border: 2px solid #3b82f6;
                        border-radius: 8px;
                        background-color: #363654;
                    }
                """)
                    
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
        if not event.mimeData().hasUrls():
            return
        
        event.acceptProposedAction()
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        
        for file_path in files:
            path = Path(file_path)
            if path.suffix.lower() in self.accepted_extensions and path.is_file():
                self.fileDropped.emit(str(path))
                self.text_label.setText(f"✓ {path.name}")
                self.text_label.setStyleSheet("color: #10b981; font-weight: bold; background: transparent; border: none;")
                self.icon_label.setText("✅")
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
        self.text_label.setStyleSheet("background: transparent; border: none;")
        self.icon_label.setText("📁")
