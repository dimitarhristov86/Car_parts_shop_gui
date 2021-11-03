import os
import sqlalchemy as sa
from configparser import ConfigParser
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import declarative_base
from utils import get_project_root

PROJECT_PATH = get_project_root()

from sqlalchemy.sql.sqltypes import String

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users_test'
    id = Column(sa.Integer, primary_key=True)
    first_name = Column(sa.String(20))
    last_name = Column(sa.String(20))


class Orders(Base):
    __tablename__ = 'orders_test'
    id = Column(sa.Integer, primary_key=True)
    ordered_parts = Column(sa.String(30), nullable=False)
    user_id = Column(sa.ForeignKey('users_test.id'), nullable=False)


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


    def get_tables(self):
        try:
            metadata = sa.MetaData()
            # self.users = sa.Table('users', metadata, autoload_with=self.engine)
            # self.car_parts = sa.Table('car_parts', metadata, autoload_with=self.engine)
            # self.orders = sa.Table('orders', metadata, autoload_with=self.engine)

            # get all tables:
            metadata.reflect(bind=self.engine)
            print(metadata.tables.keys())


        except Exception as err:
            print(f'@@@@@@@@@@@@@@@@@@@@@@: {err}')
            exit()

    def insert(self, table_name, data):
        with self.engine.connect() as conn:
            table = getattr(self, table_name)
            print(type(table))

            res = conn.execute(table.insert(), data)

    def select(self):
        pass


if __name__ == '__main__':
    db = DB()
    # print(db.get_connection_string())

    # setup engine
    db.setup_engine(db.get_connection_string())

    # create tables:
    # users = Users()

    # Base.metadata.create_all(self.engine)

    db.get_tables()

    # insert into table
    # data = {
    #     "role":'admin',
    #     "first_name":'Ada',
    #     "email":'ada@abv.bg',
    #     "password": '1234'
    # }
    # db.insert('users', data)
