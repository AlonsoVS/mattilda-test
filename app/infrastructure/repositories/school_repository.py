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



    async def get_with_filters(self, filters: dict, offset: int = 0, limit: int = 10) -> Tuple[List[School], int]:
        """Get schools with flexible filtering and pagination"""
        # Build the base query
        statement = select(SchoolEntity)
        count_statement = select(func.count()).select_from(SchoolEntity)
        
        # Apply filters
        conditions = []
        
        if filters.get('name'):
            conditions.append(col(SchoolEntity.name).ilike(f"%{filters['name']}%"))
        
        if filters.get('address'):
            conditions.append(col(SchoolEntity.address).ilike(f"%{filters['address']}%"))
        
        if filters.get('city'):
            conditions.append(col(SchoolEntity.city).ilike(f"%{filters['city']}%"))
        
        if filters.get('state'):
            conditions.append(col(SchoolEntity.state).ilike(f"%{filters['state']}%"))
        
        if filters.get('zip_code'):
            conditions.append(col(SchoolEntity.zip_code).ilike(f"%{filters['zip_code']}%"))
        
        if filters.get('phone'):
            conditions.append(col(SchoolEntity.phone_number).ilike(f"%{filters['phone']}%"))
        
        if filters.get('email'):
            conditions.append(col(SchoolEntity.email).ilike(f"%{filters['email']}%"))
        
        if filters.get('principal'):
            conditions.append(col(SchoolEntity.principal_name).ilike(f"%{filters['principal']}%"))
        
        if filters.get('is_active') is not None:
            conditions.append(SchoolEntity.is_active == filters['is_active'])
        
        # Apply conditions to both statements
        if conditions:
            from sqlmodel import and_
            filter_condition = and_(*conditions)
            statement = statement.where(filter_condition)
            count_statement = count_statement.where(filter_condition)
        
        # Get total count
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = statement.offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        schools = [SchoolMapper.to_domain(entity) for entity in entities]
        return schools, total
