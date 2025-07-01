from typing import List, Optional
from app.domain.models.school import School
from app.domain.repositories.school_repository import SchoolRepositoryInterface
from app.application.dtos.school_dto import SchoolCreateDTO, SchoolUpdateDTO, SchoolResponseDTO
from app.core.pagination import PaginationParams, PaginatedResponse


class SchoolService:
    """Service layer for school operations"""

    def __init__(self, school_repository: SchoolRepositoryInterface):
        self.school_repository = school_repository

    async def get_all_schools(self, pagination: PaginationParams) -> PaginatedResponse[SchoolResponseDTO]:
        """Get all schools with pagination"""
        schools, total = await self.school_repository.get_all(pagination.offset, pagination.limit)
        school_dtos = [self._to_response_dto(school) for school in schools]
        return PaginatedResponse.create(school_dtos, total, pagination)

    async def get_school_by_id(self, school_id: int) -> Optional[SchoolResponseDTO]:
        """Get school by ID"""
        school = await self.school_repository.get_by_id(school_id)
        if school:
            return self._to_response_dto(school)
        return None

    async def create_school(self, school_data: SchoolCreateDTO) -> SchoolResponseDTO:
        """Create a new school"""
        school = School(
            name=school_data.name,
            address=school_data.address,
            city=school_data.city,
            state=school_data.state,
            zip_code=school_data.zip_code,
            phone_number=school_data.phone or "",
            email=school_data.email or "",
            principal_name=school_data.principal or "",
            established_year=2024,  # Default value, should come from DTO
            is_active=school_data.is_active
        )
        created_school = await self.school_repository.create(school)
        return self._to_response_dto(created_school)

    async def update_school(self, school_id: int, school_data: SchoolUpdateDTO) -> Optional[SchoolResponseDTO]:
        """Update an existing school"""
        school = await self.school_repository.get_by_id(school_id)
        if not school:
            return None

        # Map DTO fields to domain model fields
        update_data = {}
        dto_data = school_data.model_dump(exclude_unset=True)
        
        if 'phone' in dto_data:
            update_data['phone_number'] = dto_data['phone']
        if 'principal' in dto_data:
            update_data['principal_name'] = dto_data['principal']
        if 'name' in dto_data:
            update_data['name'] = dto_data['name']
        if 'address' in dto_data:
            update_data['address'] = dto_data['address']
        if 'city' in dto_data:
            update_data['city'] = dto_data['city']
        if 'state' in dto_data:
            update_data['state'] = dto_data['state']
        if 'zip_code' in dto_data:
            update_data['zip_code'] = dto_data['zip_code']
        if 'email' in dto_data:
            update_data['email'] = dto_data['email']
        if 'is_active' in dto_data:
            update_data['is_active'] = dto_data['is_active']

        updated_school = school.update(**update_data)
        updated_school = await self.school_repository.update(updated_school)
        return self._to_response_dto(updated_school)

    async def delete_school(self, school_id: int) -> bool:
        """Delete a school"""
        return await self.school_repository.delete(school_id)

    async def get_schools_by_city(self, city: str, pagination: PaginationParams) -> PaginatedResponse[SchoolResponseDTO]:
        """Get schools by city with pagination"""
        schools, total = await self.school_repository.get_by_city(city, pagination.offset, pagination.limit)
        school_dtos = [self._to_response_dto(school) for school in schools]
        return PaginatedResponse.create(school_dtos, total, pagination)

    async def get_schools_by_state(self, state: str, pagination: PaginationParams) -> PaginatedResponse[SchoolResponseDTO]:
        """Get schools by state with pagination"""
        schools, total = await self.school_repository.get_by_state(state, pagination.offset, pagination.limit)
        school_dtos = [self._to_response_dto(school) for school in schools]
        return PaginatedResponse.create(school_dtos, total, pagination)

    def _to_response_dto(self, school: School) -> SchoolResponseDTO:
        """Convert domain model to response DTO"""
        return SchoolResponseDTO(
            id=school.id or 0,  # Handle None case
            name=school.name,
            address=school.address,
            city=school.city,
            state=school.state,
            zip_code=school.zip_code,
            phone=school.phone_number,
            email=school.email,
            principal=school.principal_name,
            student_count=None,  # This field doesn't exist in domain model
            is_active=school.is_active
        )
