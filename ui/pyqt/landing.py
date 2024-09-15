import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget,
    QLabel, QLineEdit, QCheckBox, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush, QColor, QIcon
from PyQt5.QtCore import Qt

from ui.pyqt.login import LoginPage


class LandingPage(QWidget):
    def __init__(self, parent=None):
        super(LandingPage, self).__init__(parent)

        self.setAutoFillBackground(True)
        palette = self.palette()
        background = QPixmap("../background.jpg").scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        gradient = QBrush(QColor(0, 0, 0, 150))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setSpacing(40)
        self.setLayout(layout)

        title = QLabel("Welcome to SocialSync")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: white;
            font-size: 42px;
            font-weight: bold;
            text-shadow: 2px 2px 5px #000000;
        """)
        title_font = QFont("Arial", 42, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)

        btn_login = QPushButton("Login")
        btn_register = QPushButton("Register")
        btn_style = """
            QPushButton {
                background-color: #1E90FF;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 15px 30px;
                border-radius: 15px;
                border: 2px solid #1E90FF;
                box-shadow: 3px 3px 10px #000000;
            }
            QPushButton:hover {
                background-color: #4682B4;
                border: 2px solid #4682B4;
                transform: scale(1.05);
            }
        """
        btn_login.setStyleSheet(btn_style)
        btn_register.setStyleSheet(btn_style)

        layout.addWidget(btn_login)
        layout.addWidget(btn_register)

        btn_login.clicked.connect(lambda: parent.show_login_page())
        btn_register.clicked.connect(lambda: parent.show_register_page())



class RegisterPage(QWidget):
    def __init__(self, parent=None):
        super(RegisterPage, self).__init__(parent)

        layout = QVBoxLayout()
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setSpacing(20)
        self.setLayout(layout)

        title = QLabel("Register")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Username field
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet("""
            QLineEdit {
                background-color: #333;
                color: white;
                font-size: 18px;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #1E90FF;
            }
            QLineEdit:focus {
                border: 2px solid #4682B4;
            }
        """)
        layout.addWidget(self.username)

        # Email field
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        self.email.setStyleSheet("""
            QLineEdit {
                background-color: #333;
                color: white;
                font-size: 18px;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #1E90FF;
            }
            QLineEdit:focus {
                border: 2px solid #4682B4;
            }
        """)
        layout.addWidget(self.email)

        # Password field
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("""
            QLineEdit {
                background-color: #333;
                color: white;
                font-size: 18px;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #1E90FF;
            }
            QLineEdit:focus {
                border: 2px solid #4682B4;
            }
        """)
        layout.addWidget(self.password)

        # Register button
        btn_register = QPushButton("Register")
        btn_register.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 15px 30px;
                border-radius: 15px;
                border: 2px solid #1E90FF;
                box-shadow: 3px 3px 10px #000000;
            }
            QPushButton:hover {
                background-color: #4682B4;
                border: 2px solid #4682B4;
                transform: scale(1.05);
            }
        """)
        layout.addWidget(btn_register)

        # Back button to return to the landing page
        btn_back = QPushButton("Back")
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 10px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        btn_back.clicked.connect(lambda: parent.show_landing_page())
        layout.addWidget(btn_back)

