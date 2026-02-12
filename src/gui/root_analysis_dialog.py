"""
Root Analysis Dialog
Displays detailed morphological classification with examples.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from root_classifier import RootClassifier


class RootAnalysisDialog(QDialog):
    """Dialog showing complete morphological analysis of an Arabic root."""

    def __init__(self, analysis, parent=None):
        super().__init__(parent)
        self.analysis = analysis
        self.setWindowTitle(f"🔬 تحليل الجذر: {analysis.root}")
        self.setMinimumSize(650, 550)
        # FIX: Use Qt.WindowType.WindowContextHelpButtonHint
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # ----- Title -----
        title = QLabel(f"🔬 تحليل الجذر: {self.analysis.root}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20pt; font-weight: bold; color: #6B5B95; padding: 10px;")
        layout.addWidget(title)

        # ----- Analysis Table -----
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["الخاصية", "القيمة"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget { border: 2px solid #C5B5A0; border-radius: 8px; }
            QTableWidget::item { padding: 8px; }
        """)

        # Prepare data
        data = [
            ("الفئة", self.analysis.category.value),
            ("النوع الفرعي", self.analysis.subtype or "—"),
            ("الوصف", self.analysis.description),
            ("مواضع حروف العلة", 
             ", ".join(str(p+1) for p in self.analysis.weak_positions) or "لا يوجد"),
            ("مواضع الهمزة", 
             ", ".join(str(p+1) for p in self.analysis.hamza_positions) or "لا يوجد"),
            ("مضعف", "نعم" if self.analysis.is_doubled else "لا"),
        ]

        table.setRowCount(len(data))
        for i, (key, val) in enumerate(data):
            table.setItem(i, 0, QTableWidgetItem(key))
            item = QTableWidgetItem(str(val))
            item.setToolTip(str(val))
            table.setItem(i, 1, item)

        layout.addWidget(table)

        # ----- Example Roots -----
        examples = RootClassifier.get_examples()
        example_text = ""
        if self.analysis.subtype:
            for cat, roots in examples.items():
                if self.analysis.subtype in cat:
                    example_text = "📚 أمثلة: " + "، ".join(roots[:5])
                    break
        if not example_text and self.analysis.category:
            # Fallback: show examples of the main category
            for cat, roots in examples.items():
                if self.analysis.category.value in cat:
                    example_text = "📚 أمثلة: " + "، ".join(roots[:5])
                    break

        if example_text:
            example_label = QLabel(example_text)
            example_label.setWordWrap(True)
            example_label.setStyleSheet("font-size: 12pt; color: #5A4E3A; padding: 10px;")
            example_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.addWidget(example_label)

        # ----- Close Button -----
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("إغلاق")
        close_btn.setMinimumHeight(45)
        close_btn.setFixedWidth(150)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)