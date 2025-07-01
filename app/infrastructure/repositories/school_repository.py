from typing import List, Optional, Tuple
from sqlmodel import Session, select, col, func
from datetime import datetime
from app.domain.models.school import School
from app.domain.repositories.school_repository import SchoolRepositoryInterface
from app.infrastructure.persistence.school_entity import SchoolEntity
from app.infrastructure.mappers.school_mapper import SchoolMapper


class SchoolRepository(SchoolRepositoryInterface):
    """Implementation of school repository"""

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get all schools with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(SchoolEntity)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(SchoolEntity).offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        schools = [SchoolMapper.to_domain(entity) for entity in entities]
        return schools, total

    async def get_by_id(self, school_id: int) -> Optional[School]:
        """Get school by ID"""
        entity = self.session.get(SchoolEntity, school_id)
        return SchoolMapper.to_domain(entity) if entity else None

    async def create(self, school: School) -> School:
        """Create a new school"""
        entity = SchoolMapper.to_entity(school)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return SchoolMapper.to_domain(entity)

    async def update(self, school: School) -> School:
        """Update an existing school"""
        if school.id is None:
            raise ValueError("Cannot update school without ID")
            
        entity = self.session.get(SchoolEntity, school.id)
        if not entity:
            raise ValueError(f"School with ID {school.id} not found")
            
        # Update entity with domain model data
        entity.updated_at = datetime.now()
        SchoolMapper.update_entity(entity, school)
        
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return SchoolMapper.to_domain(entity)

    async def delete(self, school_id: int) -> bool:
        """Delete a school"""
        entity = self.session.get(SchoolEntity, school_id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False

    async def get_by_city(self, city: str, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get schools by city with pagination"""
        city_filter = col(SchoolEntity.city).ilike(f"%{city}%")
        
        # Get total count
        count_statement = select(func.count()).select_from(SchoolEntity).where(city_filter)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(SchoolEntity).where(city_filter).offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        schools = [SchoolMapper.to_domain(entity) for entity in entities]
        return schools, total

    async def get_by_state(self, state: str, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get schools by state with pagination"""
        state_filter = col(SchoolEntity.state).ilike(f"%{state}%")
        
        # Get total count
        count_statement = select(func.count()).select_from(SchoolEntity).where(state_filter)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(SchoolEntity).where(state_filter).offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        schools = [SchoolMapper.to_domain(entity) for entity in entities]
        return schools, total
