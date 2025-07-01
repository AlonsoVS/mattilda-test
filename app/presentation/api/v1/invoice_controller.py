from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.infrastructure.database.connection import get_session
from app.infrastructure.repositories.invoice_repository import InvoiceRepository
from app.application.services.invoice_service import InvoiceService
from app.application.dtos.invoice_dto import InvoiceCreateDTO, InvoiceUpdateDTO, InvoiceResponseDTO, PaymentRecordDTO

router = APIRouter(prefix="/invoices", tags=["invoices"])


def get_invoice_service(session: Session = Depends(get_session)) -> InvoiceService:
    """Dependency to get invoice service"""
    invoice_repository = InvoiceRepository(session)
    return InvoiceService(invoice_repository)


@router.get("/", response_model=List[InvoiceResponseDTO])
async def get_invoices(invoice_service: InvoiceService = Depends(get_invoice_service)):
    """Get all invoices"""
    return await invoice_service.get_all_invoices()


@router.get("/{invoice_id}", response_model=InvoiceResponseDTO)
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
    return await invoice_service.create_invoice(invoice)


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
    return {"message": "Invoice deleted successfully"}


@router.get("/student/{student_id}", response_model=List[InvoiceResponseDTO])
async def get_invoices_by_student(
    student_id: int,
    invoice_service: InvoiceService = Depends(get_invoice_service)
):
    """Get invoices by student ID"""
    return await invoice_service.get_invoices_by_student_id(student_id)


@router.get("/school/{school_id}", response_model=List[InvoiceResponseDTO])
async def get_invoices_by_school(
    school_id: int,
    invoice_service: InvoiceService = Depends(get_invoice_service)
):
    """Get invoices by school ID"""
    return await invoice_service.get_invoices_by_school_id(school_id)


@router.get("/status/{status}", response_model=List[InvoiceResponseDTO])
async def get_invoices_by_status(
    status: str,
    invoice_service: InvoiceService = Depends(get_invoice_service)
):
    """Get invoices by status (pending, paid, overdue, cancelled)"""
    return await invoice_service.get_invoices_by_status(status)


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
        return invoice
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
