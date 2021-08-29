import sys

import mysql.connector
from PyQt5 import QtWidgets as qtw
import mysql.connector as mc
from datetime import datetime


class MainWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.btn_login.clicked.connect(self.login)
        self.btn_registration.clicked.connect(self.sign_up_form)
        self.btn_exit.clicked.connect(exit)
        self.show()

    def setup_ui(self):
        self.setWindowTitle("Car Parts Shop")
        self.setFixedSize(960, 640)
        window = qtw.QLabel(self)
        window.setStyleSheet("background-image: url(/home/dimitar/PycharmProjects/Car_parts_shop_gui/images/image.png)")
        window.setFixedSize(960, 640)
        self.login_input = qtw.QLineEdit(self)
        self.password_input = qtw.QLineEdit(self)
        self.password_input.setEchoMode(qtw.QLineEdit.Password)
        self.btn_login = qtw.QPushButton("Login")
        self.btn_exit = qtw.QPushButton("Exit")
        self.btn_registration = qtw.QPushButton("Registration")
        buttons_layout = qtw.QHBoxLayout()
        buttons_layout.addWidget(self.btn_login)
        buttons_layout.addWidget(self.btn_registration)
        buttons_layout.addWidget(self.btn_exit)
        buttons_layout.setSpacing(100)
        form_layout = qtw.QFormLayout()
        form_layout.addRow("Enter email: ", self.login_input)
        form_layout.addRow("Enter password: ", self.password_input)
        form_layout.addRow("", buttons_layout)
        self.setLayout(form_layout)

    def login(self):
        try:
            email = self.login_input.text()
            password = self.password_input.text()
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="car_parts_gui"
            )
            mycursor = mydb.cursor()
            query = f""" SELECT * FROM users WHERE 
            email='{email}' AND password='{password}'
            """
            mycursor.execute(query)
            result = mycursor.fetchone()
            if result == None:
                print("Incorrect email or password")
            else:
                print("You are logged in")
        except mysql.connector.Error as e:
            print(e)

    def sign_up_form(self):
        super().__init__()
        self.setWindowTitle('Sign up Form')
        self.setFixedSize(1200, 640)
        window = qtw.QLabel(self)
        window.setStyleSheet("background-image: url(/home/dimitar/PycharmProjects/Car_parts_shop_gui/images/image.png)")
        self.setFixedSize(1200, 640)
        self.user_first_name = qtw.QLineEdit(self)
        self.user_last_name = qtw.QLineEdit(self)
        self.user_email = qtw.QLineEdit(self)
        self.user_phone_number = qtw.QLineEdit(self)
        self.user_password = qtw.QLineEdit(self)
        self.user_confirm_password = qtw.QLineEdit(self)
        self.user_created = datetime.now()
        self.btn_submit = qtw.QPushButton('Submit')
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.user_first_name)
        layout.addWidget(self.user_last_name)
        layout.addWidget(self.user_email)
        layout.addWidget(self.user_phone_number)
        layout.addWidget(self.user_password)
        layout.addWidget(self.user_confirm_password)
        layout.addWidget(self.btn_submit)
        form_layout = qtw.QFormLayout()
        form_layout.addRow("Enter your first name: ", self.user_first_name)
        form_layout.addRow("Enter your last name: ", self.user_last_name)
        form_layout.addRow("Enter email: ", self.user_email)
        form_layout.addRow("Enter phone_number: ", self.user_phone_number)
        form_layout.addRow("Enter password: ", self.user_password)
        self.user_password.setEchoMode(qtw.QLineEdit.Password)
        form_layout.addRow("Re-enter password: ", self.user_confirm_password)
        self.user_confirm_password.setEchoMode(qtw.QLineEdit.Password)
        form_layout.addRow("", layout)
        self.setLayout(form_layout)
        self.show()

        # ---------------------------------- signals --------------------------------- #
        # self.btn_submit.clicked.connect(self.onSubmit)


app = qtw.QApplication(sys.argv)

window = MainWidget()

sys.exit(app.exec())
