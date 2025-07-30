from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import Session_Local
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)

SECRET = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 20

bcrypt_context = CryptContext(schemes=['bcrypt'], deprected='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenurl = 'auth/token')

#pydantic class for validation 
class CreateUser(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

#db connection 
def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/')
async def create_user(create_user_request: CreateUser, db: db_dependency):
    create_user_model = Users(username = create_user_request.username, hashed_password = bcrypt_context.hashed(create_user_request.password))
    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}

@router.post('/token', respose_model = Token)
async def gendrate_token(formdata: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(formdata.username, formdata.password, db)
    token = create_access_token(user.username, user.id)
    return{'access_token': token, 'token_type': 'bearer'}


def authenticate_user(username:str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str, id:int):
    encode = {'sub': username, 'id': id}
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET, algorithm=ALGORITHM)

# to validate the current user for end points 
async def get_current_users(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, details = "Coudnt valiadte user")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, details = "Coudnt valiadte user")

