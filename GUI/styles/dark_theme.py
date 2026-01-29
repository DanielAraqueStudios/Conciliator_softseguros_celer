"""
Dark Theme Stylesheet for SEGUROS UNIÓN
Modern dark mode color palette
"""

# Color Palette
COLORS = {
    'background': '#1e1e2e',
    'surface': '#2a2a3e',
    'surface_light': '#363654',
    'accent': '#3b82f6',
    'accent_hover': '#2563eb',
    'success': '#10b981',
    'warning': '#f59e0b',
    'error': '#ef4444',
    'text': '#e5e7eb',
    'text_secondary': '#9ca3af',
    'border': '#4b5563',
}

DARK_THEME_STYLESHEET = f"""
QWidget {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}}

QMainWindow {{
    background-color: {COLORS['background']};
}}

/* Tabs */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    background-color: {COLORS['surface']};
    border-radius: 8px;
}}

QTabBar::tab {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_secondary']};
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border: 1px solid {COLORS['border']};
    border-bottom: none;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['accent']};
    color: white;
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS['surface_light']};
}}

/* Buttons */
QPushButton {{
    background-color: {COLORS['accent']};
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: bold;
    min-width: 100px;
}}

QPushButton:hover {{
    background-color: {COLORS['accent_hover']};
}}

QPushButton:pressed {{
    background-color: #1e40af;
}}

QPushButton:disabled {{
    background-color: {COLORS['surface_light']};
    color: {COLORS['text_secondary']};
}}

QPushButton[success="true"] {{
    background-color: {COLORS['success']};
}}

QPushButton[warning="true"] {{
    background-color: {COLORS['warning']};
}}

QPushButton[error="true"] {{
    background-color: {COLORS['error']};
}}

/* Cards/Panels */
QFrame[frameShape="4"] {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 16px;
}}

/* Labels */
QLabel {{
    color: {COLORS['text']};
    background-color: transparent;
}}

QLabel[heading="true"] {{
    font-size: 14pt;
    font-weight: bold;
    color: {COLORS['text']};
}}

QLabel[subheading="true"] {{
    font-size: 12pt;
    font-weight: 600;
    color: {COLORS['text']};
}}

QLabel[secondary="true"] {{
    color: {COLORS['text_secondary']};
}}

/* Progress Bar */
QProgressBar {{
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    text-align: center;
    background-color: {COLORS['surface_light']};
    height: 24px;
}}

QProgressBar::chunk {{
    background-color: {COLORS['accent']};
    border-radius: 5px;
}}

/* Table */
QTableWidget {{
    background-color: {COLORS['surface']};
    alternate-background-color: {COLORS['surface_light']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    gridline-color: {COLORS['border']};
}}

QTableWidget::item {{
    padding: 8px;
}}

QTableWidget::item:selected {{
    background-color: {COLORS['accent']};
    color: white;
}}

QHeaderView::section {{
    background-color: {COLORS['surface_light']};
    color: {COLORS['text']};
    padding: 8px;
    border: none;
    font-weight: bold;
}}

/* Scroll Bar */
QScrollBar:vertical {{
    background-color: {COLORS['surface']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['text_secondary']};
}}

QScrollBar:horizontal {{
    background-color: {COLORS['surface']};
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-width: 20px;
}}

/* Text Edit / Plain Text Edit */
QTextEdit, QPlainTextEdit {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px;
    color: {COLORS['text']};
}}

/* Line Edit */
QLineEdit {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px;
    color: {COLORS['text']};
}}

QLineEdit:focus {{
    border: 2px solid {COLORS['accent']};
}}

/* Combo Box */
QComboBox {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px;
    color: {COLORS['text']};
}}

QComboBox:hover {{
    border: 1px solid {COLORS['accent']};
}}

QComboBox::drop-down {{
    border: none;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    selection-background-color: {COLORS['accent']};
}}

/* Spin Box */
QSpinBox {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px;
    color: {COLORS['text']};
}}

/* Check Box */
QCheckBox {{
    color: {COLORS['text']};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLORS['border']};
    border-radius: 4px;
    background-color: {COLORS['surface']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

/* Radio Button */
QRadioButton {{
    color: {COLORS['text']};
    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLORS['border']};
    border-radius: 9px;
    background-color: {COLORS['surface']};
}}

QRadioButton::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

/* Group Box */
QGroupBox {{
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
}}

/* Menu Bar */
QMenuBar {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    border-bottom: 1px solid {COLORS['border']};
}}

QMenuBar::item:selected {{
    background-color: {COLORS['accent']};
}}

QMenu {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
}}

QMenu::item:selected {{
    background-color: {COLORS['accent']};
}}

/* Status Bar */
QStatusBar {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    border-top: 1px solid {COLORS['border']};
}}

/* Tool Tip */
QToolTip {{
    background-color: {COLORS['surface_light']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 4px;
}}
"""

def get_stylesheet():
    """Return the complete dark theme stylesheet"""
    return DARK_THEME_STYLESHEET

def get_colors():
    """Return the color palette dictionary"""
    return COLORS
