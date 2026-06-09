"""Synthesis protocol display widget."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QGridLayout
from PySide6.QtGui import QFont
from core.utils.constants import TRANSLATIONS
from core.utils.language_manager import LanguageManager


class SynthesisProtocolWidget(QWidget):
    def __init__(self, protocol, parent=None):
        super().__init__(parent)
        self.protocol = protocol
        self.setup_ui()
    
    def tr(self, key):
        return TRANSLATIONS[LanguageManager._current_lang].get(key, key)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        header = QLabel("⚙️ " + self.tr("synthesisProtocol"))
        header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        header.setStyleSheet("color: #2196F3; border-bottom: 2px solid #2196F3;")
        layout.addWidget(header)
        
        # Summary card
        summary = QFrame()
        summary.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #667eea,stop:1 #764ba2); border-radius: 10px; padding: 15px;")
        summary_layout = QGridLayout(summary)
        
        # method is now a string, not an object with .value
        method_value = self.protocol.method if hasattr(self.protocol, 'method') else "Solution blending"
        temp_value = self.protocol.temperature_c if hasattr(self.protocol, 'temperature_c') else 25
        time_value = self.protocol.time_hours if hasattr(self.protocol, 'time_hours') else 2.5
        stir_value = self.protocol.stirring_speed_rpm if hasattr(self.protocol, 'stirring_speed_rpm') else 600
        
        info = [
            ("METHOD", method_value),
            ("TEMPERATURE", f"{temp_value}°C"),
            ("TIME", f"{time_value}h"),
            ("STIRRING", f"{stir_value}rpm")
        ]
        
        if hasattr(self.protocol, 'sonication_minutes') and self.protocol.sonication_minutes > 0:
            info.append(("SONICATION", f"{self.protocol.sonication_minutes} min"))
        
        for i, (label, value) in enumerate(info):
            l = QLabel(label)
            l.setStyleSheet("color:#fff;font-size:10px;opacity:0.8")
            v = QLabel(value)
            v.setStyleSheet("color:#fff;font-size:14px;font-weight:bold")
            summary_layout.addWidget(l, 0, i)
            summary_layout.addWidget(v, 1, i)
        
        layout.addWidget(summary)
        
        # Steps
        steps_label = QLabel("📝 " + self.tr("procedureSteps"))
        steps_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(steps_label)
        
        steps_scroll = QScrollArea()
        steps_scroll.setWidgetResizable(True)
        steps_widget = QWidget()
        steps_layout = QVBoxLayout(steps_widget)
        
        step_num = 1
        steps = self.protocol.steps if hasattr(self.protocol, 'steps') else []
        
        for step in steps:
            if step and step.strip():
                if step.upper() == step and len(step) > 5:
                    title_label = QLabel(f"📌 {step}")
                    title_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
                    title_label.setStyleSheet("color: #2196F3; margin-top: 8px;")
                    steps_layout.addWidget(title_label)
                else:
                    frame = QFrame()
                    frame.setStyleSheet("background: #f8f9fa; border-left: 3px solid #2196F3; border-radius: 5px; padding: 8px; margin: 3px;")
                    frame_layout = QHBoxLayout(frame)
                    num_label = QLabel(f"{step_num}.")
                    num_label.setStyleSheet("font-weight: bold; color: #2196F3; min-width: 30px;")
                    text_label = QLabel(step)
                    text_label.setWordWrap(True)
                    frame_layout.addWidget(num_label)
                    frame_layout.addWidget(text_label, 1)
                    steps_layout.addWidget(frame)
                    step_num += 1
        
        steps_scroll.setWidget(steps_widget)
        steps_scroll.setMaximumHeight(350)
        layout.addWidget(steps_scroll)
        
        # Equipment
        equipment = self.protocol.equipment_needed if hasattr(self.protocol, 'equipment_needed') else []
        valid_eq = [eq for eq in equipment if eq]
        if valid_eq:
            equip_label = QLabel("🔧 " + self.tr("equipmentNeeded"))
            equip_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            layout.addWidget(equip_label)
            equip_widget = QWidget()
            equip_layout = QHBoxLayout(equip_widget)
            for eq in valid_eq:
                badge = QLabel(f"• {eq}")
                badge.setStyleSheet("background: #e3f2fd; color: #1565c0; border-radius: 15px; padding: 5px 12px; margin: 2px;")
                equip_layout.addWidget(badge)
            equip_layout.addStretch()
            layout.addWidget(equip_widget)
        
        # Curing
        curing = self.protocol.curing_conditions if hasattr(self.protocol, 'curing_conditions') else None
        if curing:
            curing_label = QLabel(f"🔥 {self.tr('curingStep')}: {curing}")
            curing_label.setStyleSheet("background: #fff3e0; padding: 10px; border-radius: 8px; margin-top: 5px;")
            curing_label.setWordWrap(True)
            layout.addWidget(curing_label)
        
        # Safety notes
        safety_notes = self.protocol.safety_notes if hasattr(self.protocol, 'safety_notes') else []
        if safety_notes:
            safety_label = QLabel("⚠️ " + self.tr("safetyNotes"))
            safety_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            safety_label.setStyleSheet("color: #f44336; margin-top: 5px;")
            layout.addWidget(safety_label)
            for note in safety_notes:
                note_frame = QFrame()
                note_frame.setStyleSheet("background: #ffebee; border-radius: 5px; padding: 5px; margin: 2px;")
                note_layout = QHBoxLayout(note_frame)
                note_layout.addWidget(QLabel("⚠️"))
                note_layout.addWidget(QLabel(note))
                layout.addWidget(note_frame)
        
        layout.addStretch()