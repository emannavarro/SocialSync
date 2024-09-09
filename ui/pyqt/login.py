import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from backend.controllers.emotion_recognition import detect_face, detect_emotion, preprocess
from PyQt5.QtWidgets import QApplication
import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Emotion Detection")
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.resize(800, 600)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30ms

        self.video = cv2.VideoCapture(0)
        self.class_names = ["Angry", "Happy", "Sad", "Surprise"]

    def update_frame(self):
        ret, frame = self.video.read()
        if ret:
            gray, faces = detect_face(frame)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face_roi_gray = gray[y:y + h, x:x + w]
                face_roi_gray = preprocess(face_roi_gray)
                idx, conf = detect_emotion(face_roi_gray)

                class_name = self.class_names[idx]

                if conf > 0.3:
                    cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Convert the frame to QImage for PyQt display
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.video.release()

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super(LoginPage, self).__init__(parent)

        layout = QVBoxLayout()
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setSpacing(20)
        self.setLayout(layout)

        title = QLabel("Login")
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

        # Login button
        btn_login = QPushButton("Login")
        btn_login.setStyleSheet("""
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
        btn_login.clicked.connect(self.handle_login)  # Connect to login function
        layout.addWidget(btn_login)

    def handle_login(self):
        # Gather login credentials
        email = self.username.text()
        password = self.password.text()

        # Check if fields are empty
        if not email or not password:
            self.show_message("Error", "Please enter both email and password.")
            return

        # Send POST request to Flask backend login endpoint
        try:
            response = requests.post("http://127.0.0.1:8081/login", json={"email": email, "password": password})

            if response.status_code == 200:
                # Login successful, switch to VideoWindow
                self.switch_to_video_window()
            elif response.status_code == 401:
                # Invalid credentials
                self.show_message("Error", "Invalid credentials. Please try again.")
            else:
                # Other errors
                self.show_message("Error", f"An error occurred: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Handle any exceptions during the HTTP request
            self.show_message("Error", f"Failed to connect to server: {str(e)}")

    def switch_to_video_window(self):
        self.hide()  # Hide the login window
        self.video_window = VideoWindow()
        self.video_window.show()

    def show_message(self, title, message):
        # Display a message box with a given title and message
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

def main():
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
