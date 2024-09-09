import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

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

        # First Name field
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("First Name")
        self.first_name.setStyleSheet("""
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
        layout.addWidget(self.first_name)

        # Last Name field
        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Last Name")
        self.last_name.setStyleSheet("""
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
        layout.addWidget(self.last_name)

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
        btn_register.clicked.connect(self.handle_register)  # Connect the register button to the register logic
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

    def handle_register(self):
        # Gather registration information
        first_name = self.first_name.text()
        last_name = self.last_name.text()
        email = self.email.text()
        password = self.password.text()

        # Check if any fields are empty
        if not (first_name and last_name and email and password):
            self.show_message("Error", "All fields are required.")
            return

        # Send POST request to Flask backend register endpoint
        try:
            response = requests.post("http://127.0.0.1:8081/register", json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password
            })

            if response.status_code == 201:
                # Registration successful
                self.show_message("Success", "User registered successfully!")
            elif response.status_code == 400:
                # Missing or invalid fields
                self.show_message("Error", "Missing or invalid information.")
            else:
                # Other errors
                self.show_message("Error", f"An error occurred: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Handle any exceptions during the HTTP request
            self.show_message("Error", f"Failed to connect to server: {str(e)}")

    def show_message(self, title, message):
        # Display a message box with a given title and message
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
