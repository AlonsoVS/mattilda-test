from typing import List, Optional
from datetime import datetime
from app.domain.models.invoice import Invoice
from app.domain.enums import InvoiceStatus, PaymentMethod
from app.domain.repositories.invoice_repository import InvoiceRepositoryInterface
from app.application.dtos.invoice_dto import InvoiceCreateDTO, InvoiceUpdateDTO, InvoiceResponseDTO, PaymentRecordDTO
from app.core.pagination import PaginationParams, PaginatedResponse


class InvoiceService:
    """Service layer for invoice operations"""

    def __init__(self, invoice_repository: InvoiceRepositoryInterface):
        self.invoice_repository = invoice_repository

    async def get_all_invoices(self, pagination: PaginationParams) -> PaginatedResponse[InvoiceResponseDTO]:
        """Get all invoices with pagination"""
        invoices, total = await self.invoice_repository.get_all(pagination.offset, pagination.limit)
        invoice_dtos = [self._to_response_dto(invoice) for invoice in invoices]
        return PaginatedResponse.create(invoice_dtos, total, pagination)

    async def get_invoice_by_id(self, invoice_id: int) -> Optional[InvoiceResponseDTO]:
        """Get invoice by ID"""
        invoice = await self.invoice_repository.get_by_id(invoice_id)
        if invoice:
            return self._to_response_dto(invoice)
        return None

    async def create_invoice(self, invoice_data: InvoiceCreateDTO) -> InvoiceResponseDTO:
        """Create a new invoice"""
        current_time = datetime.now()
        total_amount = invoice_data.amount + invoice_data.tax_amount
        
        # Create domain model
        invoice = Invoice(
            invoice_number=invoice_data.invoice_number,
            student_id=invoice_data.student_id,
            school_id=invoice_data.school_id,
            amount=invoice_data.amount,
            tax_amount=invoice_data.tax_amount,
            total_amount=total_amount,
            description=invoice_data.description,
            invoice_date=invoice_data.invoice_date,
            due_date=invoice_data.due_date,
            status=InvoiceStatus.PENDING,
            created_at=current_time,
            updated_at=current_time
        )
        
        created_invoice = await self.invoice_repository.create(invoice)
        return self._to_response_dto(created_invoice)

    async def update_invoice(self, invoice_id: int, invoice_data: InvoiceUpdateDTO) -> Optional[InvoiceResponseDTO]:
        """Update an existing invoice"""
        invoice = await self.invoice_repository.get_by_id(invoice_id)
        if not invoice:
            return None

        # Update only provided fields
        update_data = invoice_data.model_dump(exclude_unset=True)
        
        # If amount or tax_amount changed, recalculate total
        if "amount" in update_data or "tax_amount" in update_data:
            new_amount = update_data.get("amount", invoice.amount)
            new_tax = update_data.get("tax_amount", invoice.tax_amount)
            update_data["total_amount"] = new_amount + new_tax

        updated_invoice = invoice.update(**update_data)
        updated_invoice = await self.invoice_repository.update(updated_invoice)
        return self._to_response_dto(updated_invoice)

    async def delete_invoice(self, invoice_id: int) -> bool:
        """Delete an invoice"""
        return await self.invoice_repository.delete(invoice_id)

    async def get_invoices_by_student_id(self, student_id: int, pagination: PaginationParams) -> PaginatedResponse[InvoiceResponseDTO]:
        """Get invoices by student ID with pagination"""
        invoices, total = await self.invoice_repository.get_by_student_id(student_id, pagination.offset, pagination.limit)
        invoice_dtos = [self._to_response_dto(invoice) for invoice in invoices]
        return PaginatedResponse.create(invoice_dtos, total, pagination)

    async def get_invoices_by_school_id(self, school_id: int, pagination: PaginationParams) -> PaginatedResponse[InvoiceResponseDTO]:
        """Get invoices by school ID with pagination"""
        invoices, total = await self.invoice_repository.get_by_school_id(school_id, pagination.offset, pagination.limit)
        invoice_dtos = [self._to_response_dto(invoice) for invoice in invoices]
        return PaginatedResponse.create(invoice_dtos, total, pagination)

    async def get_invoices_by_status(self, status: str, pagination: PaginationParams) -> PaginatedResponse[InvoiceResponseDTO]:
        """Get invoices by status with pagination"""
        invoices, total = await self.invoice_repository.get_by_status(status, pagination.offset, pagination.limit)
        invoice_dtos = [self._to_response_dto(invoice) for invoice in invoices]
        return PaginatedResponse.create(invoice_dtos, total, pagination)

    async def record_payment(self, invoice_id: int, payment_data: PaymentRecordDTO) -> Optional[InvoiceResponseDTO]:
        """Record a payment for an invoice"""
        invoice = await self.invoice_repository.get_by_id(invoice_id)
        if not invoice:
            return None

        if invoice.status == InvoiceStatus.PAID:
            raise ValueError("Invoice is already paid")

        update_data = {
            "payment_date": payment_data.payment_date,
            "payment_method": payment_data.payment_method,
            "status": InvoiceStatus.PAID
        }
        
        if payment_data.notes:
            update_data["notes"] = payment_data.notes

        updated_invoice = invoice.update(**update_data)
        updated_invoice = await self.invoice_repository.update(updated_invoice)
        return self._to_response_dto(updated_invoice)

    def _to_response_dto(self, invoice: Invoice) -> InvoiceResponseDTO:
        """Convert domain model to response DTO"""
        return InvoiceResponseDTO(
            id=invoice.id or 0,  # Handle None case
            invoice_number=invoice.invoice_number,
            student_id=invoice.student_id,
            school_id=invoice.school_id,
            amount=invoice.amount,
            tax_amount=invoice.tax_amount,
            total_amount=invoice.total_amount,
            description=invoice.description,
            invoice_date=invoice.invoice_date,
            due_date=invoice.due_date,
            payment_date=invoice.payment_date,
            payment_method=invoice.payment_method,
            status=invoice.status,
            notes=invoice.notes,
            created_at=invoice.created_at or datetime.now(),
            updated_at=invoice.updated_at or datetime.now()
        )
