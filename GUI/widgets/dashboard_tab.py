"""
Dashboard Tab - Metrics and visualizations
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QPushButton, QGroupBox)
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
        
        # Status info
        self.status_label = QLabel("No hay datos para mostrar. Ejecuta una conciliación primero.")
        self.status_label.setProperty("secondary", True)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
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
