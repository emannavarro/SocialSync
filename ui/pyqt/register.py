from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

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
