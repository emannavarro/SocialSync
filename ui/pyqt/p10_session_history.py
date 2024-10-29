import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QFrame, QHBoxLayout, QScrollArea,
                             QSizePolicy, QGraphicsDropShadowEffect, QGridLayout)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QPoint, QTimer

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #71B89A;
                color: white;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #5A9A7F;
            }
            QPushButton:pressed {
                background-color: #4A8A6F;
            }
        """)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 5)
        self.setGraphicsEffect(self.shadow)

    def enterEvent(self, event):
        self.animate_shadow(25, 0, 8)

    def leaveEvent(self, event):
        self.animate_shadow(15, 0, 5)

    def animate_shadow(self, end_blur, end_x, end_y):
        self.anim_blur = QPropertyAnimation(self.shadow, b"blurRadius")
        self.anim_blur.setEndValue(end_blur)
        self.anim_blur.setDuration(200)

        self.anim_offset = QPropertyAnimation(self.shadow, b"offset")
        self.anim_offset.setEndValue(QPoint(end_x, end_y))
        self.anim_offset.setDuration(200)

        self.anim_blur.start()
        self.anim_offset.start()

class HistoryPage(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("History")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.createHeader())
        main_layout.addWidget(self.createMainContent())
        main_layout.addWidget(self.createBottomSection())

    def createHeader(self):
        header_container = QWidget()
        header_container.setStyleSheet("background-color: white;")
        header_container.setFixedHeight(80)
        header_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 2)
        header_container.setGraphicsEffect(shadow)

        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.setSpacing(20)

        logo_label = QLabel()
        pixmap = QPixmap("images/v20_308.png")
        scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        header_layout.addWidget(logo_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        title_label = QLabel("History")
        title_label.setFont(QFont('Arial', 28, QFont.Bold))
        title_label.setStyleSheet("color: #71B89A;")
        header_layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_layout.addStretch()

        sign_out_button = AnimatedButton("Sign Out")
        sign_out_button.setFixedSize(120, 50)
        header_layout.addWidget(sign_out_button, alignment=Qt.AlignRight | Qt.AlignVCenter)

        return header_container

    def createMainContent(self):
        content = QScrollArea()
        content.setWidgetResizable(True)
        content.setStyleSheet("background-color: transparent; border: none;")
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(20)

        sessions_label = QLabel("Sessions:")
        sessions_label.setFont(QFont('Arial', 32, QFont.Bold))
        sessions_label.setStyleSheet("color: white;")
        content_layout.addWidget(sessions_label)

        sessions = [
            {"name": "John Doe", "date": "02-20-2024", "time_elapsed": "2hrs 30mins"},
            {"name": "John Doe", "date": "03-25-2024", "time_elapsed": "30mins"},
            {"name": "Jane Smith", "date": "04-01-2024", "time_elapsed": "1hr 45mins"},
            {"name": "Alice Johnson", "date": "04-05-2024", "time_elapsed": "45mins"},
            {"name": "Bob Williams", "date": "04-10-2024", "time_elapsed": "3hrs 15mins"},
        ]

        for session in sessions:
            session_widget = self.create_session_widget(session)
            content_layout.addWidget(session_widget)

        content_layout.addStretch(1)
        content.setWidget(content_widget)

        return content

    def create_session_widget(self, session):
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        layout = QHBoxLayout(widget)

        name_date = QLabel(f"{session['name']} {session['date']}")
        name_date.setStyleSheet("color: white; font-size: 18px;")

        time_elapsed = QLabel(f"Time Elapsed: {session['time_elapsed']}")
        time_elapsed.setStyleSheet("color: white; font-size: 18px;")

        layout.addWidget(name_date)
        layout.addStretch(1)
        layout.addWidget(time_elapsed)

        return widget

    def createBottomSection(self):
        section = QFrame()
        layout = QHBoxLayout(section)
        layout.setContentsMargins(50, 0, 50, 20)
        layout.setSpacing(10)

        help_button = AnimatedButton('Help')
        help_button.setFixedSize(120, 50)
        help_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #39687C;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        layout.addWidget(help_button, alignment=Qt.AlignLeft | Qt.AlignBottom)

        layout.addStretch()

        back_button = AnimatedButton('Back')
        back_button.setFixedSize(120, 50)
        layout.addWidget(back_button, alignment=Qt.AlignRight | Qt.AlignBottom)

        return section

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#71B89A"))
        gradient.setColorAt(1, QColor("#5A9A7F"))
        painter.fillRect(self.rect(), gradient)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HistoryPage()
    window.show()
    sys.exit(app.exec_())