"""
Hash Table Information Dialog
Displays statistics and list of all patterns with their templates.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt


class HashTableInfoDialog(QDialog):
    """Dialog showing hash table performance and pattern list."""

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("⚡ معلومات جدول التجزئة")
        self.setMinimumSize(700, 550)
        # FIX: Use Qt.WindowType.WindowContextHelpButtonHint
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # ----- Title -----
        title = QLabel("⚡ جدول التجزئة – الأوزان الصرفية")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #6B5B95;")
        layout.addWidget(title)

        # ----- Statistics -----
        stats = self.engine.patterns_table.display_stats()
        stats_text = f"""
        <div style='direction: rtl; font-size: 12pt; background-color: #F5EFE6; 
                    border-radius: 8px; padding: 15px;'>
            <table style='width: 100%;'>
                <tr><td><b>عدد الأوزان:</b></td><td>{stats.get('total_items', 0)}</td></tr>
                <tr><td><b>حجم الجدول:</b></td><td>{stats.get('table_size', 0)}</td></tr>
                <tr><td><b>عامل الحمولة:</b></td><td>{stats.get('load_factor', 0):.3f}</td></tr>
                <tr><td><b>عدد التصادمات:</b></td><td>{stats.get('collisions', 0)}</td></tr>
                <tr><td><b>المفاتيح الفارغة:</b></td><td>{stats.get('empty_slots', 0)}</td></tr>
            </table>
        </div>
        """
        stats_label = QLabel(stats_text)
        stats_label.setTextFormat(Qt.TextFormat.RichText)
        stats_label.setWordWrap(True)
        layout.addWidget(stats_label)

        # ----- Pattern Table -----
        table_label = QLabel("📋 قائمة الأوزان المخزنة:")
        table_label.setStyleSheet("font-size: 13pt; font-weight: bold; color: #2C2416; margin-top: 10px;")
        layout.addWidget(table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["الوزن", "القالب"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("border: 2px solid #C5B5A0; border-radius: 8px;")

        patterns = self.engine.patterns_table.get_all_patterns()
        self.table.setRowCount(len(patterns))
        for i, (name, data) in enumerate(patterns):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(data.get('template', '')))

        layout.addWidget(self.table)

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