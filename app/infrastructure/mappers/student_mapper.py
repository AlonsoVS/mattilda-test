from app.domain.models.student import Student
from app.infrastructure.persistence.student_entity import StudentEntity


class StudentMapper:
    """Mapper between Student domain model and StudentEntity persistence model"""

    @staticmethod
    def to_domain(entity: StudentEntity) -> Student:
        """Convert StudentEntity to Student domain model"""
        return Student(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            phone_number=entity.phone_number,
            date_of_birth=entity.date_of_birth,
            grade_level=entity.grade_level,
            school_id=entity.school_id,
            enrollment_date=entity.enrollment_date,
            address=entity.address,
            guardian_name=entity.guardian_name,
            guardian_phone=entity.guardian_phone,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_entity(domain: Student) -> StudentEntity:
        """Convert Student domain model to StudentEntity"""
        entity = StudentEntity(
            first_name=domain.first_name,
            last_name=domain.last_name,
            email=domain.email,
            phone_number=domain.phone_number,
            date_of_birth=domain.date_of_birth,
            grade_level=domain.grade_level,
            school_id=domain.school_id,
            enrollment_date=domain.enrollment_date,
            address=domain.address,
            guardian_name=domain.guardian_name,
            guardian_phone=domain.guardian_phone,
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
    def update_entity(entity: StudentEntity, domain: Student) -> StudentEntity:
        """Update existing entity with domain model data"""
        entity.first_name = domain.first_name
        entity.last_name = domain.last_name
        entity.email = domain.email
        entity.phone_number = domain.phone_number
        entity.date_of_birth = domain.date_of_birth
        entity.grade_level = domain.grade_level
        entity.school_id = domain.school_id
        entity.enrollment_date = domain.enrollment_date
        entity.address = domain.address
        entity.guardian_name = domain.guardian_name
        entity.guardian_phone = domain.guardian_phone
        entity.is_active = domain.is_active
        
        return entity
