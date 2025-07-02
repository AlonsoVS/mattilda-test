from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session
from datetime import date
from app.infrastructure.database.connection import get_session
from app.infrastructure.repositories.invoice_repository import InvoiceRepository
from app.application.services.invoice_service import InvoiceService
from app.application.dtos.invoice_dto import InvoiceCreateDTO, InvoiceUpdateDTO, InvoiceResponseDTO, PaymentRecordDTO, InvoiceFilterDTO
from app.domain.enums import InvoiceStatus, PaymentMethod
from app.core.pagination import PaginationParams, PaginatedResponse
from app.core.cache import cache_api_response, invalidate_cache_pattern

router = APIRouter(prefix="/invoices", tags=["invoices"])


def get_invoice_service(session: Session = Depends(get_session)) -> InvoiceService:
    """Dependency to get invoice service"""
    invoice_repository = InvoiceRepository(session)
    return InvoiceService(invoice_repository)


@router.get("/", response_model=PaginatedResponse[InvoiceResponseDTO])
@cache_api_response()  # Re-enabled with simple implementation
async def get_invoices(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    invoice_number: Optional[str] = Query(None, description="Filter by invoice number (partial match)"),
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    school_id: Optional[int] = Query(None, description="Filter by school ID"),
    amount_min: Optional[float] = Query(None, description="Filter by minimum amount"),
    amount_max: Optional[float] = Query(None, description="Filter by maximum amount"),
    tax_amount_min: Optional[float] = Query(None, description="Filter by minimum tax amount"),
    tax_amount_max: Optional[float] = Query(None, description="Filter by maximum tax amount"),
    total_amount_min: Optional[float] = Query(None, description="Filter by minimum total amount"),
    total_amount_max: Optional[float] = Query(None, description="Filter by maximum total amount"),
    description: Optional[str] = Query(None, description="Filter by description (partial match)"),
    invoice_date_from: Optional[date] = Query(None, description="Filter by invoice date from"),
    invoice_date_to: Optional[date] = Query(None, description="Filter by invoice date to"),
    due_date_from: Optional[date] = Query(None, description="Filter by due date from"),
    due_date_to: Optional[date] = Query(None, description="Filter by due date to"),
    payment_date_from: Optional[date] = Query(None, description="Filter by payment date from"),
    payment_date_to: Optional[date] = Query(None, description="Filter by payment date to"),
    status: Optional[InvoiceStatus] = Query(None, description="Filter by invoice status"),
    payment_method: Optional[PaymentMethod] = Query(None, description="Filter by payment method"),
    invoice_service: InvoiceService = Depends(get_invoice_service)
):
    """Get invoices with optional filtering and pagination"""
    pagination = PaginationParams(page=page, size=size)
    
    # Create filter DTO
    filters = InvoiceFilterDTO(
        invoice_number=invoice_number,
        student_id=student_id,
        school_id=school_id,
        amount_min=amount_min,
        amount_max=amount_max,
        tax_amount_min=tax_amount_min,
        tax_amount_max=tax_amount_max,
        total_amount_min=total_amount_min,
        total_amount_max=total_amount_max,
        description=description,
        invoice_date_from=invoice_date_from,
        invoice_date_to=invoice_date_to,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        payment_date_from=payment_date_from,
        payment_date_to=payment_date_to,
        status=status,
        payment_method=payment_method
    )
    
    # Check if any filters are applied
    if any(v is not None for v in filters.model_dump().values()):
        return await invoice_service.get_invoices_with_filters(filters, pagination)
    else:
        return await invoice_service.get_all_invoices(pagination)


@router.get("/{invoice_id}", response_model=InvoiceResponseDTO)
@cache_api_response()  # Re-enabled with simple implementation
async def get_invoice(invoice_id: int, invoice_service: InvoiceService = Depends(get_invoice_service)):
    """Get an invoice by ID"""
    invoice = await invoice_service.get_invoice_by_id(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/", response_model=InvoiceResponseDTO)
async def create_invoice(
    invoice: InvoiceCreateDTO,
    invoice_service: InvoiceService = Depends(get_invoice_service)
):
    """Create a new invoice"""
    result = await invoice_service.create_invoice(invoice)
    # Invalidate invoice and related caches
    invalidate_cache_pattern("api:get_invoices")
    invalidate_cache_pattern("api:get_student_account_statement")
    invalidate_cache_pattern("api:get_school_account_statement")
    return result


@router.put("/{invoice_id}", response_model=InvoiceResponseDTO)
async def update_invoice(
    invoice_id: int,
    invoice_update: InvoiceUpdateDTO,
    invoice_service: InvoiceService = Depends(get_invoice_service)
):
    """Update an invoice by ID"""
    invoice = await invoice_service.update_invoice(invoice_id, invoice_update)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    # Invalidate invoice and related caches
    invalidate_cache_pattern("api:get_invoices")
    invalidate_cache_pattern(f"api:get_invoice:{invoice_id}")
    invalidate_cache_pattern("api:get_student_account_statement")
    invalidate_cache_pattern("api:get_school_account_statement")
    return invoice


@router.delete("/{invoice_id}")
async def delete_invoice(
    invoice_id: int,
    invoice_service: InvoiceService = Depends(get_invoice_service)
):
    """Delete an invoice by ID"""
    success = await invoice_service.delete_invoice(invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")
    # Invalidate invoice and related caches
    invalidate_cache_pattern("api:get_invoices")
    invalidate_cache_pattern(f"api:get_invoice:{invoice_id}")
    invalidate_cache_pattern("api:get_student_account_statement")
    invalidate_cache_pattern("api:get_school_account_statement")
    return {"message": "Invoice deleted successfully"}


@router.post("/{invoice_id}/payment", response_model=InvoiceResponseDTO)
async def record_payment(
    invoice_id: int,
    payment: PaymentRecordDTO,
    invoice_service: InvoiceService = Depends(get_invoice_service)
):
    """Record a payment for an invoice"""
    try:
        invoice = await invoice_service.record_payment(invoice_id, payment)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        # Invalidate invoice and related caches (payment changes financial data)
        invalidate_cache_pattern("api:get_invoices")
        invalidate_cache_pattern(f"api:get_invoice:{invoice_id}")
        invalidate_cache_pattern("api:get_student_account_statement")
        invalidate_cache_pattern("api:get_school_account_statement")
        return invoice
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
