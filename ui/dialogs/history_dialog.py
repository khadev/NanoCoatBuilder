"""History dialog for loading/saving formulations."""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QDialogButtonBox, QMessageBox
from core.database.history_manager import HistoryManager
from core.utils.constants import TRANSLATIONS
from core.utils.language_manager import LanguageManager


class HistoryDialog(QDialog):
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.history = HistoryManager.load_history()
        self.setup_ui()
    
    def tr(self, key):
        return TRANSLATIONS[LanguageManager._current_lang].get(key, key)
    
    def setup_ui(self):
        self.setWindowTitle(self.tr("history"))
        self.setMinimumSize(500, 400)
        layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        for rec in self.history:
            self.list_widget.addItem(rec.get_display_name())
        layout.addWidget(self.list_widget)
        
        btn_box = QDialogButtonBox()
        load_btn = btn_box.addButton(self.tr("loadFromHistory"), QDialogButtonBox.ActionRole)
        del_btn = btn_box.addButton(self.tr("deleteFromHistory"), QDialogButtonBox.ActionRole)
        close_btn = btn_box.addButton(QDialogButtonBox.Close)
        
        load_btn.clicked.connect(self.load)
        del_btn.clicked.connect(self.delete)
        close_btn.clicked.connect(self.reject)
        layout.addWidget(btn_box)
    
    def load(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            selected_rec = self.history[row]
            # Call the editor's load method
            self.editor.load_from_history(selected_rec)
            self.accept()
        else:
            QMessageBox.warning(self, self.tr("history"), self.tr("selectFirst"))
    
    def delete(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            confirm = QMessageBox.question(self, "Delete", f"Delete '{self.history[row].name}'?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.history.pop(row)
                HistoryManager.save_history(self.history)
                self.list_widget.takeItem(row)
                QMessageBox.information(self, self.tr("history"), self.tr("historyDeleted"))
        else:
            QMessageBox.warning(self, self.tr("history"), self.tr("selectFirst"))