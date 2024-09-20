import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QFrame, QHBoxLayout)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QSize


class CareProfile(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #8FBC8F;")  # Sea Green color

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
        logo_pixmap = QPixmap("path_to_logo.png")  # Replace with actual path
        logo_label.setPixmap(logo_pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        title_label = QLabel("Care Profile")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        sign_out_button = self.create_button("Sign Out", "#8FBC8F", text_color="white")
        sign_out_button.setFixedSize(120, 40)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        header_layout.addWidget(sign_out_button)

        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Left sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)

        info_labels = ["Full Name", "Email", "Caretaker ID"]
        for label in info_labels:
            info_label = QLabel(label)
            info_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
            sidebar_layout.addWidget(info_label)

        # Right content
        right_content = QWidget()
        right_layout = QVBoxLayout(right_content)
        right_layout.setAlignment(Qt.AlignTop)
        right_layout.setSpacing(20)

        reset_label = QLabel("Reset")
        reset_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")

        password_button = self.create_button("Password", "#D3D3D3", text_color="#4682B4")
        email_button = self.create_button("Email", "#D3D3D3", text_color="#4682B4")

        accounts_label = QLabel("Accounts")
        accounts_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")

        edit_users_button = self.create_button("Edit Users", "#D3D3D3", text_color="#4682B4")

        right_layout.addWidget(reset_label)
        right_layout.addWidget(password_button)
        right_layout.addWidget(email_button)
        right_layout.addWidget(accounts_label)
        right_layout.addWidget(edit_users_button)

        # Bottom buttons
        bottom_buttons = QWidget()
        bottom_layout = QHBoxLayout(bottom_buttons)

        help_button = self.create_button("Help", "white", text_color="#8FBC8F")
        back_button = self.create_button("Back", "#4682B4", text_color="white")

        bottom_layout.addWidget(help_button)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(back_button)

        # Add all widgets to the main layout
        main_layout.addWidget(header)
        content_layout.addWidget(sidebar)
        content_layout.addWidget(right_content)
        main_layout.addWidget(content)
        main_layout.addWidget(bottom_buttons)

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
    window = CareProfile()
    window.show()
    sys.exit(app.exec_())