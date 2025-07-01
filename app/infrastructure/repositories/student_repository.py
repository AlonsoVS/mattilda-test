from typing import List, Optional
from sqlmodel import Session, select, col
from app.domain.entities.student import Student
from app.domain.repositories.student_repository import StudentRepositoryInterface


class StudentRepository(StudentRepositoryInterface):
    """Implementation of student repository"""

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self) -> List[Student]:
        """Get all students"""
        statement = select(Student)
        result = self.session.exec(statement)
        return list(result.all())

    async def get_by_id(self, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        return self.session.get(Student, student_id)

    async def create(self, student: Student) -> Student:
        """Create a new student"""
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)
        return student

    async def update(self, student: Student) -> Student:
        """Update an existing student"""
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)
        return student

    async def delete(self, student_id: int) -> bool:
        """Delete a student"""
        student = self.session.get(Student, student_id)
        if student:
            self.session.delete(student)
            self.session.commit()
            return True
        return False

    async def get_by_school_id(self, school_id: int) -> List[Student]:
        """Get students by school ID"""
        statement = select(Student).where(Student.school_id == school_id)
        result = self.session.exec(statement)
        return list(result.all())

    async def get_by_grade_level(self, grade_level: int) -> List[Student]:
        """Get students by grade level"""
        statement = select(Student).where(Student.grade_level == grade_level)
        result = self.session.exec(statement)
        return list(result.all())

    async def search_by_name(self, name: str) -> List[Student]:
        """Search students by name"""
        statement = select(Student).where(
            col(Student.first_name).ilike(f"%{name}%") | 
            col(Student.last_name).ilike(f"%{name}%")
        )
        result = self.session.exec(statement)
        return list(result.all())
