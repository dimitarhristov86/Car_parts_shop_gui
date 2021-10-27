import configparser
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from configparser import ConfigParser


def db_conn():
    try:
        conf_obj = ConfigParser()
        conf_obj.read('../../config.ini')
        db_section = conf_obj['mysql']
        host = db_section['host']
        user = db_section['user']
        password = db_section['password']
        port = int(db_section['port'])
        db = db_section['database']
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db}")
        metadata = MetaData()
        metadata.reflect(bind=engine)
        print("You are connected :)")
        return db_section.name, metadata
    except configparser.Error as err:
        print(err)

    # if engine:
    #     print(db_section.name)
    #     print(f'You are now connected to {db} database')