import os
import sqlalchemy as sa
from configparser import ConfigParser
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import declarative_base
from src.lib.utils import get_project_root

PROJECT_PATH = get_project_root()
Base = declarative_base()


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


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(sa.Integer, primary_key=True)
    ordered_parts = Column(sa.String(30), nullable=False)
    user_id = Column(sa.ForeignKey('users.id'), nullable=False)
    costs = Column(sa.Float(10))
    profit = Column(sa.Float(20))


class Car_parts(Base):
    __tablename__ = 'car_parts'
    id = Column(sa.Integer, primary_key=True)
    product_name = Column(sa.String(100), nullable=False)
    product_description = Column(sa.String(100))
    category = Column(sa.String(50), nullable=False)
    price = Column(sa.Float(10), nullable=False)
    sell_price = Column(sa.Float(10), nullable=False)
    application = Column(sa.String(100))
    manufacturer = Column(sa.String(100), nullable=False)


class DB:
    def __init__(self):
        pass

    def get_connection_string(self):
        config_file_path = '../../config.ini'
        if os.path.exists(config_file_path):
            conf_obj = ConfigParser()
            conf_obj.read(config_file_path)
            db_section = conf_obj['mysql']
            host = db_section['HOST']
            user = db_section['USER']
            password = db_section['PASSWORD']
            db = db_section['DATABASE']
            return f"mysql+pymysql://{user}:{password}@{host}/{db}"

    def setup_engine(self, conn_string):
        self.engine = sa.create_engine(conn_string)
        print("You are connected :)")
        return self.engine

    def get_tables(self):
        try:
            metadata = sa.MetaData()
            # get all tables:
            metadata.reflect(bind=self.engine)

        except Exception as err:
            print(err)
            exit()


if __name__ == '__main__':
    db = DB()
    print(db.get_connection_string())

    # setup engine
    db.setup_engine(db.get_connection_string())

    # create tables:
    users = Users()

    Base.metadata.create_all(bind=db.engine)

    db.get_tables()


