"""
Derivatives Management Widget – FINAL VERSION
- Dropdown shows ALL roots (never empty)
- Roots with derivatives marked with ✅
- Table shows message when no derivatives exist
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QScrollArea, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal


class DerivativesWidget(QWidget):
    """Tab for managing derivatives of existing roots."""
    derivative_removed = pyqtSignal(str, str)  # root, word
    derivatives_cleared = pyqtSignal(str)      # root

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.current_root = None
        self._setup_ui()
        self.refresh_root_list()

    def _setup_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("📚 إدارة المشتقات")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 25pt; font-weight: bold; color: #2C2416;")
        title.setMinimumHeight(50)
        main_layout.addWidget(title)

        desc = QLabel("اختر جذراً لعرض مشتقاته المجمّعة وحذفها")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("font-size: 15pt; color: #5A4E3A; font-style: italic;")
        desc.setWordWrap(True)
        main_layout.addWidget(desc)
        main_layout.addSpacing(10)

        # Root selection group
        group = QGroupBox("اختيار الجذر")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 13pt;
                font-weight: bold;
                border: 2px solid #C5B5A0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        group_layout = QHBoxLayout(group)

        lbl = QLabel("الجذر:")
        lbl.setFixedWidth(80)
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.root_combo = QComboBox()
        self.root_combo.setMinimumHeight(45)
        self.root_combo.currentTextChanged.connect(self._on_root_changed)
        self.root_combo.setToolTip("اختر جذراً لعرض مشتقاته")
        refresh_btn = QPushButton("تحديث القائمة")
        refresh_btn.setMinimumHeight(45)
        refresh_btn.clicked.connect(self.refresh_root_list)

        group_layout.addWidget(lbl)
        group_layout.addWidget(self.root_combo, 1)
        group_layout.addWidget(refresh_btn)
        main_layout.addWidget(group)

        # Derivatives table
        table_label = QLabel("المشتقات المجمّعة:")
        table_label.setStyleSheet("font-size: 13pt; font-weight: bold; color: #2C2416;")
        main_layout.addWidget(table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["الكلمة", "الوزن", "التكرار", "الإجراءات"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setStyleSheet("""
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #8573B3, stop:1 #584A7A);
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        # Make rows non‑resizable
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.verticalHeader().setDefaultSectionSize(100) 
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(250)
        main_layout.addWidget(self.table)

        # Clear all button
        self.clear_btn = QPushButton("🗑️ حذف جميع المشتقات للجذر المحدد")
        self.clear_btn.setMinimumHeight(50)
        self.clear_btn.clicked.connect(self._clear_all_derivatives)
        self.clear_btn.setEnabled(False)
        main_layout.addWidget(self.clear_btn)

        main_layout.addStretch()

        scroll.setWidget(container)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(scroll)

    # ----- Public refresh method (called by main window) -----
    def refresh(self):
        """Refresh the dropdown and table."""
        self.refresh_root_list()

    def refresh_root_list(self):
        """Populate combo box with ALL roots, marking those with derivatives."""
        self.root_combo.clear()
        self.root_combo.addItem("-- اختر جذراً --")

        # Get all roots from the tree (inorder traversal)
        all_roots = self.engine.roots_tree.display_inorder()

        # Separate roots with and without derivatives
        roots_with = []
        roots_without = []
        for root in all_roots:
            node = self.engine.roots_tree.search(root)
            if node and node.get_derivative_count() > 0:
                roots_with.append(root)
            else:
                roots_without.append(root)

        # Add roots with derivatives first (with ✅ marker)
        for root in roots_with:
            self.root_combo.addItem(f"✅ {root}")

        # Add roots without derivatives
        for root in roots_without:
            self.root_combo.addItem(root)


        # If no roots at all, show placeholder
        if self.root_combo.count() == 1:
            self.root_combo.addItem("(لا توجد جذور)")

    def _on_root_changed(self, root_text):
        """Handle root selection change."""
        # Clean the text (remove ✅ marker if present)
        if root_text.startswith("✅ "):
            root = root_text[2:]  # remove checkmark and space
        else:
            root = root_text

        if not root or root.startswith("--") or root.startswith("(لا"):
            self.table.setRowCount(0)
            self.current_root = None
            self.clear_btn.setEnabled(False)
            return

        self.current_root = root
        self.clear_btn.setEnabled(True)
        self._load_derivatives(root)

    def _load_derivatives(self, root):
        node = self.engine.roots_tree.search(root)
        if not node:
            return
        derivatives = node.get_derivatives()
        self.table.setRowCount(len(derivatives))
        for i, deriv in enumerate(derivatives):
            # Word, Pattern, Frequency cells
            self.table.setItem(i, 0, QTableWidgetItem(deriv['word']))
            self.table.setItem(i, 1, QTableWidgetItem(deriv['pattern']))
            self.table.setItem(i, 2, QTableWidgetItem(str(deriv['frequency'])))

            # Button widget
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(4, 4, 4, 4)
            btn_layout.setSpacing(8)

            # Decrement button
            dec_btn = QPushButton(" −1 تكرار")
            dec_btn.setFixedSize(120, 25)
            dec_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 12pt;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
                QPushButton:pressed {
                    background-color: #EF6C00;
                }
            """)
            dec_btn.clicked.connect(lambda checked, w=deriv['word'], p=deriv['pattern'], r=root:
                                    self._decrement_frequency(w, p, r))

            # Delete button
            del_btn = QPushButton("✖ حذف")
            del_btn.setFixedSize(120, 25)
            del_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F44336;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 12pt;
                }
                QPushButton:hover {
                    background-color: #D32F2F;
                }
                QPushButton:pressed {
                    background-color: #B71C1C;
                }
            """)
            del_btn.clicked.connect(lambda checked, w=deriv['word'], p=deriv['pattern'], r=root:
                                    self._remove_derivative(w, p, r))

            btn_layout.addWidget(dec_btn)
            btn_layout.addWidget(del_btn)
            btn_layout.addStretch()
            self.table.setCellWidget(i, 3, btn_widget)

    def _decrement_frequency(self, word, pattern, root):
        if not root:
            return
        node = self.engine.roots_tree.search(root)
        if not node:
            return
        for deriv in node.get_derivatives():
            if deriv['word'] == word and deriv['pattern'] == pattern:
                if deriv['frequency'] > 1:
                    deriv['frequency'] -= 1
                    QMessageBox.information(self, "نجاح", f"تم إنقاص تكرار '{word}' إلى {deriv['frequency']}")
                else:
                    # Ask to delete when frequency becomes 0
                    reply = QMessageBox.question(
                        self, "تكرار صفر",
                        f"التكرار الآن 0. هل تريد حذف المشتق؟",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.Yes:
                        self._remove_derivative(word, pattern)
                self._load_derivatives(root)
                return
        
    def _remove_derivative(self, word, pattern):
        """Remove a single derivative after confirmation."""
        if not self.current_root:
            return
        reply = QMessageBox.question(
            self, "تأكيد الحذف",
            f"حذف '{word}' (الوزن: {pattern}) من الجذر '{self.current_root}'؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if self.engine.remove_derivative(self.current_root, word, pattern):
                QMessageBox.information(self, "نجاح", "تم حذف المشتق")
                self.derivative_removed.emit(self.current_root, word)
                self._load_derivatives(self.current_root)
                self.refresh_root_list()  # update checkmarks
            else:
                QMessageBox.critical(self, "خطأ", "فشل حذف المشتق")

    def _clear_all_derivatives(self):
        """Clear all derivatives for the current root."""
        if not self.current_root:
            return
        reply = QMessageBox.question(
            self, "تأكيد الحذف الكلي",
            f"حذف جميع مشتقات الجذر '{self.current_root}'؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if self.engine.clear_root_derivatives(self.current_root):
                QMessageBox.information(self, "نجاح", "تم حذف جميع المشتقات")
                self.derivatives_cleared.emit(self.current_root)
                self._load_derivatives(self.current_root)
                self.refresh_root_list()
            else:
                QMessageBox.critical(self, "خطأ", "فشل حذف المشتقات")