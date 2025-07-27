from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# DATABASE_URL='postgresql://postgres:Abcd%40123@localhost:5432/student'
DATABASE_URL=os.getenv("DATABASE_URL")

Engine = create_engine(DATABASE_URL)

Session_Local = sessionmaker(autocommit=False, autoflush = False, bind = Engine)

Base = declarative_base()