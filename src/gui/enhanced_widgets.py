"""
Enhanced Widgets Module – COMPLETELY FIXED & PROFESSIONAL
Includes:
- Real‑time root validation (✅/❌ badges)
- Generation with root existence check
- Fixed generate_all (calls generate_all_for_root)
- Correct result dictionary keys ('generated_word')
- Progress dialog for long operations
- Tooltips for all controls
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTextEdit, QScrollArea, QMessageBox, QProgressDialog
)
from PyQt6.QtCore import Qt, pyqtSignal


class CardWidget(QWidget):
    """A card-style container widget with enhanced styling."""
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            CardWidget {
                background-color: #F5EFE6;
                border: 2px solid #C5B5A0;
                border-radius: 12px;
            }
        """)
        self.setMinimumHeight(150)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(16)
        self.layout.setContentsMargins(25, 25, 25, 25)
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                font-size: 14pt; font-weight: bold; color: #2C2416;
                background: transparent; border: none; padding: 5px;
            """)
            title_label.setMinimumHeight(35)
            self.layout.addWidget(title_label)

    def add_widget(self, widget):
        self.layout.addWidget(widget)


class EnhancedGenerationWidget(QWidget):
    """Enhanced word generation widget with professional validation and feedback."""
    generation_completed = pyqtSignal(dict)

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
        title = QLabel("🏗️ توليد الكلمات المشتقة")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #2C2416; padding: 10px;")
        title.setMinimumHeight(50)
        main_layout.addWidget(title)

        # Description
        desc = QLabel("أدخل الجذر الثلاثي والوزن الصرفي لتوليد الكلمة")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("font-size: 11pt; color: #5A4E3A; font-style: italic;")
        desc.setWordWrap(True)
        desc.setMinimumHeight(30)
        main_layout.addWidget(desc)
        main_layout.addSpacing(10)

        # ------------------- SINGLE GENERATION CARD -------------------
        single_card = CardWidget("توليد كلمة مفردة")

        # Root input with validation badge
        root_layout = QHBoxLayout()
        root_label = QLabel("الجذر:")
        root_label.setFixedWidth(100)
        root_label.setStyleSheet("background: transparent; border: none; font-size: 13pt; padding: 5px;")
        root_label.setMinimumHeight(45)
        root_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.root_input = QLineEdit()
        self.root_input.setPlaceholderText("مثال: كتب")
        self.root_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.root_input.setMinimumHeight(50)
        self.root_input.returnPressed.connect(self._generate_single_word)
        self.root_input.setToolTip("أدخل جذراً ثلاثياً. سيتم التحقق من وجوده تلقائياً.")

        # Status badge (✅/❌)
        self.root_status = QLabel()
        self.root_status.setFixedSize(30, 30)
        self.root_status.setStyleSheet("background: transparent; border: none; font-size: 18pt;")
        self.root_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.root_status.setToolTip("✅ موجود في الشجرة – ❌ غير موجود")

        root_layout.addWidget(root_label)
        root_layout.addWidget(self.root_input)
        root_layout.addWidget(self.root_status)

        root_widget = QWidget()
        root_widget.setLayout(root_layout)
        single_card.add_widget(root_widget)

        # Pattern combo
        pattern_layout = QHBoxLayout()
        pattern_label = QLabel("الوزن:")
        pattern_label.setFixedWidth(100)
        pattern_label.setStyleSheet("background: transparent; border: none; font-size: 13pt; padding: 5px;")
        pattern_label.setMinimumHeight(45)
        pattern_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.pattern_combo = QComboBox()
        self.pattern_combo.setMinimumHeight(50)
        self.pattern_combo.addItem("اختر وزناً")
        self.pattern_combo.setToolTip("اختر الوزن الصرفي من القائمة")

        pattern_layout.addWidget(pattern_label)
        pattern_layout.addWidget(self.pattern_combo)

        pattern_widget = QWidget()
        pattern_widget.setLayout(pattern_layout)
        single_card.add_widget(pattern_widget)

        # Generate button
        self.generate_btn = QPushButton("توليد الكلمة")
        self.generate_btn.setMinimumHeight(55)
        self.generate_btn.clicked.connect(self._generate_single_word)
        self.generate_btn.setToolTip("توليد الكلمة باستخدام الجذر والوزن المختارين")
        single_card.add_widget(self.generate_btn)

        main_layout.addWidget(single_card)

        # ------------------- ALL PATTERNS GENERATION CARD -------------------
        all_card = CardWidget("توليد جميع الأوزان")

        all_root_layout = QHBoxLayout()
        all_root_label = QLabel("الجذر:")
        all_root_label.setFixedWidth(100)
        all_root_label.setStyleSheet("background: transparent; border: none; font-size: 13pt; padding: 5px;")
        all_root_label.setMinimumHeight(45)
        all_root_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.all_root_input = QLineEdit()
        self.all_root_input.setPlaceholderText("مثال: كتب")
        self.all_root_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.all_root_input.setMinimumHeight(50)
        self.all_root_input.returnPressed.connect(self._generate_all_patterns)
        self.all_root_input.setToolTip("أدخل جذراً ثلاثياً موجوداً في الشجرة")

        # Status badge for all-root input
        self.all_root_status = QLabel()
        self.all_root_status.setFixedSize(30, 30)
        self.all_root_status.setStyleSheet("background: transparent; border: none; font-size: 18pt;")
        self.all_root_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.all_root_status.setToolTip("✅ موجود في الشجرة – ❌ غير موجود")

        all_root_layout.addWidget(all_root_label)
        all_root_layout.addWidget(self.all_root_input)
        all_root_layout.addWidget(self.all_root_status)

        all_root_widget = QWidget()
        all_root_widget.setLayout(all_root_layout)
        all_card.add_widget(all_root_widget)

        self.generate_all_btn = QPushButton("توليد جميع المشتقات")
        self.generate_all_btn.setMinimumHeight(55)
        self.generate_all_btn.clicked.connect(self._generate_all_patterns)
        self.generate_all_btn.setToolTip("توليد جميع الكلمات المشتقة لهذا الجذر باستخدام كل الأوزان")
        all_card.add_widget(self.generate_all_btn)

        main_layout.addWidget(all_card)

        # ------------------- RESULTS SECTION -------------------
        results_label = QLabel("النتائج")
        results_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2C2416; padding: 5px;")
        results_label.setMinimumHeight(35)
        main_layout.addWidget(results_label)

        self.results_box = QTextEdit()
        self.results_box.setPlaceholderText("النتائج ستظهر هنا...")
        self.results_box.setReadOnly(True)
        self.results_box.setMinimumHeight(200)
        self.results_box.setToolTip("نافذة عرض النتائج – تدعم HTML")
        main_layout.addWidget(self.results_box)

        main_layout.addStretch()

        scroll.setWidget(container)
        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(scroll)

        # Connect validation signals
        self.root_input.textChanged.connect(self._validate_root_input)
        self.all_root_input.textChanged.connect(self._validate_all_root_input)

        self.refresh()

    # ---------- VALIDATION METHODS ----------
    def _validate_root_input(self, text):
        """Update status badge based on root existence in AVL tree."""
        if not text:
            self.root_status.setText("")
            self.root_status.setToolTip("")
            return
        if self.engine.root_exists(text):
            self.root_status.setText("✅")
            self.root_status.setToolTip("الجذر موجود في الشجرة")
        else:
            self.root_status.setText("❌")
            self.root_status.setToolTip("هذا الجذر غير موجود – أضفه أولاً")

    def _validate_all_root_input(self, text):
        """Same as above for the 'all patterns' input."""
        if not text:
            self.all_root_status.setText("")
            self.all_root_status.setToolTip("")
            return
        if self.engine.root_exists(text):
            self.all_root_status.setText("✅")
            self.all_root_status.setToolTip("الجذر موجود في الشجرة")
        else:
            self.all_root_status.setText("❌")
            self.all_root_status.setToolTip("هذا الجذر غير موجود – أضفه أولاً")

    # ---------- GENERATION METHODS ----------
    def _generate_single_word(self):
        """Generate a single word from root and selected pattern."""
        root = self.root_input.text().strip()
        pattern_name = self.pattern_combo.currentText()

        if not root or pattern_name == "اختر وزناً":
            QMessageBox.warning(self, "خطأ", "الرجاء إدخال الجذر واختيار الوزن")
            return

        # Verify root exists
        if not self.engine.root_exists(root):
            QMessageBox.warning(
                self, "خطأ",
                f"الجذر '{root}' غير موجود في الشجرة.\nأضفه أولاً عبر تبويب 'الجذور'."
            )
            return

        # Show progress
        progress = QProgressDialog("جاري توليد الكلمة...", None, 0, 0, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(300)
        progress.setValue(0)

        result = self.engine.generate_word(root, pattern_name)

        progress.close()

        if result:
            self._display_single_result(result)
            self.generation_completed.emit(result)
        else:
            QMessageBox.warning(self, "خطأ", "فشل توليد الكلمة. تأكد من صحة الوزن.")

    def _generate_all_patterns(self):
        """Generate all derivatives for a root using all patterns."""
        root = self.all_root_input.text().strip()

        if not root:
            QMessageBox.warning(self, "خطأ", "الرجاء إدخال الجذر")
            return

        # Verify root exists
        if not self.engine.root_exists(root):
            QMessageBox.warning(
                self, "خطأ",
                f"الجذر '{root}' غير موجود في الشجرة.\nأضفه أولاً عبر تبويب 'الجذور'."
            )
            return

        # Show progress (indeterminate)
        progress = QProgressDialog("جاري توليد جميع المشتقات...", "إلغاء", 0, 0, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(500)
        progress.setValue(0)

        results = self.engine.generate_all_for_root(root)

        progress.close()

        if results:
            # Convert to (pattern, word) format for display
            formatted = [(r['pattern'], r['generated_word']) for r in results]
            self._display_all_results(formatted)
            self.generation_completed.emit({'root': root, 'results': results})
        else:
            QMessageBox.warning(self, "خطأ", "فشل توليد المشتقات أو لا توجد أوزان.")

    # ---------- DISPLAY METHODS ----------
    def _display_single_result(self, result):
        """Display single generation result in rich HTML."""
        html = f"""
        <div style='direction: rtl; text-align: right; padding: 15px;'>
            <h2 style='color: #6B5B95; margin-bottom: 15px;'>✅ نجح التوليد</h2>
            <table style='width: 100%; border-collapse: collapse;'>
                <tr style='background: #F5EFE6;'>
                    <td style='padding: 10px; font-weight: bold;'>الجذر:</td>
                    <td style='padding: 10px;'>{result.get('root', '')}</td>
                </tr>
                <tr>
                    <td style='padding: 10px; font-weight: bold;'>الوزن:</td>
                    <td style='padding: 10px;'>{result.get('pattern', '')}</td>
                </tr>
                <tr style='background: #F5EFE6;'>
                    <td style='padding: 10px; font-weight: bold;'>الكلمة:</td>
                    <td style='padding: 10px; font-size: 18pt; color: #2C2416;'>
                        <b>{result.get('generated_word', '')}</b>
                    </td>
                </tr>
                <tr>
                    <td style='padding: 10px; font-weight: bold;'>الوصف:</td>
                    <td style='padding: 10px;'>{result.get('description', '')}</td>
                </tr>
                <tr style='background: #F5EFE6;'>
                    <td style='padding: 10px; font-weight: bold;'>القالب:</td>
                    <td style='padding: 10px;'>{result.get('template', '')}</td>
                </tr>
            </table>
        </div>
        """
        self.results_box.setHtml(html)

    def _display_all_results(self, results):
        """Display all pattern results in a table."""
        html = """
        <div style='direction: rtl; text-align: right; padding: 15px;'>
            <h2 style='color: #6B5B95; margin-bottom: 15px;'>✅ جميع المشتقات</h2>
            <table style='width: 100%; border-collapse: collapse;'>
                <tr style='background: #6B5B95; color: white;'>
                    <th style='padding: 10px;'>الوزن</th>
                    <th style='padding: 10px;'>الكلمة</th>
                </tr>
        """
        for i, (pattern, word) in enumerate(results):
            bg = '#F5EFE6' if i % 2 == 0 else 'white'
            html += f"""
                <tr style='background: {bg};'>
                    <td style='padding: 10px;'>{pattern}</td>
                    <td style='padding: 10px; font-size: 14pt;'><b>{word}</b></td>
                </tr>
            """
        html += "</table></div>"
        self.results_box.setHtml(html)

    # ---------- REFRESH ----------
    def refresh(self):
        """Refresh pattern combo box."""
        self.pattern_combo.clear()
        self.pattern_combo.addItem("اختر وزناً")
        patterns = self.engine.patterns_table.get_all_patterns()
        for pattern_name, _ in patterns:
            self.pattern_combo.addItem(pattern_name)


class EnhancedValidationWidget(QWidget):
    """Enhanced word validation widget with support for multiple matches."""
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

        title = QLabel("✅ التحقق من الانتماء المورفولوجي")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #2C2416; padding: 10px;")
        title.setMinimumHeight(50)
        main_layout.addWidget(title)
        main_layout.addSpacing(10)

        card = CardWidget("التحقق من الكلمة")

        # Word input
        word_layout = QHBoxLayout()
        word_label = QLabel("الكلمة:")
        word_label.setFixedWidth(120)
        word_label.setStyleSheet("background: transparent; border: none; font-size: 13pt; padding: 5px;")
        word_label.setMinimumHeight(45)
        word_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("مثال: كاتب")
        self.word_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.word_input.setMinimumHeight(50)
        self.word_input.returnPressed.connect(self._validate_word)
        self.word_input.setToolTip("أدخل الكلمة المراد التحقق منها")

        word_layout.addWidget(word_label)
        word_layout.addWidget(self.word_input)

        word_widget = QWidget()
        word_widget.setLayout(word_layout)
        card.add_widget(word_widget)

        # Root input (optional)
        root_layout = QHBoxLayout()
        root_label = QLabel("الجذر (اختياري):")
        root_label.setFixedWidth(120)
        root_label.setStyleSheet("background: transparent; border: none; font-size: 13pt; padding: 5px;")
        root_label.setMinimumHeight(45)
        root_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.root_input = QLineEdit()
        self.root_input.setPlaceholderText("مثال: كتب")
        self.root_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.root_input.setMinimumHeight(50)
        self.root_input.returnPressed.connect(self._validate_word)
        self.root_input.setToolTip("اختياري – اتركه فارغاً للبحث في جميع الجذور")

        root_layout.addWidget(root_label)
        root_layout.addWidget(self.root_input)

        root_widget = QWidget()
        root_widget.setLayout(root_layout)
        card.add_widget(root_widget)

        # Hint
        hint = QLabel("💡 اترك الجذر فارغاً للبحث في جميع الجذور المخزنة")
        hint.setStyleSheet("font-size: 11pt; color: #5A4E3A; font-style: italic; padding: 5px;")
        hint.setAlignment(Qt.AlignmentFlag.AlignRight)
        hint.setMinimumHeight(30)
        card.add_widget(hint)

        # Validate button
        self.validate_btn = QPushButton("التحقق")
        self.validate_btn.setMinimumHeight(55)
        self.validate_btn.clicked.connect(self._validate_word)
        self.validate_btn.setToolTip("ابدأ عملية التحقق")
        card.add_widget(self.validate_btn)

        main_layout.addWidget(card)

        # Results
        results_label = QLabel("النتائج")
        results_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2C2416; padding: 5px;")
        results_label.setMinimumHeight(35)
        main_layout.addWidget(results_label)

        self.results_box = QTextEdit()
        self.results_box.setPlaceholderText("نتائج التحقق ستظهر هنا...")
        self.results_box.setReadOnly(True)
        self.results_box.setMinimumHeight(200)
        main_layout.addWidget(self.results_box)
        main_layout.addStretch()

        scroll.setWidget(container)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(scroll)

    def _validate_word(self):
        """Perform validation and display results (handles multiple matches)."""
        word = self.word_input.text().strip()
        root = self.root_input.text().strip() or None

        if not word:
            QMessageBox.warning(self, "خطأ", "الرجاء إدخال الكلمة")
            return

        result = self.engine.validate_word(word, root)
        self._display_validation_result(result)

    def _display_validation_result(self, result):
        """Display validation result with support for multiple matches."""
        is_valid = result.get('is_valid', False)
        color = '#4CAF50' if is_valid else '#F44336'
        status = '✅ كلمة صحيحة' if is_valid else '❌ كلمة غير صحيحة'

        html = f"""
        <div style='direction: rtl; text-align: right; padding: 15px;'>
            <h2 style='color: {color}; margin-bottom: 15px;'>{status}</h2>
            <table style='width: 100%; border-collapse: collapse;'>
                <tr style='background: #F5EFE6;'>
                    <td style='padding: 10px; font-weight: bold;'>الكلمة:</td>
                    <td style='padding: 10px;'>{result['word']}</td>
                </tr>
        """

        if is_valid:
            if 'matches' in result:
                # Multiple matches
                html += """
                <tr>
                    <td colspan='2' style='padding: 10px; font-weight: bold;'>
                        المشتقات المطابقة:
                    </td>
                </tr>
                """
                for i, match in enumerate(result['matches'], 1):
                    bg = '#F5EFE6' if i % 2 == 0 else 'white'
                    html += f"""
                    <tr style='background: {bg};'>
                        <td style='padding: 10px;'>الوزن {i}:</td>
                        <td style='padding: 10px;'>
                            {match['pattern']} (الجذر: {match['root']})
                        </td>
                    </tr>
                    """
            else:
                # Single match
                html += f"""
                <tr>
                    <td style='padding: 10px; font-weight: bold;'>الجذر:</td>
                    <td style='padding: 10px;'>{result.get('root', 'غير محدد')}</td>
                </tr>
                <tr style='background: #F5EFE6;'>
                    <td style='padding: 10px; font-weight: bold;'>الوزن:</td>
                    <td style='padding: 10px;'>{result.get('pattern', 'غير محدد')}</td>
                </tr>
                """
        else:
            if 'possible_roots' in result and result['possible_roots']:
                html += f"""
                <tr>
                    <td style='padding: 10px; font-weight: bold;'>جذور محتملة:</td>
                    <td style='padding: 10px;'>{'، '.join(result['possible_roots'])}</td>
                </tr>
                """

        html += "</table></div>"
        self.results_box.setHtml(html)