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
        painter.setFont(QFont('Arial', 16, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class ProfileSetup(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Profile Setup")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")
        self.parent = parent

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)

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

        title = QLabel("Profile Setup")
        title.setStyleSheet("""
            color: #71B89A;
            font-size: 48px;
            font-weight: bold;
        """)
        title.setAlignment(Qt.AlignCenter)

        self.upload_photo_button = QPushButton()
        self.upload_photo_button.setFixedSize(120, 120)
        self.upload_photo_button.setStyleSheet("""
            background-color: #D3D3D3;
            border-radius: 60px;
            qproperty-iconSize: 60px 60px;
""")
        self.upload_photo_button.setCursor(Qt.PointingHandCursor)
        self.upload_photo_button.clicked.connect(self.upload_photo_clicked)

        # Set default icon
        icon = QIcon("images/v14_189.png")
        self.upload_photo_button.setIcon(icon)
        self.upload_photo_button.setIconSize(QSize(60, 60))

        self.upload_label = QLabel("Upload Photo")
        self.upload_label.setStyleSheet("""
            color: #39687C;
            font-size: 24px;
            text-decoration: underline;
        """)
        self.upload_label.setAlignment(Qt.AlignCenter)
        self.upload_label.setCursor(Qt.PointingHandCursor)
        self.upload_label.mousePressEvent = self.upload_photo_clicked

        vocal_visual_button = CustomButton("Vocal and Visual Settings", self)
        vocal_visual_button.setFixedSize(400, 50)
        vocal_visual_button.setStyleSheet("""
            background-color: #D3D3D3;
            color: #39687C;
            font-size: 18px;
            font-weight: bold;
        """)
        vocal_visual_button.clicked.connect(self.vocal_visual_clicked)

        next_button = CustomButton("Next", self)
        next_button.setFixedSize(200, 50)
        next_button.setStyleSheet("""
            background-color: #71B89A;
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        next_button.clicked.connect(self.next_clicked)

        skip_button = CustomButton("Skip", self)
        skip_button.setFixedSize(200, 50)
        skip_button.setStyleSheet("""
            background-color: #71B89A;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 25px;
""")
        skip_button.clicked.connect(self.skip_clicked)

        container_layout.addWidget(title)
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        container_layout.addWidget(self.upload_photo_button, alignment=Qt.AlignCenter)
        container_layout.addWidget(self.upload_label, alignment=Qt.AlignCenter)
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        container_layout.addWidget(vocal_visual_button, alignment=Qt.AlignCenter)
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        container_layout.addWidget(next_button, alignment=Qt.AlignCenter)
        container_layout.addWidget(skip_button, alignment=Qt.AlignCenter)

        main_layout.addWidget(container)

    def upload_photo_clicked(self, event=None):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.set_profile_picture(file_name)

    def set_profile_picture(self, image_path):
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

    def vocal_visual_clicked(self):
        print("Vocal and Visual Settings clicked")

    def next_clicked(self):
        print("Next clicked")

    def skip_clicked(self):
        print("Skip clicked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProfileSetup()
    window.show()
    sys.exit(app.exec_())