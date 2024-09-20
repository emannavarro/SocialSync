from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from ui.pyqt.login import LoginPage
from ui.pyqt.register import RegisterPage

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SocialSync")
        self.setGeometry(100, 100, 1200, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Add the landing, login, and register pages to the stack
        self.login_page = LoginPage(self)
        self.register_page = RegisterPage(self)

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)

        self.stacked_widget.setCurrentWidget(self.login_page)

        self.stacked_widget.setStyleSheet("background-color: #71B89A;")  # Background color


    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.stacked_widget.repaint()

    def show_register_page(self):
        self.stacked_widget.setCurrentWidget(self.register_page)
        self.stacked_widget.repaint()

