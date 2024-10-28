import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QSizePolicy)
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import Qt, QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Profile Settings')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #8FBC8F;")  # Sea Green color

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.createHeader())
        main_layout.addWidget(self.createMainContent())
        main_layout.addWidget(self.createBottomSection())

    def createHeader(self):
        header = QWidget()
        header.setStyleSheet("background-color: white;")
        header.setFixedHeight(80)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        logo_label = QLabel()
        pixmap = QPixmap("images/v20_308.png")
        scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setFixedSize(60, 60)

        title_label = QLabel("Profile Settings")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold;")

        sign_out_button = self.create_button("Sign Out", "#8FBC8F", text_color="white")
        sign_out_button.setFixedSize(120, 40)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        header_layout.addWidget(sign_out_button)

        return header

    def createMainContent(self):
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(40)

        content_layout.addWidget(self.createLeftColumn())

        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("background-color: white;")
        content_layout.addWidget(line)

        content_layout.addWidget(self.createRightColumn())

        return content

    def createLeftColumn(self):
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        left_layout.setSpacing(20)

        profile_pic_container = QLabel()
        profile_pixmap = QPixmap("images/v25_505.png")
        profile_pic_container.setPixmap(profile_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        profile_pic_container.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(profile_pic_container, alignment=Qt.AlignLeft)

        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setAlignment(Qt.AlignLeft)
        info_layout.setSpacing(10)

        info_labels = ["Username", "Full Name", "Email"]
        for label in info_labels:
            info_label = QLabel(label)
            info_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
            info_label.setAlignment(Qt.AlignLeft)
            info_layout.addWidget(info_label)

        left_layout.addWidget(info_container)
        left_layout.addStretch(1)

        return left_column

    def createRightColumn(self):
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        right_layout.setSpacing(20)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Reset section
        reset_label = QLabel("Reset")
        reset_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        right_layout.addWidget(reset_label)

        password_button = self.create_button("Password", "#D3D3D3", text_color="#4682B4")
        email_button = self.create_button("Email", "#D3D3D3", text_color="#4682B4")
        right_layout.addWidget(password_button)
        right_layout.addWidget(email_button)

        right_layout.addSpacing(40)

        # Accounts section
        accounts_label = QLabel("Accounts")
        accounts_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        right_layout.addWidget(accounts_label)

        edit_users_button = self.create_button("Edit Users", "#D3D3D3", text_color="#4682B4")
        right_layout.addWidget(edit_users_button)

        right_layout.addStretch(1)

        return right_column

    def createBottomSection(self):
        bottom_buttons = QWidget()
        bottom_layout = QHBoxLayout(bottom_buttons)
        bottom_layout.setContentsMargins(40, 0, 40, 40)

        help_button = self.create_button("Help", "white", text_color="#8FBC8F")
        back_button = self.create_button("Back", "#4682B4", text_color="white")

        bottom_layout.addWidget(help_button)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(back_button)

        return bottom_buttons

    def create_button(self, text, bg_color, text_color="black"):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 25px;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #A9A9A9;
            }}
        """)
        button.setFixedSize(200, 50)
        button.clicked.connect(lambda: print(f"{text} button clicked"))
        return button


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())