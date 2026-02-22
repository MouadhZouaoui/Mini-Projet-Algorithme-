"""
Statistics Charts Widget
Displays root type distribution and generation activity using PyQtGraph.
"""
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt6.QtCore import Qt

from root_classifier import RootClassifier
from arabic_utils import ArabicUtils


class StatisticsChartsWidget(QWidget):
    """Widget with interactive charts for engine statistics."""

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        pg.setConfigOptions(antialias=True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # ----- Root Type Distribution Chart -----
        self.root_plot = pg.PlotWidget(title="توزيع أنواع الجذور")
        self.root_plot.setMouseEnabled(False, False)   # disable zoom/pan
        self.root_plot.setMenuEnabled(False) 
        self.root_plot.setLabel('left', 'العدد')
        self.root_plot.setLabel('bottom', 'النوع')
        self.root_plot.setBackground('#F5EFE6')
        self.root_plot.showGrid(x=True, y=True, alpha=0.3)
        self.root_plot.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.root_plot, stretch=2)

        # ----- Generation Activity Chart (roots with derivatives vs without) -----
        self.gen_plot = pg.PlotWidget(title="نشاط التوليد")
        self.gen_plot.setMouseEnabled(False, False)
        self.gen_plot.setMenuEnabled(False)
        self.gen_plot.setLabel('left', 'العدد')
        self.gen_plot.setLabel('bottom', 'الفئة')
        self.gen_plot.setBackground('#F5EFE6')
        self.gen_plot.showGrid(x=True, y=True, alpha=0.3)
        self.gen_plot.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.gen_plot, stretch=2)

        # ----- Refresh Button -----
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        refresh_btn = QPushButton("🔄 تحديث الرسوم البيانية")
        refresh_btn.setMinimumHeight(45)
        refresh_btn.setFixedWidth(250)
        refresh_btn.clicked.connect(self.refresh)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.refresh()

    def refresh(self):
        """Update charts with current engine data."""
        self._update_root_type_chart()
        self._update_generation_chart()

    def _update_root_type_chart(self):
        """Count roots by morphological category and draw bar chart."""
        roots = self.engine.roots_tree.display_inorder()
        counts = {
            "صحيح": 0,
            "مهموز": 0,
            "معتل": 0,
            "مضعف": 0,
            "آخر": 0
        }

        for root in roots:
            normalized = ArabicUtils.normalize_arabic(root, expand_shadda=True)
            analysis = RootClassifier.classify(normalized)
            cat = analysis.category.value
            if cat in counts:
                counts[cat] += 1
            else:
                counts["آخر"] += 1

        categories = list(counts.keys())
        values = list(counts.values())

        self.root_plot.clear()
        x = list(range(len(categories)))
        bg = pg.BarGraphItem(
            x=x, height=values, width=0.6,
            brush=pg.mkBrush(color='#6B5B95'),
            pen=pg.mkPen(color='#2C2416', width=1)
        )
        self.root_plot.addItem(bg)

        axis = self.root_plot.getAxis('bottom')
        axis.setTicks([[(i, cat) for i, cat in enumerate(categories)]])
        axis.setStyle(tickFont=pg.Qt.QtGui.QFont("Arial", 10))

    def _update_generation_chart(self):
        """Show number of roots with derivatives vs without."""
        all_nodes = self.engine.roots_tree.get_all_nodes()
        with_deriv = sum(1 for node in all_nodes if node.get_derivative_count() > 0)
        without_deriv = len(all_nodes) - with_deriv

        self.gen_plot.clear()
        x = [0, 1]
        values = [with_deriv, without_deriv]
        bg = pg.BarGraphItem(
            x=x, height=values, width=0.6,
            brush=pg.mkBrush(color='#8573B3'),
            pen=pg.mkPen(color='#2C2416', width=1)
        )
        self.gen_plot.addItem(bg)

        axis = self.gen_plot.getAxis('bottom')
        axis.setTicks([[ (0, "جذور بمشتقات"), (1, "جذور بدون") ]])
        axis.setStyle(tickFont=pg.Qt.QtGui.QFont("Arial", 10))