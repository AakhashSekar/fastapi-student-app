from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from sqlalchemy.orm import Session
from database import Engine, Session_Local
from models import Students
import models

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=Engine)


def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class StudentVal(BaseModel):
    id: int
    name: str
    department: str
    age: int = Field(gt=18)
    email: EmailStr
    year: int = Field(gt=0, lt=5)


@app.get("/")
async def root():
    return {"message": "FastAPI is working! Visit /docs to explore the API."}


# get all students data
@app.get('/students')
async def get_all_students(db: db_dependency, limit: int = 10):
    details = db.query(Students).limit(limit).all()
    if not details:
        raise HTTPException(status_code=404, message="Data not found")
    return details


# gets student data by id
@app.get('/students/{student_id}')
async def get_Students_By_Id(student_id: int, db: db_dependency):
    stud = db.query(Students).filter(Students.id == student_id).first()
    if not stud:
        raise HTTPException(status_code=404, message="Data not found")
    return stud


# gets student data by dep name
@app.get('/students/departments/{department_name}')
async def get_Students_By_Department(department_name: str, db: db_dependency):
    dept = db.query(Students).filter(func.lower(Students.department) == department_name.lower()).first()
    if not dept:
        raise HTTPException(status_code=404, message="Data not found")
    return dept


# gets student data by name
@app.get('/students/search/name/')
async def get_Students_By_Name(student_name: str, db: db_dependency):
    name = db.query(Students).filter(func.lower(Students.Student_name) == student_name.lower()).first()
    if not name:
        raise HTTPException(status_code=404, message="Data not found")
    return name


# gets students data by year of joining
@app.get('/students/search/')
async def get_Students_By_Year(year: int, db: db_dependency):
    yr = db.query(Students).filter(Students.year == year).first()
    if not yr:
        raise HTTPException(status_code=404, message="Data not found")
    return yr


# adds new student data  entry to student_db
@app.post('/students/create')
async def add_Students(addStudents: StudentVal, db: db_dependency):
    db_users = Students(**addStudents.model_dump())
    db.add(db_users)
    db.commit()
    db.refresh(db_users)
    return db_users


# updates the existing student data
@app.put('/student/update/{student_id}')
async def update_students(student_id: int, updateStudent: StudentVal, db: db_dependency):
    stud_edit = db.query(Students).filter(Students.id == student_id).first()
    if not stud_edit:
        raise HTTPException(status_code=404, message="Data not found")
    edited_data = updateStudent.model_dump(exclude_unset=True)
    for key, value in edited_data.items():
        setattr(stud_edit, key, value)
    db.add(stud_edit)
    db.commit()
    db.refresh(stud_edit)
    return stud_edit


# deletes the student data or entry
@app.delete('/student/remove')
async def remove_Student_Data(student_id: int, db: db_dependency):
    db_user = db.query(Students).filter(Students.id == student_id).first()
    if not db_user:
        raise HTTPException(status_code=404, message="Data not found")
    db.delete(db_user)
    db.commit()
    return {"message": "Item deleted succesfully"}