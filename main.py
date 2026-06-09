#!/usr/bin/env python3
"""Entry point for NanoCoatBuilder with splash screen."""

import sys
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.splash_screen import ModernSplashScreen
from ui.main_window import MainWindow
from core.database.ingredient_db import IngredientDB


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    splash = ModernSplashScreen()
    splash.show()
    
    loading_steps = [
        (10, "Initializing modules..."),
        (25, "Loading ingredient database..."),
        (40, "Loading resins..."),
        (55, "Loading nanocomposites..."),
        (70, "Loading pigments and additives..."),
        (85, "Preparing user interface..."),
        (95, "Almost ready..."),
        (100, "Starting application...")
    ]
    
    for progress, message in loading_steps:
        splash.update_progress(progress, message)
        time.sleep(0.2)
    
    IngredientDB.init()
    
    window = MainWindow()
    window.show()
    
    splash.finish(window)
    
    sys.exit(app.exec())