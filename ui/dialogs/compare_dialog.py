"""Compare formulations dialog."""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem, QLabel, QInputDialog, QMessageBox, QHeaderView, QDialogButtonBox
from PySide6.QtGui import QColor
from core.database.history_manager import HistoryManager
from core.utils.constants import TRANSLATIONS
from core.utils.language_manager import LanguageManager


class CompareDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history = HistoryManager.load_history()
        self.setup_ui()
    
    def tr(self, key):
        return TRANSLATIONS[LanguageManager._current_lang].get(key, key)
    
    def setup_ui(self):
        if len(self.history) < 2:
            QMessageBox.warning(self, self.tr("compare"), self.tr("needTwoHistory"))
            self.reject()
            return
        
        items = [r.get_display_name() for r in self.history]
        first, ok1 = QInputDialog.getItem(self, self.tr("compare"), self.tr("selectFirstComparison"), items, 0, False)
        if not ok1:
            self.reject()
            return
        second, ok2 = QInputDialog.getItem(self, self.tr("compare"), self.tr("selectSecondComparison"), items, 0, False)
        if not ok2:
            self.reject()
            return
        if first == second:
            QMessageBox.warning(self, self.tr("compare"), self.tr("sameFormulation"))
            self.reject()
            return
        
        idx1 = items.index(first)
        idx2 = items.index(second)
        rec1, rec2 = self.history[idx1], self.history[idx2]
        
        self.setWindowTitle(self.tr("comparisonTitle"))
        self.setMinimumSize(800, 500)
        layout = QVBoxLayout(self)
        
        # Info headers
        info_layout = QHBoxLayout()
        for rec, color in [(rec1, "#2196F3"), (rec2, "#FF9800")]:
            grp = QGroupBox()
            grp.setStyleSheet(f"QGroupBox{{border:2px solid {color}; border-radius:8px;}}")
            form = QFormLayout()
            form.addRow(self.tr("formulaName") + ":", QLabel(rec.name))
            form.addRow(self.tr("formulationType") + ":", QLabel(rec.coating_type.value))
            form.addRow(self.tr("totalWeight") + ":", QLabel(f"{rec.total_weight():.1f}g"))
            grp.setLayout(form)
            info_layout.addWidget(grp)
        layout.addLayout(info_layout)
        
        # Comparison table
        grp = QGroupBox(self.tr("ingredients"))
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([self.tr("ingredient"), "Form 1 (g)", "Form 2 (g)", "Difference", "Status"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        map1 = {i.ingredient_name: i.weight_grams for i in rec1.items if i.weight_grams > 0}
        map2 = {i.ingredient_name: i.weight_grams for i in rec2.items if i.weight_grams > 0}
        all_ing = sorted(set(map1.keys()) | set(map2.keys()))
        
        table.setRowCount(len(all_ing))
        for r, ing in enumerate(all_ing):
            w1 = map1.get(ing, 0.0)
            w2 = map2.get(ing, 0.0)
            diff = w2 - w1
            
            if w1 == 0 and w2 > 0:
                status, bg = "NEW", QColor(200, 230, 200)
            elif w1 > 0 and w2 == 0:
                status, bg = "REMOVED", QColor(255, 200, 200)
            elif abs(diff) > 0.1:
                status, bg = "MODIFIED", QColor(255, 240, 200)
            else:
                status, bg = "UNCHANGED", QColor(255, 255, 255)
            
            table.setItem(r, 0, QTableWidgetItem(ing))
            item1 = QTableWidgetItem(f"{w1:.1f}")
            item1.setBackground(bg)
            table.setItem(r, 1, item1)
            item2 = QTableWidgetItem(f"{w2:.1f}")
            item2.setBackground(bg)
            table.setItem(r, 2, item2)
            table.setItem(r, 3, QTableWidgetItem(f"{diff:+.1f}"))
            table.setItem(r, 4, QTableWidgetItem(status))
        
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        grp.setLayout(QVBoxLayout())
        grp.layout().addWidget(table)
        layout.addWidget(grp)
        
        # Close button
        btn = QDialogButtonBox(QDialogButtonBox.Close)
        btn.rejected.connect(self.reject)
        layout.addWidget(btn)