"""Results display widget with tabs."""

import matplotlib
matplotlib.use('Qt5Agg')

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QGridLayout, QGroupBox, QFrame, QScrollArea
from PySide6.QtGui import QFont
from core.utils.constants import TRANSLATIONS, APPLICATION_TYPES
from core.utils.language_manager import LanguageManager
from ui.widgets.validation_widget import ValidationRulesWidget
from ui.widgets.graph_widget import PerformanceGraphWidget
from ui.widgets.protocol_widget import SynthesisProtocolWidget


class ResultsDisplay(QWidget):
    def __init__(self, result, parent=None):
        super().__init__(parent)
        self.result = result
        self.setup_ui()
    
    def tr(self, key):
        return TRANSLATIONS[LanguageManager._current_lang].get(key, key)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #ddd; border-radius: 8px; background: white; }
            QTabBar::tab { padding: 10px 20px; margin: 2px; border-radius: 6px; font-weight: 500; }
            QTabBar::tab:selected { background: #2196F3; color: white; }
        """)
        
        # Performance Tab
        perf_tab = QWidget()
        perf_layout = QVBoxLayout(perf_tab)
        
        p = self.result.performance
        f = self.result.formulation
        
        # Formulation info
        info_grid = QGridLayout()
        info_grid.addWidget(QLabel(f"<b>{self.tr('formulaName')}:</b> {f.name}"), 0, 0)
        # coating_type is now a string, not an enum
        coating_type_value = f.coating_type if hasattr(f, 'coating_type') else "Anti-corrosion"
        info_grid.addWidget(QLabel(f"<b>{self.tr('formulationType')}:</b> {coating_type_value}"), 0, 1)
        info_grid.addWidget(QLabel(f"<b>{self.tr('environment')}:</b> {f.target_environment}"), 1, 0)
        info_grid.addWidget(QLabel(f"<b>{self.tr('application')}:</b> {self.result.application_sector}"), 1, 1)
        info_grid.addWidget(QLabel(f"<b>{self.tr('totalWeight')}:</b> {self.result.total_weight_g:.1f}g"), 2, 0)
        info_grid.addWidget(QLabel(f"<b>Cost:</b> €{self.result.total_cost:.2f}"), 2, 1)
        perf_layout.addLayout(info_grid)
        
        # Performance metrics
        metrics_group = QGroupBox(self.tr("performance"))
        metrics_layout = QGridLayout(metrics_group)
        metrics = [
            (self.tr("corrosionRate") + ":", f"{p.corrosion_rate_mm_year:.4f} mm/year" if p.corrosion_rate_mm_year else "N/A"),
            (self.tr("adhesion") + ":", f"{p.adhesion_MPa:.1f} MPa" if p.adhesion_MPa else "N/A"),
            (self.tr("saltSpray") + ":", f"{p.salt_spray_hours} hours" if p.salt_spray_hours else "N/A"),
            (self.tr("volumeSolids") + ":", f"{p.theoretical_volume_solids:.1f}%"),
            (self.tr("voc") + ":", f"{p.theoretical_voc:.0f} g/L"),
            (self.tr("costPerLitre") + ":", f"€{p.cost_per_liter:.2f}"),
            (self.tr("serviceLife") + ":", f"{p.estimated_life_years:.1f} years" if p.estimated_life_years else "N/A"),
            (self.tr("hardness") + ":", p.hardness_pencil or "N/A"),
        ]
        for i, (label, value) in enumerate(metrics):
            metrics_layout.addWidget(QLabel(label), i, 0)
            metrics_layout.addWidget(QLabel(value), i, 1)
        perf_layout.addWidget(metrics_group)
        
        # Application check
        app = self.result.application_sector
        if app in APPLICATION_TYPES:
            req = APPLICATION_TYPES[app]
            salt_ok = (p.salt_spray_hours or 0) >= req["min_salt_spray"]
            adh_ok = (p.adhesion_MPa or 0) >= req["min_adhesion"]
            vol_ok = p.theoretical_volume_solids >= req["min_volume_solids"]
            voc_ok = p.theoretical_voc <= req["max_voc"]
            all_ok = salt_ok and adh_ok and vol_ok and voc_ok
            status = f"✅ {self.tr('meetsRequirements')}" if all_ok else f"❌ {self.tr('failsRequirements')}"
            
            app_frame = QFrame()
            app_frame.setStyleSheet(f"background: {req['color']}15; border-radius: 8px; padding: 10px; margin-top: 10px; border: 1px solid {req['color']};")
            app_layout = QVBoxLayout(app_frame)
            app_layout.addWidget(QLabel(f"{req['icon']} <b>{self.tr('application')}: {app}</b> - <font color='{'#4CAF50' if all_ok else '#f44336'}'>{status}</font>"))
            app_layout.addWidget(QLabel(f"📋 {self.tr('requirements')}: Salt ≥{req['min_salt_spray']}h, Adhesion ≥{req['min_adhesion']}MPa, Solids ≥{req['min_volume_solids']}%, VOC ≤{req['max_voc']}g/L"))
            perf_layout.addWidget(app_frame)
        
        # ISO Compliance
        iso_group = QGroupBox("✅ " + self.tr("isoCompliance"))
        iso_layout = QVBoxLayout(iso_group)
        for c in self.result.iso_compliance:
            iso_layout.addWidget(QLabel(f"✔ {c}"))
        if self.result.iso_violations:
            for v in self.result.iso_violations:
                iso_layout.addWidget(QLabel(f"⚠ {v['standard']}: {v['reason']}"))
        perf_layout.addWidget(iso_group)
        
        perf_layout.addStretch()
        tabs.addTab(perf_tab, "📈 " + self.tr("performance"))
        
        # Validation Tab
        if self.result.validation_rules:
            val_tab = ValidationRulesWidget(self.result.validation_rules)
            tabs.addTab(val_tab, "📋 " + self.tr("validationRules"))
        
        # Graphs Tab
        graph_tab = PerformanceGraphWidget(self.result)
        tabs.addTab(graph_tab, "📊 " + self.tr("graphs"))
        
        # Protocol Tab
        if hasattr(self.result, 'synthesis_protocol') and self.result.synthesis_protocol:
            proto_tab = SynthesisProtocolWidget(self.result.synthesis_protocol)
            tabs.addTab(proto_tab, "⚙️ " + self.tr("synthesisProtocol"))
        
        # Characterization Tab
        char_tab = QWidget()
        char_layout = QVBoxLayout(char_tab)
        char_title = QLabel("🔬 " + self.tr("characterization"))
        char_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        char_layout.addWidget(char_title)
        
        char_data = {
            "Morphology": ["SEM", "TEM", "AFM", "Optical Microscopy"],
            "Chemical": ["FTIR", "XPS", "Raman", "EDX", "XRD"],
            "Thermal": ["TGA", "DSC", "DMA", "TMA"],
            "Mechanical": ["Tensile Testing", "Nanoindentation", "Scratch Test", "Pull-off Adhesion"],
            "Corrosion": ["Salt Spray", "EIS", "Potentiodynamic Polarization", "Immersion Test"],
            "Surface": ["Contact Angle", "Surface Roughness", "Gloss Measurement"]
        }
        for cat, techs in char_data.items():
            char_layout.addWidget(QLabel(f"<b>{cat.upper()}</b>"))
            char_layout.addWidget(QLabel(f"  {' | '.join(techs)}"))
            char_layout.addWidget(QLabel(""))
        char_layout.addStretch()
        tabs.addTab(char_tab, "🔬 " + self.tr("characterization"))
        
        layout.addWidget(tabs)