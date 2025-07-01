from typing import List, Optional
from datetime import date
from app.domain.models.student import Student
from app.domain.repositories.student_repository import StudentRepositoryInterface
from app.application.dtos.student_dto import StudentCreateDTO, StudentUpdateDTO, StudentResponseDTO
from app.core.pagination import PaginationParams, PaginatedResponse


class StudentService:
    """Service layer for student operations"""

    def __init__(self, student_repository: StudentRepositoryInterface):
        self.student_repository = student_repository

    async def get_all_students(self, pagination: PaginationParams) -> PaginatedResponse[StudentResponseDTO]:
        """Get all students with pagination"""
        students, total = await self.student_repository.get_all(pagination.offset, pagination.limit)
        student_dtos = [self._to_response_dto(student) for student in students]
        return PaginatedResponse.create(student_dtos, total, pagination)

    async def get_student_by_id(self, student_id: int) -> Optional[StudentResponseDTO]:
        """Get student by ID"""
        student = await self.student_repository.get_by_id(student_id)
        if student:
            return self._to_response_dto(student)
        return None

    async def create_student(self, student_data: StudentCreateDTO) -> StudentResponseDTO:
        """Create a new student"""
        student = Student(
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            email=student_data.email or "",
            phone_number=student_data.phone or "",
            date_of_birth=student_data.date_of_birth,
            grade_level=student_data.grade_level,
            school_id=student_data.school_id,
            enrollment_date=student_data.enrollment_date,
            address=student_data.address,
            is_active=student_data.is_active
        )
        created_student = await self.student_repository.create(student)
        return self._to_response_dto(created_student)

    async def update_student(self, student_id: int, student_data: StudentUpdateDTO) -> Optional[StudentResponseDTO]:
        """Update an existing student"""
        student = await self.student_repository.get_by_id(student_id)
        if not student:
            return None

        # Map DTO fields to domain model fields
        update_data = {}
        dto_data = student_data.model_dump(exclude_unset=True)
        
        if 'phone' in dto_data:
            update_data['phone_number'] = dto_data['phone']
        
        # Map other fields directly
        for field in ['first_name', 'last_name', 'email', 'date_of_birth', 'grade_level', 
                     'school_id', 'enrollment_date', 'address', 'is_active']:
            if field in dto_data:
                update_data[field] = dto_data[field]

        updated_student = student.update(**update_data)
        updated_student = await self.student_repository.update(updated_student)
        return self._to_response_dto(updated_student)

    async def delete_student(self, student_id: int) -> bool:
        """Delete a student"""
        return await self.student_repository.delete(student_id)

    async def get_students_by_school_id(self, school_id: int, pagination: PaginationParams) -> PaginatedResponse[StudentResponseDTO]:
        """Get students by school ID with pagination"""
        students, total = await self.student_repository.get_by_school_id(school_id, pagination.offset, pagination.limit)
        student_dtos = [self._to_response_dto(student) for student in students]
        return PaginatedResponse.create(student_dtos, total, pagination)

    async def get_students_by_grade_level(self, grade_level: int, pagination: PaginationParams) -> PaginatedResponse[StudentResponseDTO]:
        """Get students by grade level with pagination"""
        students, total = await self.student_repository.get_by_grade_level(grade_level, pagination.offset, pagination.limit)
        student_dtos = [self._to_response_dto(student) for student in students]
        return PaginatedResponse.create(student_dtos, total, pagination)

    async def search_students_by_name(self, name: str, pagination: PaginationParams) -> PaginatedResponse[StudentResponseDTO]:
        """Search students by name with pagination"""
        students, total = await self.student_repository.search_by_name(name, pagination.offset, pagination.limit)
        student_dtos = [self._to_response_dto(student) for student in students]
        return PaginatedResponse.create(student_dtos, total, pagination)

    def _to_response_dto(self, student: Student) -> StudentResponseDTO:
        """Convert domain model to response DTO"""
        return StudentResponseDTO(
            id=student.id or 0,  # Handle None case
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            phone=student.phone_number,
            date_of_birth=student.date_of_birth,
            grade_level=student.grade_level,
            school_id=student.school_id,
            enrollment_date=student.enrollment_date,
            address=student.address,
            is_active=student.is_active
        )
