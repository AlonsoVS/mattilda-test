from typing import List, Optional, Tuple
from sqlmodel import Session, select, col, func
from app.domain.entities.student import Student
from app.domain.repositories.student_repository import StudentRepositoryInterface


class StudentRepository(StudentRepositoryInterface):
    """Implementation of student repository"""

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, offset: int = 0, limit: int = 10) -> Tuple[List[Student], int]:
        """Get all students with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(Student)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(Student).offset(offset).limit(limit)
        result = self.session.exec(statement)
        return list(result.all()), total

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

    async def get_by_school_id(self, school_id: int, offset: int = 0, limit: int = 10) -> Tuple[List[Student], int]:
        """Get students by school ID with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(Student).where(Student.school_id == school_id)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(Student).where(Student.school_id == school_id).offset(offset).limit(limit)
        result = self.session.exec(statement)
        return list(result.all()), total

    async def get_by_grade_level(self, grade_level: int, offset: int = 0, limit: int = 10) -> Tuple[List[Student], int]:
        """Get students by grade level with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(Student).where(Student.grade_level == grade_level)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(Student).where(Student.grade_level == grade_level).offset(offset).limit(limit)
        result = self.session.exec(statement)
        return list(result.all()), total

    async def search_by_name(self, name: str, offset: int = 0, limit: int = 10) -> Tuple[List[Student], int]:
        """Search students by name with pagination"""
        name_filter = (
            col(Student.first_name).ilike(f"%{name}%") | 
            col(Student.last_name).ilike(f"%{name}%")
        )
        
        # Get total count
        count_statement = select(func.count()).select_from(Student).where(name_filter)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(Student).where(name_filter).offset(offset).limit(limit)
        result = self.session.exec(statement)
        return list(result.all()), total
