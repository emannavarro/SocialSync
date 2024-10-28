import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QRadioButton,
                             QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame,
                             QGraphicsDropShadowEffect, QSpacerItem)
from PyQt5.QtGui import QFont, QFontDatabase, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #71B89A;
                color: white;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #5A9A7F;
            }
            QPushButton:pressed {
                background-color: #4A8A6F;
            }
        """)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 5)
        self.setGraphicsEffect(self.shadow)

    def enterEvent(self, event):
        self.animate_shadow(25, 0, 8)

    def leaveEvent(self, event):
        self.animate_shadow(15, 0, 5)

    def animate_shadow(self, end_blur, end_x, end_y):
        self.anim_blur = QPropertyAnimation(self.shadow, b"blurRadius")
        self.anim_blur.setEndValue(end_blur)
        self.anim_blur.setDuration(200)

        self.anim_offset = QPropertyAnimation(self.shadow, b"offset")
        self.anim_offset.setEndValue(QPoint(end_x, end_y))
        self.anim_offset.setDuration(200)

        self.anim_blur.start()
        self.anim_offset.start()

class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('SocialSync Registration')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        # Load custom font
        font_id = QFontDatabase.addApplicationFont("path/to/JosefinSans-Regular.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            font_family = "Arial"

        # Create main layout
        main_layout = QVBoxLayout(self)

        # Create white background container
        self.container = QFrame(self)
        self.container.setStyleSheet("""
            background-color: white;
            border-radius: 40px;
        """)
        self.container.setFixedSize(900, 660)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 10)
        self.container.setGraphicsEffect(shadow)

        # Create grid layout for form elements
        grid = QGridLayout(self.container)
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(40, 30, 40, 30)

        # Add title
        title = QLabel("Registration")
        title.setFont(QFont(font_family, 32, QFont.Bold))
        title.setStyleSheet("color: #71B89A; margin-bottom: 10px;")
        grid.addWidget(title, 0, 0, 1, 4, Qt.AlignHCenter)

        # Create form fields
        fields = [
            ("First Name:", 1, 0), ("Address:", 1, 2),
            ("Middle Name:", 2, 0), ("City:", 2, 2),
            ("Last Name:", 3, 0), ("Zip:", 3, 2),
            ("Date of Birth:", 4, 0), ("State:", 4, 2),
            ("Email Address:", 5, 0), ("Country:", 5, 2),
            ("Phone Number:", 6, 0), ("Sex:", 6, 2),
            ("Password:", 7, 0), ("Confirm Password:", 7, 2),
        ]

        for label_text, row, col in fields:
            label = QLabel(label_text)
            label.setFont(QFont(font_family, 11))
            label.setStyleSheet("color: #23465A;")
            grid.addWidget(label, row, col)

            if label_text == "Sex:":
                sex_layout = QHBoxLayout()
                sex_layout.setSpacing(10)
                female_radio = QRadioButton("Female")
                male_radio = QRadioButton("Male")
                female_radio.setFont(QFont(font_family, 11))
                male_radio.setFont(QFont(font_family, 11))
                female_radio.setStyleSheet("color: black;")
                male_radio.setStyleSheet("color: black;")
                sex_layout.addWidget(female_radio)
                sex_layout.addWidget(male_radio)
                sex_layout.addStretch()
                grid.addLayout(sex_layout, row, col + 1)
            else:
                input_field = QLineEdit()
                input_field.setStyleSheet("""
                    background-color: #F0F0F0;
                    border: 1px solid #E0E0E0;
                    border-radius: 20px;
                    padding: 5px;
                    padding-left: 15px;
                    font-size: 14px;
                    color: #555;
                """)
                input_field.setFixedSize(260, 40)
                if "Password" in label_text:
                    input_field.setEchoMode(QLineEdit.Password)
                grid.addWidget(input_field, row, col + 1)

        # Add buttons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)
        buttons = ["Submit", "Cancel"]
        for button_text in buttons:
            button = AnimatedButton(button_text)
            button.setFixedSize(260, 40)
            button.clicked.connect(self.button_clicked)
            button_layout.addWidget(button)

        grid.addItem(QSpacerItem(20, 20), 8, 0, 1, 4)
        grid.addLayout(button_layout, 8, 0, 2, 4, Qt.AlignCenter)
        grid.addItem(QSpacerItem(20, 20), 10, 0, 1, 4)


        # Center the white background
        main_layout.addWidget(self.container, alignment=Qt.AlignCenter)

        # Animate container on show
        self.show_animation = QPropertyAnimation(self.container, b"pos")
        self.show_animation.setDuration(1000)
        self.show_animation.setStartValue(QPoint(190, -660))
        self.show_animation.setEndValue(QPoint(190, 30))
        self.show_animation.setEasingCurve(QEasingCurve.OutBack)

        # Start animation after a short delay
        QTimer.singleShot(100, self.show_animation.start)

    def button_clicked(self):
        sender = self.sender()
        print(f"{sender.text()} button clicked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegistrationForm()
    ex.show()
    sys.exit(app.exec_())