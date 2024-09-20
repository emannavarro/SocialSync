import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QFrame)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize


class ProfileSetup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #8FBC8F;")  # Sea Green color

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)

        # White rounded rectangle container
        container = QFrame()
        container.setStyleSheet("""
            background-color: white;
            border-radius: 40px;
        """)
        container.setFixedSize(500, 600)
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.setSpacing(20)

        # Profile Setup title
        title = QLabel("Profile Setup")
        title.setStyleSheet("""
            color: #8FBC8F;
            font-size: 36px;
            font-weight: bold;
        """)
        title.setAlignment(Qt.AlignCenter)

        # Upload Photo button
        upload_photo = QPushButton()
        upload_photo.setIcon(QIcon("path_to_upload_icon.png"))  # Replace with actual path
        upload_photo.setIconSize(QSize(64, 64))
        upload_photo.setStyleSheet("""
            background-color: #D3D3D3;
            border-radius: 50px;
            padding: 20px;
        """)
        upload_photo.setFixedSize(100, 100)
        upload_photo.clicked.connect(lambda: print("Upload Photo clicked"))

        upload_label = QLabel("Upload Photo")
        upload_label.setStyleSheet("""
            color: #8FBC8F;
            font-size: 14px;
            text-decoration: underline;
        """)
        upload_label.setAlignment(Qt.AlignCenter)

        # Vocal and Visual Settings button
        vocal_visual = QPushButton("Vocal and Visual Settings")
        vocal_visual.setStyleSheet("""
            background-color: #D3D3D3;
            color: #4682B4;
            border-radius: 25px;
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
        """)
        vocal_visual.clicked.connect(lambda: print("Vocal and Visual Settings clicked"))

        # Next button
        next_button = QPushButton("Next")
        next_button.setStyleSheet("""
            background-color: #8FBC8F;
            color: white;
            border-radius: 25px;
            padding: 15px;
            font-size: 24px;
            font-weight: bold;
        """)
        next_button.clicked.connect(lambda: print("Next clicked"))

        # Skip button
        skip_button = QPushButton("Skip")
        skip_button.setStyleSheet("""
            background-color: transparent;
            color: #8FBC8F;
            border: none;
            font-size: 16px;
        """)
        skip_button.clicked.connect(lambda: print("Skip clicked"))

        # Add widgets to container layout
        container_layout.addWidget(title)
        container_layout.addWidget(upload_photo, alignment=Qt.AlignCenter)
        container_layout.addWidget(upload_label)
        container_layout.addWidget(vocal_visual)
        container_layout.addWidget(next_button)
        container_layout.addWidget(skip_button)

        # Add container to main layout
        main_layout.addWidget(container)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProfileSetup()
    window.show()
    sys.exit(app.exec_())