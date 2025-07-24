from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL='postgresql://postgres:Abcd%40123@localhost:5432/student'

Engine = create_engine(DATABASE_URL)

Session_Local = sessionmaker(autocommit=False, autoFlush = False, bind = Engine)

Base = declarative_base()