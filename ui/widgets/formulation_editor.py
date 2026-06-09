"""Formulation editor widget."""

import re
import json
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QTabWidget, QLabel, QLineEdit, QComboBox, QFrame, QProgressBar, QMessageBox,
    QFileDialog, QInputDialog)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QDesktopServices

from core.database.ingredient_db import IngredientDB
from core.models.ingredient import CoatingType
from core.database.history_manager import HistoryManager, FormulationRecord
from core.analysis.coating_analyzer import CoatingAnalyzer
from core.utils.language_manager import LanguageManager
from core.utils.constants import APPLICATION_TYPES, TRANSLATIONS
from core.models import FormulationItem

from ui.widgets.ingredient_table import IngredientTable
from ui.widgets.modern_button import ModernButton


class FormulationEditor(QWidget):
    analysis_completed = Signal(object, int)
    
    def __init__(self, idx, parent=None):
        super().__init__(parent)
        self.idx = idx
        self.current_result = None
        self.setup_ui()
    
    def tr(self, key):
        return TRANSLATIONS[LanguageManager._current_lang].get(key, key)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header = QFrame()
        header.setStyleSheet("background: #f0f7ff; border-radius: 10px; padding: 10px;")
        hlayout = QGridLayout(header)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText(self.tr("formulaName"))
        self.name_edit.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        
        self.operator_edit = QLineEdit()
        self.operator_edit.setPlaceholderText("Operator")
        self.operator_edit.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        
        self.type_combo = QComboBox()
        self.type_combo.addItems([t.value for t in CoatingType])
        self.type_combo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 5px;")
        
        self.env_combo = QComboBox()
        self.env_combo.addItems(["C1 (very low)", "C2 (low)", "C3 (medium)", "C4 (high)", "C5 (very high)", "CX (extreme)"])
        self.env_combo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 5px;")
        
        self.app_combo = QComboBox()
        self.app_combo.addItems(list(APPLICATION_TYPES.keys()))
        self.app_combo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 5px;")
        
        hlayout.addWidget(QLabel(self.tr("formulaName") + ":"), 0, 0)
        hlayout.addWidget(self.name_edit, 0, 1)
        hlayout.addWidget(QLabel("Operator:"), 0, 2)
        hlayout.addWidget(self.operator_edit, 0, 3)
        hlayout.addWidget(QLabel(self.tr("formulationType") + ":"), 1, 0)
        hlayout.addWidget(self.type_combo, 1, 1)
        hlayout.addWidget(QLabel(self.tr("environment") + ":"), 1, 2)
        hlayout.addWidget(self.env_combo, 1, 3)
        hlayout.addWidget(QLabel(self.tr("application") + ":"), 2, 0)
        hlayout.addWidget(self.app_combo, 2, 1, 1, 3)
        layout.addWidget(header)
        
        # Weight Bar
        weight_frame = QFrame()
        weight_frame.setStyleSheet("background: #e8e8e8; border-radius: 8px; padding: 8px;")
        weight_layout = QHBoxLayout(weight_frame)
        self.weight_label = QLabel("0.0 / 100 g")
        self.weight_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.weight_progress = QProgressBar()
        self.weight_progress.setRange(0, 120)
        self.weight_progress.setValue(0)
        self.weight_progress.setFormat("%v g")
        weight_layout.addWidget(QLabel("⚖️ " + self.tr("totalWeight") + ":"))
        weight_layout.addWidget(self.weight_label)
        weight_layout.addWidget(self.weight_progress)
        layout.addWidget(weight_frame)
        
        # Ingredient Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #ddd; border-radius: 8px; background: white; }
            QTabBar::tab { padding: 8px 16px; margin: 2px; border-radius: 6px; }
            QTabBar::tab:selected { background: #2196F3; color: white; }
        """)
        
        self.resin_tab = IngredientTable("resin")
        self.solvent_tab = IngredientTable("solvent")
        self.pigment_tab = IngredientTable("pigment")
        self.additive_tab = IngredientTable("additive")
        self.nano_tab = IngredientTable("nanocomposite")
        self.filler_tab = IngredientTable("filler")
        
        self.tabs.addTab(self.resin_tab, "🧪 " + self.tr("resins"))
        self.tabs.addTab(self.nano_tab, "🔬 " + self.tr("nanocomposites"))
        self.tabs.addTab(self.pigment_tab, "🎨 " + self.tr("pigments"))
        self.tabs.addTab(self.solvent_tab, "💧 " + self.tr("solvents"))
        self.tabs.addTab(self.additive_tab, "⚙️ " + self.tr("additives"))
        self.tabs.addTab(self.filler_tab, "📦 " + self.tr("fillers"))
        layout.addWidget(self.tabs)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        self.validate_btn = ModernButton("validate", "✅", "#4CAF50")
        self.analyze_btn = ModernButton("analyze", "🔬", "#2196F3")
        self.save_btn = ModernButton("save", "💾", "#FF9800")
        self.json_btn = ModernButton("saveJson", "📋", "#607D8B")
        self.reset_btn = ModernButton("reset", "🔄", "#f44336")
        self.import_btn = ModernButton("importForm", "📁", "#009688")
        
        btn_layout.addWidget(self.validate_btn)
        btn_layout.addWidget(self.analyze_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.json_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.import_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Connections
        self.validate_btn.clicked.connect(self.validate_formulation)
        self.analyze_btn.clicked.connect(self.analyze)
        self.save_btn.clicked.connect(self.save_recipe)
        self.json_btn.clicked.connect(self.export_json)
        self.reset_btn.clicked.connect(self.reset)
        self.import_btn.clicked.connect(self.import_formulation)
        
        for tab in [self.resin_tab, self.solvent_tab, self.pigment_tab, self.additive_tab, self.nano_tab, self.filler_tab]:
            tab.table.cellChanged.connect(self.update_weight)
        
        self.update_weight()
    
    def refresh_ui(self):
        """Refresh all UI text after language change"""
        self.tabs.setTabText(0, "🧪 " + self.tr("resins"))
        self.tabs.setTabText(1, "🔬 " + self.tr("nanocomposites"))
        self.tabs.setTabText(2, "🎨 " + self.tr("pigments"))
        self.tabs.setTabText(3, "💧 " + self.tr("solvents"))
        self.tabs.setTabText(4, "⚙️ " + self.tr("additives"))
        self.tabs.setTabText(5, "📦 " + self.tr("fillers"))
        
        self.validate_btn.update_text()
        self.analyze_btn.update_text()
        self.save_btn.update_text()
        self.json_btn.update_text()
        self.reset_btn.update_text()
        self.import_btn.update_text()
        
        for tab in [self.resin_tab, self.solvent_tab, self.pigment_tab, 
                    self.additive_tab, self.nano_tab, self.filler_tab]:
            tab.table.setHorizontalHeaderLabels([self.tr("ingredient"), self.tr("weight")])
    
    def update_weight(self):
        total = self.get_formulation().total_weight()
        self.weight_label.setText(f"{total:.1f} / 100 g")
        self.weight_progress.setValue(int(total))
        if abs(total - 100) <= 5:
            self.weight_progress.setStyleSheet("QProgressBar::chunk { background-color: #4CAF50; border-radius: 8px; }")
        elif total < 100:
            self.weight_progress.setStyleSheet("QProgressBar::chunk { background-color: #FF9800; border-radius: 8px; }")
        else:
            self.weight_progress.setStyleSheet("QProgressBar::chunk { background-color: #f44336; border-radius: 8px; }")
    
    def get_formulation(self):
        """Get formulation as dictionary for FormulationRecord"""
        items = []
        for tab in [self.resin_tab, self.solvent_tab, self.pigment_tab, self.additive_tab, self.nano_tab, self.filler_tab]:
            for item in tab.get_items():
                items.append({
                    "ingredient_name": item.ingredient_name,
                    "weight_grams": item.weight_grams,
                    "notes": item.notes if hasattr(item, 'notes') else ""
                })
        from core.database.history_manager import FormulationRecord
        return FormulationRecord(
            name=self.name_edit.text() if self.name_edit.text() else "New Formulation",
            operator=self.operator_edit.text(),
            date=datetime.now().strftime("%Y-%m-%d"),
            coating_type=self.type_combo.currentText(),
            target_environment=self.env_combo.currentText(),
            items=items,
            timestamp=datetime.now().timestamp()
        )
    
    def validate_formulation(self):
        rec = self.get_formulation()
        if not rec.items:
            QMessageBox.warning(self, "Warning", self.tr("errorNoIngredients"))
            return
        self.save_to_history()
    
    def analyze(self):
        try:
            rec = self.get_formulation()
            if not rec.items:
                QMessageBox.warning(self, "Error", self.tr("errorNoIngredients"))
                return
            
            app_sector = self.app_combo.currentText()
            result = CoatingAnalyzer.analyze(rec, app_sector)
            self.current_result = result
            self.analysis_completed.emit(result, self.idx)
            
            errors = [r for r in result.validation_rules if r.severity == "error"]
            if errors:
                msg = f"❌ {len(errors)} Issues found:\n"
                for e in errors[:5]:
                    msg += f"  • {e.message}\n"
                QMessageBox.warning(self, "Validation Issues", msg)
            else:
                QMessageBox.information(self, "Success", "✅ Formulation validated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def save_to_history(self):
        rec = self.get_formulation()
        if not rec.items:
            QMessageBox.warning(self, "Warning", self.tr("errorNoIngredients"))
            return
        
        if not rec.name or rec.name == "New Formulation":
            name, ok = QInputDialog.getText(self, "Save", self.tr("formulaName") + ":")
            if ok and name:
                rec.name = name
                self.name_edit.setText(name)
            else:
                return
        
        history = HistoryManager.load_history()
        for i, existing in enumerate(history):
            if existing.name == rec.name:
                reply = QMessageBox.question(self, "Duplicate", f"'{rec.name}' exists. Overwrite?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    history.pop(i)
                    break
                else:
                    return
        
        history.insert(0, rec)
        HistoryManager.save_history(history)
        QMessageBox.information(self, "History", self.tr("historySaved"))
    
    def load_from_history(self, rec):
        """Load formulation from history record"""
        self.name_edit.setText(rec.name)
        self.operator_edit.setText(rec.operator)
        
        # Set coating type
        index = self.type_combo.findText(rec.coating_type)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)
        
        # Set environment
        index = self.env_combo.findText(rec.target_environment)
        if index >= 0:
            self.env_combo.setCurrentIndex(index)
        
        # Clear all tabs
        for tab in [self.resin_tab, self.solvent_tab, self.pigment_tab, 
                    self.additive_tab, self.nano_tab, self.filler_tab]:
            tab.clear()
        
        # Load ingredients - items are dictionaries
        for item in rec.items:
            name = item.get('ingredient_name', '')
            weight = item.get('weight_grams', 0)
            ing = IngredientDB.get(name)
            if ing:
                if ing.category == "resin":
                    self.resin_tab.add_by_name(name)
                    if self.resin_tab.items:
                        self.resin_tab.items[-1].weight_grams = weight
                elif ing.category == "solvent":
                    self.solvent_tab.add_by_name(name)
                    if self.solvent_tab.items:
                        self.solvent_tab.items[-1].weight_grams = weight
                elif ing.category == "pigment":
                    self.pigment_tab.add_by_name(name)
                    if self.pigment_tab.items:
                        self.pigment_tab.items[-1].weight_grams = weight
                elif ing.category == "additive":
                    self.additive_tab.add_by_name(name)
                    if self.additive_tab.items:
                        self.additive_tab.items[-1].weight_grams = weight
                elif ing.category == "nanocomposite":
                    self.nano_tab.add_by_name(name)
                    if self.nano_tab.items:
                        self.nano_tab.items[-1].weight_grams = weight
                elif ing.category == "filler":
                    self.filler_tab.add_by_name(name)
                    if self.filler_tab.items:
                        self.filler_tab.items[-1].weight_grams = weight
        
        # Update all tables
        for tab in [self.resin_tab, self.solvent_tab, self.pigment_tab, 
                    self.additive_tab, self.nano_tab, self.filler_tab]:
            tab.update_table()
        
        self.update_weight()
        QMessageBox.information(self, "Success", self.tr("historyLoaded"))
    
    def save_recipe(self):
        rec = self.get_formulation()
        fname, _ = QFileDialog.getSaveFileName(self, self.tr("save"), rec.name + ".txt", "Text files (*.txt)")
        if fname:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(f"Formulation: {rec.name}\n")
                f.write(f"Operator: {rec.operator}\n")
                f.write(f"Date: {rec.date}\n")
                f.write(f"Type: {rec.coating_type}\n")
                f.write(f"Environment: {rec.target_environment}\n")
                f.write(f"Application: {self.app_combo.currentText()}\n\n")
                f.write("INGREDIENTS:\n")
                for item in rec.items:
                    f.write(f"  {item.get('ingredient_name')}: {item.get('weight_grams')}g\n")
                f.write(f"\nTotal: {rec.total_weight():.1f}g\n")
            QMessageBox.information(self, "Saved", self.tr("recipeSaved"))
    
    def export_json(self):
        rec = self.get_formulation()
        fname, _ = QFileDialog.getSaveFileName(self, self.tr("saveJson"), rec.name + ".json", "JSON files (*.json)")
        if fname:
            data = {
                "formulation": rec.dict(),
                "metadata": {
                    "export_date": datetime.now().isoformat(),
                    "application_sector": self.app_combo.currentText()
                }
            }
            if self.current_result:
                data["analysis"] = self.current_result.__dict__
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            QMessageBox.information(self, "Exported", self.tr("jsonExported"))
    
    def reset(self):
        for tab in [self.resin_tab, self.solvent_tab, self.pigment_tab, self.additive_tab, self.nano_tab, self.filler_tab]:
            tab.clear()
        self.name_edit.setText("")
        self.operator_edit.clear()
        self.current_result = None
        self.analysis_completed.emit(None, self.idx)
        self.update_weight()
    
    def import_formulation(self):
        fname, _ = QFileDialog.getOpenFileName(self, self.tr("importForm"), "", "Text files (*.txt);;JSON (*.json)")
        if not fname:
            return
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Clear all tabs
            for tab in [self.resin_tab, self.solvent_tab, self.pigment_tab, self.additive_tab, self.nano_tab, self.filler_tab]:
                tab.clear()
            
            if fname.endswith('.json'):
                data = json.loads(content)
                if 'formulation' in data:
                    for item in data['formulation'].get('items', []):
                        name = item.get('ingredient_name', '')
                        weight = item.get('weight_grams', 0)
                        ing = IngredientDB.get(name)
                        if ing:
                            if ing.category == "resin":
                                self.resin_tab.add_by_name(name)
                                if self.resin_tab.items:
                                    self.resin_tab.items[-1].weight_grams = weight
                            elif ing.category == "solvent":
                                self.solvent_tab.add_by_name(name)
                                if self.solvent_tab.items:
                                    self.solvent_tab.items[-1].weight_grams = weight
                            elif ing.category == "pigment":
                                self.pigment_tab.add_by_name(name)
                                if self.pigment_tab.items:
                                    self.pigment_tab.items[-1].weight_grams = weight
                            elif ing.category == "additive":
                                self.additive_tab.add_by_name(name)
                                if self.additive_tab.items:
                                    self.additive_tab.items[-1].weight_grams = weight
                            elif ing.category == "nanocomposite":
                                self.nano_tab.add_by_name(name)
                                if self.nano_tab.items:
                                    self.nano_tab.items[-1].weight_grams = weight
                            elif ing.category == "filler":
                                self.filler_tab.add_by_name(name)
                                if self.filler_tab.items:
                                    self.filler_tab.items[-1].weight_grams = weight
            else:
                # Parse TXT file
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if ':' in line and 'g' in line:
                        if line.startswith(('Formulation:', 'Operator:', 'Date:', 'Type:', 'Environment:', 'Application:', 'INGREDIENTS:', 'Total:')):
                            continue
                        parts = line.split(':')
                        if len(parts) >= 2:
                            name = parts[0].strip()
                            weight_match = re.search(r'([\d\.]+)\s*g', parts[1])
                            if weight_match:
                                weight = float(weight_match.group(1))
                                ing = IngredientDB.get(name)
                                if ing:
                                    if ing.category == "resin":
                                        self.resin_tab.add_by_name(name)
                                        if self.resin_tab.items:
                                            self.resin_tab.items[-1].weight_grams = weight
                                    elif ing.category == "solvent":
                                        self.solvent_tab.add_by_name(name)
                                        if self.solvent_tab.items:
                                            self.solvent_tab.items[-1].weight_grams = weight
                                    elif ing.category == "pigment":
                                        self.pigment_tab.add_by_name(name)
                                        if self.pigment_tab.items:
                                            self.pigment_tab.items[-1].weight_grams = weight
                                    elif ing.category == "additive":
                                        self.additive_tab.add_by_name(name)
                                        if self.additive_tab.items:
                                            self.additive_tab.items[-1].weight_grams = weight
                                    elif ing.category == "nanocomposite":
                                        self.nano_tab.add_by_name(name)
                                        if self.nano_tab.items:
                                            self.nano_tab.items[-1].weight_grams = weight
                                    elif ing.category == "filler":
                                        self.filler_tab.add_by_name(name)
                                        if self.filler_tab.items:
                                            self.filler_tab.items[-1].weight_grams = weight
            
            # Update all tables
            for tab in [self.resin_tab, self.solvent_tab, self.pigment_tab, self.additive_tab, self.nano_tab, self.filler_tab]:
                tab.update_table()
            
            self.update_weight()
            QMessageBox.information(self, "Success", self.tr("importSuccess"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"{self.tr('importError')}\n{str(e)}")