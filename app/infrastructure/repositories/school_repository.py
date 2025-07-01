from typing import List, Optional
from sqlmodel import Session, select, col
from app.domain.entities.school import School
from app.domain.repositories.school_repository import SchoolRepositoryInterface


class SchoolRepository(SchoolRepositoryInterface):
    """Implementation of school repository"""

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self) -> List[School]:
        """Get all schools"""
        statement = select(School)
        result = self.session.exec(statement)
        return list(result.all())

    async def get_by_id(self, school_id: int) -> Optional[School]:
        """Get school by ID"""
        return self.session.get(School, school_id)

    async def create(self, school: School) -> School:
        """Create a new school"""
        self.session.add(school)
        self.session.commit()
        self.session.refresh(school)
        return school

    async def update(self, school: School) -> School:
        """Update an existing school"""
        self.session.add(school)
        self.session.commit()
        self.session.refresh(school)
        return school

    async def delete(self, school_id: int) -> bool:
        """Delete a school"""
        school = self.session.get(School, school_id)
        if school:
            self.session.delete(school)
            self.session.commit()
            return True
        return False

    async def get_by_city(self, city: str) -> List[School]:
        """Get schools by city"""
        statement = select(School).where(col(School.city).ilike(f"%{city}%"))
        result = self.session.exec(statement)
        return list(result.all())

    async def get_by_state(self, state: str) -> List[School]:
        """Get schools by state"""
        statement = select(School).where(col(School.state).ilike(f"%{state}%"))
        result = self.session.exec(statement)
        return list(result.all())
