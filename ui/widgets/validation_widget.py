"""Validation rules display widget."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QFrame, QScrollArea
from PySide6.QtGui import QFont
from core.utils.constants import TRANSLATIONS
from core.utils.language_manager import LanguageManager


class ValidationRulesWidget(QWidget):
    def __init__(self, rules, parent=None):
        super().__init__(parent)
        self.rules = rules
        self.setup_ui()
    
    def tr(self, key):
        return TRANSLATIONS[LanguageManager._current_lang].get(key, key)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("📋 " + self.tr("validationRules"))
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 5px;")
        layout.addWidget(title)
        
        # Create scroll area for rules
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)
        
        if not self.rules:
            success_label = QLabel("✅ " + self.tr("validationPassed"))
            success_label.setStyleSheet("background: #d4edda; color: #155724; padding: 15px; border-radius: 8px; font-size: 13px;")
            scroll_layout.addWidget(success_label)
        else:
            # Separate rules by severity
            errors = [r for r in self.rules if r.severity == "error"]
            warnings = [r for r in self.rules if r.severity == "warning"]
            infos = [r for r in self.rules if r.severity == "info"]
            
            # Errors (Critical)
            if errors:
                err_group = QGroupBox(f"❌ {len(errors)} " + self.tr("criticalErrors"))
                err_group.setStyleSheet("""
                    QGroupBox { 
                        font-weight: bold; 
                        color: #c62828; 
                        border: 2px solid #c62828; 
                        border-radius: 8px; 
                        margin-top: 10px; 
                    }
                    QGroupBox::title { 
                        subcontrol-origin: margin; 
                        left: 10px; 
                        padding: 0 5px 0 5px; 
                    }
                """)
                err_layout = QVBoxLayout(err_group)
                for rule in errors:
                    frame = QFrame()
                    frame.setStyleSheet("background: #ffebee; border-radius: 5px; margin: 5px; padding: 10px;")
                    frame_layout = QVBoxLayout(frame)
                    
                    msg_label = QLabel(f"🔴 {rule.message}")
                    msg_label.setStyleSheet("font-weight: bold; color: #c62828;")
                    msg_label.setWordWrap(True)
                    
                    rec_label = QLabel(f"💡 {rule.recommendation}")
                    rec_label.setStyleSheet("color: #555; font-size: 11px;")
                    rec_label.setWordWrap(True)
                    
                    std_label = QLabel(f"📖 {rule.standard}")
                    std_label.setStyleSheet("color: #777; font-size: 10px;")
                    std_label.setWordWrap(True)
                    
                    frame_layout.addWidget(msg_label)
                    frame_layout.addWidget(rec_label)
                    frame_layout.addWidget(std_label)
                    err_layout.addWidget(frame)
                scroll_layout.addWidget(err_group)
            
            # Warnings
            if warnings:
                warn_group = QGroupBox(f"⚠️ {len(warnings)} " + self.tr("warnings"))
                warn_group.setStyleSheet("""
                    QGroupBox { 
                        font-weight: bold; 
                        color: #e65100; 
                        border: 2px solid #ff9800; 
                        border-radius: 8px; 
                        margin-top: 10px; 
                    }
                    QGroupBox::title { 
                        subcontrol-origin: margin; 
                        left: 10px; 
                        padding: 0 5px 0 5px; 
                    }
                """)
                warn_layout = QVBoxLayout(warn_group)
                for rule in warnings:
                    frame = QFrame()
                    frame.setStyleSheet("background: #fff3e0; border-radius: 5px; margin: 5px; padding: 10px;")
                    frame_layout = QVBoxLayout(frame)
                    
                    msg_label = QLabel(f"⚠️ {rule.message}")
                    msg_label.setStyleSheet("font-weight: bold; color: #e65100;")
                    msg_label.setWordWrap(True)
                    
                    rec_label = QLabel(f"💡 {rule.recommendation}")
                    rec_label.setStyleSheet("color: #555; font-size: 11px;")
                    rec_label.setWordWrap(True)
                    
                    frame_layout.addWidget(msg_label)
                    frame_layout.addWidget(rec_label)
                    warn_layout.addWidget(frame)
                scroll_layout.addWidget(warn_group)
            
            # Info messages
            if infos:
                info_group = QGroupBox(f"ℹ️ {len(infos)} " + self.tr("information"))
                info_group.setStyleSheet("""
                    QGroupBox { 
                        font-weight: bold; 
                        color: #1565c0; 
                        border: 2px solid #2196F3; 
                        border-radius: 8px; 
                        margin-top: 10px; 
                    }
                    QGroupBox::title { 
                        subcontrol-origin: margin; 
                        left: 10px; 
                        padding: 0 5px 0 5px; 
                    }
                """)
                info_layout = QVBoxLayout(info_group)
                for rule in infos:
                    frame = QFrame()
                    frame.setStyleSheet("background: #e3f2fd; border-radius: 5px; margin: 5px; padding: 10px;")
                    frame_layout = QVBoxLayout(frame)
                    
                    msg_label = QLabel(f"ℹ️ {rule.message}")
                    msg_label.setStyleSheet("color: #1565c0;")
                    msg_label.setWordWrap(True)
                    
                    rec_label = QLabel(f"💡 {rule.recommendation}")
                    rec_label.setStyleSheet("color: #555; font-size: 11px;")
                    rec_label.setWordWrap(True)
                    
                    frame_layout.addWidget(msg_label)
                    frame_layout.addWidget(rec_label)
                    info_layout.addWidget(frame)
                scroll_layout.addWidget(info_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)