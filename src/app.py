import sys
import mysql.connector
from lib.crawler import Crawler
from lib.scraper import Scraper
from lib.db import DB, Users, Orders, Car_parts
from lib.utils import get_project_root
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine


class MainWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.session = Session()
        self.session.begin()
        self.textfield = qtw.QLabel()
        self.cursor = qtg.QTextCursor()
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
            f"background-image: url({PROJECT_ROOT}/images/1.jpg)")
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
            for row in self.session.query(Users.email, Users.password):
                if len(email) == 0 or len(password) == 0:
                    self.textfield.setStyleSheet("color: red")
                    self.textfield.setText("Please fill all fields! ")
                    break
                if email in row.email and password in row.password:
                    self.textfield.setStyleSheet("color: green")
                    self.textfield.setText("Login successfully")
                    if self.textfield.text() == 'Login successfully':
                        self.main_menu()
                    break
                else:
                    self.textfield.setStyleSheet("color: red")
                    self.textfield.setText("Incorrect email or password")
        except Exception as e:
            print(e)

    def sign_up_form(self):
        super().__init__()
        self.setWindowTitle('Sign up Form')
        self.setFixedSize(900, 422)
        self.window = qtw.QLabel(self)
        self.window.setStyleSheet(
            f"background-image: url({PROJECT_ROOT}/images/image.png)")
        self.window.setFixedSize(900, 422)
        self.submit_icon = QIcon(f'{PROJECT_ROOT}/images/submit-icon.jpg')
        self.login_icon = QIcon(f'{PROJECT_ROOT}/images/login.jpg')
        self.user_first_name = qtw.QLineEdit(self)
        self.user_last_name = qtw.QLineEdit(self)
        self.user_email = qtw.QLineEdit(self)
        self.user_phone_number = qtw.QLineEdit(self)
        self.user_password = qtw.QLineEdit(self)
        self.user_confirm_password = qtw.QLineEdit(self)
        self.user_created = datetime.now()
        self.btn_submit = qtw.QPushButton('')
        self.btn_submit.setIcon(self.submit_icon)
        size = QtCore.QSize(150, 100)
        self.btn_submit.setIconSize(size)
        self.btn_to_login = qtw.QPushButton('')
        self.btn_to_login.setIcon((self.login_icon))
        self.btn_to_login.setIconSize(size)
        self.btn_submit.setFixedSize(150, 50)
        self.btn_submit.setStyleSheet('background-color: white')
        self.btn_to_login.setFixedSize(150, 50)
        self.btn_to_login.setStyleSheet('background-color: white')
        self.textfield = qtw.QLabel(self)
        self.textfield.setStyleSheet("color: red")
        layout = qtw.QHBoxLayout()
        layout.addWidget(self.btn_submit)
        layout.addWidget(self.btn_to_login)
        layout.setSpacing(150)
        new_layout = qtw.QFormLayout()
        new_layout.addRow("Enter your first name: ", self.user_first_name)
        new_layout.addRow("Enter your last name: ", self.user_last_name)
        new_layout.addRow("Enter email: ", self.user_email)
        new_layout.addRow("Enter phone number (must start with 0...... and long 10 digits): ", self.user_phone_number)
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
        self.btn_parts_view = qtw.QPushButton('View all parts')
        self.btn_parts_view.setFixedSize(100, 50)
        self.btn_log_out = qtw.QPushButton('Log out')
        self.btn_log_out.setFixedSize(100, 50)
        # self.btn_admin_menu = qtw.QPushButton('Admin menu')
        # self.btn_admin_menu.setFixedSize(100, 50)
        btn_layout = qtw.QVBoxLayout()
        btn_layout.addWidget(self.btn_parts_view)
        btn_layout.addWidget(self.btn_log_out)
        # btn_layout.addWidget(self.btn_admin_menu)
        self.setLayout(btn_layout)
        self.btn_parts_view.clicked.connect(self.car_parts_menu)
        self.btn_log_out.clicked.connect(self.sign_in)
        self.show()

    def add_data_to_db(self):
        super().__init__()
        try:
            user_f_name = self.user_first_name.text()
            user_l_name = self.user_last_name.text()
            user_email = self.user_email.text()
            user_ph_number = self.user_phone_number.text()
            user_password = self.user_password.text()
            user_created = self.user_created
            user = [Users(role='user',
                          first_name=f'{user_f_name}',
                          last_name=f'{user_l_name}',
                          email=f'{user_email}',
                          phone_number=f'{user_ph_number}',
                          password=f'{user_password}',
                          created=f'{user_created}')]
            self.session.add_all(user)
            self.session.commit()
            self.textfield.setText("You can log in now! ")
        except mysql.connector.Error as e:
            print(e)

    def check_fields_data(self):
        super().__init__()
        phone_number = self.user_phone_number.text()
        password = self.user_password.text()
        confirm_password = self.user_confirm_password.text()
        self.textfield.setText('')
        if password != confirm_password:
            self.textfield.setStyleSheet("color: red")
            self.textfield.setText("Password doesn't match! ")
        elif not phone_number.startswith("0") or len(phone_number) < 10:
            self.textfield.setStyleSheet("color: red")
            self.textfield.setText("Incorrect phone number")
        else:
            self.add_data_to_db()
            self.textfield.setStyleSheet("color: green")
            self.textfield.setText("You can log in now!")

    def car_parts_menu(self):
        super().__init__()
        self.setWindowTitle("Car Parts")
        self.setFixedSize(1280, 720)
        self.table_widget = qtw.QTableWidget()
        self.table_widget.setRowCount(152)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Product name', 'Product description',
                                                     'Category', 'Application', 'Manufacturer'])
        self.table_widget.setColumnWidth(0, 2)
        self.table_widget.setColumnWidth(1, 400)
        self.table_widget.setColumnWidth(2, 200)
        self.table_widget.setColumnWidth(3, 100)
        self.table_widget.setColumnWidth(4, 150)
        self.table_widget.setColumnWidth(5, 100)
        row_count = 0
        for row in self.session.query(Car_parts.id, Car_parts.product_name,
                                      Car_parts.product_description,
                                      Car_parts.category, Car_parts.application,
                                      Car_parts.manufacturer).all():
            self.table_widget.setItem(row_count, 0, qtw.QTableWidgetItem(str(row[0])))
            self.table_widget.setItem(row_count, 1, qtw.QTableWidgetItem(row[1]))
            self.table_widget.setItem(row_count, 2, qtw.QTableWidgetItem(row[2]))
            self.table_widget.setItem(row_count, 3, qtw.QTableWidgetItem(row[3]))
            self.table_widget.setItem(row_count, 4, qtw.QTableWidgetItem(row[4]))
            self.table_widget.setItem(row_count, 5, qtw.QTableWidgetItem(row[5]))
            row_count += 1
        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.table_widget)
        self.setLayout(vbox)
        self.show()


crawler = Crawler('https://www.autokelly.bg/bg/products/43758570.html?ids=39849642;51224611')
crawler.run_crawler()
scraper = Scraper(crw_links=crawler.raw_links)
scraper.scrape_links_to_text()
scraper.check_table_content()
db = DB()
engine = db.setup_engine(conn_string=db.get_connection_string())
Session = sessionmaker(bind=engine)
PROJECT_ROOT = get_project_root()
app = qtw.QApplication(sys.argv)
window = MainWidget()
sys.exit(app.exec())
