"""
Dialog windows for Arabic Morphological Engine GUI.
Contains all popup dialogs for various operations.
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QLabel, QComboBox,
    QTextEdit, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QTabWidget, QWidget,
    QGroupBox, QRadioButton, QButtonGroup, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from arabic_utils import ArabicUtils
from root_classifier import RootClassifier


class LoadDataDialog(QDialog):
    """Dialog for loading data files."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Load Data Files")
        self.setMinimumWidth(500)
        
        self.roots_path = ""
        self.patterns_path = ""
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Roots file
        roots_group = QGroupBox("Roots File (roots.txt)")
        roots_layout = QHBoxLayout(roots_group)
        
        self.roots_edit = QLineEdit()
        self.roots_edit.setPlaceholderText("Select roots.txt file...")
        roots_layout.addWidget(self.roots_edit)
        
        roots_btn = QPushButton("Browse...")
        roots_btn.clicked.connect(self._browse_roots)
        roots_layout.addWidget(roots_btn)
        
        layout.addWidget(roots_group)
        
        # Patterns file
        patterns_group = QGroupBox("Patterns File (patterns.json)")
        patterns_layout = QHBoxLayout(patterns_group)
        
        self.patterns_edit = QLineEdit()
        self.patterns_edit.setPlaceholderText("Select patterns.json file...")
        patterns_layout.addWidget(self.patterns_edit)
        
        patterns_btn = QPushButton("Browse...")
        patterns_btn.clicked.connect(self._browse_patterns)
        patterns_layout.addWidget(patterns_btn)
        
        layout.addWidget(patterns_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        load_btn = QPushButton("Load Data")
        load_btn.clicked.connect(self.accept)
        btn_layout.addWidget(load_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        # Try to set default paths
        self._set_default_paths()
    
    def _set_default_paths(self):
        """Set default file paths."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            
            roots_path = os.path.join(project_root, "data", "roots.txt")
            patterns_path = os.path.join(project_root, "data", "patterns.json")
            
            if os.path.exists(roots_path):
                self.roots_edit.setText(roots_path)
                self.roots_path = roots_path
            
            if os.path.exists(patterns_path):
                self.patterns_edit.setText(patterns_path)
                self.patterns_path = patterns_path
        except:
            pass
    
    def _browse_roots(self):
        """Browse for roots file."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Roots File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self.roots_edit.setText(path)
            self.roots_path = path
    
    def _browse_patterns(self):
        """Browse for patterns file."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Patterns File",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        if path:
            self.patterns_edit.setText(path)
            self.patterns_path = path
    
    def get_paths(self):
        """Get selected file paths."""
        return self.roots_path, self.patterns_path


class AddRootDialog(QDialog):
    """Dialog for adding a new root."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("Add New Root")
        self.setMinimumWidth(400)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Root input
        form_layout = QFormLayout()
        
        self.root_edit = QLineEdit()
        self.root_edit.setPlaceholderText("Enter 3-letter Arabic root (e.g., كتب)")
        self.root_edit.setFont(QFont("Arial", 14))
        self.root_edit.textChanged.connect(self._validate_input)
        form_layout.addRow("Root:", self.root_edit)
        
        layout.addLayout(form_layout)
        
        # Validation label
        self.validation_label = QLabel()
        layout.addWidget(self.validation_label)
        
        # Analysis display
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setMaximumHeight(150)
        layout.addWidget(self.analysis_text)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add Root")
        self.add_btn.clicked.connect(self._add_root)
        self.add_btn.setEnabled(False)
        btn_layout.addWidget(self.add_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def _validate_input(self):
        """Validate root input."""
        root = self.root_edit.text().strip()
        
        if not root:
            self.validation_label.setText("")
            self.analysis_text.clear()
            self.add_btn.setEnabled(False)
            return
        
        if ArabicUtils.is_valid_root(root):
            # Check if exists
            if self.engine.roots_tree.search(root):
                self.validation_label.setText("⚠️ Root already exists")
                self.validation_label.setStyleSheet("color: orange;")
                self.add_btn.setEnabled(False)
            else:
                self.validation_label.setText("✅ Valid root")
                self.validation_label.setStyleSheet("color: green;")
                self.add_btn.setEnabled(True)
            
            # Show analysis
            analysis = RootClassifier.classify(root)
            self.analysis_text.setText(
                f"Category: {analysis.category.value}\n"
                f"Subtype: {analysis.subtype or 'N/A'}\n"
                f"Description: {analysis.description}"
            )
        else:
            self.validation_label.setText("❌ Invalid root (must be 3 Arabic letters)")
            self.validation_label.setStyleSheet("color: red;")
            self.add_btn.setEnabled(False)
            self.analysis_text.clear()
    
    def _add_root(self):
        """Add the root."""
        root = self.root_edit.text().strip()
        
        if ArabicUtils.is_valid_root(root):
            self.engine.roots_tree.insert(root)
            QMessageBox.information(
                self,
                "Success",
                f"✅ Root '{root}' added successfully!"
            )
            self.accept()


class SearchRootDialog(QDialog):
    """Dialog for searching roots."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("Search Root")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Search input
        search_layout = QHBoxLayout()
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Enter root to search (e.g., كتب)")
        self.search_edit.setFont(QFont("Arial", 12))
        self.search_edit.returnPressed.connect(self._search)
        search_layout.addWidget(self.search_edit)
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self._search)
        search_layout.addWidget(search_btn)
        
        layout.addLayout(search_layout)
        
        # Results display
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Arial", 11))
        layout.addWidget(self.results_text)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _search(self):
        """Search for root."""
        root = self.search_edit.text().strip()
        
        if not root:
            return
        
        if not ArabicUtils.is_valid_root(root):
            self.results_text.setText(f"❌ '{root}' is not a valid Arabic root")
            return
        
        node = self.engine.roots_tree.search(root)
        
        if node:
            # Root found
            derivatives = node.get_derivatives()
            
            result = f"✅ Root '{root}' found!\n\n"
            result += f"Frequency: {node.frequency}\n"
            result += f"Derivatives Count: {node.get_derivative_count()}\n"
            result += f"Height in Tree: {node.height}\n\n"
            
            if derivatives:
                result += f"Validated Derivatives ({len(derivatives)}):\n"
                result += "=" * 50 + "\n"
                for i, deriv in enumerate(derivatives, 1):
                    result += f"{i}. {deriv['word']} (Pattern: {deriv['pattern']}, Freq: {deriv['frequency']})\n"
            else:
                result += "No derivatives validated yet."
            
            self.results_text.setText(result)
        else:
            self.results_text.setText(f"❌ Root '{root}' not found in database")


class GenerateWordDialog(QDialog):
    """Dialog for generating words."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("Generate Arabic Word")
        self.setMinimumWidth(600)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Input form
        form_layout = QFormLayout()
        
        self.root_edit = QLineEdit()
        self.root_edit.setPlaceholderText("e.g., كتب")
        self.root_edit.setFont(QFont("Arial", 12))
        form_layout.addRow("Root:", self.root_edit)
        
        self.pattern_combo = QComboBox()
        self._load_patterns()
        form_layout.addRow("Pattern:", self.pattern_combo)
        
        layout.addLayout(form_layout)
        
        # Generate button
        generate_btn = QPushButton("Generate Word")
        generate_btn.clicked.connect(self._generate)
        layout.addWidget(generate_btn)
        
        # Results display
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Arial", 11))
        layout.addWidget(self.results_text)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _load_patterns(self):
        """Load patterns into combo box."""
        patterns = self.engine.patterns_table.get_all_patterns()
        
        for pattern_name, pattern_data in patterns:
            desc = pattern_data.get('description', '')
            display_text = f"{pattern_name} - {desc}" if desc else pattern_name
            self.pattern_combo.addItem(display_text, pattern_name)
    
    def _generate(self):
        """Generate word."""
        root = self.root_edit.text().strip()
        
        if not root:
            QMessageBox.warning(self, "Input Error", "Please enter a root")
            return
        
        if not ArabicUtils.is_valid_root(root):
            QMessageBox.warning(self, "Invalid Root", f"'{root}' is not a valid Arabic root")
            return
        
        pattern_name = self.pattern_combo.currentData()
        
        if not pattern_name:
            QMessageBox.warning(self, "Input Error", "Please select a pattern")
            return
        
        # Generate word
        result = self.engine.generate_word(root, pattern_name)
        
        if result:
            output = "✅ Word Generated Successfully!\n\n"
            output += f"Root: {result['root']}\n"
            output += f"Pattern: {result['pattern']}\n"
            output += f"Template: {result['template']}\n"
            output += f"Generated Word: {result['generated_word']}\n"
            output += f"Valid: {'✓' if result['is_valid'] else '✗'}\n\n"
            
            if result.get('description'):
                output += f"Description: {result['description']}\n"
            if result.get('example'):
                output += f"Example: {result['example']}\n"
            if result.get('rule'):
                output += f"Rule: {result['rule']}\n"
            
            self.results_text.setText(output)
        else:
            self.results_text.setText("❌ Failed to generate word")


class ValidateWordDialog(QDialog):
    """Dialog for validating words."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("Validate Arabic Word")
        self.setMinimumWidth(600)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Input
        input_layout = QFormLayout()
        
        self.word_edit = QLineEdit()
        self.word_edit.setPlaceholderText("Enter word to validate (e.g., كاتب)")
        self.word_edit.setFont(QFont("Arial", 12))
        input_layout.addRow("Word:", self.word_edit)
        
        # Optional root
        self.root_edit = QLineEdit()
        self.root_edit.setPlaceholderText("Optional: specific root to check")
        self.root_edit.setFont(QFont("Arial", 12))
        input_layout.addRow("Root (optional):", self.root_edit)
        
        layout.addLayout(input_layout)
        
        # Validate button
        validate_btn = QPushButton("Validate Word")
        validate_btn.clicked.connect(self._validate)
        layout.addWidget(validate_btn)
        
        # Results
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Arial", 11))
        layout.addWidget(self.results_text)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _validate(self):
        """Validate word."""
        word = self.word_edit.text().strip()
        root = self.root_edit.text().strip() or None
        
        if not word:
            QMessageBox.warning(self, "Input Error", "Please enter a word")
            return
        
        # Validate
        if root:
            validation = self.engine.validate_word(word, root)
        else:
            validation = self.engine.validate_word(word)
        
        # Display results
        output = "Validation Results\n"
        output += "=" * 50 + "\n\n"
        output += f"Word: {validation['word']}\n"
        output += f"Valid: {'✅ Yes' if validation['is_valid'] else '❌ No'}\n"
        output += f"Message: {validation['message']}\n\n"
        
        if validation['is_valid']:
            if 'matches' in validation:
                output += f"Matches Found: {len(validation['matches'])}\n\n"
                for i, match in enumerate(validation['matches'][:5], 1):
                    output += f"Match {i}:\n"
                    output += f"  Root: {match['root']}\n"
                    output += f"  Pattern: {match['pattern']}\n"
                    output += f"  Template: {match['template']}\n\n"
            else:
                output += f"Root: {validation.get('root', 'N/A')}\n"
                output += f"Pattern: {validation.get('pattern', 'N/A')}\n"
        else:
            if 'possible_roots' in validation:
                output += f"Possible Roots: {', '.join(validation['possible_roots'])}\n"
        
        self.results_text.setText(output)


class AnalyzeRootDialog(QDialog):
    """Dialog for analyzing root morphology."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("Analyze Root Morphology")
        self.setMinimumWidth(600)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Input
        input_layout = QHBoxLayout()
        
        self.root_edit = QLineEdit()
        self.root_edit.setPlaceholderText("Enter root to analyze (e.g., كتب)")
        self.root_edit.setFont(QFont("Arial", 12))
        self.root_edit.returnPressed.connect(self._analyze)
        input_layout.addWidget(self.root_edit)
        
        analyze_btn = QPushButton("Analyze")
        analyze_btn.clicked.connect(self._analyze)
        input_layout.addWidget(analyze_btn)
        
        layout.addLayout(input_layout)
        
        # Results
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Arial", 11))
        layout.addWidget(self.results_text)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _analyze(self):
        """Analyze root."""
        root = self.root_edit.text().strip()
        
        if not root:
            return
        
        if not ArabicUtils.is_valid_root(root):
            self.results_text.setText(f"❌ '{root}' is not a valid Arabic root")
            return
        
        # Analyze
        analysis = RootClassifier.classify(root)
        
        # Display results
        output = f"Root Analysis: {root}\n"
        output += "=" * 50 + "\n\n"
        output += f"Category: {analysis.category.value}\n"
        output += f"Subtype: {analysis.subtype or 'N/A'}\n"
        output += f"Description: {analysis.description}\n\n"
        
        if analysis.weak_positions:
            weak_str = ", ".join(str(p+1) for p in analysis.weak_positions)
            output += f"Weak Positions: {weak_str}\n"
        
        if analysis.hamza_positions:
            hamza_str = ", ".join(str(p+1) for p in analysis.hamza_positions)
            output += f"Hamza Positions: {hamza_str}\n"
        
        output += f"Is Doubled: {'Yes' if analysis.is_doubled else 'No'}\n"
        
        # Show examples
        examples = RootClassifier.get_examples()
        for category, roots_list in examples.items():
            if analysis.subtype and analysis.subtype in category:
                output += f"\nExamples of {analysis.subtype}:\n"
                output += ", ".join(roots_list)
                break
        
        self.results_text.setText(output)


class PatternManagementDialog(QDialog):
    """Dialog for managing patterns."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("Pattern Management")
        self.setMinimumSize(800, 600)
        
        self._setup_ui()
        self._load_patterns()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Patterns table
        self.patterns_table = QTableWidget()
        self.patterns_table.setColumnCount(4)
        self.patterns_table.setHorizontalHeaderLabels([
            "Name", "Template", "Description", "Example"
        ])
        self.patterns_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.patterns_table)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Pattern")
        add_btn.clicked.connect(self._add_pattern)
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(self._edit_pattern)
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self._delete_pattern)
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def _load_patterns(self):
        """Load patterns into table."""
        patterns = self.engine.patterns_table.get_all_patterns()
        
        self.patterns_table.setRowCount(len(patterns))
        
        for row, (name, data) in enumerate(patterns):
            self.patterns_table.setItem(row, 0, QTableWidgetItem(name))
            self.patterns_table.setItem(row, 1, QTableWidgetItem(data.get('template', '')))
            self.patterns_table.setItem(row, 2, QTableWidgetItem(data.get('description', '')))
            self.patterns_table.setItem(row, 3, QTableWidgetItem(data.get('example', '')))
    
    def _add_pattern(self):
        """Add new pattern."""
        # TODO: Implement add pattern dialog
        QMessageBox.information(self, "Info", "Add pattern dialog - to be implemented")
    
    def _edit_pattern(self):
        """Edit selected pattern."""
        # TODO: Implement edit pattern dialog
        QMessageBox.information(self, "Info", "Edit pattern dialog - to be implemented")
    
    def _delete_pattern(self):
        """Delete selected pattern."""
        current_row = self.patterns_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a pattern to delete")
            return
        
        pattern_name = self.patterns_table.item(current_row, 0).text()
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete pattern '{pattern_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.engine.delete_pattern(pattern_name)
            if success:
                self._load_patterns()
                QMessageBox.information(self, "Success", message)
            else:
                QMessageBox.critical(self, "Error", message)


class StatisticsDialog(QDialog):
    """Dialog for displaying statistics."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("Engine Statistics")
        self.setMinimumSize(600, 400)
        
        self._setup_ui()
        self._load_statistics()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setFont(QFont("Courier New", 10))
        layout.addWidget(self.stats_text)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _load_statistics(self):
        """Load and display statistics."""
        stats = self.engine.get_engine_statistics()
        
        output = "Arabic Morphological Engine Statistics\n"
        output += "=" * 60 + "\n\n"
        
        output += f"Roots Count:              {stats['roots_count']}\n"
        output += f"Patterns Count:           {stats['patterns_count']}\n"
        output += f"Generated Words:          {stats['generated_words_count']}\n"
        output += f"Unique Roots (generated): {stats['unique_roots_with_generated']}\n"
        output += f"AVL Tree Height:          {stats['avl_tree_height']}\n"
        output += f"Hash Table Load Factor:   {stats['hash_table_load_factor']:.2f}\n\n"
        
        output += "AVL Tree Information:\n"
        output += "-" * 60 + "\n"
        output += "  • Search complexity: O(log n)\n"
        output += "  • Self-balancing: Yes\n"
        output += "  • Operations: Insert, Search, Delete in O(log n)\n\n"
        
        output += "Hash Table Information:\n"
        output += "-" * 60 + "\n"
        output += "  • Average search: O(1)\n"
        output += "  • Collision resolution: Separate chaining\n"
        output += "  • Dynamic resizing: When load factor > 0.75\n"
        
        self.stats_text.setText(output)


class TreeVisualizationDialog(QDialog):
    """Dialog for visualizing AVL tree."""
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("AVL Tree Visualization")
        self.setMinimumSize(800, 600)
        
        self._setup_ui()
        self._load_tree()
    
    def _setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        
        # Tabs for different views
        tabs = QTabWidget()
        
        # ASCII view
        self.ascii_text = QTextEdit()
        self.ascii_text.setReadOnly(True)
        self.ascii_text.setFont(QFont("Courier New", 9))
        tabs.addTab(self.ascii_text, "ASCII View")
        
        # Inorder view
        self.inorder_text = QTextEdit()
        self.inorder_text.setReadOnly(True)
        self.inorder_text.setFont(QFont("Arial", 11))
        tabs.addTab(self.inorder_text, "Inorder Traversal")
        
        layout.addWidget(tabs)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _load_tree(self):
        """Load tree visualization."""
        # ASCII view
        ascii_tree = self.engine.roots_tree.display_tree_ascii()
        if ascii_tree:
            self.ascii_text.setText(ascii_tree)
        else:
            self.ascii_text.setText("Tree is empty")
        
        # Inorder view
        roots = self.engine.roots_tree.display_inorder()
        if roots:
            inorder_text = "Roots in sorted order:\n\n"
            inorder_text += ", ".join(roots)
            inorder_text += f"\n\nTotal: {len(roots)} roots"
            self.inorder_text.setText(inorder_text)
        else:
            self.inorder_text.setText("Tree is empty")