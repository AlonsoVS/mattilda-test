from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.models.school import School


class SchoolRepositoryInterface(ABC):
    """Interface for school repository"""

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get all schools with pagination"""
        pass

    @abstractmethod
    async def get_with_filters(self, filters: dict, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get schools with flexible filtering and pagination"""
        pass

    @abstractmethod
    async def get_by_id(self, school_id: int) -> Optional[School]:
        """Get school by ID"""
        pass

    @abstractmethod
    async def create(self, school: School) -> School:
        """Create a new school"""
        pass

    @abstractmethod
    async def update(self, school: School) -> School:
        """Update an existing school"""
        pass

    @abstractmethod
    async def delete(self, school_id: int) -> bool:
        """Delete a school"""
        pass


