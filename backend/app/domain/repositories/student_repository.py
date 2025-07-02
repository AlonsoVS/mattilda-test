from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.models.student import Student


class StudentRepositoryInterface(ABC):
    """Interface for student repository"""

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> Tuple[List[Student], int]:
        """Get all students with pagination"""
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
    async def count_by_school_id(self, school_id: int) -> int:
        """Count students by school ID"""
        pass

    @abstractmethod
    async def get_with_filters(self, filters: dict, offset: int = 0, limit: int = 10) -> Tuple[List[Student], int]:
        """Get students with flexible filtering and pagination"""
        pass
