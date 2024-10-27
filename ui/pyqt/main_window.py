from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from ui.pyqt.p1_guardian_login import GuardianLoginPage
from ui.pyqt.u1_user_login import LoginPage


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SocialSync")
        self.setGeometry(100, 100, 1200, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.setStyleSheet("background-color: #71B89A;")
        self.setFont(QFont("Josefin Sans", 12))

        # Initialize only the login page and add it to the stack
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.setCurrentWidget(self.login_page)

    @property
    def login_page(self):
        if not hasattr(self, '_login_page'):
            self._login_page = LoginPage(self)
        return self._login_page

    @property
    def guardian_login_page(self):
        if not hasattr(self, '_guardian_login_page'):
            self._guardian_login_page = GuardianLoginPage(self)
            self.stacked_widget.addWidget(self._guardian_login_page)
        return self._guardian_login_page

    @property
    def register_page(self):
        if not hasattr(self, '_register_page'):
            from ui.pyqt.p3_first_register import RegistrationForm
            self._register_page = RegistrationForm(self)
            self.stacked_widget.addWidget(self._register_page)
        return self._register_page

    @property
    def presesh_page(self):
        if not hasattr(self, '_presesh_page'):
            from ui.pyqt.pre_session import CustomPage as PreSession
            self._presesh_page = PreSession(self)
            self.stacked_widget.addWidget(self._presesh_page)
        return self._presesh_page

    @property
    def profile_page(self):
        if not hasattr(self, '_profile_page'):
            from ui.pyqt.u2_profile_init import ProfileSetup
            self._profile_page = ProfileSetup(self)
            self.stacked_widget.addWidget(self._profile_page)
        return self._profile_page

    @property
    def history_page(self):
        if not hasattr(self, '_history_page'):
            from ui.pyqt.p10_session_history import HistoryPage
            self._history_page = HistoryPage(self)
            self.stacked_widget.addWidget(self._history_page)
        return self._history_page

    @property
    def video_window(self):
        if not hasattr(self, '_video_window'):
            from ui.pyqt.u7_camera_working_session_dashboard import MainWindow as SessionDashboard
            self._video_window = SessionDashboard(self)
            self.stacked_widget.addWidget(self._video_window)
        return self._video_window

    @property
    def vocal_visual_setting_page(self):
        if not hasattr(self, '_vocal_visual_setting_page'):
            from ui.pyqt.u_vocal_and_visual_setting import MainWindow as VocalVisualSetting
            self._vocal_visual_setting_page = VocalVisualSetting(self)
            self.stacked_widget.addWidget(self._vocal_visual_setting_page)
        return self._vocal_visual_setting_page

    @property
    def care_profile_settings(self):
        if not hasattr(self, '_care_profile_settings'):
            from ui.pyqt.p6_care_profile_settings import CareProfile as CareProfileSettings
            self._care_profile_settings = CareProfileSettings(self)
            self.stacked_widget.addWidget(self._care_profile_settings)
        return self._care_profile_settings

    @property
    def register_patient(self):
        if not hasattr(self, '_register_patient'):
            from ui.pyqt.p4_register_patient import RegisterPatient
            self._register_patient = RegisterPatient(self)
            self.stacked_widget.addWidget(self._register_patient)
        return self._register_patient

    # Show methods use properties, ensuring pages are only created when needed
    def show_register_patient(self):
        self.stacked_widget.setCurrentWidget(self.register_patient)

    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_guardian_login_page(self):
        self.stacked_widget.setCurrentWidget(self.guardian_login_page)

    def show_register_page(self):
        self.stacked_widget.setCurrentWidget(self.register_page)

    def show_presesh_page(self):
        self.stacked_widget.setCurrentWidget(self.presesh_page)

    def show_profile_page(self):
        self.stacked_widget.setCurrentWidget(self.profile_page)

    def show_history_page(self):
        self.stacked_widget.setCurrentWidget(self.history_page)

    def show_video_window(self):
        self.stacked_widget.setCurrentWidget(self.video_window)

    def show_vocal_visual_setting_page(self):
        self.stacked_widget.setCurrentWidget(self.vocal_visual_setting_page)

    def show_care_profile_settings(self):
        self.stacked_widget.setCurrentWidget(self.care_profile_settings)
