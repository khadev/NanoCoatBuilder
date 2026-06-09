"""Beautiful splash screen with progress bar."""

from PySide6.QtWidgets import QSplashScreen, QApplication
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QLinearGradient, QBrush, QPen, QPainterPath
from PySide6.QtCore import Qt, QRect


class ModernSplashScreen(QSplashScreen):
    """Modern splash screen with gradient background and working progress bar."""
    
    def __init__(self):
        self.width = 600
        self.height = 400
        self.current_progress = 0
        self.status_message = "Initializing..."
        
        # Create pixmap for splash screen
        pixmap = QPixmap(self.width, self.height)
        pixmap.fill(Qt.transparent)
        
        super().__init__(pixmap)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Initial paint
        self.repaint()
    
    def paintEvent(self, event):
        """Custom paint event to draw the splash screen."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width, self.height, 20, 20)
        painter.setClipPath(path)
        
        # Draw gradient background
        gradient = QLinearGradient(0, 0, self.width, self.height)
        gradient.setColorAt(0, QColor(26, 35, 126))  # #1a237e
        gradient.setColorAt(0.5, QColor(40, 53, 147))  # #283593
        gradient.setColorAt(1, QColor(57, 73, 171))  # #3949ab
        painter.fillRect(0, 0, self.width, self.height, QBrush(gradient))
        
        # Draw border
        painter.setPen(QPen(QColor(255, 255, 255, 50), 2))
        painter.drawRoundedRect(0, 0, self.width, self.height, 20, 20)
        
        # Draw icon
        painter.setPen(Qt.white)
        painter.setFont(QFont("Segoe UI", 48, QFont.Bold))
        painter.drawText(QRect(0, 40, self.width, 80), Qt.AlignCenter, "🔬")
        
        # Draw title
        painter.setFont(QFont("Segoe UI", 24, QFont.Bold))
        painter.drawText(QRect(0, 120, self.width, 50), Qt.AlignCenter, "NanoCoatBuilder")
        
        # Draw subtitle
        painter.setFont(QFont("Segoe UI", 12))
        painter.setPen(QColor(255, 255, 255, 200))
        painter.drawText(QRect(0, 170, self.width, 30), Qt.AlignCenter, "Advanced Coating Formulation Software")
        
        # Draw version
        painter.setFont(QFont("Segoe UI", 10))
        painter.setPen(QColor(255, 255, 255, 150))
        painter.drawText(QRect(0, 200, self.width, 25), Qt.AlignCenter, "Version 1.0 - Research Edition")
        
        # Draw status message
        painter.setFont(QFont("Segoe UI", 11))
        painter.setPen(QColor(255, 255, 255, 220))
        painter.drawText(QRect(0, 260, self.width, 30), Qt.AlignCenter, self.status_message)
        
        # Draw progress bar background
        progress_bg_rect = QRect(50, 300, self.width - 100, 8)
        painter.setBrush(QBrush(QColor(255, 255, 255, 50)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(progress_bg_rect, 10, 10)
        
        # Draw progress bar fill
        progress_fill_width = int((self.width - 100) * (self.current_progress / 100))
        if progress_fill_width > 0:
            progress_fill_rect = QRect(50, 300, progress_fill_width, 8)
            fill_gradient = QLinearGradient(50, 300, progress_fill_width + 50, 308)
            fill_gradient.setColorAt(0, QColor(76, 175, 80))  # #4CAF50
            fill_gradient.setColorAt(1, QColor(139, 195, 74))  # #8BC34A
            painter.setBrush(QBrush(fill_gradient))
            painter.drawRoundedRect(progress_fill_rect, 10, 10)
        
        # Draw progress text
        painter.setFont(QFont("Segoe UI", 10))
        painter.setPen(QColor(255, 255, 255, 200))
        painter.drawText(QRect(0, 315, self.width, 25), Qt.AlignCenter, f"{int(self.current_progress)}%")
        
        # Draw copyright
        painter.setFont(QFont("Segoe UI", 9))
        painter.setPen(QColor(255, 255, 255, 100))
        painter.drawText(QRect(0, self.height - 30, self.width, 20), Qt.AlignCenter, "© 2026 - For Research Purposes")
        
        painter.end()
    
    def update_progress(self, value, message):
        """Update progress bar and status message."""
        self.current_progress = value
        self.status_message = message
        self.repaint()
        # Force immediate update
        QApplication.processEvents()
    
    def finish(self, window):
        """Close splash screen and show main window."""
        self.hide()
        window.show()
        window.raise_()
        window.activateWindow()