from typing import List, Optional, Tuple
from sqlmodel import Session, func, select
from datetime import datetime
from app.domain.models.invoice import Invoice
from app.domain.repositories.invoice_repository import InvoiceRepositoryInterface
from app.infrastructure.persistence.invoice_entity import InvoiceEntity
from app.infrastructure.mappers.invoice_mapper import InvoiceMapper


class InvoiceRepository(InvoiceRepositoryInterface):
    """Implementation of invoice repository"""

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, offset: int = 0, limit: int = 10) -> Tuple[List[Invoice], int]:
        """Get all invoices with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(InvoiceEntity)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(InvoiceEntity).offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        invoices = [InvoiceMapper.to_domain(entity) for entity in entities]
        return invoices, total

    async def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """Get invoice by ID"""
        entity = self.session.get(InvoiceEntity, invoice_id)
        return InvoiceMapper.to_domain(entity) if entity else None

    async def create(self, invoice: Invoice) -> Invoice:
        """Create a new invoice"""
        entity = InvoiceMapper.to_entity(invoice)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return InvoiceMapper.to_domain(entity)

    async def update(self, invoice: Invoice) -> Invoice:
        """Update an existing invoice"""
        if invoice.id is None:
            raise ValueError("Cannot update invoice without ID")
            
        entity = self.session.get(InvoiceEntity, invoice.id)
        if not entity:
            raise ValueError(f"Invoice with ID {invoice.id} not found")
            
        # Update entity with domain model data
        entity.updated_at = datetime.now()
        InvoiceMapper.update_entity(entity, invoice)
        
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return InvoiceMapper.to_domain(entity)

    async def delete(self, invoice_id: int) -> bool:
        """Delete an invoice"""
        entity = self.session.get(InvoiceEntity, invoice_id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False

    async def get_by_student_id(self, student_id: int, offset: int = 0, limit: int = 10) -> Tuple[List[Invoice], int]:
        """Get invoices by student ID with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(InvoiceEntity).where(InvoiceEntity.student_id == student_id)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(InvoiceEntity).where(InvoiceEntity.student_id == student_id).offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        invoices = [InvoiceMapper.to_domain(entity) for entity in entities]
        return invoices, total

    async def get_by_school_id(self, school_id: int, offset: int = 0, limit: int = 10) -> Tuple[List[Invoice], int]:
        """Get invoices by school ID with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(InvoiceEntity).where(InvoiceEntity.school_id == school_id)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(InvoiceEntity).where(InvoiceEntity.school_id == school_id).offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        invoices = [InvoiceMapper.to_domain(entity) for entity in entities]
        return invoices, total

    async def get_by_status(self, status: str, offset: int = 0, limit: int = 10) -> Tuple[List[Invoice], int]:
        """Get invoices by status with pagination"""
        # Get total count
        count_statement = select(func.count()).select_from(InvoiceEntity).where(InvoiceEntity.status == status)
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = select(InvoiceEntity).where(InvoiceEntity.status == status).offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        invoices = [InvoiceMapper.to_domain(entity) for entity in entities]
        return invoices, total
