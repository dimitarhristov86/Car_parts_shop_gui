import sys

import mysql.connector
from PyQt5 import QtWidgets as qtw
import mysql.connector as mc
from datetime import datetime


class MainWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.btn_sign_in.clicked.connect(self.sign_in)
        self.btn_sign_up.clicked.connect(self.sign_up_form)
        self.btn_exit.clicked.connect(exit)
        self.show()

    def setup_ui(self):
        self.setWindowTitle("Car Parts Shop")
        self.setFixedSize(900, 422)
        window = qtw.QLabel(self)
        window.setStyleSheet("background-image: url(/home/dimitar/PycharmProjects/Car_parts_shop_gui/images/1.jpg)")
        window.setFixedSize(900, 422)
        self.btn_sign_in = qtw.QPushButton("Sign in")
        self.btn_exit = qtw.QPushButton("Exit")
        self.btn_sign_up = qtw.QPushButton("Sign up")
        self.textfield = qtw.QLabel(self)
        self.textfield.setStyleSheet('color: red')
        buttons_layout = qtw.QHBoxLayout()
        buttons_layout.addWidget(self.btn_sign_in)
        buttons_layout.addWidget(self.btn_sign_up)
        buttons_layout.addWidget(self.btn_exit)
        buttons_layout.setSpacing(100)
        form_layout = qtw.QFormLayout()
        form_layout.addRow(self.textfield)
        form_layout.addRow("", buttons_layout)
        self.setLayout(form_layout)

    def sign_in(self):
        super().__init__()
        self.setWindowTitle('Sign in Form')
        self.login_input = qtw.QLineEdit(self)
        self.password_input = qtw.QLineEdit(self)
        self.password_input.setEchoMode(qtw.QLineEdit.Password)
        self.textfield = qtw.QLabel(self)
        self.textfield.setStyleSheet('color: red')
        btn_submit = qtw.QPushButton('Submit')
        btn_exit = qtw.QPushButton('Exit')
        btn_layout = qtw.QHBoxLayout()
        btn_layout.addWidget(btn_submit)
        btn_layout.addWidget(btn_exit)
        btn_layout.setSpacing(100)
        form_layout = qtw.QFormLayout()
        form_layout.addRow("Enter email: ", self.login_input)
        form_layout.addRow("Enter password: ", self.password_input)
        form_layout.addRow(self.textfield)
        form_layout.addRow("", btn_layout)
        self.setLayout(form_layout)
        self.show()
        btn_submit.clicked.connect(self.user_verification)
        self.main_menu()
        btn_exit.clicked.connect(exit)

    def user_verification(self):
        try:
            email = self.login_input.text()
            password = self.password_input.text()
            if len(email) == 0 and len(password) == 0:
                self.textfield.setText("Please fill all fields! ")
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
        self.setFixedSize(900, 422)
        self.user_first_name = qtw.QLineEdit(self)
        self.user_last_name = qtw.QLineEdit(self)
        self.user_email = qtw.QLineEdit(self)
        self.user_phone_number = qtw.QLineEdit(self)
        self.user_password = qtw.QLineEdit(self)
        self.user_confirm_password = qtw.QLineEdit(self)
        date_time = datetime.now()
        self.user_created = date_time.strftime("%Y/%m/%d %H:%M:%S")
        self.btn_submit = qtw.QPushButton('Submit')
        self.btn_submit.setFixedSize(150, 50)
        self.textfield = qtw.QLabel(self)
        self.textfield.setStyleSheet("color: red")
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.btn_submit)
        new_layout = qtw.QFormLayout()
        new_layout.addRow("Enter your first name: ", self.user_first_name)
        new_layout.addRow("Enter your last name: ", self.user_last_name)
        new_layout.addRow("Enter email: ", self.user_email)
        new_layout.addRow("Enter phone_number: ", self.user_phone_number)
        new_layout.addRow("Enter password: ", self.user_password)
        self.user_password.setEchoMode(qtw.QLineEdit.Password)
        new_layout.addRow("Re-enter password: ", self.user_confirm_password)
        self.user_confirm_password.setEchoMode(qtw.QLineEdit.Password)
        new_layout.addRow(self.textfield)
        new_layout.addRow("", layout)
        self.setLayout(new_layout)
        self.show()
        self.btn_submit.clicked.connect(self.add_data_to_db)
        user_input = [self.user_first_name, self.user_last_name, self.user_email, self.user_phone_number,
                      self.user_password, self.user_confirm_password]
        for item in user_input:
            if len(user_input) == 0:
                self.textfield.setText("Please fill all fields! ")


    def main_menu(self):
        super().__init__()
        self.setWindowTitle("Car Parts Shop Main Menu")
        self.setFixedSize(900, 422)
        window = qtw.QLabel(self)
        window.setStyleSheet("background-color: blue")
        window.setFixedSize(900, 422)


    def add_data_to_db(self):
        super().__init__()
        try:
            user_f_name = self.user_first_name.text()
            user_l_name = self.user_last_name.text()
            user_email = self.user_email.text()
            user_ph_number = self.user_phone_number.text()
            user_password = self.user_password.text()
            user_created = self.user_created
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="car_parts_gui"
            )
            mycursor = mydb.cursor()
            query = f"""
            INSERT INTO users(first_name, last_name, email, phone_number, password, created)
            VALUES('{user_f_name}', '{user_l_name}', '{user_email}',
            '{user_ph_number}', '{user_password}', '{user_created}')
            """
            mycursor.execute(query)
        except mysql.connector.Error as e:
            print(e)


app = qtw.QApplication(sys.argv)

window = MainWidget()

sys.exit(app.exec())
