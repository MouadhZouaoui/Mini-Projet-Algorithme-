"""
Splash Screen with animated progress and elegant design.
"""
from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import (
    QPixmap, QPainter, QColor, QPen, QBrush,
    QLinearGradient, QFont
)


class SplashScreen(QSplashScreen):
    """Custom splash screen with gradient background and progress bar."""

    def __init__(self):
        # Create base pixmap
        pixmap = QPixmap(700, 450)
        pixmap.fill(Qt.GlobalColor.transparent)
        super().__init__(pixmap)
        self.progress = 0
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def drawContents(self, painter):
        """Custom paint event with gradient and text."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#6B5B95"))
        gradient.setColorAt(1, QColor("#8573B3"))
        painter.fillRect(self.rect(), QBrush(gradient))

        # Draw rounded rectangle border
        painter.setPen(QPen(QColor("#C5B5A0"), 4))
        painter.drawRoundedRect(2, 2, self.width()-4, self.height()-4, 20, 20)

        # Title
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "🌙")

        painter.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        painter.drawText(
            self.rect().adjusted(0, 80, 0, 0),
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
            "المحرك المورفولوجي"
        )

        # Subtitle
        painter.setFont(QFont("Arial", 14, QFont.Weight.Normal))
        painter.drawText(
            self.rect().adjusted(0, 140, 0, 0),
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
            "للبحث في الجذور العربية وأوزانها"
        )

        # Progress bar background
        bar_x = 150
        bar_y = self.height() - 100
        bar_width = self.width() - 300
        bar_height = 20
        painter.fillRect(bar_x, bar_y, bar_width, bar_height, QColor("#E8DCC8"))

        # Progress fill
        fill_width = int(bar_width * self.progress / 100)
        painter.fillRect(bar_x, bar_y, fill_width, bar_height, QColor("#4CAF50"))

        # Progress text
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        painter.drawText(
            bar_x + bar_width + 20, bar_y + 16,
            f"{self.progress}%"
        )

        # Loading message
        if self.progress < 30:
            msg = "جاري تهيئة المحرك..."
        elif self.progress < 60:
            msg = "جاري تحميل الجذور..."
        elif self.progress < 90:
            msg = "جاري تحميل الأوزان..."
        else:
            msg = "جاهز للتشغيل!"

        painter.setFont(QFont("Arial", 12, QFont.Weight.Normal))
        painter.drawText(
            bar_x, bar_y - 30,
            bar_width, 30,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
            msg
        )

    def updateProgress(self, value):
        """Update progress value and repaint."""
        self.progress = value
        self.repaint()  # Use repaint() instead of repaint() to force immediate redraw