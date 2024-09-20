import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QFrame, QPushButton)
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QPixmap

class CustomPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Window properties
        self.setWindowTitle('Custom PyQt Design')
        self.setFixedSize(1280, 1024)

        # Main container background
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(113, 183, 154, 1);
            }
        """)

        # Top container
        top_container = QFrame(self)
        top_container.setFixedSize(self.width(), 141)
        top_container.move(0, 0)
        top_container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 1);
            border: 1px solid rgba(0, 0, 0, 1);
        """)

        # Home Label with background
        home_label_container = QLabel(self)
        home_label_container.setStyleSheet("background-color: rgba(178, 255, 209, 1);")
        home_label_container.setFixedSize(280, 110)
        home_label_container.move(20, 15)

        home_label = QLabel('Home', home_label_container)
        home_label.setFont(QFont('Josefin Sans', 70, QFont.Bold))
        home_label.setStyleSheet("color: rgba(0,0,0,1);")
        home_label.setAlignment(Qt.AlignCenter)
        home_label.setGeometry(home_label_container.rect())

        # Creating Profile, History, Help, and Sign Out buttons
        self.create_top_button('Profile', 1046, 54, 99, 32)
        self.create_top_button('History', 1150, 54, 99, 32)
        self.create_top_button('Sign Out', 1254, 54, 99, 32)
        self.create_top_button('Help', 20, 960, 99, 32)

        # Adjusting the Happiness Container to be smaller and centered
        happiness_container = QLabel(self)
        happiness_container.setFixedSize(280, 280)  # Smaller size
        happiness_container.move(80, 180)  # Adjusted to be more centered
        happiness_container.setStyleSheet("""
            background-color: rgba(217,217,217,1);
            border: 2px solid rgba(0,0,0,1);
            border-radius: 140px;
        """)

        # Adding Happiness Labels inside Oval Container (adjusted sizes)
        self.create_centered_text_label('Happiness: 90%', happiness_container, 20, 'rgba(12,150,67,1)', offset=-60)
        self.create_centered_text_label('Sad: 3%', happiness_container, 20, 'rgba(77,77,77,1)', offset=-20)
        self.create_centered_text_label('Upset: 2%', happiness_container, 20, 'rgba(191,27,27,1)', offset=20)
        self.create_centered_text_label('Annoyed: 1%', happiness_container, 20, 'rgba(199,180,7,1)', offset=60)

        # Emoji placeholder
        emoji_placeholder = QLabel(self)
        pixmap_emoji = QPixmap("./images/v32_182.png")  # Ensure path is correct
        if not pixmap_emoji.isNull():  # Check if image is loaded successfully
            emoji_placeholder.setPixmap(pixmap_emoji)
            emoji_placeholder.setScaledContents(True)
            emoji_placeholder.setFixedSize(150, 150)
            emoji_placeholder.move(450, 280)  # Adjusted to be centered horizontally
        else:
            emoji_placeholder.setText("Image not found")
            emoji_placeholder.setFixedSize(150, 150)
            emoji_placeholder.move(450, 280)

        # Confidence Label
        confidence_label = QLabel('Confidence: 78%', self)
        confidence_label.setFont(QFont('Josefin Sans', 36, QFont.Bold))
        confidence_label.setStyleSheet("color: rgba(255,255,255,1);")
        confidence_label.setAlignment(Qt.AlignCenter)
        confidence_label.setFixedSize(300, 60)
        confidence_label.move(500, 460)  # Centered under the emoji

        # Mona Lisa Image Placeholder
        mona_lisa_placeholder = QLabel(self)
        pixmap_mona_lisa = QPixmap("./images/v32_188.png")  # Ensure path is correct
        if not pixmap_mona_lisa.isNull():  # Check if image is loaded successfully
            mona_lisa_placeholder.setPixmap(pixmap_mona_lisa)
            mona_lisa_placeholder.setScaledContents(True)
            mona_lisa_placeholder.setFixedSize(300, 300)
            mona_lisa_placeholder.move(850, 180)  # Adjusted for better alignment
        else:
            mona_lisa_placeholder.setText("Image not found")
            mona_lisa_placeholder.setFixedSize(300, 300)
            mona_lisa_placeholder.move(850, 180)

        # Bottom Container
        bottom_container = QFrame(self)
        bottom_container.setFixedSize(900, 200)
        bottom_container.move(200, 750)
        bottom_container.setStyleSheet("""
            background-color: rgba(178, 255, 208, 1);
            border-radius: 40px;
        """)

        # Happiness Description and Response
        happiness_desc = QLabel('Happiness:', bottom_container)
        happiness_desc.setFont(QFont('Josefin Sans', 24, QFont.Bold))
        happiness_desc.setStyleSheet("color: rgba(0,0,0,1);")
        happiness_desc.move(20, 20)

        happiness_desc_text = QLabel(
            'Happiness is a good feeling you get when something nice happens or when you\'re doing something you enjoy. It can feel like a warm, comfortable glow inside you.',
            bottom_container)
        happiness_desc_text.setFont(QFont('Josefin Sans', 16, QFont.Bold))
        happiness_desc_text.setWordWrap(True)
        happiness_desc_text.setStyleSheet("color: rgba(0,0,0,1);")
        happiness_desc_text.setFixedSize(860, 60)
        happiness_desc_text.move(20, 60)

        respond_label = QLabel('Respond:', bottom_container)
        respond_label.setFont(QFont('Josefin Sans', 24, QFont.Bold))
        respond_label.setStyleSheet("color: rgba(0,0,0,1);")
        respond_label.move(20, 130)

        response_text = QLabel('Smile to the person\nHave a higher pitched voice', bottom_container)
        response_text.setFont(QFont('Josefin Sans', 18, QFont.Bold))
        response_text.setStyleSheet("color: rgba(0,0,0,1);")
        response_text.move(120, 130)

    def create_top_button(self, text, x, y, width, height):
        button = QPushButton(text, self)
        button.setFont(QFont('Josefin Sans', 16, QFont.Bold))
        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(113, 184, 154, 1);
                color: rgba(255, 255, 255, 1);
                border: 1px solid rgba(35, 70, 90, 1);
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(143, 204, 174, 1);
            }
        """)
        button.setFixedSize(width, height)
        button.move(x, y)

    def create_text_label(self, text, x, y, size, color):
        label = QLabel(text, self)
        label.setFont(QFont('Josefin Sans', size, QFont.Bold))
        label.setStyleSheet(f"color: {color};")
        label.move(x, y)

    def create_centered_text_label(self, text, container, size, color, offset=0):
        """Creates a centered label inside a given container with an optional offset"""
        label = QLabel(text, container)
        label.setFont(QFont('Josefin Sans', size, QFont.Bold))
        label.setStyleSheet(f"color: {color};")
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(QRect(
            0,  # x position relative to container
            (container.height() // 2) + offset - (size // 2),  # y position relative to container
            container.width(),  # width
            50  # height
        ))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CustomPage()
    ex.show()
    sys.exit(app.exec_())
