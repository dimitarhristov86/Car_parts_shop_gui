import os
import sqlalchemy as sa
from configparser import ConfigParser
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import declarative_base
from src.lib.utils import get_project_root
# get the project path
PROJECT_PATH = get_project_root()
# declarative_base() returns a Base class from which all classes(tables) will inherit
Base = declarative_base()


# create Users table in db
class Users(Base):
    __tablename__ = 'users'
    id = Column(sa.Integer, primary_key=True)
    role = Column(sa.String(5))
    first_name = Column(sa.String(20))
    last_name = Column(sa.String(20))
    email = Column(sa.String(100))
    phone_number = Column(sa.String(10))
    password = Column(sa.String(20))
    created = Column(sa.DateTime())


# create Orders table in db
class Orders(Base):
    __tablename__ = 'orders'
    id = Column(sa.Integer, primary_key=True)
    ordered_parts = Column(sa.String(30), nullable=False)
    user_id = Column(sa.ForeignKey('users.id'), nullable=False)
    costs = Column(sa.Float(10))
    profit = Column(sa.Float(20))


# create Car_parts table in db
class Car_parts(Base):
    __tablename__ = 'car_parts'
    id = Column(sa.Integer, primary_key=True)
    product_name = Column(sa.String(100), nullable=False)
    product_description = Column(sa.String(100))
    category = Column(sa.String(50), nullable=False)
    application = Column(sa.String(100))
    manufacturer = Column(sa.String(100), nullable=False)


class DB:

    def get_connection_string(self):
        # set variable for config.ini file path as str
        config_file_path = f'{PROJECT_PATH}/config.ini'
        # check if the path(config.ini file) exist
        if os.path.exists(config_file_path):
            # set variable for ConfigParser() class which is used for configuration purposes
            conf_obj = ConfigParser()
            # read the config.ini file
            conf_obj.read(config_file_path)
            # set variables for database connection
            db_section = conf_obj['mysql']
            host = db_section['HOST']
            user = db_section['USER']
            password = db_section['PASSWORD']
            db = db_section['DATABASE']
            # returning the connection string for db connection
            return f"mysql+pymysql://{user}:{password}@{host}/{db}"
        else:
            print("No configuration file found! ")

    def setup_engine(self, conn_string):
        # initialize connection engine that will take the connection string to connect to db
        self.engine = sa.create_engine(conn_string)
        print("You are connected :)")
        return self.engine



