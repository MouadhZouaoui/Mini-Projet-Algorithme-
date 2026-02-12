"""
AVL Tree Visualizer using QGraphicsView
Draws nodes with root text, height/balance info, and animated layout.
"""
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QBrush, QPen, QColor, QFont, QPainter


class AVLTreeVisualizer(QGraphicsView):
    """Interactive AVL tree visualizer with automatic positioning."""

    def __init__(self, tree, parent=None):
        super().__init__(parent)
        self.tree = tree
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setBackgroundBrush(QBrush(QColor("#F5EFE6")))
        self.node_radius = 25
        self.level_height = 80
        self.refresh()

    def refresh(self):
        """Redraw the tree from root."""
        self.scene.clear()
        if self.tree.root is None:
            text = self.scene.addText("🌳 الشجرة فارغة")
            text.setDefaultTextColor(QColor("#5A4E3A"))
            text.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            text.setPos(10, 10)
            return
        self._draw_node(self.tree.root, 0, 0, 250)  # start x offset

    def _draw_node(self, node, x, y, x_offset):
        """Recursively draw node and its children."""
        if node is None:
            return

        # ----- Node circle -----
        ellipse = QGraphicsEllipseItem(
            QRectF(x - self.node_radius, y - self.node_radius,
                   2 * self.node_radius, 2 * self.node_radius)
        )
        ellipse.setBrush(QBrush(QColor("#6B5B95")))
        ellipse.setPen(QPen(QColor("#2C2416"), 2))
        self.scene.addItem(ellipse)

        # ----- Root text -----
        text = QGraphicsTextItem(node.root)
        text.setDefaultTextColor(QColor("white"))
        text.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        text.setPos(
            x - text.boundingRect().width() / 2,
            y - text.boundingRect().height() / 2
        )
        self.scene.addItem(text)

        # ----- Height info (small label) -----
        height_text = QGraphicsTextItem(f"h={node.height}")
        height_text.setDefaultTextColor(QColor("#2C2416"))
        height_text.setFont(QFont("Arial", 8))
        height_text.setPos(x + self.node_radius + 5, y - self.node_radius - 15)
        self.scene.addItem(height_text)

        # ----- Draw left child -----
        if node.left:
            child_x = x - x_offset
            child_y = y + self.level_height
            self._draw_node(node.left, child_x, child_y, x_offset / 1.8)
            # Draw edge
            self.scene.addLine(
                x, y + self.node_radius,
                child_x, child_y - self.node_radius,
                QPen(QColor("#C5B5A0"), 2)
            )

        # ----- Draw right child -----
        if node.right:
            child_x = x + x_offset
            child_y = y + self.level_height
            self._draw_node(node.right, child_x, child_y, x_offset / 1.8)
            self.scene.addLine(
                x, y + self.node_radius,
                child_x, child_y - self.node_radius,
                QPen(QColor("#C5B5A0"), 2)
            )

    def wheelEvent(self, event):
        """Enable zoom with mouse wheel."""
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        if event.angleDelta().y() > 0:
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.scale(zoom_out_factor, zoom_out_factor)