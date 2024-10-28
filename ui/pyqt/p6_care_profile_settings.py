import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QFrame, QSizePolicy, QGraphicsDropShadowEffect, QGridLayout)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint

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

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Care Profile Settings')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.createHeader())
        main_layout.addWidget(self.createMainContent())
        main_layout.addWidget(self.createBottomSection())

    def createHeader(self):
        header_container = QWidget(self)
        header_container.setStyleSheet("background-color: white;")
        header_container.setFixedHeight(80)
        header_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 2)
        header_container.setGraphicsEffect(shadow)

        header_inner_layout = QHBoxLayout(header_container)
        header_inner_layout.setContentsMargins(20, 0, 20, 0)
        header_inner_layout.setSpacing(20)

        logo_label = QLabel(self)
        pixmap = QPixmap('images/v20_308.png')
        scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        header_inner_layout.addWidget(logo_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_title = QLabel('Care Profile Settings', self)
        header_title.setFont(QFont('Arial', 28, QFont.Bold))
        header_title.setStyleSheet("color: #71B89A;")
        header_inner_layout.addWidget(header_title, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_inner_layout.addStretch()

        sign_out_button = AnimatedButton("Sign Out", self)
        sign_out_button.setFixedSize(120, 50)
        header_inner_layout.addWidget(sign_out_button, alignment=Qt.AlignRight | Qt.AlignVCenter)

        return header_container

    def createMainContent(self):
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(40)

        content_layout.addWidget(self.createLeftColumn())
        content_layout.addWidget(self.createRightColumn())

        return content

    def createLeftColumn(self):
        left_column = QFrame()
        left_column.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 10)
        left_column.setGraphicsEffect(shadow)

        left_layout = QVBoxLayout(left_column)
        left_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        left_layout.setSpacing(20)
        left_layout.setContentsMargins(20, 20, 20, 20)

        profile_pic_container = QLabel()
        profile_pixmap = QPixmap("images/v25_505.png")
        profile_pic_container.setPixmap(profile_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        profile_pic_container.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(profile_pic_container, alignment=Qt.AlignLeft)

        info_labels = ["Username", "Full Name", "Email"]
        for label in info_labels:
            info_label = QLabel(label)
            info_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
            info_label.setAlignment(Qt.AlignLeft)
            left_layout.addWidget(info_label)

        left_layout.addStretch(1)

        return left_column

    def createRightColumn(self):
        right_column = QFrame()
        right_column.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 10)
        right_column.setGraphicsEffect(shadow)

        right_layout = QVBoxLayout(right_column)
        right_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        right_layout.setSpacing(20)
        right_layout.setContentsMargins(20, 20, 20, 20)

        reset_label = QLabel("Reset")
        reset_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        right_layout.addWidget(reset_label)

        buttons = ["Password", "Email", "Edit Users"]
        for text in buttons:
            button = self.create_settings_button(text)
            right_layout.addWidget(button)

        right_layout.addStretch(1)

        return right_column

    def createBottomSection(self):
        section = QFrame()
        layout = QHBoxLayout(section)
        layout.setContentsMargins(50, 0, 50, 20)
        layout.setSpacing(10)

        help_button = AnimatedButton('Help', self)
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

        back_button = AnimatedButton('Back', self)
        back_button.setFixedSize(120, 50)
        back_button.setStyleSheet("""
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
        layout.addWidget(back_button, alignment=Qt.AlignRight | Qt.AlignBottom)

        return section

    def create_settings_button(self, text):
        button = AnimatedButton(text, self)
        button.setStyleSheet("""
            QPushButton {
                background-color: #C1F0D1;
                color: black;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #A9E4BC;
            }
        """)
        button.setFixedSize(200, 50)
        button.clicked.connect(lambda: print(f"{text} button clicked"))
        return button

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#71B89A"))
        gradient.setColorAt(1, QColor("#5A9A7F"))
        painter.fillRect(self.rect(), gradient)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())