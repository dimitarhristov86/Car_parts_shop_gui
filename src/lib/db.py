from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, sql

#  connect engine to mysql db
engine = create_engine('mysql+pymysql://root:@localhost/car_parts_gui')
# create metadata instance, which will return tables in db
metadata = MetaData()
print(metadata.tables)
# reflect db schema to Metadata
metadata.reflect(bind=engine)
print(metadata.tables)
