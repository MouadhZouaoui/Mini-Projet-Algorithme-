"""
Main Window for Arabic Morphological Engine GUI
Connects PyQt6 interface with the morphological engine backend.
"""

import json
import os
from typing import Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QMessageBox, QFileDialog, QStatusBar,
    QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon

# Import custom widgets
from .dialogs import (
    LoadDataDialog, AddRootDialog, SearchRootDialog,
    GenerateWordDialog, ValidateWordDialog, AnalyzeRootDialog,
    PatternManagementDialog, StatisticsDialog, TreeVisualizationDialog
)
from .widgets import (
    DashboardWidget, RootsWidget, PatternsWidget, 
    GenerationWidget, ValidationWidget, AnalysisWidget
)


class MainWindow(QMainWindow):
    """Main application window for Arabic Morphological Engine."""
    
    def __init__(self, engine):
        """
        Initialize main window.
        
        Args:
            engine: MorphologicalEngine instance
        """
        super().__init__()
        
        self.engine = engine
        self.data_loaded = False
        
        self._setup_ui()
        self._create_menu_bar()
        self._create_status_bar()
        self._connect_signals()
        
        # Try to auto-load data
        QTimer.singleShot(100, self._try_auto_load_data)
    
    def _setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("🌙 Arabic Morphological Engine")
        self.setMinimumSize(1200, 800)
        
        # Apply stylesheet
        self._apply_stylesheet()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # Create tab pages
        self.dashboard_widget = DashboardWidget(self.engine)
        self.roots_widget = RootsWidget(self.engine)
        self.patterns_widget = PatternsWidget(self.engine)
        self.generation_widget = GenerationWidget(self.engine)
        self.validation_widget = ValidationWidget(self.engine)
        self.analysis_widget = AnalysisWidget(self.engine)
        
        # Add tabs
        self.tabs.addTab(self.dashboard_widget, "📊 Dashboard")
        self.tabs.addTab(self.roots_widget, "📚 Roots (جذور)")
        self.tabs.addTab(self.patterns_widget, "🏗️ Patterns (أوزان)")
        self.tabs.addTab(self.generation_widget, "⚙️ Generation (توليد)")
        self.tabs.addTab(self.validation_widget, "✅ Validation (تحقق)")
        self.tabs.addTab(self.analysis_widget, "🔬 Analysis (تحليل)")
        
        main_layout.addWidget(self.tabs)
    
    def _apply_stylesheet(self):
        """Apply custom stylesheet with beige and purple theme."""
        stylesheet = """
            * {
                font-family: Arial, sans-serif;
            }
            
            QMainWindow {
                
            }
            
            QWidget {
                
                color: #2C2C2C;
            }
            
            QTabWidget::pane {
                
            }
            
            QTabBar::tab {
                color: #2C2C2C;
                padding: 8px 20px;
                margin-right: 2px;
                font-size: 11px;
                font-weight: bold;
            }
            
            QTabBar::tab:selected {
                
                border-bottom: 3px solid #7B68A6;
            }
            
            QPushButton {
                background-color: #7B68A6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }
            
            QPushButton:hover {
                background-color: #8B77B6;
            }
            
            QPushButton:pressed {
                background-color: #6B5896;
            }
            
            QLineEdit, QTextEdit {
                background-color: #FEFDFB;
                color: #2C2C2C;
                border-radius: 4px;
                padding: 6px;
                font-size: 11px;
            }
            
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #7B68A6;
            }
            
            QLabel {
                color: #2C2C2C;
                font-size: 11px;
            }
            
            QGroupBox {
                color: #2C2C2C;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                font-size: 11px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            
            QTableWidget {
                background-color: #FEFDFB;
                font-size: 10px;
            }
            
            QTableWidget::item {
                padding: 4px;
                background-color: #FEFDFB;
                color: #2C2C2C;
            }
            
            QTableWidget::item:selected {
                background-color: #E8C9B8;
            }
            
            QHeaderView::section {
                color: #2C2C2C;
                padding: 6px;
                font-weight: bold;
                font-size: 10px;
            }
            
            QComboBox {
                background-color: #FEFDFB;
                color: #2C2C2C;
                border-radius: 4px;
                padding: 6px;
                font-size: 11px;
            }
            
            QComboBox::drop-down {
                border: none;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7B68A6;
            }
            
            QComboBox QAbstractItemView {
                background-color: #FEFDFB;
                color: #2C2C2C;
                selection-background-color: #E8C9B8;
            }
            
            QMenuBar {
                color: #2C2C2C;
                font-size: 11px;
            }
            
            QMenuBar::item:selected {
            }
            
            QMenu {
                
                color: #2C2C2C;
                font-size: 11px;
            }
            
            QMenu::item:selected {
                background-color: #E8C9B8;
            }
            
            QStatusBar {
                color: #2C2C2C;
                font-size: 10px;
            }
            
            QDialog {
                
            }
            
            QMessageBox QLabel {
                color: #2C2C2C;
            }
        """
        self.setStyleSheet(stylesheet)
    
    def _create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        load_action = QAction("📥 Load Data...", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_data)
        file_menu.addAction(load_action)
        
        reload_action = QAction("🔄 Reload Data", self)
        reload_action.setShortcut("Ctrl+R")
        reload_action.triggered.connect(self.reload_data)
        file_menu.addAction(reload_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("💾 Export Results...", self)
        export_action.setShortcut("Ctrl+S")
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("🚪 Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Operations menu
        ops_menu = menubar.addMenu("&Operations")
        
        add_root_action = QAction("➕ Add Root...", self)
        add_root_action.setShortcut("Ctrl+N")
        add_root_action.triggered.connect(self.add_root)
        ops_menu.addAction(add_root_action)
        
        search_action = QAction("🔍 Search Root...", self)
        search_action.setShortcut("Ctrl+F")
        search_action.triggered.connect(self.search_root)
        ops_menu.addAction(search_action)
        
        ops_menu.addSeparator()
        
        generate_action = QAction("🏗️ Generate Word...", self)
        generate_action.setShortcut("Ctrl+G")
        generate_action.triggered.connect(self.generate_word)
        ops_menu.addAction(generate_action)
        
        validate_action = QAction("✅ Validate Word...", self)
        validate_action.setShortcut("Ctrl+V")
        validate_action.triggered.connect(self.validate_word)
        ops_menu.addAction(validate_action)
        
        analyze_action = QAction("🔬 Analyze Root...", self)
        analyze_action.setShortcut("Ctrl+A")
        analyze_action.triggered.connect(self.analyze_root)
        ops_menu.addAction(analyze_action)
        
        # Patterns menu
        patterns_menu = menubar.addMenu("&Patterns")
        
        manage_patterns_action = QAction("🔄 Manage Patterns...", self)
        manage_patterns_action.triggered.connect(self.manage_patterns)
        patterns_menu.addAction(manage_patterns_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        stats_action = QAction("📊 Statistics...", self)
        stats_action.triggered.connect(self.show_statistics)
        view_menu.addAction(stats_action)
        
        tree_viz_action = QAction("🌳 Tree Visualization...", self)
        tree_viz_action.triggered.connect(self.show_tree_visualization)
        view_menu.addAction(tree_viz_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("ℹ️ About...", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def _create_status_bar(self):
        """Create status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _connect_signals(self):
        """Connect widget signals."""
        # Dashboard signals
        self.dashboard_widget.load_data_requested.connect(self.load_data)
        self.dashboard_widget.add_root_requested.connect(self.add_root)
        self.dashboard_widget.generate_word_requested.connect(self.generate_word)
        
        # Tab change signal
        self.tabs.currentChanged.connect(self._on_tab_changed)
    
    def _on_tab_changed(self, index):
        """Handle tab change."""
        # Refresh current tab
        current_widget = self.tabs.widget(index)
        if hasattr(current_widget, 'refresh'):
            current_widget.refresh()
    
    def _try_auto_load_data(self):
        """Try to auto-load data from default location."""
        try:
            # Get script directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            
            roots_path = os.path.join(project_root, "data", "roots.txt")
            patterns_path = os.path.join(project_root, "data", "patterns.json")
            
            if os.path.exists(roots_path) and os.path.exists(patterns_path):
                self._load_data_from_files(roots_path, patterns_path)
        except Exception as e:
            # Silent fail for auto-load
            pass
    
    def load_data(self):
        """Load data from files."""
        dialog = LoadDataDialog(self)
        if dialog.exec():
            roots_path, patterns_path = dialog.get_paths()
            self._load_data_from_files(roots_path, patterns_path)
    
    def _load_data_from_files(self, roots_path: str, patterns_path: str):
        """Load data from specific file paths."""
        try:
            # Load roots
            with open(roots_path, 'r', encoding='utf-8') as f:
                roots = [line.strip() for line in f if line.strip()]
                self.engine.load_roots(roots)
            
            # Load patterns
            with open(patterns_path, 'r', encoding='utf-8') as f:
                patterns = json.load(f)
                self.engine.load_patterns(patterns)
            
            self.data_loaded = True
            
            # Update UI
            self._refresh_all_widgets()
            
            # Show success message
            stats = self.engine.get_engine_statistics()
            msg = f"✅ Data loaded successfully!\n\n"
            msg += f"Roots: {stats['roots_count']}\n"
            msg += f"Patterns: {stats['patterns_count']}"
            
            QMessageBox.information(self, "Success", msg)
            self.status_bar.showMessage(
                f"Data loaded: {stats['roots_count']} roots, {stats['patterns_count']} patterns"
            )
            
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Error", f"File not found: {e}")
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Error", f"Invalid JSON: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
    
    def reload_data(self):
        """Reload data from last loaded files."""
        if not self.data_loaded:
            self.load_data()
        else:
            self._try_auto_load_data()
    
    def add_root(self):
        """Add a new root."""
        dialog = AddRootDialog(self.engine, self)
        if dialog.exec():
            self._refresh_all_widgets()
    
    def search_root(self):
        """Search for a root."""
        dialog = SearchRootDialog(self.engine, self)
        dialog.exec()
    
    def generate_word(self):
        """Generate a word from root and pattern."""
        dialog = GenerateWordDialog(self.engine, self)
        if dialog.exec():
            self._refresh_all_widgets()
    
    def validate_word(self):
        """Validate an Arabic word."""
        dialog = ValidateWordDialog(self.engine, self)
        dialog.exec()
    
    def analyze_root(self):
        """Analyze root morphology."""
        dialog = AnalyzeRootDialog(self.engine, self)
        dialog.exec()
    
    def manage_patterns(self):
        """Open pattern management dialog."""
        dialog = PatternManagementDialog(self.engine, self)
        if dialog.exec():
            self._refresh_all_widgets()
    
    def show_statistics(self):
        """Show engine statistics."""
        dialog = StatisticsDialog(self.engine, self)
        dialog.exec()
    
    def show_tree_visualization(self):
        """Show AVL tree visualization."""
        dialog = TreeVisualizationDialog(self.engine, self)
        dialog.exec()
    
    def export_results(self):
        """Export generated words."""
        # Get save file path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Results",
            "",
            "JSON Files (*.json);;CSV Files (*.csv);;Text Files (*.txt)"
        )
        
        if not file_path:
            return
        
        try:
            # Determine format from extension
            if file_path.endswith('.json'):
                export_format = 'json'
            elif file_path.endswith('.csv'):
                export_format = 'csv'
            else:
                export_format = 'text'
            
            # Export data
            export_data = self.engine.export_results(export_format)
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(export_data)
            
            QMessageBox.information(
                self,
                "Success",
                f"Results exported to:\n{file_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to export: {e}"
            )
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
        <h2>🌙 Arabic Morphological Engine</h2>
        <p><b>Version:</b> 1.0</p>
        <p><b>Author:</b> Zouaoui Mouadh</p>
        <p><b>Course:</b> Algorithmique 2026</p>
        
        <h3>Features:</h3>
        <ul>
            <li>AVL Tree for Arabic roots storage (O(log n) search)</li>
            <li>Hash Table for morphological patterns (O(1) access)</li>
            <li>Word generation from roots and patterns</li>
            <li>Word validation and pattern recognition</li>
            <li>Root morphological analysis</li>
            <li>GUI and CLI interfaces</li>
        </ul>
        
        <h3>Technologies:</h3>
        <ul>
            <li>Python 3.x</li>
            <li>PyQt6 for GUI</li>
            <li>Custom data structures (AVL Tree, Hash Table)</li>
        </ul>
        """
        
        QMessageBox.about(self, "About", about_text)
    
    def _refresh_all_widgets(self):
        """Refresh all widget displays."""
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if hasattr(widget, 'refresh'):
                widget.refresh()
    
    def closeEvent(self, event):
        """Handle window close event."""
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()