from app.domain.models.school import School
from app.infrastructure.persistence.school_entity import SchoolEntity


class SchoolMapper:
    """Mapper between School domain model and SchoolEntity persistence model"""

    @staticmethod
    def to_domain(entity: SchoolEntity) -> School:
        """Convert SchoolEntity to School domain model"""
        return School(
            id=entity.id,
            name=entity.name,
            address=entity.address,
            city=entity.city,
            state=entity.state,
            zip_code=entity.zip_code,
            phone_number=entity.phone_number,
            email=entity.email,
            principal_name=entity.principal_name,
            established_year=entity.established_year,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_entity(domain: School) -> SchoolEntity:
        """Convert School domain model to SchoolEntity"""
        entity = SchoolEntity(
            name=domain.name,
            address=domain.address,
            city=domain.city,
            state=domain.state,
            zip_code=domain.zip_code,
            phone_number=domain.phone_number,
            email=domain.email,
            principal_name=domain.principal_name,
            established_year=domain.established_year,
            is_active=domain.is_active
        )
        
        if domain.id is not None:
            entity.id = domain.id
        if domain.created_at is not None:
            entity.created_at = domain.created_at
        if domain.updated_at is not None:
            entity.updated_at = domain.updated_at
            
        return entity

    @staticmethod
    def update_entity(entity: SchoolEntity, domain: School) -> SchoolEntity:
        """Update existing entity with domain model data"""
        entity.name = domain.name
        entity.address = domain.address
        entity.city = domain.city
        entity.state = domain.state
        entity.zip_code = domain.zip_code
        entity.phone_number = domain.phone_number
        entity.email = domain.email
        entity.principal_name = domain.principal_name
        entity.established_year = domain.established_year
        entity.is_active = domain.is_active
        
        return entity
