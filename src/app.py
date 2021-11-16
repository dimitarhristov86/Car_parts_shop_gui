import sys
import mysql.connector
from lib.crawler import Crawler
from lib.scraper import Scraper
from lib.db import DB, Users, Orders, Car_parts
from lib.utils import get_project_root
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine

PROJECT_ROOT = get_project_root()
engine = create_engine(f"mysql+pymysql://root:Dh_8601205280@localhost/car_parts_gui")
Session = sessionmaker(bind=engine)


class MainWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.add_scraped_data_to_db()
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
                if email and password in row:
                    self.main_menu()
                    self.textfield.setStyleSheet("color: green")
                    self.textfield.setText("Login successfully")
                    break
                else:
                    self.textfield.setText("Incorrect email or password")
            if len(email) == 0 or len(password) == 0:
                self.textfield.setText("Please fill all fields! ")
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
        self.btn_submit = qtw.QPushButton('Submit')
        self.btn_submit.setIcon(self.submit_icon)
        self.btn_to_login = qtw.QPushButton('Click here to log in')
        self.btn_to_login.setIcon((self.login_icon))
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
        self.btn_parts_view.clicked.connect(self.car_parts_menu)
        self.btn_log_out.clicked.connect(self.setup_ui)

    def add_data_to_db(self):
        super().__init__()
        try:
            user_f_name = self.user_first_name.text()
            user_l_name = self.user_last_name.text()
            user_email = self.user_email.text()
            user_ph_number = self.user_phone_number.text()
            user_password = self.user_password.text()
            user_created = self.user_created
            user = [Users(role='admin',
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
        email = self.user_email.text()
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

    # TODO: self.session doesn't recognized in add_scraped_data_to_db()
    def add_scraped_data_to_db(self):
        super().__init__()
        item_info = []
        for items in scraper.scrape_links_to_text():
            item_info.append(items)
        for item in item_info:
            item_name = item
            item_description = 'Engine oil for light vehicles'
            item_category = 'Engine oil'
            item_application = 'Use in light vehicles'
            item_manufacturer = item[0]
            car_part = [Car_parts(
                product_name=item_name,
                product_description=item_description,
                category=item_category,
                application=item_application,
                manufacturer=item_manufacturer)]
            self.session.add_all(car_part)
            self.session.commit()

    # def car_parts_menu(self):
    #     super().__init__()
    #     self.setWindowTitle("Car Parts")
    #     self.setFixedSize(900, 422)
    #     self.btn_show_parts = qtw.QPushButton("Show parts")
    #     layout = qtw.QVBoxLayout()
    #     layout.addWidget(self.table_widget)
    #     layout.addWidget(self.btn_show_parts)
    #     self.table_widget.setColumnCount(7)
    #     self.table_widget.setHorizontalHeaderLabels(['Code', 'Product name', 'Category', 'Client price',
    #                                                  'Application', 'Manufacturer'])
    #
    #     self.show()


crawler = Crawler('https://www.autokelly.bg/bg/products/43758570.html?ids=39849642;51224611')
crawler.run_crawler()
scraper = Scraper(crw_links=crawler.raw_links)
scraper.scrape_links_to_text()
app = qtw.QApplication(sys.argv)
window = MainWidget()
sys.exit(app.exec())
