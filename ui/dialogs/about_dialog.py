"""About dialog."""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About NanoCoatBuilder")
        self.setMinimumSize(400, 300)
        layout = QVBoxLayout(self)
        
        about_text = QLabel("""
        <div style='text-align:center;'>
            <h2 style='color:#2196F3;'>🔬 NanoCoatBuilder</h2>
            <p>Advanced Coating Formulation Software</p>
            <p><b>Developer:</b> Oukil Khaled Ibn Elwalid</p>
            <hr>
            <p><b>Features:</b><br>
            - 50+ ingredients including nanocomposites<br>
            - 7 application sectors with specific requirements<br>
            - ISO compliance validation<br>
            - Automatic synthesis protocol generation<br>
            - Performance prediction with graphs<br>
            - Export to HTML/JSON<br>
            - History and comparison tools<br>
            - Bilingual interface (English/French)</p>
            <p>© 2026 - For research purposes</p>
        </div>
        """)
        about_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(about_text)