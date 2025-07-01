from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.models.invoice import Invoice


class InvoiceRepositoryInterface(ABC):
    """Interface for invoice repository"""

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> Tuple[List[Invoice], int]:
        """Get all invoices with pagination"""
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
    async def get_by_student_id(self, student_id: int, offset: int = 0, limit: int = 10) -> Tuple[List[Invoice], int]:
        """Get invoices by student ID with pagination"""
        pass

    @abstractmethod
    async def get_by_school_id(self, school_id: int, offset: int = 0, limit: int = 10) -> Tuple[List[Invoice], int]:
        """Get invoices by school ID with pagination"""
        pass

    @abstractmethod
    async def get_by_status(self, status: str, offset: int = 0, limit: int = 10) -> Tuple[List[Invoice], int]:
        """Get invoices by status with pagination"""
        pass
