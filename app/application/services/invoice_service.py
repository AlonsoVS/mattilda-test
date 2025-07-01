from typing import List, Optional
from datetime import datetime
from app.domain.entities.invoice import Invoice
from app.domain.repositories.invoice_repository import InvoiceRepositoryInterface
from app.application.dtos.invoice_dto import InvoiceCreateDTO, InvoiceUpdateDTO, InvoiceResponseDTO, PaymentRecordDTO


class InvoiceService:
    """Service layer for invoice operations"""

    def __init__(self, invoice_repository: InvoiceRepositoryInterface):
        self.invoice_repository = invoice_repository

    async def get_all_invoices(self) -> List[InvoiceResponseDTO]:
        """Get all invoices"""
        invoices = await self.invoice_repository.get_all()
        return [InvoiceResponseDTO.model_validate(invoice) for invoice in invoices]

    async def get_invoice_by_id(self, invoice_id: int) -> Optional[InvoiceResponseDTO]:
        """Get invoice by ID"""
        invoice = await self.invoice_repository.get_by_id(invoice_id)
        if invoice:
            return InvoiceResponseDTO.model_validate(invoice)
        return None

    async def create_invoice(self, invoice_data: InvoiceCreateDTO) -> InvoiceResponseDTO:
        """Create a new invoice"""
        current_time = datetime.now()
        total_amount = invoice_data.amount + invoice_data.tax_amount
        
        invoice_dict = invoice_data.model_dump()
        invoice_dict.update({
            "total_amount": total_amount,
            "created_at": current_time,
            "updated_at": current_time
        })
        
        invoice = Invoice(**invoice_dict)
        created_invoice = await self.invoice_repository.create(invoice)
        return InvoiceResponseDTO.model_validate(created_invoice)

    async def update_invoice(self, invoice_id: int, invoice_data: InvoiceUpdateDTO) -> Optional[InvoiceResponseDTO]:
        """Update an existing invoice"""
        invoice = await self.invoice_repository.get_by_id(invoice_id)
        if not invoice:
            return None

        # Update only provided fields
        update_data = invoice_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(invoice, field, value)

        # Recalculate total if amount or tax changed
        if "amount" in update_data or "tax_amount" in update_data:
            invoice.total_amount = invoice.amount + invoice.tax_amount

        updated_invoice = await self.invoice_repository.update(invoice)
        return InvoiceResponseDTO.model_validate(updated_invoice)

    async def delete_invoice(self, invoice_id: int) -> bool:
        """Delete an invoice"""
        return await self.invoice_repository.delete(invoice_id)

    async def get_invoices_by_student_id(self, student_id: int) -> List[InvoiceResponseDTO]:
        """Get invoices by student ID"""
        invoices = await self.invoice_repository.get_by_student_id(student_id)
        return [InvoiceResponseDTO.model_validate(invoice) for invoice in invoices]

    async def get_invoices_by_school_id(self, school_id: int) -> List[InvoiceResponseDTO]:
        """Get invoices by school ID"""
        invoices = await self.invoice_repository.get_by_school_id(school_id)
        return [InvoiceResponseDTO.model_validate(invoice) for invoice in invoices]

    async def get_invoices_by_status(self, status: str) -> List[InvoiceResponseDTO]:
        """Get invoices by status"""
        invoices = await self.invoice_repository.get_by_status(status)
        return [InvoiceResponseDTO.model_validate(invoice) for invoice in invoices]

    async def record_payment(self, invoice_id: int, payment_data: PaymentRecordDTO) -> Optional[InvoiceResponseDTO]:
        """Record a payment for an invoice"""
        invoice = await self.invoice_repository.get_by_id(invoice_id)
        if not invoice:
            return None

        if invoice.status == "paid":
            raise ValueError("Invoice is already paid")

        invoice.payment_date = payment_data.payment_date
        invoice.payment_method = payment_data.payment_method
        invoice.status = "paid"
        
        if payment_data.notes:
            invoice.notes = payment_data.notes

        updated_invoice = await self.invoice_repository.update(invoice)
        return InvoiceResponseDTO.model_validate(updated_invoice)
