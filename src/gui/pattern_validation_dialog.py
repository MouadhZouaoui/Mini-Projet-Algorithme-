"""
Pattern Template Validation Dialog
Quickly test if a pattern template follows Arabic morphological rules.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class PatternValidationDialog(QDialog):
    """Dialog to validate pattern template syntax."""

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("✅ التحقق من قالب الوزن")
        self.setMinimumWidth(500)
        # FIX: Use Qt.WindowType.WindowContextHelpButtonHint
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Title
        title = QLabel("✅ التحقق من صحة قالب الوزن")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #6B5B95;")
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "أدخل قالباً صرفياً للتحقق من تركيبته.\n"
            "مثال: 1ا2و3 ، 1ا23 ، م1و2و3"
        )
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("font-size: 11pt; color: #5A4E3A; font-style: italic;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Input field
        self.template_input = QLineEdit()
        self.template_input.setPlaceholderText("أدخل القالب هنا...")
        self.template_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.template_input.setMinimumHeight(50)
        self.template_input.returnPressed.connect(self._validate)
        layout.addWidget(self.template_input)

        # Validate button
        validate_btn = QPushButton("تحقق")
        validate_btn.setMinimumHeight(50)
        validate_btn.clicked.connect(self._validate)
        layout.addWidget(validate_btn)

        # Result label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("font-size: 12pt; padding: 10px;")
        layout.addWidget(self.result_label)

        # Close button
        close_btn = QPushButton("إغلاق")
        close_btn.setMinimumHeight(45)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def _validate(self):
        template = self.template_input.text().strip()
        if not template:
            QMessageBox.warning(self, "تنبيه", "الرجاء إدخال قالب")
            return

        is_valid, message = self.engine.validate_pattern_template(template)
        if is_valid:
            self.result_label.setText(f"✅ {message}")
            self.result_label.setStyleSheet("color: #4CAF50; font-weight: bold; padding: 10px;")
        else:
            self.result_label.setText(f"❌ {message}")
            self.result_label.setStyleSheet("color: #F44336; font-weight: bold; padding: 10px;")