from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.entities.school import School


class SchoolRepositoryInterface(ABC):
    """Interface for school repository"""

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get all schools with pagination"""
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

    @abstractmethod
    async def get_by_city(self, city: str, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get schools by city with pagination"""
        pass

    @abstractmethod
    async def get_by_state(self, state: str, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get schools by state with pagination"""
        pass
