from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session
from datetime import date
from app.infrastructure.database.connection import get_session
from app.infrastructure.repositories.student_repository import StudentRepository
from app.infrastructure.repositories.invoice_repository import InvoiceRepository
from app.infrastructure.repositories.school_repository import SchoolRepository
from app.application.services.student_service import StudentService
from app.application.dtos.student_dto import (
    StudentCreateDTO, 
    StudentUpdateDTO, 
    StudentResponseDTO, 
    StudentFilterDTO,
    StudentAccountStatementDTO
)
from app.core.pagination import PaginationParams, PaginatedResponse
from app.core.cache import cache_api_response, cache_static_data, invalidate_cache_pattern
from app.core.dependencies import get_current_active_user, get_current_user_optional
from app.domain.models.user import User

router = APIRouter(prefix="/students", tags=["students"])


def get_student_service(session: Session = Depends(get_session)) -> StudentService:
    """Dependency to get student service with all required repositories"""
    student_repository = StudentRepository(session)
    invoice_repository = InvoiceRepository(session)
    school_repository = SchoolRepository(session)
    return StudentService(student_repository, invoice_repository, school_repository)


@router.get("/", response_model=PaginatedResponse[StudentResponseDTO])
@cache_api_response()
async def get_students(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    first_name: Optional[str] = Query(None, description="Filter by first name (partial match)"),
    last_name: Optional[str] = Query(None, description="Filter by last name (partial match)"),
    email: Optional[str] = Query(None, description="Filter by email (partial match)"),
    phone: Optional[str] = Query(None, description="Filter by phone (partial match)"),
    date_of_birth: Optional[date] = Query(None, description="Filter by exact date of birth"),
    grade_level: Optional[int] = Query(None, description="Filter by grade level"),
    school_id: Optional[int] = Query(None, description="Filter by school ID"),
    enrollment_date: Optional[date] = Query(None, description="Filter by exact enrollment date"),
    address: Optional[str] = Query(None, description="Filter by address (partial match)"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    student_service: StudentService = Depends(get_student_service)
):
    """Get students with optional filtering and pagination (public endpoint with optional auth)"""
    pagination = PaginationParams(page=page, size=size)
    
    # Create filter DTO
    filters = StudentFilterDTO(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        date_of_birth=date_of_birth,
        grade_level=grade_level,
        school_id=school_id,
        enrollment_date=enrollment_date,
        address=address,
        is_active=is_active
    )
    
    # Check if any filters are applied
    if any(v is not None for v in filters.model_dump().values()):
        return await student_service.get_students_with_filters(filters, pagination)
    else:
        return await student_service.get_all_students(pagination)


@router.get("/{student_id}", response_model=StudentResponseDTO)
@cache_static_data()
async def get_student(
    student_id: int, 
    current_user: Optional[User] = Depends(get_current_user_optional),
    student_service: StudentService = Depends(get_student_service)
):
    """Get a student by ID (public endpoint with optional auth)"""
    student = await student_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=StudentResponseDTO)
async def create_student(
    student: StudentCreateDTO,
    current_user: User = Depends(get_current_active_user),
    student_service: StudentService = Depends(get_student_service)
):
    """Create a new student (requires authentication)"""
    result = await student_service.create_student(student)
    # Invalidate student and school-related caches
    invalidate_cache_pattern("api:get_students")
    invalidate_cache_pattern("static:get_student")
    invalidate_cache_pattern("api:get_school_account_statement")
    return result


@router.put("/{student_id}", response_model=StudentResponseDTO)
async def update_student(
    student_id: int,
    student_update: StudentUpdateDTO,
    current_user: User = Depends(get_current_active_user),
    student_service: StudentService = Depends(get_student_service)
):
    """Update a student by ID (requires authentication)"""
    student = await student_service.update_student(student_id, student_update)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    # Invalidate student and related caches
    invalidate_cache_pattern("api:get_students")
    invalidate_cache_pattern(f"static:get_student:{student_id}")
    invalidate_cache_pattern("api:get_student_account_statement")
    invalidate_cache_pattern("api:get_school_account_statement")
    return student


@router.delete("/{student_id}")
async def delete_student(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    student_service: StudentService = Depends(get_student_service)
):
    """Delete a student by ID (requires authentication)"""
    success = await student_service.delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    # Invalidate student and related caches
    invalidate_cache_pattern("api:get_students")
    invalidate_cache_pattern(f"static:get_student:{student_id}")
    invalidate_cache_pattern("api:get_student_account_statement")
    invalidate_cache_pattern("api:get_school_account_statement")
    return {"message": "Student deleted successfully"}


@router.get("/{student_id}/account-statement", response_model=StudentAccountStatementDTO)
@cache_api_response()
async def get_student_account_statement(
    student_id: int,
    date_from: Optional[date] = Query(None, description="Statement period start date (defaults to beginning of current year)"),
    date_to: Optional[date] = Query(None, description="Statement period end date (defaults to today)"),
    current_user: User = Depends(get_current_active_user),
    student_service: StudentService = Depends(get_student_service)
):
    """Get comprehensive account statement for a student including all invoices, payments, and financial summary (requires authentication)"""
    try:
        statement = await student_service.get_student_account_statement(student_id, date_from, date_to)
        if not statement:
            raise HTTPException(status_code=404, detail="Student not found")
        return statement
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating account statement: {str(e)}")
