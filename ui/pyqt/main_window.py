from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from ui.pyqt.guardian_login import LoginPage
from ui.pyqt.P1_U1_user_login import LoginPage
from ui.pyqt.p3_first_register import RegistrationForm
from ui.pyqt.u4_home import MainWindow as PreSession
from ui.pyqt.u7_camera_working_session_dashboard import MainWindow as SessionDashboard
from ui.pyqt.u2_profile_init import ProfileSetup
from ui.pyqt.p10_session_history import HistoryPage
from ui.pyqt.u_vocal_and_visual_setting import MainWindow as VocalVisualSetting
from ui.pyqt.p6_care_profile_settings import MainWindow as CareProfileSettings
from ui.pyqt.p5_session_overview import OverviewScreen as SessionOverview


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SocialSync")
        self.setGeometry(100, 100, 1200, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.setStyleSheet("background-color: #71B89A;")
        self.setFont(QFont("Josefin Sans", 12))

        # Add the login, register, and dashboard pages to the stack
        self.login_page = LoginPage(self)  # Pass MainWindow as reference
        self.register_page = RegistrationForm(self)
        self.presesh_page = PreSession(self)
        self.profile_page = ProfileSetup(self)
        self.history_page = HistoryPage(self)
        self.video_window = SessionDashboard(self)
        self.vocal_visual_setting_page = VocalVisualSetting(self)
        self.care_profile_settings = CareProfileSettings(self)



        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.presesh_page)
        self.stacked_widget.addWidget(self.profile_page)
        self.stacked_widget.addWidget(self.history_page)
        self.stacked_widget.addWidget(self.video_window)
        self.stacked_widget.addWidget(self.vocal_visual_setting_page)
        self.stacked_widget.addWidget(self.care_profile_settings)




        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_register_page(self):
        self.stacked_widget.setCurrentWidget(self.register_page)

    def show_presesh_page(self):
        self.stacked_widget.setCurrentWidget(self.presesh_page)

    def show_profile_page(self):
        self.stacked_widget.setCurrentWidget(self.profile_page)

    def show_vocal_visual_setting_page(self):
        self.stacked_widget.setCurrentWidget(self.vocal_visual_setting_page)

    def show_history_page(self):
        self.stacked_widget.setCurrentWidget(self.history_page)

    def show_video_window(self):
        self.stacked_widget.setCurrentWidget(self.video_window)

    def show_care_profile_settings(self):
        self.stacked_widget.setCurrentWidget(self.care_profile_settings)

