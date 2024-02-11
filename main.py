from fastapi import FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI(docs_url="/")
Base = declarative_base()

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String)
    phone = Column(Integer)
    age = Column(Integer)

class TeacherModel(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String)
    surname = Column(String)
    phone = Column(Integer)
    adress = Column(String)
    age = Column(Integer)

class ClassModel(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class GradeModel(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    class_id = Column(Integer, index=True)
    grade = Column(Integer)

class SubjectModel(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

class Teacher(BaseModel):
    name: str
    subject: str
    surname: str
    phone: int
    adress: str
    age: int

class Subject(BaseModel):
    name: str

students_router = APIRouter(prefix="/students", tags=["Управление студентами"])
classes_router = APIRouter(prefix="/classes", tags=["Управление классами"])
grades_router = APIRouter(prefix="/grades", tags=["Управление оценками"])
teachers_router = APIRouter(prefix="/teachers", tags=["Управление учителями"])

class Student(BaseModel):
    name: str
    id: int
    surname: str
    phone: int
    age: int

@students_router.post("/students/", response_model=Student)
def create_student(student: Student):
    db = SessionLocal()
    db_student = StudentModel(
        name=student.name,
        id=student.id,
        surname=student.surname,
        phone=student.phone,
        age=student.age
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    db.close()
    return db_student

@students_router.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int):
    db = SessionLocal()
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    db.close()
    return db_student

@students_router.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student):
    db = SessionLocal()
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    db.close()
    return db_student


class Class(BaseModel):
    name: str

class Grade(BaseModel):
    student_id: int
    class_id: int
    grade: int
classes_router = APIRouter(prefix="/classes", tags=["Управление классами"])

@classes_router.post("/classes/", response_model=Class)
def create_class(class_: Class):
    db = SessionLocal()
    db_class = ClassModel(**class_.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    db.close()
    return db_class

@classes_router.get("/classes/{class_id}", response_model=Class)
def read_class(class_id: int):
    db = SessionLocal()
    db_class = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    db.close()
    return db_class

@classes_router.put("/classes/{class_id}", response_model=Class)
def update_class(class_id: int, class_: Class):
    db = SessionLocal()
    db_class = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    for key, value in class_.dict().items():
        setattr(db_class, key, value)
    db.commit()
    db.refresh(db_class)
    db.close()
    return db_class

@grades_router.post("/grades/", response_model=Grade)
def create_grade(grade: Grade):
    db = SessionLocal()
    db_grade = GradeModel(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    db.close()
    return db_grade

@grades_router.get("/grades/{grade_id}", response_model=Grade)
def read_grade(grade_id: int):
    db = SessionLocal()
    db_grade = db.query(GradeModel).filter(GradeModel.id == grade_id).first()
    db.close()
    return db_grade

@grades_router.put("/grades/{grade_id}", response_model=Grade)
def update_grade(grade_id: int, grade: Grade):
    db = SessionLocal()
    db_grade = db.query(GradeModel).filter(GradeModel.id == grade_id).first()
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Grade not found")
    for key, value in grade.dict().items():
        setattr(db_grade, key, value)
    db.commit()
    db.refresh(db_grade)
    db.close()
    return db_grade

@teachers_router.post("/teachers/", response_model=Teacher)
def create_teacher(teacher: Teacher):
    db = SessionLocal()
    db_teacher = TeacherModel(
        name=teacher.name,
        subject=teacher.subject,
        surname=teacher.surname,
        phone=teacher.phone,
        adress=teacher.adress,
        age=teacher.age
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    db.close()
    return db_teacher

@teachers_router.get("/teachers/{teacher_id}", response_model=Teacher)
def read_teacher(teacher_id: int):
    db = SessionLocal()
    db_teacher = db.query(TeacherModel).filter(TeacherModel.id == teacher_id).first()
    db.close()
    return db_teacher

@teachers_router.put("/teachers/{teacher_id}", response_model=Teacher)
def update_teacher(teacher_id: int, teacher: Teacher):
    db = SessionLocal()
    db_teacher = db.query(TeacherModel).filter(TeacherModel.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    for key, value in teacher.dict().items():
        setattr(db_teacher, key, value)
    db.commit()
    db.refresh(db_teacher)
    db.close()
    return db_teacher


@students_router.delete("/students/{student_id}")
def delete_student(student_id: int):
    db = SessionLocal()
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if student is not None:
        db.delete(student)
        db.commit()
    db.close()
    return {"message": "Student deleted"}

@classes_router.delete("/classes/{class_id}")
def delete_class(class_id: int):
    db = SessionLocal()
    classes = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    if classes is not None:
        db.delete(classes)
        db.commit()
    db.close()
    return {"message": "Class deleted"}

@teachers_router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    db = SessionLocal()
    teacher = db.query(TeacherModel).filter(TeacherModel.id == teacher_id).first()
    if teacher is not None:
        db.delete(teacher)
        db.commit()
    db.close()
    return {"message": "Teacher deleted"}

@grades_router.delete("/grades/{grade_id}")
def delete_grade(grade_id: int):
    db = SessionLocal()
    grade = db.query(GradeModel).filter(GradeModel.id == grade_id).first()
    if grade is not None:
        db.delete(grade)
        db.commit()
    db.close()
    return {"message": "Grade deleted"}

app.include_router(students_router)
app.include_router(classes_router)
app.include_router(grades_router)
app.include_router(teachers_router)