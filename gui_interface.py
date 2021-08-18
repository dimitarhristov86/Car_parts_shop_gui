import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import  QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setWindowTitle("Car Parts Shop")
        self.setGeometry(100, 100, 1280, 800)
        wi = qtw.QLabel(self)
        wi.setStyleSheet("background-image: url(/home/dimitar_hristov86/PycharmProjects/Car_parts_shop/images/2161518548_eb13cddfe5.jpg)")
        wi.setFixedSize(1280, 800)
        login_input = qtw.QLineEdit(self)
        password_input = qtw.QLineEdit(self)
        password_input.setEchoMode(qtw.QLineEdit.Password)
        self.btn_login = qtw.QPushButton("Login")
        self.btn_exit = qtw.QPushButton("Exit")
        self.btn_registration = qtw.QPushButton("Registration")
        buttons_layout = qtw.QHBoxLayout()
        buttons_layout.addWidget(self.btn_login)
        buttons_layout.addWidget(self.btn_exit)
        buttons_layout.addWidget(self.btn_registration)
        buttons_layout.setSpacing(100)
        form_layout = qtw.QFormLayout()
        form_layout.addRow("Enter email: ", login_input)
        form_layout.addRow("Enter password: ", password_input)
        form_layout.addRow("", buttons_layout)
        self.setLayout(form_layout)


app = qtw.QApplication(sys.argv)

window = MainWidget()

window.show()

sys.exit(app.exec())
