from typing import List, Optional, Tuple
from sqlmodel import Session, select, col, func
from datetime import datetime
from app.domain.models.student import Student
from app.domain.repositories.student_repository import StudentRepositoryInterface
from app.infrastructure.persistence.student_entity import StudentEntity
from app.infrastructure.mappers.student_mapper import StudentMapper


class StudentRepository(StudentRepositoryInterface):
    """Implementation of student repository"""

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, offset: int = 0, limit: int = 10) -> Tuple[List[Student], int]:
        """Get all students with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(StudentEntity)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(StudentEntity).offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        students = [StudentMapper.to_domain(entity) for entity in entities]
        return students, total

    async def get_by_id(self, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        entity = self.session.get(StudentEntity, student_id)
        return StudentMapper.to_domain(entity) if entity else None

    async def create(self, student: Student) -> Student:
        """Create a new student"""
        entity = StudentMapper.to_entity(student)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return StudentMapper.to_domain(entity)

    async def update(self, student: Student) -> Student:
        """Update an existing student"""
        if student.id is None:
            raise ValueError("Cannot update student without ID")
            
        entity = self.session.get(StudentEntity, student.id)
        if not entity:
            raise ValueError(f"Student with ID {student.id} not found")
            
        # Update entity with domain model data
        entity.updated_at = datetime.now()
        StudentMapper.update_entity(entity, student)
        
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return StudentMapper.to_domain(entity)

    async def delete(self, student_id: int) -> bool:
        """Delete a student"""
        entity = self.session.get(StudentEntity, student_id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False

    async def get_by_school_id(self, school_id: int, offset: int = 0, limit: int = 10) -> Tuple[List[Student], int]:
        """Get students by school ID with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(StudentEntity).where(StudentEntity.school_id == school_id)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(StudentEntity).where(StudentEntity.school_id == school_id).offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        students = [StudentMapper.to_domain(entity) for entity in entities]
        return students, total

    async def get_by_grade_level(self, grade_level: int, offset: int = 0, limit: int = 10) -> Tuple[List[Student], int]:
        """Get students by grade level with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(StudentEntity).where(StudentEntity.grade_level == grade_level)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(StudentEntity).where(StudentEntity.grade_level == grade_level).offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        students = [StudentMapper.to_domain(entity) for entity in entities]
        return students, total

    async def search_by_name(self, name: str, offset: int = 0, limit: int = 10) -> Tuple[List[Student], int]:
        """Search students by name with pagination"""
        name_filter = (
            col(StudentEntity.first_name).ilike(f"%{name}%") | 
            col(StudentEntity.last_name).ilike(f"%{name}%")
        )
        
        # Get total count
        count_statement = select(func.count()).select_from(StudentEntity).where(name_filter)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(StudentEntity).where(name_filter).offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        students = [StudentMapper.to_domain(entity) for entity in entities]
        return students, total

    async def count_by_school_id(self, school_id: int) -> int:
        """Count students by school ID"""
        count_statement = select(func.count()).select_from(StudentEntity).where(StudentEntity.school_id == school_id)
        return self.session.exec(count_statement).one()
