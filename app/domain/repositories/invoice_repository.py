from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.invoice import Invoice


class InvoiceRepositoryInterface(ABC):
    """Interface for invoice repository"""

    @abstractmethod
    async def get_all(self) -> List[Invoice]:
        """Get all invoices"""
        pass

    @abstractmethod
    async def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """Get invoice by ID"""
        pass

    @abstractmethod
    async def create(self, invoice: Invoice) -> Invoice:
        """Create a new invoice"""
        pass

    @abstractmethod
    async def update(self, invoice: Invoice) -> Invoice:
        """Update an existing invoice"""
        pass

    @abstractmethod
    async def delete(self, invoice_id: int) -> bool:
        """Delete an invoice"""
        pass

    @abstractmethod
    async def get_by_student_id(self, student_id: int) -> List[Invoice]:
        """Get invoices by student ID"""
        pass

    @abstractmethod
    async def get_by_school_id(self, school_id: int) -> List[Invoice]:
        """Get invoices by school ID"""
        pass

    @abstractmethod
    async def get_by_status(self, status: str) -> List[Invoice]:
        """Get invoices by status"""
        pass
