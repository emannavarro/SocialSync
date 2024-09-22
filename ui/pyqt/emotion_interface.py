import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect


class RoundedFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("RoundedFrame")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)


class EmotionDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emotion Analysis Dashboard")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #71B79A;
            }
            QLabel {
                color: black;
                font-family: 'Arial';
            }
            QPushButton {
                background-color: #8FBC8F;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 5px 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2E8B57;
            }
            #RoundedFrame {
                background-color: white;
                border-radius: 20px;
            }
        """)
        self.setGeometry(100, 100, 1000, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Header
        header = QWidget()
        header.setStyleSheet("background-color: white;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)

        home_label = QLabel("Home")
        home_label.setFont(QFont("Arial", 24, QFont.Bold))
        header_layout.addWidget(home_label)

        header_layout.addStretch()

        for text in ["Profile", "History", "Sign Out"]:
            btn = QPushButton(text)
            header_layout.addWidget(btn)

        main_layout.addWidget(header)

        # Content
        content = QWidget()
        content_layout = QHBoxLayout(content)

        # Emotion percentages
        emotions_frame = RoundedFrame()
        emotions_layout = QVBoxLayout(emotions_frame)

        ai_icon = QLabel()
        ai_pixmap = QPixmap("ai_icon.png")  # You'll need to provide this image
        ai_icon.setPixmap(ai_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        emotions_layout.addWidget(ai_icon)

        emotions_data = [
            ("Happiness: 90%", "#0C9643"),
            ("Sad: 3%", "#4D4D4D"),
            ("Upset: 2%", "#BF1B1B"),
            ("Annoyed 1%:", "#C7B407")
        ]
        for text, color in emotions_data:
            label = QLabel(text)
            label.setStyleSheet(f"color: {color}; font-size: 16px; font-weight: bold;")
            emotions_layout.addWidget(label)

        content_layout.addWidget(emotions_frame)

        # Center content
        center_content = QWidget()
        center_layout = QVBoxLayout(center_content)

        # Confidence
        confidence = QLabel("Confidence: 78%")
        confidence.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        center_layout.addWidget(confidence, alignment=Qt.AlignCenter)

        # Smiley face
        smiley = QLabel()
        smiley_pixmap = QPixmap("smiley.png")  # You'll need to provide this image
        smiley.setPixmap(smiley_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        center_layout.addWidget(smiley, alignment=Qt.AlignCenter)

        content_layout.addWidget(center_content)

        # Facial recognition diagram
        facial_recognition = QLabel()
        facial_pixmap = QPixmap("facial_recognition.png")  # You'll need to provide this image
        facial_recognition.setPixmap(facial_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        content_layout.addWidget(facial_recognition)

        main_layout.addWidget(content)

        # Information box
        info_box = QFrame()
        info_box.setStyleSheet("background-color: #B2FFD0; border-radius: 20px; padding: 20px;")
        info_layout = QVBoxLayout(info_box)

        info_title = QLabel("Happiness:")
        info_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        info_layout.addWidget(info_title)

        info_text = QLabel(
            "Happiness is a good feeling you get when something nice happens or when you're doing something you enjoy. It can feel like a warm, comfortable glow inside you.")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)

        response_title = QLabel("Respond:")
        response_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        info_layout.addWidget(response_title)

        response_text = QLabel("Smile to the person\nHave a higher pitched voice")
        info_layout.addWidget(response_text)

        main_layout.addWidget(info_box)

        # Help button
        help_btn = QPushButton("Help")
        help_btn.setFixedSize(100, 40)
        main_layout.addWidget(help_btn, alignment=Qt.AlignLeft)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmotionDashboard()
    window.show()
    sys.exit(app.exec_())