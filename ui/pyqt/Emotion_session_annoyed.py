import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt, QRectF


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Emotion Recognition UI')
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet("background-color: rgba(113,183,154,1);")
        self.setFont(QFont("Josefin Sans", 12))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.createHeader())
        layout.addWidget(self.createMainContent())
        layout.addWidget(self.createBottomSection())

    def createHeader(self):
        header = QWidget()
        header.setFixedHeight(100)
        header.setStyleSheet("background-color: white;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(50, 0, 50, 0)

        home_label = QLabel('Home', self)
        home_label.setFont(QFont('Josefin Sans', 32, QFont.Bold))
        home_label.setStyleSheet("color: black;")
        header_layout.addWidget(home_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_layout.addStretch()

        for text in ["Profile", "History", "Sign Out"]:
            button = QPushButton(text, self)
            button.setFixedSize(150, 50)
            button.setFont(QFont('Josefin Sans', 16))
            button.setStyleSheet("""
                color: white;
                background-color: rgba(113, 184, 154, 1);
                border-radius: 25px;
            """)
            header_layout.addWidget(button)
            if text != "Sign Out":
                header_layout.addSpacing(20)

        return header

    def createMainContent(self):
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(50)

        content_layout.addWidget(self.createEmotionBubble())
        content_layout.addWidget(self.createConfidenceSection())
        content_layout.addWidget(self.createMonaLisaSection())

        return content

    def createEmotionBubble(self):
        bubble = QFrame()
        bubble.setFixedSize(360, 360)
        bubble.setStyleSheet("background-color: transparent;")

        # Create a custom oval shape
        oval = QLabel(bubble)
        oval.setFixedSize(360, 360)
        oval.setStyleSheet("""
            background-color: white;
            border-radius: 180px;
        """)

        profile_logo = QLabel(bubble)
        profile_logo.setPixmap(
            QPixmap("images/v20_308.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        profile_logo.move(20, 20)

        emotions = [
            ("Annoyed: 90%", 90, 110, QColor(255, 193, 7)),
            ("Happiness: 3%", 90, 170, QColor(12, 150, 67)),
            ("Sad: 2%", 90, 230, QColor(77, 77, 77)),
            ("Upset: 1%", 90, 290, QColor(191, 27, 27))
        ]

        for text, x, y, color in emotions:
            label = QLabel(text, bubble)
            label.setStyleSheet(f"""
                font-size: 22px;
                color: rgb({color.red()}, {color.green()}, {color.blue()});
                background-color: transparent;
                font-weight: bold;
            """)
            label.move(x, y)

        return bubble

    def createConfidenceSection(self):
        section = QFrame()
        section.setFixedSize(360, 360)
        layout = QVBoxLayout(section)

        confidence_label = QLabel("Confidence: 78%", section)
        confidence_label.setStyleSheet("font-size: 32px; color: white;")
        confidence_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(confidence_label)

        annoyed_face_label = QLabel(section)
        annoyed_face_label.setPixmap(
            QPixmap("images/v25_545.png").scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        annoyed_face_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(annoyed_face_label)

        return section

    def createMonaLisaSection(self):
        section = QFrame()
        section.setFixedSize(360, 360)
        mona_lisa_label = QLabel(section)

        # Load the original image
        original_pixmap = QPixmap("images/v32_188.png")

        # Scale the image to fit the section
        scaled_pixmap = original_pixmap.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        mona_lisa_label.setPixmap(scaled_pixmap)
        mona_lisa_label.setAlignment(Qt.AlignCenter)
        return section

    def createExplanationSection(self):
        section = QLabel()
        section.setText("""
        <p><strong style='font-size: 24px;'>Annoyed:</strong><br>
        Annoyed is feeling bothered or irritated by something small or repeated.</p>

        <p><strong style='font-size: 24px;'>Respond:</strong><br>
        Tell the person to stop Leave or change the subject Tell them they are annoying you</p>
        """)
        section.setWordWrap(True)
        section.setStyleSheet("""
            font-size: 18px;
            color: #333;
            background-color: rgba(255,233,0,1);
            padding: 30px;
            border-radius: 20px;
        """)
        section.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        return section

    def createBottomSection(self):
        section = QFrame()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(50, 20, 50, 50)

        explanation = self.createExplanationSection()
        layout.addWidget(explanation)

        help_button = QPushButton('Help', self)
        help_button.setFixedSize(100, 40)
        help_button.setFont(QFont('Josefin Sans', 16, QFont.Bold))
        help_button.setStyleSheet("""
            QPushButton {
                color: #5F9EA0;
                background-color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
        """)
        layout.addWidget(help_button, alignment=Qt.AlignLeft)

        return section

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw main background
        painter.setBrush(QBrush(QColor(113, 183, 154)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 100, self.width(), self.height() - 100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())