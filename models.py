from sqlalchemy import Column, Integer, String
from database import Base

class Students(Base):
    __tablename__ = 'student_details'
    id = Column(Integer, primary_key = True, index= True, autoincrement= True)
    name = Column(String, index = True)
    department = Column(String)
    age = Column(Integer)
    email = Column(String)
    year = Column(Integer)

class Users(Base):
    __tablename__='User'
    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    username = Column(String)
    password = Column(String)
