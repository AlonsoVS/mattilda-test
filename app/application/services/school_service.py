from typing import List, Optional
from app.domain.entities.school import School
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
        school_dtos = [SchoolResponseDTO.model_validate(school) for school in schools]
        return PaginatedResponse.create(school_dtos, total, pagination)

    async def get_school_by_id(self, school_id: int) -> Optional[SchoolResponseDTO]:
        """Get school by ID"""
        school = await self.school_repository.get_by_id(school_id)
        if school:
            return SchoolResponseDTO.model_validate(school)
        return None

    async def create_school(self, school_data: SchoolCreateDTO) -> SchoolResponseDTO:
        """Create a new school"""
        school = School(**school_data.model_dump())
        created_school = await self.school_repository.create(school)
        return SchoolResponseDTO.model_validate(created_school)

    async def update_school(self, school_id: int, school_data: SchoolUpdateDTO) -> Optional[SchoolResponseDTO]:
        """Update an existing school"""
        school = await self.school_repository.get_by_id(school_id)
        if not school:
            return None

        # Update only provided fields
        update_data = school_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(school, field, value)

        updated_school = await self.school_repository.update(school)
        return SchoolResponseDTO.model_validate(updated_school)

    async def delete_school(self, school_id: int) -> bool:
        """Delete a school"""
        return await self.school_repository.delete(school_id)

    async def get_schools_by_city(self, city: str, pagination: PaginationParams) -> PaginatedResponse[SchoolResponseDTO]:
        """Get schools by city with pagination"""
        schools, total = await self.school_repository.get_by_city(city, pagination.offset, pagination.limit)
        school_dtos = [SchoolResponseDTO.model_validate(school) for school in schools]
        return PaginatedResponse.create(school_dtos, total, pagination)

    async def get_schools_by_state(self, state: str, pagination: PaginationParams) -> PaginatedResponse[SchoolResponseDTO]:
        """Get schools by state with pagination"""
        schools, total = await self.school_repository.get_by_state(state, pagination.offset, pagination.limit)
        school_dtos = [SchoolResponseDTO.model_validate(school) for school in schools]
        return PaginatedResponse.create(school_dtos, total, pagination)
