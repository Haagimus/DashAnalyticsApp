from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


server = 'FRXSV-DAUPHIN'
dbname = 'FRXResourceDemand'
FRXResourceDemandURL = 'mssql://' + server + '/' + dbname + '?trusted_connection=yes&driver=SQL+Server'

engine = create_engine(FRXResourceDemandURL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
