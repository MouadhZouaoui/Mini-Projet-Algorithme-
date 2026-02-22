"""
Enhanced Roots and Patterns Widgets – FINAL FIXED VERSION
All layout issues resolved:
- Scroll area container has Preferred vertical policy to allow scroll bars
- Input fields expand horizontally
- Roots list takes all remaining vertical space
"""

import os 
from PyQt6.QtWidgets import (
    QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QDialogButtonBox, QScrollArea,
    QFileDialog, QGridLayout, QSizePolicy, QTextEdit, QDialog, QFrame
)
from PyQt6.QtCore import QEvent, Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QPixmap

from arabic_utils import ArabicUtils
from root_classifier import RootClassifier
from .root_analysis_dialog import RootAnalysisDialog
from .enhanced_widgets import CardWidget

class EnhancedDashboardWidget(QWidget):
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.recent_actions = []
        self._setup_ui()
        self._start_refresh_timer()

    def _setup_ui(self):
        # Outer scroll area
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Container widget
        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Main layout for container
        main_layout = QVBoxLayout(self.container)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("🌙 لوحة التحكم")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 25pt; font-weight: bold; color: #2C2416;")
        title.setMinimumHeight(40)
        main_layout.addWidget(title)

        # Subtitle
        desc = QLabel("نظرة عامة على النظام وإحصائيات حية")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("font-size: 15pt; color: #5A4E3A; font-style: italic;")
        desc.setWordWrap(True)
        main_layout.addWidget(desc)
        main_layout.addSpacing(10)

        # ---------- Counter Cards (two rows, two columns) ----------
        stats = self.engine.get_engine_statistics()
        self.roots_card = self._create_counter_card("🌱", "الجذور", stats['roots_count'])
        self.patterns_card = self._create_counter_card("📐", "الأوزان", stats['patterns_count'])
        self.derivatives_card = self._create_counter_card("📝", "المشتقات", stats['generated_words_count'])
        self.tree_card = self._create_counter_card("🌳", "ارتفاع الشجرة", stats['avl_tree_height'])

        # Row 1
        row1 = QHBoxLayout()
        row1.setSpacing(20)
        row1.addWidget(self.roots_card, 1)
        row1.addWidget(self.patterns_card, 1)
        main_layout.addLayout(row1)

        # Row 2
        row2 = QHBoxLayout()
        row2.setSpacing(20)
        row2.addWidget(self.derivatives_card, 1)
        row2.addWidget(self.tree_card, 1)
        main_layout.addLayout(row2)

        # ---------- Quick Action Cards (two rows, two columns) ----------
        actions_label = QLabel("إجراءات سريعة")
        actions_label.setStyleSheet("font-size: 25pt; font-weight: bold; color: #2C2416;")
        main_layout.addWidget(actions_label)

        self.add_card = self._create_action_card("plus.png", "إضافة جذر")
        self.gen_card = self._create_action_card("reminder.png", "توليد كلمة")
        self.val_card = self._create_action_card("check-mark.png", "تحقق")
        self.deriv_card = self._create_action_card("agenda.png", "المشتقات")

        # Row A
        rowA = QHBoxLayout()
        rowA.setSpacing(20)
        rowA.addWidget(self.add_card, 1)
        rowA.addWidget(self.gen_card, 1)
        main_layout.addLayout(rowA)

        # Row B
        rowB = QHBoxLayout()
        rowB.setSpacing(20)
        rowB.addWidget(self.val_card, 1)
        rowB.addWidget(self.deriv_card, 1)
        main_layout.addLayout(rowB)

        # ---------- Charts ----------
        charts_label = QLabel("إحصائيات مرئية")
        charts_label.setStyleSheet("font-size: 25pt; font-weight: bold; color: #2C2416;")
        main_layout.addWidget(charts_label)

        from .charts_widget import StatisticsChartsWidget
        self.charts = StatisticsChartsWidget(self.engine)
        self.charts.setMinimumHeight(300)
        self.charts.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.charts, 1)

        # ---------- Recent Activity ----------
        activity_label = QLabel("آخر النشاطات")
        activity_label.setStyleSheet("font-size: 25pt; font-weight: bold; color: #2C2416;")
        main_layout.addWidget(activity_label)

        self.activity_list = QListWidget()
        self.activity_list.setMinimumHeight(150)
        self.activity_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.activity_list.setStyleSheet("""
            QListWidget {
                background-color: #FAF0E6;
                border: 2px solid #C5B5A0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self._update_activity_feed()
        main_layout.addWidget(self.activity_list, 1)

        self.scroll.setWidget(self.container)

        # Final layout for this widget
        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(self.scroll)

        # Adjust container width when viewport resizes
        self.scroll.viewport().installEventFilter(self)
        # Also adjust after a short delay to ensure initial size
        QTimer.singleShot(100, self._adjust_container_width)

    def eventFilter(self, obj, event):
        if obj == self.scroll.viewport() and event.type() == QEvent.Type.Resize:
            self._adjust_container_width()
        return super().eventFilter(obj, event)

    def _adjust_container_width(self):
        """Force container to be at least as wide as the viewport."""
        vp_width = self.scroll.viewport().width()
        if vp_width > 0:
            self.container.setMinimumWidth(vp_width)

    # ---------- Helper Methods (unchanged) ----------
    def _create_counter_card(self, emoji, label, value):
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setObjectName("displayCard")
        card.setStyleSheet("""
            QFrame#displayCard {
                background: qlineargradient(
                x1:0, y1:0,
                x2:1, y2:1,
                stop:0 #fdfcfb,
                stop:1 #e2d1c3
            );
                border-radius: 12px;
                border: 2px solid #C5B5A0;
                padding: 15px;
            }
        """)
        card.setMinimumHeight(100)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        top = QHBoxLayout()
        top.setAlignment(Qt.AlignmentFlag.AlignCenter)  # ← ADD THIS LINE

        emoji_lbl = QLabel(emoji)
        emoji_lbl.setStyleSheet("font-size: 30pt;")
        # emoji_lbl.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_lbl = QLabel(label)

        label_lbl.setStyleSheet("font-size: 30pt; font-weight: bold; color: #2C2416;")
        # label_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        top.addWidget(emoji_lbl)
        top.addWidget(label_lbl)
        layout.addLayout(top)

        value_lbl = QLabel(str(value))
        value_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_lbl.setStyleSheet("font-size: 35pt; font-weight: bold; color: #6B5B95;")
        # value_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(value_lbl)

        card.value_label = value_lbl
        return card

    def _get_image_path(self, filename):
        """Return absolute path to an image in the images folder."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(script_dir, "images")
        return os.path.join(images_dir, filename)

    def _create_action_card(self, image_filename, text):
        card = QFrame()
        card.setFrameShape(QFrame.Shape.NoFrame)
        card.setObjectName("actionCard")
        card.setStyleSheet("""
            QFrame#actionCard {
                background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #D4C4B0,
                stop:1 #8B7355
                );
                border: 2px solid #C5B5A0;
                padding: 10px;
                border-radius: 12px;
            }
            QFrame#actionCard:hover {
                background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #8B7355,
                stop:1 #5D4E37
                );
                border: 3px solid #5D4E37;
                           
            }               
            QLabel {
                background-color: transparent;
                border: none;
                padding: 5px;
                border-radius: 8px;
            }
        """)
        card.setFixedSize(300, 200)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # emoji_lbl = QLabel(emoji)
        # emoji_lbl.setStyleSheet("font-size: 30pt;")
        # emoji_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # emoji_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) 
        # 
        img_label = QLabel()
        image_path = self._get_image_path(image_filename)
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            img_label.setPixmap(scaled)
        else:
            print(f"⚠️ Could not load image: {image_path} – falling back to emoji")
            img_label.setText("➕")
            img_label.setStyleSheet("font-size: 36pt;")
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(img_label) 

        text_lbl = QLabel(text)
        text_lbl.setStyleSheet("font-size: 20pt; font-weight: bold; color: #2C2416; margin:0pt")

        text_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_lbl.setWordWrap(True)
        text_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)  

        layout.addWidget(text_lbl)

        card.mousePressEvent = lambda e, t=text: self._on_action_clicked(t)
        return card

    def _on_action_clicked(self, action):
        main = self.window()
        if hasattr(main, 'tabs'):
            if action == "إضافة جذر":
                main.tabs.setCurrentWidget(main.roots_widget)
            elif action == "توليد كلمة":
                main.tabs.setCurrentWidget(main.generation_widget)
            elif action == "تحقق":
                main.tabs.setCurrentWidget(main.validation_widget)
            elif action == "المشتقات":
                main.tabs.setCurrentWidget(main.derivatives_widget)
        self._add_activity(f"🖱️ {action}")

    def _add_activity(self, text):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.recent_actions.insert(0, f"[{timestamp}] {text}")
        self.recent_actions = self.recent_actions[:10]
        self._update_activity_feed()

    def _update_activity_feed(self):
        self.activity_list.clear()
        if self.recent_actions:
            for a in self.recent_actions:
                self.activity_list.addItem(a)
        else:
            self.activity_list.addItem("لا توجد نشاطات بعد")

    def _start_refresh_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)
        self.timer.start(10000)

    def _update_stats(self):
        stats = self.engine.get_engine_statistics()
        self.roots_card.value_label.setText(str(stats['roots_count']))
        self.patterns_card.value_label.setText(str(stats['patterns_count']))
        self.derivatives_card.value_label.setText(str(stats['generated_words_count']))
        self.tree_card.value_label.setText(str(stats['avl_tree_height']))
        self.charts.refresh()
        self._add_activity("🔄 تحديث تلقائي")

    def refresh(self):
        self._update_stats()

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)
# ============================================================================
# FINAL DASHBOARD – with scroll area and guaranteed expansion
# ============================================================================
#     def __init__(self, engine, parent=None):
#         super().__init__(parent)
#         self.engine = engine
#         self.recent_actions = []
#         self._setup_ui()
#         self._start_refresh_timer()

#     def _setup_ui(self):
#         # Main scroll area – expands fully
#         scroll = QScrollArea(self)
#         scroll.setWidgetResizable(True)
#         scroll.setFrameShape(QScrollArea.Shape.NoFrame)
#         scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

#         container = QWidget()
#         container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

#         main_layout = QVBoxLayout(container)
#         main_layout.setSpacing(30)
#         main_layout.setContentsMargins(30, 30, 30, 30)

#         # Title & subtitle
#         title = QLabel("🌙 لوحة التحكم")
#         title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         title.setStyleSheet("font-size: 22pt; font-weight: bold; color: #2C2416;")
#         main_layout.addWidget(title)

#         subtitle = QLabel("نظرة عامة على النظام وإحصائيات حية")
#         subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         subtitle.setStyleSheet("font-size: 12pt; color: #5A4E3A; font-style: italic;")
#         main_layout.addWidget(subtitle)

#         # ---------- Counter Cards (Grid 2x2) ----------
#         counter_layout = QGridLayout()
#         counter_layout.setSpacing(20)

#         stats = self.engine.get_engine_statistics()
#         self.roots_card = self._create_counter_card("🌱", "الجذور", stats['roots_count'])
#         self.patterns_card = self._create_counter_card("📐", "الأوزان", stats['patterns_count'])
#         self.derivatives_card = self._create_counter_card("📝", "المشتقات", stats['generated_words_count'])
#         self.tree_card = self._create_counter_card("🌳", "ارتفاع الشجرة", stats['avl_tree_height'])

#         counter_layout.addWidget(self.roots_card, 0, 0)
#         counter_layout.addWidget(self.patterns_card, 0, 1)
#         counter_layout.addWidget(self.derivatives_card, 1, 0)
#         counter_layout.addWidget(self.tree_card, 1, 1)

#         main_layout.addLayout(counter_layout)

#         # ---------- Quick Action Cards ----------
#         actions_label = QLabel("⚡ إجراءات سريعة")
#         actions_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2C2416;")
#         main_layout.addWidget(actions_label)

#         actions_layout = QHBoxLayout()
#         actions_layout.setSpacing(20)
#         actions_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

#         self.add_card = self._create_action_card("➕", "إضافة جذر")
#         self.gen_card = self._create_action_card("✨", "توليد كلمة")
#         self.val_card = self._create_action_card("✅", "تحقق")
#         self.deriv_card = self._create_action_card("📚", "المشتقات")

#         actions_layout.addWidget(self.add_card)
#         actions_layout.addWidget(self.gen_card)
#         actions_layout.addWidget(self.val_card)
#         actions_layout.addWidget(self.deriv_card)

#         main_layout.addLayout(actions_layout)

#         # ---------- Charts (Integrated) ----------
#         charts_label = QLabel("📊 إحصائيات مرئية")
#         charts_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2C2416;")
#         main_layout.addWidget(charts_label)

#         from .charts_widget import StatisticsChartsWidget
#         self.charts = StatisticsChartsWidget(self.engine)
#         self.charts.setMinimumHeight(300)
#         self.charts.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
#         main_layout.addWidget(self.charts, 1)   # takes extra vertical space

#         # ---------- Recent Activity ----------
#         activity_label = QLabel("🕒 آخر النشاطات")
#         activity_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2C2416;")
#         main_layout.addWidget(activity_label)

#         self.activity_list = QListWidget()
#         self.activity_list.setMinimumHeight(150)
#         self.activity_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
#         self.activity_list.setStyleSheet("""
#             QListWidget {
#                 background-color: #FAF0E6;
#                 border: 2px solid #C5B5A0;
#                 border-radius: 8px;
#                 padding: 10px;
#             }
#         """)
#         self._update_activity_feed()
#         main_layout.addWidget(self.activity_list)

#         scroll.setWidget(container)

#         wrapper = QVBoxLayout(self)
#         wrapper.setContentsMargins(0, 0, 0, 0)
#         wrapper.addWidget(scroll)

#     # ---------- Counter Card ----------
#     def _create_counter_card(self, emoji, label, value):
#         card = QFrame()
#         card.setFrameShape(QFrame.Shape.StyledPanel)
#         card.setStyleSheet("""
#             QFrame {
#                 background-color: #F5EFE6;
#                 border: 2px solid #C5B5A0;
#                 border-radius: 12px;
#                 padding: 15px;
#             }
#         """)
#         card.setMinimumHeight(120)
#         card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

#         layout = QVBoxLayout(card)
#         top = QHBoxLayout()
#         emoji_lbl = QLabel(emoji)
#         emoji_lbl.setStyleSheet("font-size: 28pt;")
#         label_lbl = QLabel(label)
#         label_lbl.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2C2416;")
#         top.addWidget(emoji_lbl)
#         top.addWidget(label_lbl)
#         top.addStretch()
#         layout.addLayout(top)

#         self.value_lbl = QLabel(str(value))
#         self.value_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.value_lbl.setStyleSheet("font-size: 24pt; font-weight: bold; color: #6B5B95;")
#         layout.addWidget(self.value_lbl)

#         card.value_label = self.value_lbl
#         return card

#     # ---------- Quick Action Card ----------
#     def _create_action_card(self, emoji, text):
#         card = QFrame()
#         card.setFrameShape(QFrame.Shape.StyledPanel)
#         card.setStyleSheet("""
#             QFrame {
#                 background-color: #F5EFE6;
#                 border: 2px solid #C5B5A0;
#                 border-radius: 12px;
#                 padding: 10px;
#             }
#             QFrame:hover {
#                 background-color: #E8DCC8;
#                 border-color: #6B5B95;
#             }
#         """)
#         card.setFixedSize(150, 150)

#         layout = QVBoxLayout(card)
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         emoji_lbl = QLabel(emoji)
#         emoji_lbl.setStyleSheet("font-size: 36pt;")
#         text_lbl = QLabel(text)
#         text_lbl.setStyleSheet("font-size: 12pt; font-weight: bold; color: #2C2416;")
#         text_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(emoji_lbl)
#         layout.addWidget(text_lbl)

#         card.mousePressEvent = lambda e, t=text: self._on_action_clicked(t)
#         return card

#     def _on_action_clicked(self, action):
#         main = self.window()
#         if hasattr(main, 'tabs'):
#             if action == "إضافة جذر":
#                 main.tabs.setCurrentWidget(main.roots_widget)
#             elif action == "توليد كلمة":
#                 main.tabs.setCurrentWidget(main.generation_widget)
#             elif action == "تحقق":
#                 main.tabs.setCurrentWidget(main.validation_widget)
#             elif action == "المشتقات":
#                 main.tabs.setCurrentWidget(main.derivatives_widget)
#         self._add_activity(f"🖱️ {action}")

#     # ---------- Activity Feed ----------
#     def _add_activity(self, text):
#         from datetime import datetime
#         timestamp = datetime.now().strftime("%H:%M:%S")
#         self.recent_actions.insert(0, f"[{timestamp}] {text}")
#         self.recent_actions = self.recent_actions[:10]
#         self._update_activity_feed()

#     def _update_activity_feed(self):
#         self.activity_list.clear()
#         if self.recent_actions:
#             for a in self.recent_actions:
#                 self.activity_list.addItem(a)
#         else:
#             self.activity_list.addItem("✨ لا توجد نشاطات بعد")

#     # ---------- Timer ----------
#     def _start_refresh_timer(self):
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self._update_stats)
#         self.timer.start(5000)

#     def _update_stats(self):
#         stats = self.engine.get_engine_statistics()
#         self.roots_card.value_label.setText(str(stats['roots_count']))
#         self.patterns_card.value_label.setText(str(stats['patterns_count']))
#         self.derivatives_card.value_label.setText(str(stats['generated_words_count']))
#         self.tree_card.value_label.setText(str(stats['avl_tree_height']))
#         self.charts.refresh()
#         self._add_activity("🔄 تحديث تلقائي")

#     def refresh(self):
#         self._update_stats()

#     def closeEvent(self, event):
#         self.timer.stop()
#         super().closeEvent(event)
        

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
        self.refresh()

    def _setup_ui(self):
        # Outer scroll area – expands to fill tab
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

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
        title.setStyleSheet("font-size: 25pt; font-weight: bold; color: #2C2416; padding: 10px;")
        title.setMinimumHeight(50)
        main_layout.addWidget(title)

        desc = QLabel("اكتشف وأضف الجذور العربية مع تحليل تصنيفها الصرفي")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("font-size: 15pt; color: #5A4E3A; font-style: italic;")
        desc.setWordWrap(True)
        desc.setMinimumHeight(30)
        main_layout.addWidget(desc)

        # ---------- ADD ROOT CARD ----------
        add_card = CardWidget("إضافة جذر جديد")
        input_layout = QHBoxLayout()
        input_label = QLabel("الجذر:")
        input_label.setFixedWidth(60)
        input_label.setStyleSheet("background: transparent; border: none; font-size: 13pt; padding: 5px;")
        input_label.setMinimumHeight(45)
        input_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # self.root_input = QLineEdit()
        self.root_input = ArabicUtils.create_arabic_line_edit("مثال: درس")
        self.root_input.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.root_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.root_input.setMinimumHeight(40)
        self.root_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.root_input.returnPressed.connect(self._add_root)
        self.root_input.setToolTip("أدخل جذراً ثلاثياً. سيتم توسعة الشدة تلقائياً.")

        add_btn = QPushButton("إضافة")
        add_btn.setMinimumWidth(100)
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
        search_label.setStyleSheet("background: transparent; border: none; font-size: 13pt; padding: 5px;")
        search_label.setMinimumHeight(45)

        self.search_combo = QComboBox()
        self.search_combo.setEditable(False)                # allow typing
        self.search_combo.setPlaceholderText("ابحث عن جذر...")
        self.search_combo.setMinimumHeight(50)
        self.search_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.search_combo.setToolTip("اختر أو اكتب جذراً للبحث عنه")

        search_btn = QPushButton("بحث")
        search_btn.setMinimumWidth(100)
        search_btn.setMinimumHeight(50)
        search_btn.clicked.connect(self._search_root)

        analyze_btn = QPushButton("تحليل")
        analyze_btn.setMinimumWidth(100)
        analyze_btn.setMinimumHeight(50)
        analyze_btn.clicked.connect(self._analyze_root)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_combo, 1)
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
        return ArabicUtils.normalize_arabic(root, expand_shadda=True, preserve_alif_maqsura = True)

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
        root = self.search_combo.currentText().strip()
        if not root:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار جذر للبحث")
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
                for deriv in derivatives[:10]:
                    info += f"<li><b>{deriv['word']}</b> (الوزن: {deriv['pattern']}, التكرار: {deriv['frequency']})</li>"
                if len(derivatives) > 10:
                    info += f"<li>... و {len(derivatives)-10} مشتق آخر</li>"
                info += "</ul>"
            else:
                info += "<p><i>لا توجد مشتقات لهذا الجذر بعد.</i></p>"

            dialog = QDialog(self)
            dialog.setWindowTitle(f"معلومات الجذر: {root}")
            dialog.setMinimumSize(600, 400)
            dialog.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

            layout = QVBoxLayout(dialog)
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

            close_btn = QPushButton("إغلاق")
            close_btn.setMinimumHeight(40)
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)

            dialog.exec()
        else:
            QMessageBox.warning(self, "غير موجود", f"الجذر '{root}' غير موجود في الشجرة")
    # ---------- ANALYZE ROOT ----------
    def _analyze_root(self):
        root = self.search_combo.currentText().strip() or self.root_input.text().strip()
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
        self.search_combo.clear()
        roots = self.engine.roots_tree.display_inorder()
        self.search_combo.addItems(roots)
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
        title.setStyleSheet("font-size: 25pt; font-weight: bold; color: #2C2416; padding: 10px;")
        title.setMinimumHeight(40)
        main_layout.addWidget(title)

        desc = QLabel("أضف، عدل، أو احذف الأوزان الصرفية للنظام")        
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("font-size: 15pt; color: #5A4E3A; font-style: italic;")
        desc.setWordWrap(True)
        desc.setMinimumHeight(30)
        main_layout.addWidget(desc)
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
        header = self.patterns_table.horizontalHeader()
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
        self.patterns_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.patterns_table.verticalHeader().setDefaultSectionSize(30) 
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