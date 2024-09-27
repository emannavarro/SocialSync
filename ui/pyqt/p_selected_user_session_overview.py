import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class OverviewScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set fixed window size to 1280x720
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71b79a;")  # Green background color

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # No margins

        # Header: Full width, with logo placeholder and profile button
        header_container = QWidget(self)  # Container for header
        header_container.setStyleSheet("background-color: white;")
        header_container.setFixedHeight(80)  # Height of the header
        header_container.setFixedWidth(1280)  # Full screen width

        header_inner_layout = QHBoxLayout(header_container)
        header_inner_layout.setContentsMargins(20, 0, 20, 0)  # Padding inside header

        # Placeholder for Logo
        logo_label = QLabel('Logo', self)
        logo_label.setFont(QFont('Josefin Sans', 28, QFont.Bold))
        logo_label.setStyleSheet("color: black;")  # Black text for the logo
        header_inner_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        # Title "Session Overview Home" next to logo
        header_title = QLabel('Session Overview Home', self)
        header_title.setFont(QFont('Josefin Sans', 28, QFont.Bold))
        header_title.setStyleSheet("color: black;")  # Black text for title
        header_inner_layout.addWidget(header_title, alignment=Qt.AlignLeft)

        # Profile and History buttons side by side at the top right
        profile_button = self.create_button('Profile', 120, 50, bg_color="#d3d3d3", text_color="black")
        history_button = self.create_button('History', 120, 50, bg_color="#d3d3d3", text_color="black")

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(profile_button)
        buttons_layout.addWidget(history_button)

        header_inner_layout.addLayout(buttons_layout)
        main_layout.addWidget(header_container)

        # Row layout for Individual's Name and Preferences
        row_layout = QHBoxLayout()

        # Individual's Name section (left side)
        name_layout = QVBoxLayout()
        name_label = QLabel("Individual's Name:", self)
        name_label.setFont(QFont('Josefin Sans', 20, QFont.Bold))
        name_label.setStyleSheet("color: black;")
        name_layout.addWidget(name_label)

        name_button = self.create_button("John Doe", 200, 50, bg_color="white", text_color="black")
        name_layout.addWidget(name_button)

        change_user_button = self.create_button("Change User", 200, 50, bg_color="white", text_color="black")
        name_layout.addWidget(change_user_button)

        row_layout.addLayout(name_layout)

        # Individual's Preferences section (right side with padding)
        preferences_layout = QVBoxLayout()
        preferences_layout.setContentsMargins(600, 0, 0, 0)  # Padding to position preferences on the right

        preferences_label = QLabel("Individual's Preferences:", self)
        preferences_label.setFont(QFont('Josefin Sans', 20, QFont.Bold))
        preferences_label.setStyleSheet("color: black;")
        preferences_layout.addWidget(preferences_label)

        preference_button = self.create_button("Teddy bears calms John down", 300, 50, bg_color="white",
                                               text_color="black")
        preferences_layout.addWidget(preference_button)

        add_preference_layout = QHBoxLayout()
        add_preference_button = self.create_button("+ Add Preference", 150, 50, bg_color="white", text_color="black")
        add_preference_layout.addWidget(add_preference_button)

        preferences_layout.addLayout(add_preference_layout)
        row_layout.addLayout(preferences_layout)

        main_layout.addLayout(row_layout)

        # Individual's Percentages section
        percentages_label = QLabel("Individual's Percentages:", self)
        percentages_label.setFont(QFont('Josefin Sans', 20, QFont.Bold))
        percentages_label.setStyleSheet("color: black;")
        main_layout.addWidget(percentages_label)

        percentages_container = QFrame(self)
        percentages_container.setFixedHeight(250)
        percentages_container.setStyleSheet("background-color: white; border-radius: 50px;")
        percentages_layout = QHBoxLayout(percentages_container)

        percentages_left_layout = QVBoxLayout()

        happiness_label = QLabel("Happiness: 90%", self)
        happiness_label.setFont(QFont('Josefin Sans', 20, QFont.Bold))
        happiness_label.setStyleSheet("color: green;")
        percentages_left_layout.addWidget(happiness_label)

        sad_label = QLabel("Sad: 3%", self)
        sad_label.setFont(QFont('Josefin Sans', 20, QFont.Bold))
        sad_label.setStyleSheet("color: gray;")
        percentages_left_layout.addWidget(sad_label)

        upset_label = QLabel("Upset: 2%", self)
        upset_label.setFont(QFont('Josefin Sans', 20, QFont.Bold))
        upset_label.setStyleSheet("color: red;")
        percentages_left_layout.addWidget(upset_label)

        annoyed_label = QLabel("Annoyed: 1%", self)
        annoyed_label.setFont(QFont('Josefin Sans', 20, QFont.Bold))
        annoyed_label.setStyleSheet("color: yellow;")
        percentages_left_layout.addWidget(annoyed_label)

        percentages_layout.addLayout(percentages_left_layout)

        # Confidence text moved to the right with bigger font size
        confidence_label = QLabel("Confidence: 78%", self)
        confidence_label.setFont(QFont('Josefin Sans', 36, QFont.Bold))  # Bigger font size
        confidence_label.setStyleSheet("color: black;")
        percentages_layout.addWidget(confidence_label, alignment=Qt.AlignRight)

        main_layout.addWidget(percentages_container)

        # Help button at the bottom left with padding
        help_button_layout = QHBoxLayout()
        help_button_layout.setContentsMargins(20, 0, 0, 20)  # Padding for bottom-left corner
        help_button = self.create_button('Help', 120, 50, bg_color="white", text_color="#71b79a")
        help_button_layout.addWidget(help_button, alignment=Qt.AlignLeft)
        main_layout.addLayout(help_button_layout)

    def create_button(self, text, width, height, bg_color, text_color):
        button = QPushButton(text, self)
        button.setFixedSize(width, height)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #A9A9A9;
            }}
        """)
        button.clicked.connect(lambda: print(f"{text} button clicked"))  # Placeholder event listener
        return button


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OverviewScreen()
    window.show()
    sys.exit(app.exec_())
