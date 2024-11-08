import sys
from collections import deque

import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QFrame, QSizePolicy, QGraphicsDropShadowEffect, QProgressBar)
from PyQt5.QtGui import QFont, QPixmap, QImage, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation
from backend.controllers.emotion_recognition import detect_face, detect_emotion, preprocess
from ui.pyqt.cv_window import VideoWindow


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


class RoundedFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # Reference to the main stacked window
        self.initUI()

        # Initialize video feed from VideoWindow
        self.video_window = VideoWindow()  # Create an instance of VideoWindow for video handling
        self.video_window.timer.timeout.connect(self.update_video_feed)  # Use the timer from VideoWindow

        # Initialize a deque to store the last 100 emotion detections
        self.emotion_history = deque(maxlen=100)

    def initUI(self):
        self.setWindowTitle('Emotion Recognition UI')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.createHeader())
        main_layout.addWidget(self.createMainContent())
        main_layout.addWidget(self.createBottomSection())

    def createHeader(self):
        header_container = QWidget(self)
        header_container.setStyleSheet("background-color: white;")
        header_container.setFixedHeight(80)
        header_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 2)
        header_container.setGraphicsEffect(shadow)

        header_inner_layout = QHBoxLayout(header_container)
        header_inner_layout.setContentsMargins(20, 0, 20, 0)
        header_inner_layout.setSpacing(20)

        logo_label = QLabel(self)
        pixmap = QPixmap('images/v20_308.png')
        scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        header_inner_layout.addWidget(logo_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_title = QLabel('Emotion Recognition', self)
        header_title.setFont(QFont('Arial', 28, QFont.Bold))
        header_title.setStyleSheet("color: #71B89A;")
        header_inner_layout.addWidget(header_title, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_inner_layout.addStretch()

        for text in ["Profile", "History", "Sign Out"]:
            button = AnimatedButton(text, self)
            button.setFixedSize(120, 50)
            button.clicked.connect(lambda checked, btn=text: self.handle_button_click(btn))
            header_inner_layout.addWidget(button, alignment=Qt.AlignRight | Qt.AlignVCenter)

        return header_container

    def handle_button_click(self, btn_name):
        """ Handle button clicks for Profile, History, and Sign Out """
        if btn_name == "Profile":
            self.main_window.show_profile_setting_gui()
        elif btn_name == "History":
            self.main_window.show_history_page()
        elif btn_name == "Sign Out":
            self.main_window.show_login_page()

    def createMainContent(self):
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(20)
        content_layout.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(self.createEmotionalFeedback(), alignment=Qt.AlignCenter)
        content_layout.addWidget(self.createConfidenceSection(), alignment=Qt.AlignCenter)
        content_layout.addWidget(self.createVideoFeedSection(), alignment=Qt.AlignCenter)

        return content

    def createEmotionalFeedback(self):
        feedback = RoundedFrame()
        feedback.setFixedSize(320, 240)

        layout = QVBoxLayout(feedback)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        header = QLabel("Emotional Feedback", feedback)
        header.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Initialize the emotions data structure to update later, including percentage labels
        self.emotions_data = {
            "Annoyed": (QColor(255, 193, 7), QLabel(feedback), QProgressBar(feedback), QLabel("0%", feedback)),
            "Happiness": (QColor(46, 204, 113), QLabel(feedback), QProgressBar(feedback), QLabel("0%", feedback)),
            "Sad": (QColor(52, 152, 219), QLabel(feedback), QProgressBar(feedback), QLabel("0%", feedback)),
            "Upset": (QColor(231, 76, 60), QLabel(feedback), QProgressBar(feedback), QLabel("0%", feedback))
        }

        for emotion, (color, label, progress_bar, percentage_label) in self.emotions_data.items():
            emotion_layout = QHBoxLayout()
            label.setText(emotion)
            label.setStyleSheet("color: white; font-size: 18px;")

            percentage_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

            progress_bar.setRange(0, 100)
            progress_bar.setValue(0)
            progress_bar.setTextVisible(False)
            progress_bar.setFixedHeight(10)
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: rgba(255, 255, 255, 0.3);
                    border-radius: 5px;
                }}
                QProgressBar::chunk {{
                    background-color: {color.name()};
                    border-radius: 5px;
                }}
            """)

            emotion_layout.addWidget(label)
            emotion_layout.addWidget(progress_bar)
            emotion_layout.addWidget(percentage_label)

            layout.addLayout(emotion_layout)

        return feedback
    def createConfidenceSection(self):
        section = RoundedFrame()
        section.setFixedSize(320, 240)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # Initialize a QLabel for confidence display to update later
        self.confidence_label = QLabel("Confidence: 0%", section)
        self.confidence_label.setStyleSheet("font-size: 22px; color: white; font-weight: bold;")
        self.confidence_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.confidence_label)

        self.annoyed_face_label = QLabel(section)
        annoyed_face_pixmap = QPixmap("images/v25_545.png").scaled(180, 180, Qt.KeepAspectRatio,
                                                                   Qt.SmoothTransformation)
        self.annoyed_face_label.setPixmap(annoyed_face_pixmap)
        self.annoyed_face_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.annoyed_face_label)

        return section

    # Update emotional feedback and confidence dynamically based on video feed data
    def update_feedback(self, emotions, confidence):
        # Update each emotion's progress bar and label
        for emotion, (color, label, progress_bar) in self.emotions_data.items():
            if emotion in emotions:
                percentage = emotions[emotion]
                progress_bar.setValue(percentage)
                percentage_label = progress_bar.parent().findChildren(QLabel)[-1]  # Locate percentage label in layout
                percentage_label.setText(f"{percentage}%")

        # Update the confidence label
        self.confidence_label.setText(f"Confidence: {int(confidence * 100)}%")

    def createVideoFeedSection(self):
        section = RoundedFrame()
        section.setFixedSize(320, 240)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(0)

        self.video_label = QLabel(section)
        self.video_label.setFixedSize(288, 208)
        self.video_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_label)

        return section

    def createBottomSection(self):
        section = QFrame()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(50, 0, 50, 20)
        layout.setSpacing(20)

        explanation = self.createExplanationSection()
        layout.addWidget(explanation)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Add the existing Help button
        help_button = AnimatedButton('Help', self)
        help_button.setFixedSize(120, 50)
        help_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #39687C;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        button_layout.addWidget(help_button)

        # Add stretch to push buttons to opposite sides
        button_layout.addStretch()

        # Add the new End Session button
        end_session_button = AnimatedButton('End Session', self)
        end_session_button.setFixedSize(120, 50)
        end_session_button.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: white;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        end_session_button.clicked.connect(self.endSession)
        button_layout.addWidget(end_session_button)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        return section

    def createExplanationSection(self):
        section = QLabel()
        section.setFixedSize(1180, 240)
        section.setText("""
<p><strong style='font-size: 30px;'>Annoyed:</strong><br>
Being annoyed is when you feel irritated or slightly angry because something is bothering you.</p>

<p><strong style='font-size: 30px;'>Respond:</strong><br>
• Take a deep breath<br>
• Express your feelings calmly<br>
• Try to address the source of annoyance</p>
""")
        section.setWordWrap(True)
        section.setStyleSheet("""
            font-size: 20px;
            color: #333333;
            background-color: #C1F0D1;
            padding: 28px;
            border-radius: 25px;
        """)
        section.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 10)
        section.setGraphicsEffect(shadow)

        return section

    def update_video_feed(self):
        """ Update video feed in the main window by reusing video logic from VideoWindow. """
        ret, frame = self.video_window.video.read()
        if ret:
            gray, faces = detect_face(frame)

            # Process each detected face
            for (x, y, w, h) in faces:
                # Draw a rectangle around the detected face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
                face_roi_gray = gray[y:y + h, x:x + w]
                face_roi_gray = preprocess(face_roi_gray)
                idx, conf = detect_emotion(face_roi_gray)

                # Get the emotion label based on the detected index
                emotion_label = self.video_window.class_names[idx]

                # Display the emotion label on the bounding box with larger font
                label_position = (x, y - 10) if y > 20 else (x, y + h + 20)
                cv2.putText(frame, emotion_label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 4)

                # Append current emotion data to history
                self.emotion_history.append((idx, conf))

                # Calculate the average emotion percentages over the last 100 frames
                self.update_emotional_feedback()

            # Convert the frame to QImage for PyQt display
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(
                QPixmap.fromImage(qt_image).scaled(288, 208, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def update_emotional_feedback(self):
        # Assuming `self.video_window.class_names` gives the list of emotions
        emotion_counts = np.zeros(len(self.video_window.class_names))
        total_conf = 0

        # Sum the detected emotions and confidence levels from history
        for idx, conf in self.emotion_history:
            emotion_counts[idx] += conf
            total_conf += conf

        # Calculate the percentages based on total confidence
        if total_conf > 0:
            emotion_percentages = (emotion_counts / total_conf) * 100
        else:
            emotion_percentages = np.zeros(len(self.video_window.class_names))  # Set all to zero if no confidence

        # Update the emotional feedback UI elements based on calculated percentages
        for i, (emotion, (color, label, progress_bar, percentage_label)) in enumerate(self.emotions_data.items()):
            # Get the current percentage for this emotion
            percentage = int(emotion_percentages[i])

            # Set the progress bar and percentage label to reflect the percentage
            progress_bar.setValue(percentage)
            percentage_label.setText(f"{percentage}%")

            # Reset style if percentage is zero to ensure the bar appears empty
            if percentage == 0:
                progress_bar.setStyleSheet(f"""
                     QProgressBar {{
                         background-color: rgba(255, 255, 255, 0.3);
                         border-radius: 5px;
                     }}
                     QProgressBar::chunk {{
                         background-color: rgba(0, 0, 0, 0);  # Transparent when 0%
                         border-radius: 5px;
                     }}
                 """)
            else:
                progress_bar.setStyleSheet(f"""
                     QProgressBar {{
                         background-color: rgba(255, 255, 255, 0.3);
                         border-radius: 5px;
                     }}
                     QProgressBar::chunk {{
                         background-color: {color.name()};
                         border-radius: 5px;
                     }}
                 """)

        # Update confidence with the average confidence across recent frames
        avg_confidence = total_conf / len(self.emotion_history) if self.emotion_history else 0
        self.confidence_label.setText(f"Confidence: {int(avg_confidence * 100)}%")
    def endSession(self):
        """Handle the End Session button click"""
        self.video_window.timer.stop()
        self.video_window.video.release()
        self.main_window.show_user_session_overview()


    def closeEvent(self, event):
        """ Ensure video resources are released when closing the window. """
        self.video_window.timer.stop()
        self.video_window.video.release()
        event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#71B89A"))
        gradient.setColorAt(1, QColor("#5A9A7F"))
        painter.fillRect(self.rect(), gradient)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())