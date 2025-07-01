from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from app.domain.entities.invoice import Invoice
from app.domain.repositories.invoice_repository import InvoiceRepositoryInterface


class InvoiceRepository(InvoiceRepositoryInterface):
    """Implementation of invoice repository"""

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self) -> List[Invoice]:
        """Get all invoices"""
        statement = select(Invoice)
        result = self.session.exec(statement)
        return list(result.all())

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

    async def get_by_student_id(self, student_id: int) -> List[Invoice]:
        """Get invoices by student ID"""
        statement = select(Invoice).where(Invoice.student_id == student_id)
        result = self.session.exec(statement)
        return list(result.all())

    async def get_by_school_id(self, school_id: int) -> List[Invoice]:
        """Get invoices by school ID"""
        statement = select(Invoice).where(Invoice.school_id == school_id)
        result = self.session.exec(statement)
        return list(result.all())

    async def get_by_status(self, status: str) -> List[Invoice]:
        """Get invoices by status"""
        statement = select(Invoice).where(Invoice.status == status.lower())
        result = self.session.exec(statement)
        return list(result.all())
