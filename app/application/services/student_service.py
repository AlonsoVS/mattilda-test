from typing import List, Optional
from app.domain.entities.student import Student
from app.domain.repositories.student_repository import StudentRepositoryInterface
from app.application.dtos.student_dto import StudentCreateDTO, StudentUpdateDTO, StudentResponseDTO


class StudentService:
    """Service layer for student operations"""

    def __init__(self, student_repository: StudentRepositoryInterface):
        self.student_repository = student_repository

    async def get_all_students(self) -> List[StudentResponseDTO]:
        """Get all students"""
        students = await self.student_repository.get_all()
        return [StudentResponseDTO.model_validate(student) for student in students]

    async def get_student_by_id(self, student_id: int) -> Optional[StudentResponseDTO]:
        """Get student by ID"""
        student = await self.student_repository.get_by_id(student_id)
        if student:
            return StudentResponseDTO.model_validate(student)
        return None

    async def create_student(self, student_data: StudentCreateDTO) -> StudentResponseDTO:
        """Create a new student"""
        student = Student(**student_data.model_dump())
        created_student = await self.student_repository.create(student)
        return StudentResponseDTO.model_validate(created_student)

    async def update_student(self, student_id: int, student_data: StudentUpdateDTO) -> Optional[StudentResponseDTO]:
        """Update an existing student"""
        student = await self.student_repository.get_by_id(student_id)
        if not student:
            return None

        # Update only provided fields
        update_data = student_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(student, field, value)

        updated_student = await self.student_repository.update(student)
        return StudentResponseDTO.model_validate(updated_student)

    async def delete_student(self, student_id: int) -> bool:
        """Delete a student"""
        return await self.student_repository.delete(student_id)

    async def get_students_by_school_id(self, school_id: int) -> List[StudentResponseDTO]:
        """Get students by school ID"""
        students = await self.student_repository.get_by_school_id(school_id)
        return [StudentResponseDTO.model_validate(student) for student in students]

    async def get_students_by_grade_level(self, grade_level: int) -> List[StudentResponseDTO]:
        """Get students by grade level"""
        students = await self.student_repository.get_by_grade_level(grade_level)
        return [StudentResponseDTO.model_validate(student) for student in students]

    async def search_students_by_name(self, name: str) -> List[StudentResponseDTO]:
        """Search students by name"""
        students = await self.student_repository.search_by_name(name)
        return [StudentResponseDTO.model_validate(student) for student in students]
