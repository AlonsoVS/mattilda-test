from typing import List, Optional, Tuple
from sqlmodel import Session, select, col, func
from app.domain.entities.school import School
from app.domain.repositories.school_repository import SchoolRepositoryInterface


class SchoolRepository(SchoolRepositoryInterface):
    """Implementation of school repository"""

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get all schools with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(School)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(School).offset(offset).limit(limit)
        result = self.session.exec(statement)
        return list(result.all()), total

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

    async def get_by_city(self, city: str, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get schools by city with pagination"""
        city_filter = col(School.city).ilike(f"%{city}%")
        
        # Get total count
        count_statement = select(func.count()).select_from(School).where(city_filter)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(School).where(city_filter).offset(offset).limit(limit)
        result = self.session.exec(statement)
        return list(result.all()), total

    async def get_by_state(self, state: str, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get schools by state with pagination"""
        state_filter = col(School.state).ilike(f"%{state}%")
        
        # Get total count
        count_statement = select(func.count()).select_from(School).where(state_filter)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(School).where(state_filter).offset(offset).limit(limit)
        result = self.session.exec(statement)
        return list(result.all()), total
