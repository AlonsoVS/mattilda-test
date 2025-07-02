from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session
from datetime import date
from app.infrastructure.database.connection import get_session
from app.infrastructure.repositories.school_repository import SchoolRepository
from app.infrastructure.repositories.student_repository import StudentRepository
from app.infrastructure.repositories.invoice_repository import InvoiceRepository
from app.application.services.school_service import SchoolService
from app.application.dtos.school_dto import SchoolCreateDTO, SchoolUpdateDTO, SchoolResponseDTO, SchoolFilterDTO, SchoolAccountStatementDTO
from app.core.pagination import PaginationParams, PaginatedResponse

router = APIRouter(prefix="/schools", tags=["schools"])


def get_school_service(session: Session = Depends(get_session)) -> SchoolService:
    """Dependency to get school service"""
    school_repository = SchoolRepository(session)
    student_repository = StudentRepository(session)
    invoice_repository = InvoiceRepository(session)
    return SchoolService(school_repository, student_repository, invoice_repository)


@router.get("/", response_model=PaginatedResponse[SchoolResponseDTO])
async def get_schools(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    name: Optional[str] = Query(None, description="Filter by school name (partial match)"),
    address: Optional[str] = Query(None, description="Filter by address (partial match)"),
    city: Optional[str] = Query(None, description="Filter by city (partial match)"),
    state: Optional[str] = Query(None, description="Filter by state (partial match)"),
    zip_code: Optional[str] = Query(None, description="Filter by zip code (partial match)"),
    phone: Optional[str] = Query(None, description="Filter by phone (partial match)"),
    email: Optional[str] = Query(None, description="Filter by email (partial match)"),
    principal: Optional[str] = Query(None, description="Filter by principal (partial match)"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    school_service: SchoolService = Depends(get_school_service)
):
    """Get schools with optional filtering and pagination"""
    pagination = PaginationParams(page=page, size=size)
    
    # Create filter DTO
    filters = SchoolFilterDTO(
        name=name,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        phone=phone,
        email=email,
        principal=principal,
        is_active=is_active
    )
    
    # Check if any filters are applied
    if any(v is not None for v in filters.model_dump().values()):
        return await school_service.get_schools_with_filters(filters, pagination)
    else:
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


@router.get("/{school_id}/account-statement", response_model=SchoolAccountStatementDTO)
async def get_school_account_statement(
    school_id: int,
    date_from: Optional[date] = Query(None, description="Statement period start date (defaults to beginning of current year)"),
    date_to: Optional[date] = Query(None, description="Statement period end date (defaults to today)"),
    school_service: SchoolService = Depends(get_school_service)
):
    """Get comprehensive account statement for a school including all students' financial data, totals, and statistics"""
    try:
        statement = await school_service.get_school_account_statement(school_id, date_from, date_to)
        if not statement:
            raise HTTPException(status_code=404, detail="School not found")
        return statement
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating school account statement: {str(e)}")
