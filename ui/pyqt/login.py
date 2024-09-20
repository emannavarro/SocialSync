import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SocialSync Care')
        self.setFixedSize(1280, 720)  # Set fixed size to 1280x720 pixels
        self.setStyleSheet("""
              QWidget {
                  background-color: #71B89A;
              }
          """)

        # Container for login elements
        container = QFrame(self)
        container.setFixedSize(700, 700)  # Fixed size for the container
        container.setStyleSheet("background-color: #FFFFFF; border-radius: 20px;")
        # container.move(440, 150)  # Adjust position to center the container
        container.move(290, 10)  # Adjust position to center the container

        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)  # Margins inside the container

        # Placeholder for the logo
        logoLabel = QLabel('Logo')
        logoLabel.setFont(QFont('Arial', 20))
        logoLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(logoLabel)

        # Title
        titleLabel = QLabel('SocialSync Care')
        titleLabel.setFont(QFont('Arial', 24))
        titleLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(titleLabel)

        # Username Field
        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setPlaceholderText("Username")
        self.setupLineEdit(self.usernameLineEdit)
        layout.addWidget(self.usernameLineEdit)

        # Password Field
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setPlaceholderText("Password")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.setupLineEdit(self.passwordLineEdit)
        layout.addWidget(self.passwordLineEdit)

        # Sign In Button
        signInButton = QPushButton("Sign In")
        self.setupButton(signInButton, "#00897B", "#00695C")  # Adjust the button color
        signInButton.clicked.connect(lambda: print("Sign In button clicked"))
        layout.addWidget(signInButton)

        # New User Button
        newUserButton = QPushButton("New User?")
        self.setupButton(newUserButton, "#B2DFDB", "#80CBC4")  # Lighter color button
        newUserButton.clicked.connect(lambda: print("New User button clicked"))
        layout.addWidget(newUserButton)

        # Forgot Password Link
        forgotPassLabel = QLabel("Forgot Password?")
        forgotPassLabel.setFont(QFont('Arial', 12))
        forgotPassLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(forgotPassLabel)

    def setupLineEdit(self, lineEdit):
        lineEdit.setFont(QFont('Arial', 16))
        lineEdit.setStyleSheet("QLineEdit { border: 2px solid #B2DFDB; border-radius: 10px; padding: 5px; background-color: #FFFFFF; }")

    def setupButton(self, button, color, hoverColor):
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(f"QPushButton {{ background-color: {color}; color: black; border-radius: 10px; padding: 10px; }}"
                             f"QPushButton:hover {{ background-color: {hoverColor}; }}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LoginPage()
    ex.show()
    sys.exit(app.exec_())
