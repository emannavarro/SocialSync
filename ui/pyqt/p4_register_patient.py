import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class RegisterPatient(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.setWindowTitle('Register User')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # White rounded rectangle container
        container = QWidget(self)
        container.setStyleSheet("""
            background-color: white;
            border-radius: 20px;
        """)
        container.setFixedSize(360, 500)
        container_layout = QVBoxLayout(container)

        # Title
        title = QLabel("Register User")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #71B89A;")
        container_layout.addWidget(title)

        # Input fields
        fields = ["First Name", "Last Name", "Email Address", "Password"]
        self.inputs = {}
        for field in fields:
            input_field = QLineEdit()
            input_field.setPlaceholderText(field)
            input_field.setStyleSheet("""
                background-color: #E0E0E0;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
            """)
            container_layout.addWidget(input_field)
            self.inputs[field] = input_field

        # Make password field secure
        self.inputs["Password"].setEchoMode(QLineEdit.Password)

        # Submit button
        submit_btn = QPushButton("Submit")
        submit_btn.setStyleSheet("""
            background-color: #71B89A;
            color: white;
            border-radius: 15px;
            padding: 10px;
            font-size: 18px;
            font-weight: bold;
        """)
        submit_btn.clicked.connect(self.submit_form)
        container_layout.addWidget(submit_btn)

        # Cancel option
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            background-color: transparent;
            color: black;
            border: none;
            font-size: 16px;
        """)
        cancel_btn.clicked.connect(self.close)
        container_layout.addWidget(cancel_btn)

        # Center the container in the main window
        layout.addWidget(container, alignment=Qt.AlignCenter)

    def submit_form(self):
        # Here you would typically process the form data
        print("Form submitted:")
        for field, input_field in self.inputs.items():
            print(f"{field}: {input_field.text()}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegisterPatient()
    ex.show()
    sys.exit(app.exec_())