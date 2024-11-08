import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QRadioButton,
                             QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QGraphicsDropShadowEffect, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

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
        """)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 5)
        self.setGraphicsEffect(self.shadow)

class RegistrationForm(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Registration')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        main_layout = QVBoxLayout(self)

        container = QWidget(self)
        container.setStyleSheet("""
            background-color: white;
            border-radius: 40px;
        """)
        container.setFixedSize(1120, 680)  # Reduced height to move it up
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 10)
        container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 20, 40, 20)  # Reduced top and bottom margins
        container_layout.setSpacing(15)  # Reduced spacing

        title = QLabel("Registration")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #71B89A; margin-bottom: 10px;")  # Reduced margin
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(15)  # Reduced vertical spacing
        form_layout.setHorizontalSpacing(10)

        fields = [
            ("First Name:", 0, 0, 1), ("Address:", 0, 3, 4),
            ("Middle Name:", 1, 0, 1), ("City:", 1, 3, 4),
            ("Last Name:", 2, 0, 1), ("Zip:", 2, 3, 4),
            ("Date of Birth:", 3, 0, 1), ("State:", 3, 3, 4),
            ("Email Address:", 4, 0, 1), ("Country:", 4, 3, 4),
            ("Password:", 5, 0, 1),
            ("Phone Number:", 6, 0, 1), ("Gender:", 6, 3, 4),
        ]

        self.input_fields = {}

        for label_text, row, col, input_col in fields:
            label = QLabel(label_text)
            label.setStyleSheet("color: #23465A; font-size: 14px; padding-right: 10px;")
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            form_layout.addWidget(label, row, col)

            if label_text == "Gender:":
                gender_layout = QHBoxLayout()
                self.female_radio = QRadioButton("Female")
                self.male_radio = QRadioButton("Male")
                self.female_radio.setStyleSheet("color: #23465A; font-size: 14px;")
                self.male_radio.setStyleSheet("color: #23465A; font-size: 14px;")
                gender_layout.addWidget(self.female_radio)
                gender_layout.addWidget(self.male_radio)
                gender_layout.addStretch()
                form_layout.addLayout(gender_layout, row, input_col)
            else:
                input_field = QLineEdit()
                input_field.setStyleSheet("""
                    background-color: #F0F0F0;
                    border: none;
                    border-radius: 20px;
                    padding: 10px 15px;
                    font-size: 14px;
                    color: #555;
                """)
                input_field.setFixedHeight(40)
                form_layout.addWidget(input_field, row, input_col)
                self.input_fields[label_text.replace(":", "").lower().replace(" ", "_")] = input_field

        container_layout.addLayout(form_layout)

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["Name", "Email", "User ID"])
        self.user_table.setStyleSheet("""
            QTableWidget {
                background-color: #F0F0F0;
                border: none;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #71B89A;
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 10px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 10px;
            }
            QTableWidget::item {
                color: black;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #71B89A;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setFixedHeight(150)  # Further reduced height
        container_layout.addWidget(self.user_table)
        self.load_users()

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        add_user_btn = AnimatedButton("Add User")
        cancel_btn = AnimatedButton("Cancel")
        submit_btn = AnimatedButton("Submit")

        for btn in [add_user_btn, cancel_btn, submit_btn]:
            btn.setFixedSize(200, 50)
            if btn == submit_btn:
                btn.clicked.connect(self.submit_form)
            elif btn == cancel_btn:
                btn.clicked.connect(self.cancel_form)
            else:
                btn.clicked.connect(self.button_clicked)
            button_layout.addWidget(btn)

        container_layout.addLayout(button_layout)
        main_layout.addWidget(container, alignment=Qt.AlignCenter)
        main_layout.setAlignment(Qt.AlignCenter)  # Center the container vertically

    def submit_form(self):
        # Get input from the fields
        first_name = self.input_fields['first_name'].text()
        middle_name = self.input_fields['middle_name'].text()
        last_name = self.input_fields['last_name'].text()
        date_of_birth = self.input_fields['date_of_birth'].text()
        email = self.input_fields['email_address'].text()
        password = self.input_fields['password'].text()
        phone_number = self.input_fields['phone_number'].text()
        address = self.input_fields['address'].text()
        city = self.input_fields['city'].text()
        zip_code = self.input_fields['zip'].text()
        state = self.input_fields['state'].text()
        country = self.input_fields['country'].text()
        gender = 'Female' if self.female_radio.isChecked() else 'Male' if self.male_radio.isChecked() else ''

        # Prepare the data payload
        data = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "email": email,
            "password": password,
            "phone_number": phone_number,
            "address": address,
            "city": city,
            "zip_code": zip_code,
            "state": state,
            "country": country,
            "gender": gender
        }

        try:
            # Send the POST request with JSON data
            response = requests.post("http://127.0.0.1:8081/register", json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print("Raw API response:", data) # Added line

            # Check if registration was successful
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "User registered successfully!")
                self.main_window.show_profile_page()
            else:
                QMessageBox.warning(self, "Registration Failed", "Invalid data or server error.")

        except requests.exceptions.RequestException as e:
            # Handle connection errors or other exceptions
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def cancel_form(self):
        if self.main_window:
            self.main_window.show_login_page()

    def button_clicked(self):
        sender = self.sender()
        if sender.text() == "Add User" and self.main_window:
            self.main_window.show_session_overview()
        else:
            print(f"{sender.text()} button clicked")

    def load_users(self):
        try:
            response = requests.get("http://127.0.0.1:8081/getusers")
            if response.status_code == 200:
                data = response.json()
                users = data.get('users', [])
                print("Raw user data:", users)  # Debug print

                # Clear existing rows
                self.user_table.setRowCount(0)

                # Add new rows
                for user in users:
                    row_position = self.user_table.rowCount()
                    self.user_table.insertRow(row_position)

                    # Combine first and last name
                    full_name = f"{user['first_name']} {user['last_name']}"

                    # Get user ID
                    user_id = f"{user['user_id']}"

                    # Set items in the table
                    self.user_table.setItem(row_position, 0, QTableWidgetItem(full_name))
                    self.user_table.setItem(row_position, 1, QTableWidgetItem(user['email']))
                    self.user_table.setItem(row_position, 2, QTableWidgetItem(user_id))

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to load users: {str(e)}")
        except KeyError as e:
            QMessageBox.critical(self, "Error", f"Unexpected data format: {str(e)}")
            print("Error details:", str(e))  # Debug print

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QWidget()
    registration_form = RegistrationForm(main_window)
    registration_form.show()
    sys.exit(app.exec_())