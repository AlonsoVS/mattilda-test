from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.student import Student


class StudentRepositoryInterface(ABC):
    """Interface for student repository"""

    @abstractmethod
    async def get_all(self) -> List[Student]:
        """Get all students"""
        pass

    @abstractmethod
    async def get_by_id(self, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        pass

    @abstractmethod
    async def create(self, student: Student) -> Student:
        """Create a new student"""
        pass

    @abstractmethod
    async def update(self, student: Student) -> Student:
        """Update an existing student"""
        pass

    @abstractmethod
    async def delete(self, student_id: int) -> bool:
        """Delete a student"""
        pass

    @abstractmethod
    async def get_by_school_id(self, school_id: int) -> List[Student]:
        """Get students by school ID"""
        pass

    @abstractmethod
    async def get_by_grade_level(self, grade_level: int) -> List[Student]:
        """Get students by grade level"""
        pass

    @abstractmethod
    async def search_by_name(self, name: str) -> List[Student]:
        """Search students by name"""
        pass
