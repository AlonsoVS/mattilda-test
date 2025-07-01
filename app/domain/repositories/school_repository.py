from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.school import School


class SchoolRepositoryInterface(ABC):
    """Interface for school repository"""

    @abstractmethod
    async def get_all(self) -> List[School]:
        """Get all schools"""
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
    async def get_by_city(self, city: str) -> List[School]:
        """Get schools by city"""
        pass

    @abstractmethod
    async def get_by_state(self, state: str) -> List[School]:
        """Get schools by state"""
        pass
