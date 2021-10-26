from sqlalchemy import create_engine
from sqlalchemy import MetaData
from configparser import ConfigParser


def db_conn():
    conf_obj = ConfigParser()
    conf_obj.read('../../config.ini')
    db_section = conf_obj['mysql']
    host = db_section['HOST']
    user = db_section['USER']
    password = db_section['PASSWORD']
    port = int(db_section['PORT'])
    db = db_section['DATABASE']
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db}")
    metadata = MetaData()
    metadata.reflect(bind=engine)
    if engine:
        print(f'You are now connected to {db} database')


db_conn()
