import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QFrame, QSpacerItem, QSizePolicy, QFileDialog, QPushButton)
from PyQt5.QtGui import QFont, QIcon, QPainter, QColor, QPixmap
from PyQt5.QtCore import Qt, QSize
import os

class CustomButton(QPushButton):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.palette().button().color()))
        painter.drawRoundedRect(self.rect(), 25, 25)

        painter.setPen(QColor(self.palette().buttonText().color()))
        painter.setFont(QFont('Arial', 28, QFont.Bold))  # Consistent font size for the buttons
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class ProfileSetup(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Profile Setup")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")
        self.parent = parent

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)

        # White rounded rectangle container
        container = QFrame()
        container.setStyleSheet("""
            background-color: white;
            border-radius: 70px;
        """)
        container.setFixedSize(800, 600)
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignHCenter)
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(50, 50, 50, 50)

        # Profile Setup title
        title = QLabel("Profile Setup")
        title.setStyleSheet("""
            color: #71B89A;
            font-size: 48px;
            font-weight: bold;
        """)
        title.setAlignment(Qt.AlignCenter)

        # Upload Photo button with default profile picture
        self.upload_photo_button = QPushButton()
        self.upload_photo_button.setFixedSize(120, 120)
        self.upload_photo_button.setStyleSheet("""
            background-color: #D3D3D3;
            border-radius: 60px;
        """)
        self.upload_photo_button.setCursor(Qt.PointingHandCursor)
        self.upload_photo_button.clicked.connect(self.upload_photo_clicked)

        # Load and set the default profile picture
        image_path = os.path.join("images", "default-profile.jpg")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(120, 120, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            # Create a circular mask for the pixmap
            mask = QPixmap(pixmap.size())
            mask.fill(Qt.transparent)

            painter = QPainter(mask)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(Qt.white)
            painter.drawEllipse(pixmap.rect())
            painter.end()

            pixmap.setMask(mask.createMaskFromColor(Qt.transparent, Qt.MaskInColor))
            self.upload_photo_button.setIcon(QIcon(pixmap))
            self.upload_photo_button.setIconSize(QSize(120, 120))
        else:
            print(f"Image not found at {image_path}")

        # Upload photo label (Clickable)
        self.upload_label = QLabel("<u>Upload Photo</u>")
        self.upload_label.setStyleSheet("""
            color: #4682B4;
            font-size: 24px;
        """)
        self.upload_label.setAlignment(Qt.AlignCenter)
        self.upload_label.setCursor(Qt.PointingHandCursor)
        self.upload_label.mousePressEvent = self.upload_photo_clicked  # Connect label click to photo upload

        # Next button (aligned similarly to the Confirm button in VocalVisualSettingsScreen)
        next_button = CustomButton("Next", self)
        next_button.setFixedSize(200, 50)
        next_button.setStyleSheet("""
            background-color: #71B89A;
            color: white;
            font-size: 28px;
            font-weight: bold;
        """)
        next_button.clicked.connect(self.next_clicked)

        # Add widgets to container layout with spacers
        container_layout.addWidget(title)
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        container_layout.addWidget(self.upload_photo_button, alignment=Qt.AlignCenter)
        container_layout.addWidget(self.upload_label, alignment=Qt.AlignCenter)
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        container_layout.addStretch(1)  # Add stretch to push the Next button lower
        container_layout.addWidget(next_button, alignment=Qt.AlignCenter)
        container_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add container to main layout
        main_layout.addWidget(container)

    def upload_photo_clicked(self, event=None):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        file_dialog.setNameFilters(["Images (*.png *.jpg *.jpeg *.bmp)"])
        file_dialog.setWindowTitle("Select Profile Picture")

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            self.set_profile_picture(selected_file)

    def set_profile_picture(self, image_path):
        """Set the profile picture from the given image path."""
        pixmap = QPixmap(image_path).scaled(120, 120, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        mask = QPixmap(pixmap.size())
        mask.fill(Qt.transparent)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.drawEllipse(pixmap.rect())
        painter.end()

        pixmap.setMask(mask.createMaskFromColor(Qt.transparent, Qt.MaskInColor))
        self.upload_photo_button.setIcon(QIcon(pixmap))
        self.upload_photo_button.setIconSize(QSize(120, 120))

    def next_clicked(self):
        print("Next clicked")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProfileSetup(None)  # Pass None as the parent for testing
    window.show()
    sys.exit(app.exec_())
