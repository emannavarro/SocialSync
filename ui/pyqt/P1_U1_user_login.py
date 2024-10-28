import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QLinearGradient, QPen
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, QPoint, QTimer

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

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SocialSync')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        # Main container
        self.container = QWidget(self)
        self.container.setGeometry(QRect(190, 30, 900, 660))
        self.container.setStyleSheet("""
            background-color: white;
            border-radius: 40px;
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 10)
        self.container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        # Logo
        logo_label = QLabel(self.container)
        logo_pixmap = QPixmap("images/v26_35.png")
        logo_label.setPixmap(logo_pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setFixedSize(180, 180)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # SocialSync text
        title_label = QLabel("SocialSync", self.container)
        title_label.setStyleSheet("color: #71B89A; font-size: 42px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Username input
        self.username_input = self.create_input("Username")
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        # Password input
        self.password_input = self.create_input("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        # Sign In button
        self.sign_in_button = AnimatedButton("Sign In", self.container)
        self.sign_in_button.setFixedSize(300, 50)
        layout.addWidget(self.sign_in_button, alignment=Qt.AlignCenter)

        # New User button
        self.new_user_button = AnimatedButton("New User?", self.container)
        self.new_user_button.setFixedSize(300, 50)
        layout.addWidget(self.new_user_button, alignment=Qt.AlignCenter)

        # Forgot Password button
        self.forgot_password_button = AnimatedButton("Forgot Password?", self.container)
        self.forgot_password_button.setFixedSize(300, 50)
        layout.addWidget(self.forgot_password_button, alignment=Qt.AlignCenter)

        # Add hover animations
        for button in [self.sign_in_button, self.new_user_button, self.forgot_password_button]:
            button.setCursor(Qt.PointingHandCursor)

        # Animate container on show
        self.show_animation = QPropertyAnimation(self.container, b"pos")
        self.show_animation.setDuration(1000)
        self.show_animation.setStartValue(QPoint(190, -660))
        self.show_animation.setEndValue(QPoint(190, 30))
        self.show_animation.setEasingCurve(QEasingCurve.OutBack)

        # Start animation after a short delay
        QTimer.singleShot(100, self.show_animation.start)

    def create_input(self, placeholder):
        input_field = QLineEdit(self.container)
        input_field.setPlaceholderText(placeholder)
        input_field.setFixedSize(300, 50)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid #E0E0E0;
                border-radius: 25px;
                padding-left: 20px;
                font-size: 16px;
                color: #555;
            }
            QLineEdit:focus {
                border: 2px solid #71B89A;
            }
        """)
        return input_field

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create gradient background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#71B89A"))
        gradient.setColorAt(1, QColor("#5A9A7F"))
        painter.fillRect(self.rect(), gradient)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())