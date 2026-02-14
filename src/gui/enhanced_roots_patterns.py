"""
Enhanced Roots and Patterns Widgets – FINAL FIXED VERSION
All layout issues resolved:
- Scroll area container has Preferred vertical policy to allow scroll bars
- Input fields expand horizontally
- Roots list takes all remaining vertical space
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QDialogButtonBox, QScrollArea,
    QFileDialog, QGridLayout, QSizePolicy, QTextEdit, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal

from arabic_utils import ArabicUtils
from root_classifier import RootClassifier
from .root_analysis_dialog import RootAnalysisDialog
from .enhanced_widgets import CardWidget


# ============================================================================
# DASHBOARD WIDGET (unchanged)
# ============================================================================
class EnhancedDashboardWidget(QWidget):
    """Enhanced dashboard widget with statistics cards."""

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._setup_ui()

    def _setup_ui(self):
        # Scrollable container
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("🌙 محرك البحث المورفولوجي")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 18pt; font-weight: bold; color: #2C2416;
            padding: 10px; margin-bottom: 5px;
        """)
        title.setMinimumHeight(50)
        main_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("استكشف الجذور العربية وأوزانها الصرفية")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 11pt; color: #5A4E3A; font-style: italic;
            padding: 5px;
        """)
        subtitle.setWordWrap(True)
        subtitle.setMinimumHeight(30)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(10)

        # Stats grid
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)

        stats = self.engine.get_engine_statistics()

        self.roots_card = self._create_stat_card("🌱", "الجذور", str(stats['roots_count']))
        self.patterns_card = self._create_stat_card("📐", "الأوزان", str(stats['patterns_count']))
        self.derivatives_card = self._create_stat_card("📝", "المشتقات", str(stats['generated_words_count']))
        self.tree_card = self._create_stat_card("🌳", "ارتفاع الشجرة", str(stats['avl_tree_height']))

        stats_layout.addWidget(self.roots_card, 0, 0)
        stats_layout.addWidget(self.patterns_card, 0, 1)
        stats_layout.addWidget(self.derivatives_card, 1, 0)
        stats_layout.addWidget(self.tree_card, 1, 1)

        main_layout.addLayout(stats_layout)

        # Info card
        info_card = CardWidget("معلومات النظام")
        info_text = """
        <div style='direction: rtl; font-size: 13pt;'>
            <h3 style='color: #6B5B95;'>المميزات:</h3>
            <ul>
                <li>🌳 <b>شجرة AVL للجذور:</b> O(log n)</li>
                <li>⚡ <b>جدول التجزئة للأوزان:</b> O(1)</li>
                <li>🔄 <b>توليد الكلمات</b> مع مراعاة أنواع الجذور</li>
                <li>✅ <b>التحقق المورفولوجي</b> مع دعم المشتقات المتعددة</li>
                <li>📚 <b>إدارة المشتقات</b> (عرض، حذف)</li>
                <li>📊 <b>إحصائيات مرئية</b> ورسوم بيانية</li>
            </ul>
        </div>
        """
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setMinimumHeight(150)
        info_card.add_widget(info_label)

        main_layout.addWidget(info_card)
        main_layout.addStretch()

        scroll.setWidget(container)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(scroll)

    def _create_stat_card(self, icon, label, value):
        """Create a statistic card."""
        card = CardWidget()
        card.setMinimumHeight(100)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 36pt;")

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #2C2416;")

        text_label = QLabel(label)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #5A4E3A;")

        card.card_layout.addWidget(icon_label)
        card.card_layout.addWidget(value_label)
        card.card_layout.addWidget(text_label)

        return card

    def refresh(self):
        """Refresh dashboard statistics."""
        try:
            stats = self.engine.get_engine_statistics()
            self.roots_card.card_layout.itemAt(1).widget().setText(str(stats['roots_count']))
            self.patterns_card.card_layout.itemAt(1).widget().setText(str(stats['patterns_count']))
            self.derivatives_card.card_layout.itemAt(1).widget().setText(str(stats['generated_words_count']))
            self.tree_card.card_layout.itemAt(1).widget().setText(str(stats['avl_tree_height']))
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")


# ============================================================================
# ROOTS WIDGET – FINAL FIXED LAYOUT
# ============================================================================
class EnhancedRootsWidget(QWidget):
    """Roots management with correct expanding layout."""
    root_added = pyqtSignal(str)
    root_selected = pyqtSignal(str)

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._setup_ui()

    def _setup_ui(self):
        # Outer scroll area – expands to fill tab
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Container widget – expand horizontally only, allow vertical to exceed viewport
        container = QWidget()
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Main layout for container
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("📚 إدارة الجذور")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #2C2416; padding: 10px;")
        title.setMinimumHeight(50)
        main_layout.addWidget(title)

        # ---------- ADD ROOT CARD ----------
        add_card = CardWidget("إضافة جذر جديد")
        input_layout = QHBoxLayout()
        input_label = QLabel("الجذر:")
        input_label.setFixedWidth(60)
        input_label.setStyleSheet("background: transparent; border: none; font-size: 13pt; padding: 5px;")
        input_label.setMinimumHeight(45)
        input_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.root_input = QLineEdit()
        self.root_input.setPlaceholderText("مثال: درس")
        self.root_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.root_input.setMinimumHeight(50)
        self.root_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.root_input.returnPressed.connect(self._add_root)
        self.root_input.setToolTip("أدخل جذراً ثلاثياً. سيتم توسعة الشدة تلقائياً.")

        add_btn = QPushButton("إضافة")
        add_btn.setMaximumWidth(100)
        add_btn.setMinimumHeight(50)
        add_btn.clicked.connect(self._add_root)

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.root_input, 1)  # stretch
        input_layout.addWidget(add_btn)

        input_widget = QWidget()
        input_widget.setLayout(input_layout)
        add_card.add_widget(input_widget)
        main_layout.addWidget(add_card)

        # ---------- SEARCH & ANALYZE CARD ----------
        search_card = CardWidget("البحث والتحليل")
        search_layout = QHBoxLayout()
        search_label = QLabel("ابحث / حلل:")
        search_label.setFixedWidth(100)
        search_label.setStyleSheet("background: transparent; border: none; font-size: 13pt; padding: 5px;")
        search_label.setMinimumHeight(45)
        search_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث عن جذر...")
        self.search_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.search_input.setMinimumHeight(50)
        self.search_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.search_input.returnPressed.connect(self._search_root)

        search_btn = QPushButton("بحث")
        search_btn.setMaximumWidth(80)
        search_btn.setMinimumHeight(50)
        search_btn.clicked.connect(self._search_root)

        analyze_btn = QPushButton("🔬 تحليل")
        analyze_btn.setMaximumWidth(80)
        analyze_btn.setMinimumHeight(50)
        analyze_btn.clicked.connect(self._analyze_root)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(analyze_btn)

        search_widget = QWidget()
        search_widget.setLayout(search_layout)
        search_card.add_widget(search_widget)
        main_layout.addWidget(search_card)

        # ---------- ROOTS LIST CARD – MUST EXPAND ----------
        roots_card = CardWidget("الجذور المخزنة")
        roots_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Stats label
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 11pt; color: #5A4E3A; font-style: italic;")
        self.stats_label.setMinimumHeight(25)
        roots_card.add_widget(self.stats_label)

        # Roots list
        self.roots_list = QListWidget()
        self.roots_list.setMinimumHeight(150)  # small minimum, will expand
        self.roots_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.roots_list.itemClicked.connect(self._on_root_selected)
        self.roots_list.setToolTip("انقر على أي جذر لاستعراض معلوماته")
        roots_card.add_widget(self.roots_list)

        # Critical: list takes all extra space inside the card
        roots_card.card_layout.setStretchFactor(self.roots_list, 1)

        # Add roots card with stretch factor 1 – takes remaining vertical space
        main_layout.addWidget(roots_card, 1)

        # NO stretch at the end – roots_card will expand

        scroll.setWidget(container)

        # Main layout for this widget (just the scroll area)
        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(scroll)

        self.refresh()

    # ---------- NORMALIZATION HELPER ----------
    def _normalize_root(self, root):
        return ArabicUtils.normalize_arabic(root, expand_shadda=True)

    # ---------- ADD ROOT ----------
    def _add_root(self):
        root = self.root_input.text().strip()
        if not root:
            QMessageBox.warning(self, "تحذير", "يرجى إدخال الجذر")
            return
        if not ArabicUtils.is_valid_root(root):
            QMessageBox.warning(self, "تحذير", f"'{root}' ليس جذراً صالحاً (يجب 3 أحرف)")
            return
        normalized = self._normalize_root(root)
        if self.engine.root_exists(normalized):
            node = self.engine.roots_tree.search(normalized)
            stored = node.root if node else normalized
            QMessageBox.information(
                self, "تنبيه",
                f"الجذر '{root}' (بصيغته الطبيعية: {stored}) موجود بالفعل"
            )
            return
        self.engine.roots_tree.insert(root)
        QMessageBox.information(self, "نجاح", f"✅ تم إضافة الجذر '{root}'")
        self.root_input.clear()
        self.refresh()
        self.root_added.emit(root)

    # ---------- SEARCH ROOT ----------
    def _search_root(self):
        """Search for a root and show detailed information in a custom dialog."""
        root = self.search_input.text().strip()
        if not root:
            QMessageBox.warning(self, "تحذير", "يرجى إدخال الجذر للبحث")
            return

        normalized = self._normalize_root(root)
        node = self.engine.roots_tree.search(normalized)

        if node:
            # Build rich text info
            info = f"<h2 style='color: #6B5B95;'>✅ الجذر: {node.root}</h2>"
            info += f"<p><b>📊 التكرار:</b> {node.frequency}</p>"
            info += f"<p><b>📚 عدد المشتقات:</b> {node.get_derivative_count()}</p>"
            info += f"<p><b>📏 الارتفاع في الشجرة:</b> {node.height}</p>"

            derivatives = node.get_derivatives()
            if derivatives:
                info += "<h3 style='color: #2C2416;'>📝 المشتقات:</h3><ul>"
                for deriv in derivatives[:10]:  # Show first 10
                    info += f"<li><b>{deriv['word']}</b> (الوزن: {deriv['pattern']}, التكرار: {deriv['frequency']})</li>"
                if len(derivatives) > 10:
                    info += f"<li>... و {len(derivatives)-10} مشتق آخر</li>"
                info += "</ul>"
            else:
                info += "<p><i>لا توجد مشتقات لهذا الجذر بعد.</i></p>"

            # Create custom dialog
            dialog = QDialog(self)
            dialog.setWindowTitle(f"معلومات الجذر: {root}")
            dialog.setMinimumSize(600, 400)
            dialog.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

            layout = QVBoxLayout(dialog)

            # Text edit for rich text
            text_edit = QTextEdit()
            text_edit.setHtml(info)
            text_edit.setReadOnly(True)
            text_edit.setStyleSheet("""
                QTextEdit {
                    background-color: #F5EFE6;
                    border: 2px solid #C5B5A0;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 12pt;
                }
            """)
            layout.addWidget(text_edit)

            # Close button
            close_btn = QPushButton("إغلاق")
            close_btn.setMinimumHeight(40)
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)

            dialog.exec()
        else:
            QMessageBox.warning(self, "غير موجود", f"الجذر '{root}' غير موجود في الشجرة")

    # ---------- ANALYZE ROOT ----------
    def _analyze_root(self):
        root = self.search_input.text().strip() or self.root_input.text().strip()
        if not root:
            QMessageBox.warning(self, "تنبيه", "أدخل جذراً للتحليل")
            return
        normalized = self._normalize_root(root)
        analysis = RootClassifier.classify(normalized)
        dialog = RootAnalysisDialog(analysis, self)
        dialog.exec()

    # ---------- ROOT SELECTION ----------
    def _on_root_selected(self, item):
        self.root_selected.emit(item.text())

    # ---------- REFRESH ----------
    def refresh(self):
        self.roots_list.clear()
        roots = self.engine.roots_tree.display_inorder()
        for root in roots:
            self.roots_list.addItem(root)
        stats = self.engine.get_engine_statistics()
        self.stats_label.setText(f"📊 إجمالي الجذور: {stats['roots_count']}")


# ============================================================================
# PATTERNS WIDGET (unchanged)
# ============================================================================
class EnhancedPatternsWidget(QWidget):
    """Enhanced patterns management widget with validation, export, import."""
    pattern_added = pyqtSignal(str)
    pattern_modified = pyqtSignal(str)

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._setup_ui()

    def _setup_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("🏗️ الأوزان الصرفية")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #2C2416; padding: 10px;")
        title.setMinimumHeight(50)
        main_layout.addWidget(title)
        main_layout.addSpacing(10)

        # ---------- ADD BUTTON ----------
        add_btn = QPushButton("➕ إضافة وزن جديد")
        add_btn.setMinimumHeight(55)
        add_btn.clicked.connect(self._add_pattern)
        add_btn.setToolTip("إضافة وزن صرفي جديد مع التحقق من صحة القالب")
        main_layout.addWidget(add_btn)

        # ---------- PATTERNS TABLE CARD ----------
        patterns_card = CardWidget("الأوزان المتاحة")
        self.patterns_table = QTableWidget()
        self.patterns_table.setColumnCount(4)
        self.patterns_table.setHorizontalHeaderLabels(["الاسم", "القالب", "الوصف", "مثال"])
        self.patterns_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.patterns_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.patterns_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.patterns_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.patterns_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.patterns_table.itemDoubleClicked.connect(self._edit_pattern)
        self.patterns_table.setToolTip("انقر مرتين لتعديل الوزن")
        patterns_card.add_widget(self.patterns_table)
        main_layout.addWidget(patterns_card)

        # ---------- ACTION BUTTONS ----------
        actions_layout = QHBoxLayout()

        edit_btn = QPushButton("✏️ تعديل")
        edit_btn.setMinimumHeight(50)
        edit_btn.clicked.connect(self._edit_selected_pattern)
        edit_btn.setToolTip("تعديل الوزن المحدد")

        delete_btn = QPushButton("🗑️ حذف")
        delete_btn.setMinimumHeight(50)
        delete_btn.clicked.connect(self._delete_selected_pattern)
        delete_btn.setToolTip("حذف الوزن المحدد")

        export_btn = QPushButton("📤 تصدير الأوزان")
        export_btn.setMinimumHeight(50)
        export_btn.clicked.connect(self._export_patterns)
        export_btn.setToolTip("تصدير جميع الأوزان إلى ملف JSON")

        import_btn = QPushButton("📥 استيراد الأوزان")
        import_btn.setMinimumHeight(50)
        import_btn.clicked.connect(self._import_patterns)
        import_btn.setToolTip("استيراد أوزان من ملف JSON")

        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        actions_layout.addWidget(export_btn)
        actions_layout.addWidget(import_btn)
        actions_layout.addStretch()

        main_layout.addLayout(actions_layout)
        main_layout.addStretch()

        scroll.setWidget(container)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(scroll)

        self.refresh()

    # ---------- VALIDATION HELPER ----------
    def _validate_template(self, template):
        """Validate template and show message if invalid."""
        is_valid, msg = self.engine.validate_pattern_template(template)
        if not is_valid:
            QMessageBox.warning(self, "قالب غير صالح", msg)
        return is_valid

    # ---------- ADD PATTERN ----------
    def _add_pattern(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("إضافة وزن جديد")
        dialog.setMinimumWidth(500)

        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()

        name_input = QLineEdit()
        name_input.setPlaceholderText("مثال: فاعل")
        name_input.setAlignment(Qt.AlignmentFlag.AlignRight)

        template_input = QLineEdit()
        template_input.setPlaceholderText("مثال: 1ا2و3")
        template_input.setAlignment(Qt.AlignmentFlag.AlignRight)

        desc_input = QLineEdit()
        desc_input.setPlaceholderText("مثال: اسم الفاعل")
        desc_input.setAlignment(Qt.AlignmentFlag.AlignRight)

        example_input = QLineEdit()
        example_input.setPlaceholderText("مثال: كاتب")
        example_input.setAlignment(Qt.AlignmentFlag.AlignRight)

        form_layout.addRow("الاسم:", name_input)
        form_layout.addRow("القالب:", template_input)
        form_layout.addRow("الوصف:", desc_input)
        form_layout.addRow("مثال:", example_input)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = name_input.text().strip()
            template = template_input.text().strip()
            desc = desc_input.text().strip()
            example = example_input.text().strip()

            if not name or not template:
                QMessageBox.warning(self, "تحذير", "يرجى ملء الاسم والقالب")
                return

            # Validate template
            if not self._validate_template(template):
                return

            success, message = self.engine.add_pattern(name, template, desc, example)
            if success:
                QMessageBox.information(self, "نجاح", f"✅ {message}")
                self.refresh()
                self.pattern_added.emit(name)
            else:
                QMessageBox.warning(self, "خطأ", f"❌ {message}")

    # ---------- EDIT PATTERN ----------
    def _edit_pattern(self, item):
        row = item.row()
        self._edit_pattern_at_row(row)

    def _edit_selected_pattern(self):
        current_row = self.patterns_table.currentRow()
        if current_row >= 0:
            self._edit_pattern_at_row(current_row)
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار وزن للتعديل")

    def _edit_pattern_at_row(self, row):
        name = self.patterns_table.item(row, 0).text()
        pattern_data = self.engine.patterns_table.search(name)
        if not pattern_data:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"تعديل الوزن: {name}")
        dialog.setMinimumWidth(500)

        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()

        template_input = QLineEdit(pattern_data.get('template', ''))
        template_input.setAlignment(Qt.AlignmentFlag.AlignRight)

        desc_input = QLineEdit(pattern_data.get('description', ''))
        desc_input.setAlignment(Qt.AlignmentFlag.AlignRight)

        example_input = QLineEdit(pattern_data.get('example', ''))
        example_input.setAlignment(Qt.AlignmentFlag.AlignRight)

        form_layout.addRow("القالب:", template_input)
        form_layout.addRow("الوصف:", desc_input)
        form_layout.addRow("مثال:", example_input)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_template = template_input.text().strip()
            new_desc = desc_input.text().strip()
            new_example = example_input.text().strip()

            # Validate template if changed
            if new_template != pattern_data.get('template'):
                if not self._validate_template(new_template):
                    return

            updates = {
                'template': new_template,
                'description': new_desc,
                'example': new_example
            }

            success, message = self.engine.edit_pattern(name, **updates)
            if success:
                QMessageBox.information(self, "نجاح", f"✅ {message}")
                self.refresh()
                self.pattern_modified.emit(name)
            else:
                QMessageBox.warning(self, "خطأ", f"❌ {message}")

    # ---------- DELETE PATTERN ----------
    def _delete_selected_pattern(self):
        current_row = self.patterns_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار وزن للحذف")
            return

        name = self.patterns_table.item(current_row, 0).text()
        reply = QMessageBox.question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف الوزن '{name}'؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.engine.delete_pattern(name)
            if success:
                QMessageBox.information(self, "نجاح", f"✅ {message}")
                self.refresh()
            else:
                QMessageBox.warning(self, "خطأ", f"❌ {message}")

    # ---------- EXPORT PATTERNS ----------
    def _export_patterns(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "تصدير الأوزان", "", "JSON Files (*.json)"
        )
        if path:
            if self.engine.export_patterns_to_file(path):
                QMessageBox.information(self, "نجاح", f"تم التصدير إلى:\n{path}")
            else:
                QMessageBox.critical(self, "خطأ", "فشل تصدير الأوزان")

    # ---------- IMPORT PATTERNS ----------
    def _import_patterns(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "استيراد الأوزان", "", "JSON Files (*.json)"
        )
        if path:
            success, msg = self.engine.import_patterns_from_file(path)
            if success:
                QMessageBox.information(self, "نجاح", msg)
                self.refresh()
            else:
                QMessageBox.critical(self, "خطأ", msg)

    # ---------- REFRESH ----------
    def refresh(self):
        self.patterns_table.setRowCount(0)
        patterns = self.engine.list_patterns(detailed=True)
        for name, data in patterns.items():
            row = self.patterns_table.rowCount()
            self.patterns_table.insertRow(row)
            self.patterns_table.setItem(row, 0, QTableWidgetItem(name))
            self.patterns_table.setItem(row, 1, QTableWidgetItem(data.get('template', '')))
            self.patterns_table.setItem(row, 2, QTableWidgetItem(data.get('description', '')))
            self.patterns_table.setItem(row, 3, QTableWidgetItem(data.get('example', '')))