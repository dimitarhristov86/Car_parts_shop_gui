import sys

import mysql.connector
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import mysql.connector as mc
from mysql.connector import connection


class MainWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.btn_login.clicked.connect(self.login)
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
            result = mycursor.fetchall()

            if result == None:
                print("Incorrect email or password")

            else:
                print("You are logged in")

        except mysql.connector.Error as e:
            print(e)


app = qtw.QApplication(sys.argv)

window = MainWidget()

window.show()

sys.exit(app.exec())
