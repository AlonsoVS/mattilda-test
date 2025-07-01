from typing import List, Optional
from sqlmodel import Session, func, select
from datetime import datetime
from app.domain.entities.invoice import Invoice
from app.domain.repositories.invoice_repository import InvoiceRepositoryInterface


class InvoiceRepository(InvoiceRepositoryInterface):
    """Implementation of invoice repository"""

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, offset: int = 0, limit: int = 10) -> tuple[List[Invoice], int]:
        """Get all invoices with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(Invoice)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(Invoice).offset(offset).limit(limit)
        result = self.session.exec(statement)
        return list(result.all()), total

    async def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """Get invoice by ID"""
        return self.session.get(Invoice, invoice_id)

    async def create(self, invoice: Invoice) -> Invoice:
        """Create a new invoice"""
        self.session.add(invoice)
        self.session.commit()
        self.session.refresh(invoice)
        return invoice

    async def update(self, invoice: Invoice) -> Invoice:
        """Update an existing invoice"""
        invoice.updated_at = datetime.now()
        self.session.add(invoice)
        self.session.commit()
        self.session.refresh(invoice)
        return invoice

    async def delete(self, invoice_id: int) -> bool:
        """Delete an invoice"""
        invoice = self.session.get(Invoice, invoice_id)
        if invoice:
            self.session.delete(invoice)
            self.session.commit()
            return True
        return False

    async def get_by_student_id(self, student_id: int, offset: int = 0, limit: int = 10) -> tuple[List[Invoice], int]:
        """Get invoices by student ID with pagination"""
        statement = select(Invoice).where(Invoice.student_id == student_id).offset(offset).limit(limit)
        result = self.session.exec(statement)
        invoices = list(result.all())
        count_statement = select(func.count()).select_from(Invoice).where(Invoice.student_id == student_id)
        total = self.session.exec(count_statement).one()
        return invoices, total

    async def get_by_school_id(self, school_id: int, offset: int = 0, limit: int = 10) -> tuple[List[Invoice], int]:
        """Get invoices by school ID with pagination"""
        statement = select(Invoice).where(Invoice.school_id == school_id).offset(offset).limit(limit)
        result = self.session.exec(statement)
        invoices = list(result.all())
        count_statement = select(func.count()).select_from(Invoice).where(Invoice.school_id == school_id)
        total = self.session.exec(count_statement).one()
        return invoices, total

    async def get_by_status(self, status: str, offset: int = 0, limit: int = 10) -> tuple[List[Invoice], int]:
        """Get invoices by status with pagination"""
        statement = select(Invoice).where(Invoice.status == status.lower()).offset(offset).limit(limit)
        result = self.session.exec(statement)
        invoices = list(result.all())
        count_statement = select(func.count()).select_from(Invoice).where(Invoice.status == status.lower())
        total = self.session.exec(count_statement).one()
        return invoices, total
