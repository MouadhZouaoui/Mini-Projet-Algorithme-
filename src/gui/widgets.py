"""
Custom widgets for Arabic Morphological Engine GUI.
Contains tab widgets for different functionalities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QTextEdit, QGroupBox, QGridLayout, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from arabic_utils import ArabicUtils
from root_classifier import RootClassifier


class DashboardWidget(QWidget):
    """Dashboard overview widget."""
    
    load_data_requested = pyqtSignal()
    add_root_requested = pyqtSignal()
    generate_word_requested = pyqtSignal()
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Welcome message
        welcome = QLabel("🌙 Welcome to Arabic Morphological Engine")
        welcome.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome)
        
        # Statistics group
        stats_group = QGroupBox("Statistics")
        stats_layout = QGridLayout(stats_group)
        
        self.roots_label = QLabel("Roots: 0")
        self.roots_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(self.roots_label, 0, 0)
        
        self.patterns_label = QLabel("Patterns: 0")
        self.patterns_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(self.patterns_label, 0, 1)
        
        self.generated_label = QLabel("Generated Words: 0")
        self.generated_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(self.generated_label, 1, 0)
        
        self.tree_height_label = QLabel("Tree Height: 0")
        self.tree_height_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(self.tree_height_label, 1, 1)
        
        layout.addWidget(stats_group)
        
        # Quick actions
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        load_btn = QPushButton("📥 Load Data")
        load_btn.clicked.connect(self.load_data_requested.emit)
        actions_layout.addWidget(load_btn)
        
        add_root_btn = QPushButton("➕ Add Root")
        add_root_btn.clicked.connect(self.add_root_requested.emit)
        actions_layout.addWidget(add_root_btn)
        
        generate_btn = QPushButton("🏗️ Generate Word")
        generate_btn.clicked.connect(self.generate_word_requested.emit)
        actions_layout.addWidget(generate_btn)
        
        layout.addWidget(actions_group)
        
        # Info text
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(200)
        info_text.setText(
            "Features:\n"
            "• AVL Tree for Arabic roots storage (O(log n) search)\n"
            "• Hash Table for morphological patterns (O(1) access)\n"
            "• Word generation from roots and patterns\n"
            "• Word validation and pattern recognition\n"
            "• Root morphological analysis\n\n"
            "Get started by loading data files!"
        )
        layout.addWidget(info_text)
        
        layout.addStretch()
    
    def refresh(self):
        """Refresh statistics."""
        stats = self.engine.get_engine_statistics()
        
        self.roots_label.setText(f"Roots: {stats['roots_count']}")
        self.patterns_label.setText(f"Patterns: {stats['patterns_count']}")
        self.generated_label.setText(f"Generated Words: {stats['generated_words_count']}")
        self.tree_height_label.setText(f"Tree Height: {stats['avl_tree_height']}")


class RootsWidget(QWidget):
    """Widget for displaying and managing roots."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Arabic Roots (الجذور)")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Roots table
        self.roots_table = QTableWidget()
        self.roots_table.setColumnCount(4)
        self.roots_table.setHorizontalHeaderLabels([
            "Root", "Frequency", "Derivatives", "Height"
        ])
        self.roots_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.roots_table)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(refresh_btn)
    
    def refresh(self):
        """Refresh roots display."""
        all_nodes = self.engine.roots_tree.get_all_nodes()
        
        self.roots_table.setRowCount(len(all_nodes))
        
        for row, node in enumerate(all_nodes):
            self.roots_table.setItem(row, 0, QTableWidgetItem(node.root))
            self.roots_table.setItem(row, 1, QTableWidgetItem(str(node.frequency)))
            self.roots_table.setItem(row, 2, QTableWidgetItem(str(node.get_derivative_count())))
            self.roots_table.setItem(row, 3, QTableWidgetItem(str(node.height)))


class PatternsWidget(QWidget):
    """Widget for displaying and managing patterns."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Morphological Patterns (الأوزان)")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Patterns table
        self.patterns_table = QTableWidget()
        self.patterns_table.setColumnCount(4)
        self.patterns_table.setHorizontalHeaderLabels([
            "Name", "Template", "Description", "Example"
        ])
        self.patterns_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.patterns_table)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(refresh_btn)
    
    def refresh(self):
        """Refresh patterns display."""
        patterns = self.engine.patterns_table.get_all_patterns()
        
        self.patterns_table.setRowCount(len(patterns))
        
        for row, (name, data) in enumerate(patterns):
            self.patterns_table.setItem(row, 0, QTableWidgetItem(name))
            self.patterns_table.setItem(row, 1, QTableWidgetItem(data.get('template', '')))
            self.patterns_table.setItem(row, 2, QTableWidgetItem(data.get('description', '')))
            self.patterns_table.setItem(row, 3, QTableWidgetItem(data.get('example', '')))


class GenerationWidget(QWidget):
    """Widget for word generation."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Word Generation (توليد الكلمات)")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Generated words table
        self.generation_table = QTableWidget()
        self.generation_table.setColumnCount(5)
        self.generation_table.setHorizontalHeaderLabels([
            "Root", "Pattern", "Template", "Generated Word", "Valid"
        ])
        self.generation_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.generation_table)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(refresh_btn)
    
    def refresh(self):
        """Refresh generation display."""
        # Get all derivatives from all roots
        all_derivatives = []
        all_nodes = self.engine.roots_tree.get_all_nodes()
        
        for node in all_nodes:
            for deriv in node.get_derivatives():
                all_derivatives.append({
                    'root': node.root,
                    'word': deriv['word'],
                    'pattern': deriv['pattern'],
                    'frequency': deriv['frequency']
                })
        
        self.generation_table.setRowCount(len(all_derivatives))
        
        for row, deriv in enumerate(all_derivatives):
            # Get pattern data
            pattern_data = self.engine.patterns_table.search(deriv['pattern'])
            template = pattern_data.get('template', '') if pattern_data else ''
            
            self.generation_table.setItem(row, 0, QTableWidgetItem(deriv['root']))
            self.generation_table.setItem(row, 1, QTableWidgetItem(deriv['pattern']))
            self.generation_table.setItem(row, 2, QTableWidgetItem(template))
            self.generation_table.setItem(row, 3, QTableWidgetItem(deriv['word']))
            self.generation_table.setItem(row, 4, QTableWidgetItem("✓"))


class ValidationWidget(QWidget):
    """Widget for word validation."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Word Validation (التحقق من الكلمات)")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Info text
        info = QLabel("Use Operations → Validate Word to validate Arabic words")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Results area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("Validation results will appear here...")
        layout.addWidget(self.results_text)
    
    def refresh(self):
        """Refresh validation display."""
        pass


class AnalysisWidget(QWidget):
    """Widget for root analysis."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Root Analysis (تحليل الجذور)")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Analysis table showing root categories
        self.analysis_table = QTableWidget()
        self.analysis_table.setColumnCount(4)
        self.analysis_table.setHorizontalHeaderLabels([
            "Root", "Category", "Subtype", "Description"
        ])
        self.analysis_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.analysis_table)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(refresh_btn)
    
    def refresh(self):
        """Refresh analysis display."""
        all_roots = self.engine.roots_tree.display_inorder()
        
        self.analysis_table.setRowCount(len(all_roots))
        
        for row, root in enumerate(all_roots):
            analysis = RootClassifier.classify(root)
            
            self.analysis_table.setItem(row, 0, QTableWidgetItem(root))
            self.analysis_table.setItem(row, 1, QTableWidgetItem(analysis.category.value))
            self.analysis_table.setItem(row, 2, QTableWidgetItem(analysis.subtype or 'N/A'))
            self.analysis_table.setItem(row, 3, QTableWidgetItem(analysis.description))