from configparser import ConfigParser
import mysql.connector as mc


def db_connect():
    mydb = mc.connect(
        host=db_config[0],
        user=db_config[1],
        password=db_config[2],
        database=db_config[3])
    return mydb


def read_db_config(filename='config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)
    host = parser['mysql']['host']
    user = parser['mysql']['user']
    password = parser['mysql']['password']
    db = parser['mysql']['database']
    db_config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in the {filename} file')
    return host, user, password, db


db_config = read_db_config()
