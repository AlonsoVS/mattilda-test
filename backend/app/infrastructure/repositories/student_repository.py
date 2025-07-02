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

    async def count_by_school_id(self, school_id: int) -> int:
        """Count students by school ID"""
        count_statement = select(func.count()).select_from(StudentEntity).where(StudentEntity.school_id == school_id)
        return self.session.exec(count_statement).one()

    async def get_with_filters(self, filters: dict, offset: int = 0, limit: int = 10) -> Tuple[List[Student], int]:
        """Get students with flexible filtering and pagination"""
        # Build the base query
        statement = select(StudentEntity)
        count_statement = select(func.count()).select_from(StudentEntity)
        
        # Apply filters
        conditions = []
        
        if filters.get('first_name'):
            conditions.append(col(StudentEntity.first_name).ilike(f"%{filters['first_name']}%"))
        
        if filters.get('last_name'):
            conditions.append(col(StudentEntity.last_name).ilike(f"%{filters['last_name']}%"))
        
        if filters.get('email'):
            conditions.append(col(StudentEntity.email).ilike(f"%{filters['email']}%"))
        
        if filters.get('phone'):
            conditions.append(col(StudentEntity.phone_number).ilike(f"%{filters['phone']}%"))
        
        if filters.get('date_of_birth'):
            conditions.append(StudentEntity.date_of_birth == filters['date_of_birth'])
        
        if filters.get('grade_level') is not None:
            conditions.append(StudentEntity.grade_level == filters['grade_level'])
        
        if filters.get('school_id') is not None:
            conditions.append(StudentEntity.school_id == filters['school_id'])
        
        if filters.get('enrollment_date'):
            conditions.append(StudentEntity.enrollment_date == filters['enrollment_date'])
        
        if filters.get('address'):
            conditions.append(col(StudentEntity.address).ilike(f"%{filters['address']}%"))
        
        if filters.get('is_active') is not None:
            conditions.append(StudentEntity.is_active == filters['is_active'])
        
        # Apply conditions to both statements
        if conditions:
            from sqlmodel import and_
            filter_condition = and_(*conditions)
            statement = statement.where(filter_condition)
            count_statement = count_statement.where(filter_condition)
        
        # Get total count
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = statement.offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        students = [StudentMapper.to_domain(entity) for entity in entities]
        return students, total
