"""Ingredient table widget for adding/removing ingredients."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QInputDialog, QMessageBox, QHeaderView
from PySide6.QtCore import Qt
from core.database.ingredient_db import IngredientDB
from core.models import FormulationItem
from core.utils.constants import TRANSLATIONS
from core.utils.language_manager import LanguageManager


class IngredientTable(QWidget):
    def __init__(self, category, parent=None):
        super().__init__(parent)
        self.category = category
        self.items = []
        self.setup_ui()
    
    def tr(self, key):
        return TRANSLATIONS[LanguageManager._current_lang].get(key, key)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([self.tr("ingredient"), self.tr("weight")])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(200)
        layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ " + self.tr("addRow"))
        self.add_btn.setStyleSheet("background: #4CAF50; color: white; border: none; border-radius: 4px; padding: 6px 12px;")
        self.add_btn.clicked.connect(self.add)
        self.remove_btn = QPushButton("➖ " + self.tr("removeRow"))
        self.remove_btn.setStyleSheet("background: #f44336; color: white; border: none; border-radius: 4px; padding: 6px 12px;")
        self.remove_btn.clicked.connect(self.remove)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.update_table()
    
    def add(self):
        ing_list = IngredientDB.get_by_category(self.category)
        if not ing_list:
            QMessageBox.warning(self, "Warning", f"No ingredients in {self.category}")
            return
        names = [i.name for i in ing_list]
        sel, ok = QInputDialog.getItem(self, "Add", self.tr("selectIngredient"), names, 0, False)
        if ok and sel:
            self.items.append(FormulationItem(ingredient_name=sel, weight_grams=0.0))
            self.update_table()
    
    def add_by_name(self, name):
        if not any(i.ingredient_name == name for i in self.items):
            self.items.append(FormulationItem(ingredient_name=name, weight_grams=0.0))
    
    def remove(self):
        row = self.table.currentRow()
        if row >= 0:
            self.items.pop(row)
            self.update_table()
    
    def update_table(self):
        self.table.blockSignals(True)
        self.table.setRowCount(len(self.items))
        for r, it in enumerate(self.items):
            self.table.setItem(r, 0, QTableWidgetItem(it.ingredient_name))
            self.table.setItem(r, 1, QTableWidgetItem(str(it.weight_grams) if it.weight_grams > 0 else "0"))
        self.table.blockSignals(False)
        self.table.cellChanged.connect(self.on_change)
    
    def on_change(self, row, col):
        if row >= len(self.items) or col != 1:
            return
        try:
            weight = float(self.table.item(row, col).text() or "0")
            # Create a new FormulationItem instead of modifying
            self.items[row] = FormulationItem(
                ingredient_name=self.items[row].ingredient_name,
                weight_grams=weight,
                notes=self.items[row].notes if hasattr(self.items[row], 'notes') else ""
            )
        except ValueError:
            pass
    
    def get_items(self):
        return self.items
    
    def clear(self):
        self.items.clear()
        self.update_table()