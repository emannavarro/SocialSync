import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap, QFontMetrics, QPainter, QColor
from PyQt5.QtCore import Qt


class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.adjustSize()

    def adjustSize(self):
        font = QFont('Arial', 18, QFont.Bold)
        metrics = QFontMetrics(font)
        text_width = metrics.horizontalAdvance(self.text())
        self.setFixedWidth(text_width + 40)  # Add some padding

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw rounded rectangle
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor('white'))
        painter.drawRoundedRect(self.rect(), 25, 25)

        # Draw text
        painter.setPen(QColor('black'))
        painter.setFont(QFont('Arial', 18, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header: Full width, with logo and title
        header_container = QWidget(self)
        header_container.setStyleSheet("background-color: white;")
        header_container.setFixedHeight(80)
        header_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        header_inner_layout = QHBoxLayout(header_container)
        header_inner_layout.setContentsMargins(10, 0, 10, 0)  # Adjusted to match padding
        header_inner_layout.setSpacing(10)  # Add space between elements

        # Logo
        logo_label = QLabel(self)
        pixmap = QPixmap('images/v20_308.png')  # Adjust this path as necessary
        scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        header_inner_layout.addWidget(logo_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        # Title "Home" next to logo
        header_title = QLabel('Home', self)
        header_title.setFont(QFont('Arial', 28, QFont.Bold))
        header_title.setStyleSheet("color: black;")
        header_inner_layout.addWidget(header_title, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_inner_layout.addStretch()

        # Profile, History, and Sign Out buttons on the right
        profile_button = self.create_button('Profile', 120, 50, bg_color="#71B89A", text_color="white")
        history_button = self.create_button('History', 120, 50, bg_color="#71B89A", text_color="white")
        signout_button = self.create_button('Sign Out', 120, 50, bg_color="#71B89A", text_color="white")

        header_inner_layout.addWidget(profile_button, alignment=Qt.AlignRight | Qt.AlignVCenter)
        header_inner_layout.addWidget(history_button, alignment=Qt.AlignRight | Qt.AlignVCenter)
        header_inner_layout.addWidget(signout_button, alignment=Qt.AlignRight | Qt.AlignVCenter)

        main_layout.addWidget(header_container)

        # Centered content layout for welcome text and start button
        centered_layout = QVBoxLayout()
        centered_layout.setContentsMargins(0, 0, 0, 0)
        centered_layout.setAlignment(Qt.AlignCenter)

        # Welcome message
        welcome_label = QLabel("Welcome, John Doe", self)
        welcome_label.setFont(QFont('Arial', 48, QFont.Bold))
        welcome_label.setStyleSheet("color: white;")
        welcome_label.setAlignment(Qt.AlignCenter)
        centered_layout.addWidget(welcome_label)

        # Start button
        start_button = QPushButton("Start", self)
        start_button.setFixedSize(800, 200)
        start_button.setFont(QFont('Arial', 36, QFont.Bold))
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #C1F0D1;
                color: black;
                border-radius: 100px;
            }
            QPushButton:hover {
                background-color: #A9E4BC;
            }
        """)
        centered_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        start_button.clicked.connect(lambda: print("Start button clicked"))

        main_layout.addLayout(centered_layout)

        # Help button at the bottom
        help_button_layout = QHBoxLayout()
        help_button_layout.setContentsMargins(20, 0, 0, 20)  # Padding for bottom-left corner
        help_button = self.create_button('Help', 120, 50, "white", "#39687C")
        help_button_layout.addWidget(help_button, alignment=Qt.AlignLeft)
        help_button_layout.addStretch()
        main_layout.addLayout(help_button_layout)

        self.setLayout(main_layout)

    def create_button(self, text, width, height, bg_color, text_color):
        button = QPushButton(text, self)
        button.setFixedSize(width, height)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: {height // 2}px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #A9A9A9;
            }}
        """)
        return button


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
