"""Main window for NanoCoatBuilder."""

import sys
import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QAction, QFont, QColor, QDesktopServices
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
    QLabel, QLineEdit, QSplitter, QScrollArea, QFrame, QMessageBox,
    QDialog, QListWidget, QFileDialog, QInputDialog, QGroupBox, QFormLayout,
    QDialogButtonBox, QMenuBar, QMenu, QStatusBar, QToolBar, QSizePolicy,
    QComboBox, QProgressBar
)

from core.database.ingredient_db import IngredientDB
from core.models.ingredient import CoatingType
from core.database.history_manager import HistoryManager, FormulationRecord
from core.analysis.coating_analyzer import CoatingAnalyzer, AnalysisResult
from core.utils.language_manager import LanguageManager
from core.utils.constants import APPLICATION_TYPES, TRANSLATIONS
from core.utils.rag_agent import RAGAgent

from ui.widgets.ingredient_table import IngredientTable
from ui.widgets.results_display import ResultsDisplay
from ui.widgets.modern_button import ModernButton
from ui.dialogs.history_dialog import HistoryDialog
from ui.dialogs.compare_dialog import CompareDialog
from ui.dialogs.about_dialog import AboutDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        LanguageManager.init()
        self.formulations = []
        self.init_ui()
    
    def tr(self, key):
        return TRANSLATIONS[LanguageManager._current_lang].get(key, key)
    
    def init_ui(self):
        self.setWindowTitle("🔬 " + TRANSLATIONS[LanguageManager._current_lang]["title"])
        self.setMinimumSize(1400, 900)
        self.showMaximized()
        
        # Menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.tr("newForm"), lambda: self.add_formulation())
        file_menu.addAction(self.tr("importForm"), lambda: self.import_current())
        file_menu.addSeparator()
        file_menu.addAction(self.tr("history"), lambda: self.show_history())
        file_menu.addAction(self.tr("compare"), lambda: self.compare_formulations())
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.show_about)
        
        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        new_btn = QPushButton("➕ " + self.tr("newForm"))
        new_btn.setStyleSheet("background: #2196F3; color: white; border: none; border-radius: 5px; padding: 8px 15px;")
        new_btn.clicked.connect(self.add_formulation)
        toolbar.addWidget(new_btn)
        
        history_btn = QPushButton("📜 " + self.tr("history"))
        history_btn.setStyleSheet("background: #9C27B0; color: white; border: none; border-radius: 5px; padding: 8px 15px;")
        history_btn.clicked.connect(self.show_history)
        toolbar.addWidget(history_btn)
        
        compare_btn = QPushButton("🔄 " + self.tr("compare"))
        compare_btn.setStyleSheet("background: #FF9800; color: white; border: none; border-radius: 5px; padding: 8px 15px;")
        compare_btn.clicked.connect(self.compare_formulations)
        toolbar.addWidget(compare_btn)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        
        self.lang_en = QPushButton("🇬🇧 EN")
        self.lang_en.setStyleSheet("background: #4CAF50; color: white; border: none; border-radius: 5px; padding: 8px 15px;")
        self.lang_en.clicked.connect(lambda: self.set_lang("EN"))
        self.lang_fr = QPushButton("🇫🇷 FR")
        self.lang_fr.setStyleSheet("background: #FF9800; color: white; border: none; border-radius: 5px; padding: 8px 15px;")
        self.lang_fr.clicked.connect(lambda: self.set_lang("FR"))
        toolbar.addWidget(self.lang_en)
        toolbar.addWidget(self.lang_fr)
        
        # Main splitter
        splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(splitter)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        splitter.addWidget(self.tab_widget)
        
        self.results_scroll = QScrollArea()
        self.results_scroll.setWidgetResizable(True)
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_scroll.setWidget(self.results_container)
        splitter.addWidget(self.results_scroll)
        splitter.setSizes([int(self.width() * 0.45), int(self.width() * 0.55)])
        
        self.statusBar().showMessage(self.tr("statusReady"))
        self.add_formulation()
        self.show_welcome()
    
    def set_lang(self, lang):
        LanguageManager.set_language(lang)
        self.setWindowTitle("🔬 " + TRANSLATIONS[lang]["title"])
        self.statusBar().showMessage(self.tr("statusReady"))
        
        # Update all formulations (tabs)
        for editor in self.formulations:
            if hasattr(editor, 'refresh_ui'):
                editor.refresh_ui()
        
        # Refresh current results if any
        current_idx = self.tab_widget.currentIndex()
        if current_idx >= 0 and current_idx < len(self.formulations):
            editor = self.formulations[current_idx]
            if hasattr(editor, 'current_result') and editor.current_result:
                self.show_results(editor.current_result, current_idx)
        
        QMessageBox.information(self, "Language", f"Switched to {'English' if lang=='EN' else 'Français'}")
    
    def add_formulation(self):
        from ui.widgets.formulation_editor import FormulationEditor
        idx = len(self.formulations)
        editor = FormulationEditor(idx)
        editor.analysis_completed.connect(self.show_results)
        self.formulations.append(editor)
        self.tab_widget.addTab(editor, f"Formulation {idx+1}")
        self.tab_widget.setCurrentWidget(editor)
    
    def close_tab(self, idx):
        if len(self.formulations) <= 1:
            QMessageBox.warning(self, "Warning", "Cannot close the only tab")
            return
        self.tab_widget.removeTab(idx)
        self.formulations.pop(idx)
    
    def show_results(self, result: Optional[AnalysisResult], tab_idx: int):
        if self.tab_widget.currentIndex() != tab_idx:
            return
        self.clear_results()
        if result is None:
            self.show_welcome()
        else:
            self.results_layout.addWidget(ResultsDisplay(result))
    
    def clear_results(self):
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def show_welcome(self):
        welcome = QLabel("""
        <div style='text-align:center; padding:40px;'>
            <div style='background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 15px; padding: 30px;'>
                <h1 style='color:#2196F3;'>🔬 NanoCoatBuilder</h1>
                <p style='color:#1976D2;'>Advanced Coating Formulation Software</p>
            </div>
            <div style='margin-top: 20px; text-align: left; max-width: 600px; margin-left: auto; margin-right: auto;'>
                <h3 style='color:#1565C0;'>📋 Instructions:</h3>
                <p style='color:#0D47A1;'>1. Click on any tab (Resins, Nanocomposites, Pigments, etc.)</p>
                <p style='color:#0D47A1;'>2. Click <b style='color:#2196F3;'>ADD</b> to select ingredients from the database</p>
                <p style='color:#0D47A1;'>3. Enter weights in grams (target total: <b style='color:#2196F3;'>100g</b>)</p>
                <p style='color:#0D47A1;'>4. Select <b style='color:#2196F3;'>Application Sector</b> (Navy, Aviation, Space, etc.)</p>
                <p style='color:#0D47A1;'>5. Click <b style='color:#2196F3;'>VALIDATE (100g)</b> to save or <b style='color:#2196F3;'>FULL ANALYSIS</b> for predictions</p>
                <p style='color:#0D47A1;'>6. Results include: Performance, Validation, Graphs, Protocol, Characterization, References</p>
                <p style='color:#0D47A1;'>7. Click <b style='color:#2196F3;'>EXPORT PDF</b> to save report as HTML (printable as PDF)</p>
            </div>
        </div>
        """)
        welcome.setAlignment(Qt.AlignCenter)
        self.results_layout.addWidget(welcome)
    
    def import_current(self):
        idx = self.tab_widget.currentIndex()
        if idx >= 0:
            self.formulations[idx].import_formulation()
    
    def show_history(self):
        from ui.dialogs.history_dialog import HistoryDialog
        current_editor = self.formulations[self.tab_widget.currentIndex()]
        dialog = HistoryDialog(current_editor, self)
        dialog.exec()
    
    def compare_formulations(self):
        dialog = CompareDialog(self)
        dialog.exec()
    
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()