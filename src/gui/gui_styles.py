"""
GUI Styling System for Arabic Morphological Engine
Complete styling with proper sizing and layout fixes.
"""

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication


class AppStyles:
    """Centralized styling for the application."""
    
    # Color Palette
    COLORS = {
        'background': '#E8DCC8',
        'surface': '#F5EFE6',
        'surface_dark': '#D4C4B0',
        'primary': '#6B5B95',
        'primary_hover': '#8573B3',
        'primary_pressed': '#584A7A',
        'text_primary': '#2C2416',
        'text_secondary': '#5A4E3A',
        'text_on_primary': '#FFFFFF',
        'border': '#C5B5A0',
        'divider': '#D4C4B0',
        'success': '#4CAF50',
        'warning': '#FF9800',
        'error': '#F44336',
        'info': '#2196F3',
    }
    
    @staticmethod
    def get_main_stylesheet():
        """Get main application stylesheet."""
        return f"""
        /* Main Window */
        QMainWindow, QWidget {{
            background-color: {AppStyles.COLORS['background']};
            color: {AppStyles.COLORS['text_primary']};
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 12pt;
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 2px solid {AppStyles.COLORS['border']};
            background-color: {AppStyles.COLORS['surface']};
            border-radius: 8px;
            padding: 8px;
        }}
        
        QTabBar::tab {{
            background-color: {AppStyles.COLORS['surface_dark']};
            color: {AppStyles.COLORS['text_primary']};
            padding: 12px 24px;
            margin: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-size: 13pt;
            font-weight: bold;
            min-height: 35px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {AppStyles.COLORS['primary']};
            color: {AppStyles.COLORS['text_on_primary']};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {AppStyles.COLORS['primary_hover']};
            color: {AppStyles.COLORS['text_on_primary']};
        }}
        
        /* Labels */
        QLabel {{
            color: {AppStyles.COLORS['text_primary']};
            background-color: transparent;
            border: none;
            min-height: 22px;
            padding: 2px;
        }}
        
        /* Push Buttons */
        QPushButton {{
            background-color: {AppStyles.COLORS['primary']};
            color: {AppStyles.COLORS['text_on_primary']};
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 13pt;
            font-weight: bold;
            min-height: 45px;
        }}
        
        QPushButton:hover {{
            background-color: {AppStyles.COLORS['primary_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {AppStyles.COLORS['primary_pressed']};
        }}
        
        QPushButton:disabled {{
            background-color: {AppStyles.COLORS['surface_dark']};
            color: {AppStyles.COLORS['text_secondary']};
        }}
        
        /* Line Edit */
        QLineEdit {{
            background-color: {AppStyles.COLORS['surface']};
            color: {AppStyles.COLORS['text_primary']};
            border: 2px solid {AppStyles.COLORS['border']};
            border-radius: 8px;
            padding: 12px;
            font-size: 13pt;
            min-height: 45px;
        }}
        
        QLineEdit:focus {{
            border: 2px solid {AppStyles.COLORS['primary']};
        }}
        
        /* Text Edit */
        QTextEdit, QPlainTextEdit {{
            background-color: {AppStyles.COLORS['surface']};
            color: {AppStyles.COLORS['text_primary']};
            border: 2px solid {AppStyles.COLORS['border']};
            border-radius: 8px;
            padding: 12px;
            font-size: 12pt;
        }}
        
        /* Combo Box */
        QComboBox {{
            background-color: {AppStyles.COLORS['surface']};
            color: {AppStyles.COLORS['text_primary']};
            border: 2px solid {AppStyles.COLORS['border']};
            border-radius: 8px;
            padding: 12px;
            font-size: 13pt;
            min-height: 45px;
        }}
        
        QComboBox:focus {{
            border: 2px solid {AppStyles.COLORS['primary']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {AppStyles.COLORS['surface']};
            border: 2px solid {AppStyles.COLORS['border']};
            border-radius: 8px;
            selection-background-color: {AppStyles.COLORS['primary']};
            selection-color: {AppStyles.COLORS['text_on_primary']};
            padding: 8px;
        }}
        
        /* List Widget */
        QListWidget {{
            background-color: {AppStyles.COLORS['surface']};
            color: {AppStyles.COLORS['text_primary']};
            border: 2px solid {AppStyles.COLORS['border']};
            border-radius: 8px;
            padding: 8px;
        }}
        
        QListWidget::item {{
            padding: 8px;
            border-radius: 4px;
            margin: 2px;
            min-height: 30px;
        }}
        
        QListWidget::item:selected {{
            background-color: {AppStyles.COLORS['primary']};
            color: {AppStyles.COLORS['text_on_primary']};
        }}
        
        QListWidget::item:hover:!selected {{
            background-color: {AppStyles.COLORS['surface_dark']};
        }}
        
        /* Table Widget */
        QTableWidget {{
            background-color: {AppStyles.COLORS['surface']};
            color: {AppStyles.COLORS['text_primary']};
            border: 2px solid {AppStyles.COLORS['border']};
            border-radius: 8px;
            gridline-color: {AppStyles.COLORS['divider']};
        }}
        
        QTableWidget::item {{
            padding: 8px;
            min-height: 30px;
        }}
        
        QTableWidget::item:selected {{
            background-color: {AppStyles.COLORS['primary']};
            color: {AppStyles.COLORS['text_on_primary']};
        }}
        
        QHeaderView::section {{
            background-color: {AppStyles.COLORS['primary']};
            color: {AppStyles.COLORS['text_on_primary']};
            padding: 10px;
            border: none;
            font-weight: bold;
            min-height: 35px;
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {AppStyles.COLORS['surface_dark']};
            color: {AppStyles.COLORS['text_primary']};
            padding: 4px;
            min-height: 30px;
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 8px 12px;
            border-radius: 4px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {AppStyles.COLORS['primary']};
            color: {AppStyles.COLORS['text_on_primary']};
        }}
        
        /* Menu */
        QMenu {{
            background-color: {AppStyles.COLORS['surface']};
            color: {AppStyles.COLORS['text_primary']};
            border: 2px solid {AppStyles.COLORS['border']};
            border-radius: 8px;
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 24px;
            border-radius: 4px;
            min-height: 25px;
        }}
        
        QMenu::item:selected {{
            background-color: {AppStyles.COLORS['primary']};
            color: {AppStyles.COLORS['text_on_primary']};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {AppStyles.COLORS['surface_dark']};
            color: {AppStyles.COLORS['text_primary']};
            border-top: 2px solid {AppStyles.COLORS['border']};
            min-height: 25px;
        }}
        
        /* Dialog */
        QDialog {{
            background-color: {AppStyles.COLORS['background']};
        }}
        
        /* Message Box */
        QMessageBox {{
            background-color: {AppStyles.COLORS['surface']};
        }}
        
        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: {AppStyles.COLORS['surface_dark']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {AppStyles.COLORS['primary']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {AppStyles.COLORS['primary_hover']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* Card Widget - Custom */
        CardWidget {{
            background-color: {AppStyles.COLORS['surface']};
            border: 2px solid {AppStyles.COLORS['border']};
            border-radius: 12px;
        }}
        """
    
    @staticmethod
    def get_card_style():
        """Get style for cards."""
        return f"""
        background-color: {AppStyles.COLORS['surface']};
        border: 2px solid {AppStyles.COLORS['border']};
        border-radius: 12px;
        """
    
    @staticmethod
    def apply_app_style(app: QApplication):
        """Apply styling to application."""
        app.setStyleSheet(AppStyles.get_main_stylesheet())
        
        # Set font
        font = QFont("Segoe UI", 12)
        app.setFont(font)
