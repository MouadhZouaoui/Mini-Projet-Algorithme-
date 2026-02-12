"""
Enhanced Main Window – Complete Integration
Includes all tabs, menus, and dialogs.
"""
import json
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton,
    QMessageBox, QFileDialog, QStatusBar, QApplication
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QShortcut, QKeySequence

# Import custom widgets
from .enhanced_widgets import EnhancedGenerationWidget, EnhancedValidationWidget
from .enhanced_roots_patterns import EnhancedRootsWidget, EnhancedPatternsWidget, EnhancedDashboardWidget
from .derivatives_widget import DerivativesWidget
from .charts_widget import StatisticsChartsWidget
from .tree_dialog import TreeOperationsDialog
from .hash_dialog import HashTableInfoDialog
from .pattern_validation_dialog import PatternValidationDialog
from .gui_styles import AppStyles
from .splash_screen import SplashScreen


class EnhancedMainWindow(QMainWindow):
    """Main application window with all integrated features."""

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.data_loaded = False
        self._setup_ui()
        self._create_menu_bar()
        self._create_status_bar()
        self._connect_signals()
        self._setup_shortcuts()

        # Try auto-load data after window is shown
        QTimer.singleShot(100, self._try_auto_load_data)

    def _setup_ui(self):
        """Setup central widget and tabs."""
        self.setWindowTitle("🌙 محرك البحث المورفولوجي للغة العربية")
        self.setMinimumSize(1300, 850)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        # Create all tabs
        self.dashboard_widget = EnhancedDashboardWidget(self.engine)
        self.generation_widget = EnhancedGenerationWidget(self.engine)
        self.validation_widget = EnhancedValidationWidget(self.engine)
        self.roots_widget = EnhancedRootsWidget(self.engine)
        self.patterns_widget = EnhancedPatternsWidget(self.engine)
        self.derivatives_widget = DerivativesWidget(self.engine)
        self.charts_widget = StatisticsChartsWidget(self.engine)

        # Add tabs in logical order
        self.tabs.addTab(self.dashboard_widget, "📊 لوحة التحكم")
        self.tabs.addTab(self.roots_widget, "🌱 الجذور")
        self.tabs.addTab(self.patterns_widget, "🏗️ الأوزان")
        self.tabs.addTab(self.generation_widget, "✨ توليد الكلمات")
        self.tabs.addTab(self.validation_widget, "✅ التحقق")
        self.tabs.addTab(self.derivatives_widget, "📚 المشتقات")
        self.tabs.addTab(self.charts_widget, "📈 إحصائيات مرئية")

        main_layout.addWidget(self.tabs)

    def _create_menu_bar(self):
        """Create menu bar with all actions."""
        menubar = self.menuBar()
        menubar.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        # ----- File Menu -----
        file_menu = menubar.addMenu("ملف")

        load_action = QAction("📥 تحميل البيانات", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_data_dialog)
        file_menu.addAction(load_action)

        reload_action = QAction("🔄 إعادة تحميل", self)
        reload_action.setShortcut("Ctrl+R")
        reload_action.triggered.connect(self.reload_data)
        file_menu.addAction(reload_action)

        file_menu.addSeparator()

        export_action = QAction("💾 تصدير النتائج", self)
        export_action.setShortcut("Ctrl+S")
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("🚪 خروج", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # ----- Tools Menu -----
        tools_menu = menubar.addMenu("🔧 أدوات")

        tree_action = QAction("🌳 عمليات الشجرة", self)
        tree_action.triggered.connect(self.show_tree_dialog)
        tools_menu.addAction(tree_action)

        hash_action = QAction("⚡ معلومات جدول التجزئة", self)
        hash_action.triggered.connect(self.show_hash_dialog)
        tools_menu.addAction(hash_action)

        tools_menu.addSeparator()

        validate_pattern_action = QAction("✅ التحقق من قالب الوزن", self)
        validate_pattern_action.triggered.connect(self.show_pattern_validation_dialog)
        tools_menu.addAction(validate_pattern_action)

        # ----- View Menu -----
        view_menu = menubar.addMenu("عرض")

        self.stats_action = QAction("📊 لوحة التحكم", self)
        self.stats_action.triggered.connect(lambda: self.tabs.setCurrentWidget(self.dashboard_widget))
        view_menu.addAction(self.stats_action)

        # ----- Help Menu -----
        help_menu = menubar.addMenu("مساعدة")

        about_action = QAction("ℹ️ حول", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def _create_status_bar(self):
        """Create status bar with initial message."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("جاهز", 5000)

    def _connect_signals(self):
        """Connect signals between widgets."""
        try:
            # Tab change
            self.tabs.currentChanged.connect(self._on_tab_changed)

            # Data change signals
            self.roots_widget.root_added.connect(self._on_data_changed)
            self.patterns_widget.pattern_added.connect(self._on_data_changed)
            self.patterns_widget.pattern_modified.connect(self._on_data_changed)

            # Generation
            self.generation_widget.generation_completed.connect(self._on_generation_completed)

            # Derivatives
            self.derivatives_widget.derivative_removed.connect(self._on_derivative_removed)
            self.derivatives_widget.derivatives_cleared.connect(self._on_derivatives_cleared)

        except Exception as e:
            print(f"Signal connection error: {e}")

    def _setup_shortcuts(self):
        """Setup global keyboard shortcuts."""
        # Switch tabs
        QShortcut(QKeySequence("Ctrl+1"), self, lambda: self.tabs.setCurrentIndex(0))
        QShortcut(QKeySequence("Ctrl+2"), self, lambda: self.tabs.setCurrentIndex(1))
        QShortcut(QKeySequence("Ctrl+3"), self, lambda: self.tabs.setCurrentIndex(2))
        QShortcut(QKeySequence("Ctrl+4"), self, lambda: self.tabs.setCurrentIndex(3))
        QShortcut(QKeySequence("Ctrl+5"), self, lambda: self.tabs.setCurrentIndex(4))
        QShortcut(QKeySequence("Ctrl+6"), self, lambda: self.tabs.setCurrentIndex(5))
        QShortcut(QKeySequence("Ctrl+7"), self, lambda: self.tabs.setCurrentIndex(6))

        # Quick actions
        QShortcut(QKeySequence("Ctrl+N"), self, lambda: self.tabs.setCurrentWidget(self.roots_widget))
        QShortcut(QKeySequence("Ctrl+G"), self, lambda: self.tabs.setCurrentWidget(self.generation_widget))
        QShortcut(QKeySequence("Ctrl+V"), self, lambda: self.tabs.setCurrentWidget(self.validation_widget))

    # ---------- Data Loading ----------
    def _try_auto_load_data(self):
        """Try to auto-load data from default paths."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
            data_dir = os.path.join(project_root, "data")
            roots_path = os.path.join(data_dir, "roots.txt")
            patterns_path = os.path.join(data_dir, "patterns.json")

            if os.path.exists(roots_path) and os.path.exists(patterns_path):
                self._load_data_from_files(roots_path, patterns_path, silent=True)
            else:
                self.status_bar.showMessage("البيانات غير موجودة – يرجى تحميلها يدوياً", 5000)
        except Exception as e:
            print(f"Auto-load error: {e}")

    def load_data_dialog(self):
        """Open file dialog to load roots and patterns."""
        try:
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialogButtonBox

            dialog = QDialog(self)
            dialog.setWindowTitle("تحميل البيانات")
            dialog.setMinimumWidth(600)

            layout = QVBoxLayout(dialog)

            # Roots file
            roots_layout = QHBoxLayout()
            roots_label = QLabel("ملف الجذور:")
            roots_label.setFixedWidth(100)
            roots_input = QLineEdit()
            roots_input.setReadOnly(True)
            roots_browse = QPushButton("استعراض")

            def browse_roots():
                file, _ = QFileDialog.getOpenFileName(dialog, "اختر ملف الجذور", "", "Text Files (*.txt)")
                if file:
                    roots_input.setText(file)

            roots_browse.clicked.connect(browse_roots)
            roots_layout.addWidget(roots_label)
            roots_layout.addWidget(roots_input)
            roots_layout.addWidget(roots_browse)

            # Patterns file
            patterns_layout = QHBoxLayout()
            patterns_label = QLabel("ملف الأوزان:")
            patterns_label.setFixedWidth(100)
            patterns_input = QLineEdit()
            patterns_input.setReadOnly(True)
            patterns_browse = QPushButton("استعراض")

            def browse_patterns():
                file, _ = QFileDialog.getOpenFileName(dialog, "اختر ملف الأوزان", "", "JSON Files (*.json)")
                if file:
                    patterns_input.setText(file)

            patterns_browse.clicked.connect(browse_patterns)
            patterns_layout.addWidget(patterns_label)
            patterns_layout.addWidget(patterns_input)
            patterns_layout.addWidget(patterns_browse)

            layout.addLayout(roots_layout)
            layout.addLayout(patterns_layout)

            # Buttons
            buttons = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok |
                QDialogButtonBox.StandardButton.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                roots_path = roots_input.text()
                patterns_path = patterns_input.text()
                if roots_path and patterns_path:
                    self._load_data_from_files(roots_path, patterns_path)
                else:
                    QMessageBox.warning(self, "تحذير", "يرجى اختيار كلا الملفين")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ: {str(e)}")

    def _load_data_from_files(self, roots_path, patterns_path, silent=False):
        """Internal method to load data and refresh UI."""
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
            self._refresh_all_widgets()

            if not silent:
                stats = self.engine.get_engine_statistics()
                msg = f"✅ تم تحميل البيانات بنجاح!\n\n"
                msg += f"الجذور: {stats['roots_count']}\n"
                msg += f"الأوزان: {stats['patterns_count']}"
                QMessageBox.information(self, "نجاح", msg)

            self.status_bar.showMessage(
                f"تم التحميل: {self.engine.roots_tree.count_nodes()} جذر، "
                f"{len(self.engine.patterns_table)} وزن", 5000
            )

        except Exception as e:
            if not silent:
                QMessageBox.critical(self, "خطأ", f"فشل تحميل البيانات: {e}")

    def reload_data(self):
        """Reload data from last used paths or auto-load."""
        if not self.data_loaded:
            self.load_data_dialog()
        else:
            self._try_auto_load_data()

    # ---------- Export ----------
    def export_results(self):
        """Export generated words to file."""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "تصدير النتائج",
                "",
                "JSON Files (*.json);;CSV Files (*.csv);;Text Files (*.txt)"
            )
            if not file_path:
                return

            if file_path.endswith('.json'):
                export_format = 'json'
            elif file_path.endswith('.csv'):
                export_format = 'csv'
            else:
                export_format = 'text'

            export_data = self.engine.export_results(export_format)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(export_data)

            QMessageBox.information(self, "نجاح", f"تم التصدير إلى:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل التصدير: {e}")

    # ---------- Dialogs ----------
    def show_tree_dialog(self):
        dialog = TreeOperationsDialog(self.engine, self)
        dialog.exec()

    def show_hash_dialog(self):
        dialog = HashTableInfoDialog(self.engine, self)
        dialog.exec()

    def show_pattern_validation_dialog(self):
        dialog = PatternValidationDialog(self.engine, self)
        dialog.exec()

    def show_about(self):
        about_text = """
        <div style='direction: rtl; text-align: center;'>
            <h2 style='color: #6B5B95;'>🌙 محرك البحث المورفولوجي</h2>
            <p><b>الإصدار:</b> 2.0</p>
            <p><b>المطورون:</b> Zouaoui Mouadh, Ayari Yosr, Khadhraoui Malak</p>
            <p><b>جامعة:</b> [اسم الجامعة]</p>
            <hr>
            <p style='font-size: 11pt;'>هيكل بيانات متقدم للتعامل مع الجذور العربية<br>
            شجرة AVL للجذور – جدول تجزئة للأوزان</p>
        </div>
        """
        QMessageBox.about(self, "حول", about_text)

    # ---------- Signal Handlers ----------
    def _on_tab_changed(self, index):
        """Refresh widget when its tab becomes visible."""
        widget = self.tabs.widget(index)
        if hasattr(widget, 'refresh'):
            widget.refresh()

    def _on_data_changed(self):
        """Refresh all widgets that display data."""
        self._refresh_all_widgets()

    def _on_generation_completed(self, result):
        """Show generation feedback in status bar."""
        word = result.get('generated_word', result.get('word', ''))
        self.status_bar.showMessage(f"✅ تم توليد: {word}", 3000)

    def _on_derivative_removed(self, root, word):
        self.status_bar.showMessage(f"🗑️ تم حذف '{word}' من الجذر '{root}'", 3000)

    def _on_derivatives_cleared(self, root):
        self.status_bar.showMessage(f"🧹 تم حذف جميع مشتقات '{root}'", 3000)

    def _refresh_all_widgets(self):
        """Refresh all tabs that have a refresh method."""
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if hasattr(widget, 'refresh'):
                try:
                    widget.refresh()
                except Exception as e:
                    print(f"Refresh error in {widget.__class__.__name__}: {e}")

    # ---------- Close Event ----------
    def closeEvent(self, event):
        """Confirm exit."""
        reply = QMessageBox.question(
            self,
            "تأكيد الخروج",
            "هل أنت متأكد من الخروج؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


# ---------- Application Entry Point ----------
def run_gui_app(engine):
    """Run the GUI application with splash screen."""
    import sys
    app = QApplication(sys.argv)

    # Apply global styling
    AppStyles.apply_app_style(app)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    # Show splash screen
    splash = SplashScreen()
    splash.show()
    splash.updateProgress(10)
    app.processEvents()

    # Simulate loading (or real loading if needed)
    splash.updateProgress(40)
    app.processEvents()

    # Create main window
    window = EnhancedMainWindow(engine)
    splash.updateProgress(80)
    app.processEvents()

    window.show()
    splash.updateProgress(100)
    app.processEvents()
    splash.finish(window)

    sys.exit(app.exec())