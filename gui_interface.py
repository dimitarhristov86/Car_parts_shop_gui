import sys

import mysql.connector
from PyQt5 import QtWidgets as qtw
import mysql.connector as mc
from datetime import datetime


class MainWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.textfield = qtw.QLabel()
        self.textfield.setStyleSheet('color: red')
        self.textfield.setText('')
        self.btn_sign_in.clicked.connect(self.sign_in)
        self.btn_sign_up.clicked.connect(self.sign_up_form)
        self.btn_exit.clicked.connect(exit)
        self.show()

    def setup_ui(self):
        self.setWindowTitle("Car Parts Shop")
        self.setFixedSize(900, 422)
        self.window = qtw.QLabel(self)
        self.window.setStyleSheet(
            "background-image: url(/home/dimitar/PycharmProjects/Car_parts_shop_gui/images/1.jpg)")
        self.window.setFixedSize(900, 422)
        self.btn_sign_in = qtw.QPushButton("Sign in")
        self.btn_exit = qtw.QPushButton("Exit")
        self.btn_sign_up = qtw.QPushButton("Sign up")
        buttons_layout = qtw.QHBoxLayout()
        buttons_layout.addWidget(self.btn_sign_in)
        buttons_layout.addWidget(self.btn_sign_up)
        buttons_layout.addWidget(self.btn_exit)
        buttons_layout.setSpacing(100)
        form_layout = qtw.QFormLayout()
        form_layout.addRow("", buttons_layout)
        self.setLayout(form_layout)

    def sign_in(self):
        super().__init__()
        self.setWindowTitle('Sign in Form')
        self.login_input = qtw.QLineEdit(self)
        self.password_input = qtw.QLineEdit(self)
        self.password_input.setEchoMode(qtw.QLineEdit.Password)
        self.btn_submit = qtw.QPushButton('Submit')
        self.btn_exit = qtw.QPushButton('Exit')
        btn_layout = qtw.QHBoxLayout()
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_exit)
        btn_layout.setSpacing(100)
        form_layout = qtw.QFormLayout()
        form_layout.addRow("Enter email: ", self.login_input)
        form_layout.addRow("Enter password: ", self.password_input)
        form_layout.addRow(self.textfield)
        form_layout.addRow("", btn_layout)
        self.setLayout(form_layout)
        self.btn_submit.clicked.connect(self.user_verification)
        self.btn_exit.clicked.connect(exit)
        self.textfield.setText("")
        self.show()

    def user_verification(self):
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
            self.result = mycursor.fetchone()
            if len(email) == 0 and len(password) == 0:
                print("Please fill all fields! ")
                self.textfield.setText("Please fill all fields! ")
            elif self.result == None:
                print("Incorrect email or password")
                self.textfield.setText("Incorrect email or password! ")
            else:
                print("You are logged in")
                self.main_menu()
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
        self.user_created = datetime.now()
        self.btn_submit = qtw.QPushButton('Submit')
        self.btn_to_login = qtw.QPushButton('Click here to log in')
        self.btn_submit.setFixedSize(150, 50)
        self.btn_to_login.setFixedSize(150, 50)
        self.textfield = qtw.QLabel(self)
        self.textfield.setStyleSheet("color: red")
        layout = qtw.QHBoxLayout()
        layout.addWidget(self.btn_submit)
        layout.addWidget(self.btn_to_login)
        layout.setSpacing(300)
        new_layout = qtw.QFormLayout()
        new_layout.addRow("Enter your first name: ", self.user_first_name)
        new_layout.addRow("Enter your last name: ", self.user_last_name)
        new_layout.addRow("Enter email: ", self.user_email)
        new_layout.addRow("Enter phone number: ", self.user_phone_number)
        new_layout.addRow("Enter password (20 characters max): ", self.user_password)
        self.user_password.setEchoMode(qtw.QLineEdit.Password)
        new_layout.addRow("Confirm password (20 characters max): ", self.user_confirm_password)
        self.user_confirm_password.setEchoMode(qtw.QLineEdit.Password)
        new_layout.addRow(self.textfield)
        new_layout.addRow("", layout)
        self.setLayout(new_layout)
        self.textfield.setText("")
        self.show()
        self.btn_to_login.clicked.connect(self.sign_in)
        self.btn_submit.clicked.connect(self.check_fields_data)

    def main_menu(self):
        super().__init__()
        self.setWindowTitle("Car Parts Shop Main Menu")
        self.setFixedSize(900, 422)
        self.btn_parts_view = qtw.QPushButton('View all parts')
        self.btn_buy_parts = qtw.QPushButton('Buy parts')
        self.btn_log_out = qtw.QPushButton('Log out')
        self.btn_admin_menu = qtw.QPushButton('Admin menu')
        btn_layout = qtw.QVBoxLayout()
        btn_layout.addWidget(self.btn_parts_view)
        btn_layout.addWidget(self.btn_buy_parts)
        btn_layout.addWidget(self.btn_log_out)
        btn_layout.addWidget(self.btn_admin_menu)
        self.setLayout(btn_layout)
        self.show()

    def add_data_to_db(self):
        super().__init__()
        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="car_parts_gui")
            mycursor = mydb.cursor()
            # role = self.role
            user_f_name = self.user_first_name.text()
            user_l_name = self.user_last_name.text()
            user_email = self.user_email.text()
            user_ph_number = self.user_phone_number.text()
            user_password = self.user_password.text()
            user_created = self.user_created
            query = 'INSERT INTO users(first_name, last_name, email, phone_number, password, created) ' \
                    'VALUES(%s, %s, %s, %s, %s, %s)'
            values = (user_f_name, user_l_name, user_email, user_ph_number, user_password, user_created)
            mycursor.execute(query, values)
            mydb.commit()
            self.textfield.setText("You can log in now! ")
        except mysql.connector.Error as e:
            print(e)

    def check_fields_data(self):
        super().__init__()
        password = self.user_password.text()
        confirm_password = self.user_confirm_password.text()
        self.textfield.setText('')
        if password != confirm_password:
            self.textfield.setText("Password doesn't match! ")
        else:
            self.add_data_to_db()
            self.textfield.setText("You can log in now!")


app = qtw.QApplication(sys.argv)

window = MainWidget()

sys.exit(app.exec())
