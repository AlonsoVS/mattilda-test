from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select, col
from app.database import get_session
from app.models import Student, StudentCreate, StudentRead, StudentUpdate

student_router = APIRouter(prefix="/students", tags=["students"])


@student_router.get("/", response_model=List[StudentRead])
async def get_students(session: Session = Depends(get_session)):
    """Get all students"""
    students = session.exec(select(Student)).all()
    return students


@student_router.get("/{student_id}", response_model=StudentRead)
async def get_student(student_id: int, session: Session = Depends(get_session)):
    """Get a student by ID"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@student_router.post("/", response_model=StudentRead)
async def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    """Create a new student"""
    db_student = Student.model_validate(student)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student


@student_router.put("/{student_id}", response_model=StudentRead)
async def update_student(
    student_id: int, 
    student_update: StudentUpdate, 
    session: Session = Depends(get_session)
):
    """Update a student by ID"""
    db_student = session.get(Student, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Update only provided fields
    update_data = student_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student


@student_router.delete("/{student_id}")
async def delete_student(student_id: int, session: Session = Depends(get_session)):
    """Delete a student by ID"""
    db_student = session.get(Student, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    session.delete(db_student)
    session.commit()
    return {"message": "Student deleted successfully"}


@student_router.get("/school/{school_id}", response_model=List[StudentRead])
async def get_students_by_school(school_id: int, session: Session = Depends(get_session)):
    """Get students by school ID"""
    statement = select(Student).where(Student.school_id == school_id)
    students = session.exec(statement).all()
    return students


@student_router.get("/grade/{grade_level}", response_model=List[StudentRead])
async def get_students_by_grade(grade_level: int, session: Session = Depends(get_session)):
    """Get students by grade level"""
    statement = select(Student).where(Student.grade_level == grade_level)
    students = session.exec(statement).all()
    return students


@student_router.get("/search/by-name/{name}", response_model=List[StudentRead])
async def search_students_by_name(name: str, session: Session = Depends(get_session)):
    """Search students by first or last name"""
    statement = select(Student).where(
        col(Student.first_name).ilike(f"%{name}%") | 
        col(Student.last_name).ilike(f"%{name}%")
    )
    students = session.exec(statement).all()
    return students
