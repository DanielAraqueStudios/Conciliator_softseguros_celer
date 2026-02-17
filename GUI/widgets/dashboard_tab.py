"""
Dashboard Tab - Metrics and visualizations
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QPushButton, QGroupBox, QTextEdit,
                             QTabWidget, QScrollArea, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import pandas as pd
from datetime import datetime
from pathlib import Path


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
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        # Create content widget
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title = QLabel("DASHBOARD DE MÉTRICAS")
        title.setProperty("heading", True)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.export_button = QPushButton("📊 Exportar a Excel")
        self.export_button.clicked.connect(self.export_to_excel)
        self.export_button.setEnabled(False)  # Disabled until data is loaded
        buttons_layout.addWidget(self.export_button)
        
        self.refresh_button = QPushButton("🔄 Actualizar Datos")
        self.refresh_button.clicked.connect(self.refresh_metrics)
        buttons_layout.addWidget(self.refresh_button)
        
        layout.addLayout(buttons_layout)
        
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
        self.case_chart.setMinimumHeight(300)
        charts_layout.addWidget(self.case_chart)
        
        # Amount distribution chart
        self.amount_chart = ChartWidget(self, width=5, height=4, dpi=100)
        self.amount_chart.setMinimumHeight(300)
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
        
        layout.addStretch()
        content_widget.setLayout(layout)
        
        # Set content widget to scroll area
        scroll.setWidget(content_widget)
        
        # Set scroll area as main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
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
        
        # Enable export button when data is loaded
        self.export_button.setEnabled(True)
        
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
    
    def export_to_excel(self):
        """Export all cases to Excel file with 5 sheets using A-W column mapping"""
        if not self.conciliator_results:
            QMessageBox.warning(self, "Sin Datos", "No hay datos para exportar. Ejecuta una conciliación primero.")
            return
        
        # Ask user for file location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Reporte de Conciliación",
            str(Path.home() / f"Conciliacion_Allianz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"),
            "Excel Files (*.xlsx)"
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            # Extract case data
            caso1 = self.conciliator_results.get('no_pagado', [])
            caso2_especial = self.conciliator_results.get('actualizar_recibo_softseguros', [])
            caso2 = self.conciliator_results.get('actualizar_sistema', [])
            caso3_allianz = self.conciliator_results.get('only_allianz', [])
            caso3_combined = self.conciliator_results.get('only_combined', [])
            
            # Create Excel writer
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Sheet 1: CASO 1 - No han pagado
                if caso1:
                    df1 = self._prepare_caso1_dataframe(caso1)
                    df1.to_excel(writer, sheet_name='CASO 1 - No Pagado', index=False)
                
                # Sheet 2: CASO 2 ESPECIAL - Actualizar Softseguros
                if caso2_especial:
                    df2_esp = self._prepare_caso2_especial_dataframe(caso2_especial)
                    df2_esp.to_excel(writer, sheet_name='CASO 2 ESP - Act Softseguros', index=False)
                
                # Sheet 3: CASO 2 - Actualizar Sistema
                if caso2:
                    df2 = self._prepare_caso2_dataframe(caso2)
                    df2.to_excel(writer, sheet_name='CASO 2 - Act Sistema', index=False)
                
                # Sheet 4: CASO 3 - Solo Allianz
                if caso3_allianz:
                    df3_allianz = self._prepare_caso3_allianz_dataframe(caso3_allianz)
                    df3_allianz.to_excel(writer, sheet_name='CASO 3 - Solo Allianz', index=False)
                
                # Sheet 5: CASO 3 - Solo Softseguros/Celer
                if caso3_combined:
                    df3_combined = self._prepare_caso3_combined_dataframe(caso3_combined)
                    df3_combined.to_excel(writer, sheet_name='CASO 3 - Solo Soft-Celer', index=False)
            
            QMessageBox.information(
                self,
                "Exportación Exitosa",
                f"Reporte exportado correctamente a:\n{file_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error de Exportación",
                f"Error al exportar el archivo:\n{str(e)}"
            )
    
    def _prepare_caso1_dataframe(self, caso1: list) -> pd.DataFrame:
        """Prepare CASO 1 data in B-W format from COLUMN_MAPPING.md"""
        data = []
        for item in caso1:
            row = {
                'Dias': '',
                'Tomador': item.get('tomador_combined', ''),
                'Tipo_Doc': '',
                'Identificacion': '',
                'Poliza': item.get('poliza', ''),
                'Documento': item.get('recibo_combined', ''),
                'Cuota': '',
                'Placa': '',
                'Saldo': item.get('saldo_combined', 0),
                'Aseguradora': 'ALLIANZ',
                'Ramo': '',
                'Carta_Cobro': '',
                'F_Inicio': item.get('fecha', ''),
                'F_Expedicion': '',
                'F_Creacion': '',
                'Ejecutivo': '',
                'Unidad': '',
                'Descripcion_Riesgo': '',
                'Celular_Pers': '',
                'Celular_Lab': '',
                'Mail_Lab': '',
                'Mail_Pers': '',
                # Additional conciliation fields
                'Cliente Allianz': item.get('cliente_allianz', ''),
                'Recibo Allianz': item.get('recibo_allianz', ''),
                'Cartera Allianz': item.get('cartera_allianz', 0),
                'Actualizar Softseguros': 'SÍ' if item.get('necesita_actualizar_softseguros') else 'NO'
            }
            data.append(row)
        return pd.DataFrame(data)
    
    def _prepare_caso2_especial_dataframe(self, caso2_especial: list) -> pd.DataFrame:
        """Prepare CASO 2 ESPECIAL data in B-W format from COLUMN_MAPPING.md"""
        data = []
        for item in caso2_especial:
            row = {
                'Dias': '',
                'Tomador': item.get('tomador_softseguros', ''),
                'Tipo_Doc': '',
                'Identificacion': '',
                'Poliza': item.get('poliza', ''),
                'Documento': item.get('recibo_allianz', ''),
                'Cuota': '',
                'Placa': '',
                'Saldo': item.get('saldo_softseguros', 0),
                'Aseguradora': 'ALLIANZ',
                'Ramo': '',
                'Carta_Cobro': '',
                'F_Inicio': item.get('fecha', ''),
                'F_Expedicion': '',
                'F_Creacion': '',
                'Ejecutivo': '',
                'Unidad': '',
                'Descripcion_Riesgo': '',
                'Celular_Pers': '',
                'Celular_Lab': '',
                'Mail_Lab': '',
                'Mail_Pers': '',
                # Additional conciliation fields
                'Cliente Allianz': item.get('cliente_allianz', ''),
                'Cartera Allianz': item.get('cartera_allianz', 0),
                'Alerta': 'Softseguros NO tiene anexo/recibo registrado'
            }
            data.append(row)
        return pd.DataFrame(data)
    
    def _prepare_caso2_dataframe(self, caso2: list) -> pd.DataFrame:
        """Prepare CASO 2 data in B-W format from COLUMN_MAPPING.md"""
        data = []
        for item in caso2:
            row = {
                'Dias': '',
                'Tomador': item.get('tomador_combined', ''),
                'Tipo_Doc': '',
                'Identificacion': '',
                'Poliza': item.get('poliza', ''),
                'Documento': item.get('recibo_combined', ''),
                'Cuota': '',
                'Placa': '',
                'Saldo': item.get('saldo_combined', 0),
                'Aseguradora': 'ALLIANZ',
                'Ramo': '',
                'Carta_Cobro': '',
                'F_Inicio': item.get('fecha', ''),
                'F_Expedicion': '',
                'F_Creacion': '',
                'Ejecutivo': '',
                'Unidad': '',
                'Descripcion_Riesgo': '',
                'Celular_Pers': '',
                'Celular_Lab': '',
                'Mail_Lab': '',
                'Mail_Pers': '',
                # Additional conciliation fields
                'Recibo Allianz': item.get('recibo_allianz', ''),
                'Cliente Allianz': item.get('cliente_allianz', ''),
                'Cartera Allianz': item.get('cartera_allianz', 0)
            }
            data.append(row)
        return pd.DataFrame(data)
    
    def _prepare_caso3_allianz_dataframe(self, caso3: list) -> pd.DataFrame:
        """Prepare CASO 3 Allianz data in B-W format from COLUMN_MAPPING.md"""
        data = []
        for item in caso3:
            row = {
                'Dias': '',
                'Tomador': item.get('cliente_allianz', ''),
                'Tipo_Doc': '',
                'Identificacion': '',
                'Poliza': item.get('poliza', ''),
                'Documento': item.get('recibo_allianz', ''),
                'Cuota': '',
                'Placa': '',
                'Saldo': item.get('cartera_allianz', 0),
                'Aseguradora': 'ALLIANZ',
                'Ramo': '',
                'Carta_Cobro': '',
                'F_Inicio': item.get('fecha', ''),
                'F_Expedicion': '',
                'F_Creacion': '',
                'Ejecutivo': '',
                'Unidad': '',
                'Descripcion_Riesgo': '',
                'Celular_Pers': '',
                'Celular_Lab': '',
                'Mail_Lab': '',
                'Mail_Pers': ''
            }
            data.append(row)
        return pd.DataFrame(data)
    
    def _prepare_caso3_combined_dataframe(self, caso3: list) -> pd.DataFrame:
        """Prepare CASO 3 Combined data in B-W format from COLUMN_MAPPING.md"""
        data = []
        for item in caso3:
            row = {
                'Dias': '',
                'Tomador': item.get('tomador_combined', ''),
                'Tipo_Doc': '',
                'Identificacion': '',
                'Poliza': item.get('poliza', ''),
                'Documento': item.get('recibo_combined', ''),
                'Cuota': '',
                'Placa': '',
                'Saldo': item.get('saldo_combined', 0),
                'Aseguradora': 'ALLIANZ',
                'Ramo': '',
                'Carta_Cobro': '',
                'F_Inicio': item.get('fecha', ''),
                'F_Expedicion': '',
                'F_Creacion': '',
                'Ejecutivo': '',
                'Unidad': '',
                'Descripcion_Riesgo': '',
                'Celular_Pers': '',
                'Celular_Lab': '',
                'Mail_Lab': '',
                'Mail_Pers': ''
            }
            data.append(row)
        return pd.DataFrame(data)
