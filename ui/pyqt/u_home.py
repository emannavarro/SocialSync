import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QFrame, QHBoxLayout)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class HomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #8FBC8F;")  # Sea Green color for background

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet("background-color: white;")
        header.setFixedHeight(80)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        logo_label = QLabel()
        logo_pixmap = QPixmap("path_to_logo.png")  # Replace with actual path to the logo
        logo_label.setPixmap(logo_pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        header_layout.addWidget(logo_label)

        # Right-aligned title label for "Home"
        title_label = QLabel("Home")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        title_label.setAlignment(Qt.AlignRight)  # Align title to the right
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label, alignment=Qt.AlignRight)
        title_layout.setContentsMargins(0, 10, 20, 0)  # Padding from top and right
        header_layout.addLayout(title_layout)

        profile_button = self.create_button("Profile", "#8FBC8F", text_color="white")
        history_button = self.create_button("History", "#8FBC8F", text_color="white")
        sign_out_button = self.create_button("Sign Out", "#8FBC8F", text_color="white")

        header_layout.addStretch(1)
        header_layout.addWidget(profile_button)
        header_layout.addWidget(history_button)
        header_layout.addWidget(sign_out_button)

        # Welcome Label
        welcome_label = QLabel("Welcome, John Doe")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")

        # Start Button (updated with rounded edges and very light green color)
        start_button = self.create_button("Start", "#CCFFCC", text_color="black")  # Very light green color
        start_button.setFixedSize(400, 150)

        # Help Button (positioned at bottom left with padding)
        help_button = self.create_button("Help", "white", text_color="#8FBC8F")
        help_button.setFixedSize(100, 50)

        # Bottom layout for Help button (aligned to bottom left with padding)
        bottom_buttons = QWidget()
        bottom_layout = QHBoxLayout(bottom_buttons)
        bottom_layout.setContentsMargins(20, 0, 0, 20)  # Padding from left and bottom
        bottom_layout.addWidget(help_button)

        # Add widgets to main layout
        main_layout.addWidget(header)
        main_layout.addStretch(1)
        main_layout.addWidget(welcome_label)
        main_layout.addStretch(1)
        main_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)
        main_layout.addWidget(bottom_buttons, alignment=Qt.AlignLeft | Qt.AlignBottom)

    def create_button(self, text, bg_color, text_color="black"):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 20px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #A9A9A9;
            }}
        """)
        button.setFixedSize(200, 40)
        button.clicked.connect(lambda: print(f"{text} button clicked"))
        return button


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomeScreen()
    window.show()
    sys.exit(app.exec_())
