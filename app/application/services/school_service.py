from typing import List, Optional
from app.domain.entities.school import School
from app.domain.repositories.school_repository import SchoolRepositoryInterface
from app.application.dtos.school_dto import SchoolCreateDTO, SchoolUpdateDTO, SchoolResponseDTO


class SchoolService:
    """Service layer for school operations"""

    def __init__(self, school_repository: SchoolRepositoryInterface):
        self.school_repository = school_repository

    async def get_all_schools(self) -> List[SchoolResponseDTO]:
        """Get all schools"""
        schools = await self.school_repository.get_all()
        return [SchoolResponseDTO.model_validate(school) for school in schools]

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

    async def get_schools_by_city(self, city: str) -> List[SchoolResponseDTO]:
        """Get schools by city"""
        schools = await self.school_repository.get_by_city(city)
        return [SchoolResponseDTO.model_validate(school) for school in schools]

    async def get_schools_by_state(self, state: str) -> List[SchoolResponseDTO]:
        """Get schools by state"""
        schools = await self.school_repository.get_by_state(state)
        return [SchoolResponseDTO.model_validate(school) for school in schools]
