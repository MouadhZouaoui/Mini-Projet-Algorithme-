"""
Tree Operations Dialog
Displays tree statistics, inorder list, and visual representation.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QWidget
)
from PyQt6.QtCore import Qt

from .tree_visualizer import AVLTreeVisualizer


class TreeOperationsDialog(QDialog):
    """Dialog for exploring AVL tree structure and statistics."""

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("🌳 عمليات شجرة AVL")
        self.setMinimumSize(900, 650)
        # FIX: Use Qt.WindowType.WindowContextHelpButtonHint
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Tabs
        tabs = QTabWidget()
        tabs.setDocumentMode(True)

        # ----- Tab 1: Statistics & Inorder List -----
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)

        stats = self.engine.get_engine_statistics()
        tree_height = stats.get('avl_tree_height', 0)
        node_count = stats.get('roots_count', 0)

        # Info display
        info_text = f"""
        <div style='direction: rtl; font-size: 12pt;'>
            <h3 style='color: #6B5B95;'>📊 إحصائيات الشجرة</h3>
            <table style='width: 100%; border-collapse: collapse;'>
                <tr><td style='padding: 8px;'><b>عدد العقد:</b></td>
                    <td style='padding: 8px;'>{node_count}</td></tr>
                <tr><td style='padding: 8px;'><b>ارتفاع الشجرة:</b></td>
                    <td style='padding: 8px;'>{tree_height}</td></tr>
                <tr><td style='padding: 8px;'><b>عدد المشتقات:</b></td>
                    <td style='padding: 8px;'>{stats.get('generated_words_count', 0)}</td></tr>
                <tr><td style='padding: 8px;'><b>الجذور الفريدة مع مشتقات:</b></td>
                    <td style='padding: 8px;'>{stats.get('unique_roots_with_generated', 0)}</td></tr>
            </table>
        """

        # Inorder list
        roots = self.engine.roots_tree.display_inorder()
        if roots:
            info_text += "<h3 style='color: #6B5B95; margin-top: 20px;'>📋 قائمة الجذور (ترتيب تصاعدي)</h3>"
            info_text += "<p style='font-family: monospace; font-size: 11pt; line-height: 1.6;'>"
            info_text += " – ".join(roots)
            info_text += "</p>"
        else:
            info_text += "<p><i>الشجرة فارغة</i></p>"

        info_text += "</div>"

        info_label = QLabel(info_text)
        info_label.setTextFormat(Qt.TextFormat.RichText)
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        info_label.setStyleSheet("background-color: #F5EFE6; border-radius: 8px; padding: 15px;")

        stats_layout.addWidget(info_label)
        stats_layout.addStretch()

        # ----- Tab 2: Tree Visualizer -----
        visual_tab = QWidget()
        visual_layout = QVBoxLayout(visual_tab)

        self.visualizer = AVLTreeVisualizer(self.engine.roots_tree)
        visual_layout.addWidget(self.visualizer)

        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 تحديث الرسم")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.clicked.connect(self.visualizer.refresh)
        btn_layout.addStretch()
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        visual_layout.addLayout(btn_layout)

        tabs.addTab(stats_tab, "📊 إحصائيات وقائمة")
        tabs.addTab(visual_tab, "🎨 تصور الشجرة")

        layout.addWidget(tabs)

        # ----- Close Button -----
        close_btn = QPushButton("إغلاق")
        close_btn.setMinimumHeight(45)
        close_btn.setFixedWidth(150)
        close_btn.clicked.connect(self.accept)
        btn_holder = QHBoxLayout()
        btn_holder.addStretch()
        btn_holder.addWidget(close_btn)
        btn_holder.addStretch()
        layout.addLayout(btn_holder)

        self.setLayout(layout)