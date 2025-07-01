from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.infrastructure.database.connection import get_session
from app.infrastructure.repositories.student_repository import StudentRepository
from app.application.services.student_service import StudentService
from app.application.dtos.student_dto import StudentCreateDTO, StudentUpdateDTO, StudentResponseDTO

router = APIRouter(prefix="/students", tags=["students"])


def get_student_service(session: Session = Depends(get_session)) -> StudentService:
    """Dependency to get student service"""
    student_repository = StudentRepository(session)
    return StudentService(student_repository)


@router.get("/", response_model=List[StudentResponseDTO])
async def get_students(student_service: StudentService = Depends(get_student_service)):
    """Get all students"""
    return await student_service.get_all_students()


@router.get("/{student_id}", response_model=StudentResponseDTO)
async def get_student(student_id: int, student_service: StudentService = Depends(get_student_service)):
    """Get a student by ID"""
    student = await student_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=StudentResponseDTO)
async def create_student(
    student: StudentCreateDTO,
    student_service: StudentService = Depends(get_student_service)
):
    """Create a new student"""
    return await student_service.create_student(student)


@router.put("/{student_id}", response_model=StudentResponseDTO)
async def update_student(
    student_id: int,
    student_update: StudentUpdateDTO,
    student_service: StudentService = Depends(get_student_service)
):
    """Update a student by ID"""
    student = await student_service.update_student(student_id, student_update)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}")
async def delete_student(
    student_id: int,
    student_service: StudentService = Depends(get_student_service)
):
    """Delete a student by ID"""
    success = await student_service.delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}


@router.get("/school/{school_id}", response_model=List[StudentResponseDTO])
async def get_students_by_school(
    school_id: int,
    student_service: StudentService = Depends(get_student_service)
):
    """Get students by school ID"""
    return await student_service.get_students_by_school_id(school_id)


@router.get("/grade/{grade_level}", response_model=List[StudentResponseDTO])
async def get_students_by_grade(
    grade_level: int,
    student_service: StudentService = Depends(get_student_service)
):
    """Get students by grade level"""
    return await student_service.get_students_by_grade_level(grade_level)


@router.get("/search/by-name/{name}", response_model=List[StudentResponseDTO])
async def search_students_by_name(
    name: str,
    student_service: StudentService = Depends(get_student_service)
):
    """Search students by first or last name"""
    return await student_service.search_students_by_name(name)
