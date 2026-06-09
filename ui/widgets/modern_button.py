"""Modern styled button widget."""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from core.utils.constants import TRANSLATIONS
from core.utils.language_manager import LanguageManager


class ModernButton(QPushButton):
    def __init__(self, text_key, icon="", color="#2196F3", parent=None):
        super().__init__(parent)
        self.text_key = text_key
        self.icon = icon
        self.color = color
        self.update_text()
        self.setFixedHeight(38)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 12px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background-color: {self._adj(color, -20)}; }}
        """)

    def update_text(self):
        text = TRANSLATIONS[LanguageManager._current_lang].get(self.text_key, self.text_key)
        self.setText(f"{self.icon} {text}" if self.icon else text)

    def _adj(self, color, pct):
        c = color.lstrip('#')
        r, g, b = (int(c[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = max(0, min(255, r + pct)), max(0, min(255, g + pct)), max(0, min(255, b + pct))
        return f"#{r:02x}{g:02x}{b:02x}"