"""
Dashboard Tab - Metrics and visualizations
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QPushButton, QGroupBox, QTextEdit,
                             QTabWidget)
from PyQt6.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MetricCard(QFrame):
    """Card widget for displaying a metric"""
    
    def __init__(self, title: str, value: str = "0", color: str = "#3b82f6", parent=None):
        super().__init__(parent)
        self.color = color
        self.setup_ui(title, value)
        
    def setup_ui(self, title: str, value: str):
        """Setup the UI"""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            MetricCard {{
                border-left: 4px solid {self.color};
                border-radius: 8px;
                background-color: #2a2a3e;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        self.title_label = QLabel(title)
        self.title_label.setProperty("secondary", True)
        
        self.value_label = QLabel(value)
        self.value_label.setProperty("heading", True)
        self.value_label.setStyleSheet(f"color: {self.color}; font-size: 32pt;")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        
        self.setLayout(layout)
        
    def update_value(self, value: str):
        """Update the metric value"""
        self.value_label.setText(value)


class ChartWidget(FigureCanvasQTAgg):
    """Matplotlib chart widget"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1e1e2e')
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        
        # Style the axes
        self.axes.set_facecolor('#2a2a3e')
        self.axes.tick_params(colors='#e5e7eb')
        self.axes.spines['bottom'].set_color('#4b5563')
        self.axes.spines['top'].set_color('#4b5563')
        self.axes.spines['right'].set_color('#4b5563')
        self.axes.spines['left'].set_color('#4b5563')


class DashboardTab(QWidget):
    """Tab for displaying metrics and charts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conciliator_results = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title = QLabel("DASHBOARD DE MÉTRICAS")
        title.setProperty("heading", True)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Refresh button
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch()
        self.refresh_button = QPushButton("🔄 Actualizar Datos")
        self.refresh_button.clicked.connect(self.refresh_metrics)
        refresh_layout.addWidget(self.refresh_button)
        layout.addLayout(refresh_layout)
        
        # Metrics cards
        metrics_group = QGroupBox("Métricas Generales")
        metrics_layout = QGridLayout()
        
        self.total_records_card = MetricCard("Total Registros", "0", "#3b82f6")
        self.coincidences_card = MetricCard("Coincidencias", "0", "#10b981")
        self.pending_card = MetricCard("Pendientes", "0", "#f59e0b")
        self.match_rate_card = MetricCard("Tasa de Coincidencia", "0%", "#8b5cf6")
        
        metrics_layout.addWidget(self.total_records_card, 0, 0)
        metrics_layout.addWidget(self.coincidences_card, 0, 1)
        metrics_layout.addWidget(self.pending_card, 1, 0)
        metrics_layout.addWidget(self.match_rate_card, 1, 1)
        
        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)
        
        # Charts
        charts_group = QGroupBox("Visualizaciones")
        charts_layout = QHBoxLayout()
        
        # Case distribution chart
        self.case_chart = ChartWidget(self, width=5, height=4, dpi=100)
        charts_layout.addWidget(self.case_chart)
        
        # Amount distribution chart
        self.amount_chart = ChartWidget(self, width=5, height=4, dpi=100)
        charts_layout.addWidget(self.amount_chart)
        
        charts_group.setLayout(charts_layout)
        layout.addWidget(charts_group)
        
        # Details section with tabs for each case
        details_group = QGroupBox("Detalles de Casos")
        details_layout = QVBoxLayout()
        
        self.case_tabs = QTabWidget()
        self.case_tabs.setMinimumHeight(300)
        
        # Create text areas for each case
        self.caso1_text = QTextEdit()
        self.caso1_text.setReadOnly(True)
        self.caso1_text.setPlaceholderText("No hay datos para CASO 1")
        
        self.caso2_especial_text = QTextEdit()
        self.caso2_especial_text.setReadOnly(True)
        self.caso2_especial_text.setPlaceholderText("No hay datos para CASO 2 ESPECIAL")
        
        self.caso2_text = QTextEdit()
        self.caso2_text.setReadOnly(True)
        self.caso2_text.setPlaceholderText("No hay datos para CASO 2")
        
        self.caso3_allianz_text = QTextEdit()
        self.caso3_allianz_text.setReadOnly(True)
        self.caso3_allianz_text.setPlaceholderText("No hay datos para CASO 3 - Allianz")
        
        self.caso3_combined_text = QTextEdit()
        self.caso3_combined_text.setReadOnly(True)
        self.caso3_combined_text.setPlaceholderText("No hay datos para CASO 3 - Softseguros/Celer")
        
        # Add tabs
        self.case_tabs.addTab(self.caso1_text, "CASO 1 - No han pagado")
        self.case_tabs.addTab(self.caso2_especial_text, "CASO 2 ESP - Actualizar Softseguros")
        self.case_tabs.addTab(self.caso2_text, "CASO 2 - Actualizar sistema")
        self.case_tabs.addTab(self.caso3_allianz_text, "CASO 3 - Solo Allianz")
        self.case_tabs.addTab(self.caso3_combined_text, "CASO 3 - Solo Softseguros/Celer")
        
        details_layout.addWidget(self.case_tabs)
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        # Status info
        self.status_label = QLabel("No hay datos para mostrar. Ejecuta una conciliación primero.")
        self.status_label.setProperty("secondary", True)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Initialize with empty charts
        self.update_case_chart({})
        self.update_amount_chart([])
        
    def refresh_metrics(self):
        """Refresh dashboard metrics"""
        # This will be connected to load actual data
        self.status_label.setText("Actualizando datos...")
        
    def update_metrics(self, total: int, coincidences: int, pending: int):
        """Update metric cards"""
        self.total_records_card.update_value(str(total))
        self.coincidences_card.update_value(str(coincidences))
        self.pending_card.update_value(str(pending))
        
        match_rate = (coincidences / total * 100) if total > 0 else 0
        self.match_rate_card.update_value(f"{match_rate:.2f}%")
        
        self.status_label.setText(f"Última actualización: {self.get_current_time()}")
        
    def update_case_chart(self, case_data: dict):
        """Update case distribution chart"""
        self.case_chart.axes.clear()
        
        if case_data:
            cases = list(case_data.keys())
            counts = list(case_data.values())
            colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][:len(cases)]
            
            bars = self.case_chart.axes.bar(cases, counts, color=colors)
            self.case_chart.axes.set_title('Distribución por Casos', color='#e5e7eb', fontsize=12)
            self.case_chart.axes.set_xlabel('Casos', color='#e5e7eb')
            self.case_chart.axes.set_ylabel('Cantidad', color='#e5e7eb')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                self.case_chart.axes.text(bar.get_x() + bar.get_width()/2., height,
                                         f'{int(height)}',
                                         ha='center', va='bottom', color='#e5e7eb')
        else:
            self.case_chart.axes.text(0.5, 0.5, 'Sin datos', 
                                     ha='center', va='center', 
                                     transform=self.case_chart.axes.transAxes,
                                     color='#6b7280', fontsize=16)
            
        self.case_chart.draw()
        
    def update_amount_chart(self, amounts: list):
        """Update amount distribution chart"""
        self.amount_chart.axes.clear()
        
        if amounts:
            self.amount_chart.axes.hist(amounts, bins=20, color='#3b82f6', alpha=0.7)
            self.amount_chart.axes.set_title('Distribución de Montos', color='#e5e7eb', fontsize=12)
            self.amount_chart.axes.set_xlabel('Monto', color='#e5e7eb')
            self.amount_chart.axes.set_ylabel('Frecuencia', color='#e5e7eb')
        else:
            self.amount_chart.axes.text(0.5, 0.5, 'Sin datos', 
                                       ha='center', va='center',
                                       transform=self.amount_chart.axes.transAxes,
                                       color='#6b7280', fontsize=16)
            
        self.amount_chart.draw()
        
    def get_current_time(self):
        """Get current formatted time"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def update_results(self, results: dict):
        """Update dashboard with conciliation results"""
        self.conciliator_results = results
        
        # Extract case data
        caso1 = results.get('no_pagado', [])
        caso2_especial = results.get('actualizar_recibo_softseguros', [])
        caso2 = results.get('actualizar_sistema', [])
        caso3_allianz = results.get('only_allianz', [])
        caso3_combined = results.get('only_combined', [])
        
        total = len(caso1) + len(caso2_especial) + len(caso2) + len(caso3_allianz) + len(caso3_combined)
        coincidences = len(caso1)
        pending = len(caso2) + len(caso2_especial) + len(caso3_allianz) + len(caso3_combined)
        
        # Update metrics
        self.update_metrics(total, coincidences, pending)
        
        # Update charts
        case_data = {
            'CASO 1': len(caso1),
            'CASO 2 ESP': len(caso2_especial),
            'CASO 2': len(caso2),
            'CASO 3 Allianz': len(caso3_allianz),
            'CASO 3 Soft/Celer': len(caso3_combined)
        }
        self.update_case_chart(case_data)
        
        # Update case details
        self.update_caso1_details(caso1)
        self.update_caso2_especial_details(caso2_especial)
        self.update_caso2_details(caso2)
        self.update_caso3_allianz_details(caso3_allianz)
        self.update_caso3_combined_details(caso3_combined)
        
    def format_currency(self, value):
        """Format value as currency"""
        try:
            return f"${value:,.2f}"
        except:
            return str(value)
    
    def update_caso1_details(self, caso1: list):
        """Update CASO 1 details"""
        self.caso1_text.clear()
        if not caso1:
            self.caso1_text.setPlainText("No hay pólizas en CASO 1")
            return
        
        text = f"CASO 1 - NO HAN PAGADO (Cartera Pendiente)\n"
        text += f"Total: {len(caso1)} pólizas\n"
        text += "=" * 80 + "\n\n"
        
        for i, item in enumerate(caso1, 1):
            text += f"{i}. Póliza: {item.get('poliza', 'N/A')}\n"
            text += f"   Recibo Combined: {item.get('recibo_combined', 'N/A')} | "
            text += f"Recibo Allianz: {item.get('recibo_allianz', 'N/A')}\n"
            text += f"   Fecha: {item.get('fecha', 'N/A')}\n"
            text += f"   Tomador: {item.get('tomador_combined', 'N/A')}\n"
            text += f"   Cliente Allianz: {item.get('cliente_allianz', 'N/A')}\n"
            text += f"   Saldo Combined: {self.format_currency(item.get('saldo_combined', 0))} | "
            text += f"Cartera Allianz: {self.format_currency(item.get('cartera_allianz', 0))}\n"
            if item.get('necesita_actualizar_softseguros'):
                text += f"   ⚠️ ACTUALIZAR RECIBO EN SOFTSEGUROS (actualmente solo en CELER)\n"
            text += "\n"
        
        self.caso1_text.setPlainText(text)
    
    def update_caso2_especial_details(self, caso2_especial: list):
        """Update CASO 2 ESPECIAL details"""
        self.caso2_especial_text.clear()
        if not caso2_especial:
            self.caso2_especial_text.setPlainText("No hay pólizas en CASO 2 ESPECIAL")
            return
        
        text = f"CASO 2 ESPECIAL - ACTUALIZAR RECIBO EN SOFTSEGUROS\n"
        text += f"Total: {len(caso2_especial)} pólizas\n"
        text += "=" * 80 + "\n\n"
        
        for i, item in enumerate(caso2_especial, 1):
            text += f"{i}. Póliza: {item.get('poliza', 'N/A')}\n"
            text += f"   Recibo Allianz: {item.get('recibo_allianz', 'N/A')}\n"
            text += f"   Fecha: {item.get('fecha', 'N/A')}\n"
            text += f"   Tomador Softseguros: {item.get('tomador_softseguros', 'N/A')}\n"
            text += f"   Cliente Allianz: {item.get('cliente_allianz', 'N/A')}\n"
            text += f"   Saldo Softseguros: {self.format_currency(item.get('saldo_softseguros', 0))} | "
            text += f"Cartera Allianz: {self.format_currency(item.get('cartera_allianz', 0))}\n"
            text += "   ⚠️ Softseguros NO tiene anexo/recibo registrado\n"
            text += "\n"
        
        self.caso2_especial_text.setPlainText(text)
    
    def update_caso2_details(self, caso2: list):
        """Update CASO 2 details"""
        self.caso2_text.clear()
        if not caso2:
            self.caso2_text.setPlainText("No hay pólizas en CASO 2")
            return
        
        text = f"CASO 2 - ACTUALIZAR SISTEMA (Recibo diferente)\n"
        text += f"Total: {len(caso2)} pólizas\n"
        text += "=" * 80 + "\n\n"
        
        for i, item in enumerate(caso2, 1):
            text += f"{i}. Póliza: {item.get('poliza', 'N/A')}\n"
            text += f"   Recibo Combined: {item.get('recibo_combined', 'N/A')} | "
            text += f"Recibo Allianz: {item.get('recibo_allianz', 'N/A')}\n"
            text += f"   Fecha: {item.get('fecha', 'N/A')}\n"
            text += f"   Tomador: {item.get('tomador_combined', 'N/A')}\n"
            text += f"   Cliente Allianz: {item.get('cliente_allianz', 'N/A')}\n"
            text += f"   Saldo Combined: {self.format_currency(item.get('saldo_combined', 0))} | "
            text += f"Cartera Allianz: {self.format_currency(item.get('cartera_allianz', 0))}\n"
            text += "\n"
        
        self.caso2_text.setPlainText(text)
    
    def update_caso3_allianz_details(self, caso3: list):
        """Update CASO 3 Allianz details"""
        self.caso3_allianz_text.clear()
        if not caso3:
            self.caso3_allianz_text.setPlainText("No hay pólizas solo en Allianz")
            return
        
        text = f"CASO 3 - SOLO EN ALLIANZ (Corregir póliza)\n"
        text += f"Total: {len(caso3)} pólizas\n"
        text += "=" * 80 + "\n\n"
        
        for i, item in enumerate(caso3, 1):
            text += f"{i}. Póliza: {item.get('poliza', 'N/A')}\n"
            text += f"   Recibo: {item.get('recibo_allianz', 'N/A')}\n"
            text += f"   Fecha: {item.get('fecha', 'N/A')}\n"
            text += f"   Cliente: {item.get('cliente_allianz', 'N/A')}\n"
            text += f"   Cartera: {self.format_currency(item.get('cartera_allianz', 0))}\n"
            text += "\n"
        
        self.caso3_allianz_text.setPlainText(text)
    
    def update_caso3_combined_details(self, caso3: list):
        """Update CASO 3 Combined details"""
        self.caso3_combined_text.clear()
        if not caso3:
            self.caso3_combined_text.setPlainText("No hay pólizas solo en Softseguros/Celer")
            return
        
        text = f"CASO 3 - SOLO EN SOFTSEGUROS/CELER\n"
        text += f"Total: {len(caso3)} pólizas\n"
        text += "=" * 80 + "\n\n"
        
        for i, item in enumerate(caso3, 1):
            text += f"{i}. Póliza: {item.get('poliza', 'N/A')}\n"
            text += f"   Recibo: {item.get('recibo_combined', 'N/A')}\n"
            text += f"   Fecha: {item.get('fecha', 'N/A')}\n"
            text += f"   Tomador: {item.get('tomador_combined', 'N/A')}\n"
            text += f"   Saldo: {self.format_currency(item.get('saldo_combined', 0))}\n"
            text += "\n"
        
        self.caso3_combined_text.setPlainText(text)
