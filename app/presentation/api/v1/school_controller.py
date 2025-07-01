from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session
from app.infrastructure.database.connection import get_session
from app.infrastructure.repositories.school_repository import SchoolRepository
from app.application.services.school_service import SchoolService
from app.application.dtos.school_dto import SchoolCreateDTO, SchoolUpdateDTO, SchoolResponseDTO
from app.core.pagination import PaginationParams, PaginatedResponse

router = APIRouter(prefix="/schools", tags=["schools"])


def get_school_service(session: Session = Depends(get_session)) -> SchoolService:
    """Dependency to get school service"""
    school_repository = SchoolRepository(session)
    return SchoolService(school_repository)


@router.get("/", response_model=PaginatedResponse[SchoolResponseDTO])
async def get_schools(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    school_service: SchoolService = Depends(get_school_service)
):
    """Get all schools with pagination"""
    pagination = PaginationParams(page=page, size=size)
    return await school_service.get_all_schools(pagination)


@router.get("/{school_id}", response_model=SchoolResponseDTO)
async def get_school(school_id: int, school_service: SchoolService = Depends(get_school_service)):
    """Get a school by ID"""
    school = await school_service.get_school_by_id(school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


@router.post("/", response_model=SchoolResponseDTO)
async def create_school(
    school: SchoolCreateDTO,
    school_service: SchoolService = Depends(get_school_service)
):
    """Create a new school"""
    return await school_service.create_school(school)


@router.put("/{school_id}", response_model=SchoolResponseDTO)
async def update_school(
    school_id: int,
    school_update: SchoolUpdateDTO,
    school_service: SchoolService = Depends(get_school_service)
):
    """Update a school by ID"""
    school = await school_service.update_school(school_id, school_update)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


@router.delete("/{school_id}")
async def delete_school(
    school_id: int,
    school_service: SchoolService = Depends(get_school_service)
):
    """Delete a school by ID"""
    success = await school_service.delete_school(school_id)
    if not success:
        raise HTTPException(status_code=404, detail="School not found")
    return {"message": "School deleted successfully"}


@router.get("/search/by-city/{city}", response_model=PaginatedResponse[SchoolResponseDTO])
async def get_schools_by_city(
    city: str,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    school_service: SchoolService = Depends(get_school_service)
):
    """Get schools by city with pagination"""
    pagination = PaginationParams(page=page, size=size)
    return await school_service.get_schools_by_city(city, pagination)


@router.get("/search/by-state/{state}", response_model=PaginatedResponse[SchoolResponseDTO])
async def get_schools_by_state(
    state: str,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    school_service: SchoolService = Depends(get_school_service)
):
    """Get schools by state with pagination"""
    pagination = PaginationParams(page=page, size=size)
    return await school_service.get_schools_by_state(state, pagination)
