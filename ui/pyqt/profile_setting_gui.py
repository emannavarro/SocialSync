import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame)
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QSize

class RoundedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(150, 40)
        self.setStyleSheet("""
            QPushButton {
                background-color: #39687C;
                color: white;
                border: none;
                border-radius: 20px;
                font-family: 'Josefin Sans';
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #71B89A;
            }
        """)

class SettingsButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(400, 60)
        self.setStyleSheet("""
            QPushButton {
                background-color: #D9D9D9;
                color: #39687C;
                border: none;
                border-radius: 30px;
                font-family: 'Josefin Sans';
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                qproperty-alignment: AlignCenter;
                padding: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #C0C0C0;
            }
        """)

class ProfileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Profile")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B79A;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setFixedHeight(70)
        header.setStyleSheet("background-color: white; border-bottom: 1px solid black;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        logo_label = QLabel()
        logo_pixmap = QPixmap("images/v26_279.png")
        logo_label.setPixmap(logo_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_layout.addWidget(logo_label)

        title = QLabel("Profile")
        title.setFont(QFont("Josefin Sans", 24, QFont.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        sign_out_btn = RoundedButton("Sign Out")
        sign_out_btn.setStyleSheet(sign_out_btn.styleSheet().replace("#39687C", "#71B89A"))
        header_layout.addWidget(sign_out_btn)

        main_layout.addWidget(header)

        # Content
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Left column
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setAlignment(Qt.AlignTop)

        profile_pic_container = QFrame()
        profile_pic_container.setFixedSize(200, 200)
        profile_pic_container.setStyleSheet("""
            background-color: white;
            border: 1px solid #CCCCCC;
            border-radius: 10px;
        """)
        profile_pic_layout = QVBoxLayout(profile_pic_container)

        profile_pic = QLabel()
        profile_pixmap = QPixmap("images/v25_505.png")
        profile_pic.setPixmap(profile_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        profile_pic.setAlignment(Qt.AlignCenter)
        profile_pic_layout.addWidget(profile_pic)

        left_layout.addWidget(profile_pic_container)

        for text in ["Username", "Full Name", "Email"]:
            label = QLabel(text)
            label.setStyleSheet("color: white; font-family: 'Josefin Sans'; font-size: 24px; font-weight: bold;")
            left_layout.addWidget(label)

        content_layout.addWidget(left_column)



        # Right column
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)

        settings_label = QLabel("Settings")
        settings_label.setStyleSheet("color: white; font-family: 'Josefin Sans'; font-size: 36px; font-weight: bold;")
        right_layout.addWidget(settings_label, alignment=Qt.AlignHCenter)

        for text in ["Vocal and Visual Settings", "Password", "Email", "Profile Pic"]:
            btn = SettingsButton(text)
            right_layout.addWidget(btn, alignment=Qt.AlignHCenter)

        reset_btn = SettingsButton("Reset")
        right_layout.addWidget(reset_btn, alignment=Qt.AlignHCenter)

        content_layout.addWidget(right_column)

        main_layout.addWidget(content)

        # Footer
        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 0, 20, 20)

        help_btn = RoundedButton("Help")
        footer_layout.addWidget(help_btn, alignment=Qt.AlignLeft)

        footer_layout.addStretch()

        back_btn = RoundedButton("Back")
        footer_layout.addWidget(back_btn, alignment=Qt.AlignRight)

        main_layout.addWidget(footer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileApp()
    window.show()
    sys.exit(app.exec_())