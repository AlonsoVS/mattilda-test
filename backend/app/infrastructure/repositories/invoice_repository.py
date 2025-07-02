from typing import List, Optional, Tuple
from sqlmodel import Session, func, select, col
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

    async def get_with_filters(self, filters: dict, offset: int = 0, limit: int = 10) -> Tuple[List[Invoice], int]:
        """Get invoices with flexible filtering and pagination"""
        # Build the base query
        statement = select(InvoiceEntity)
        count_statement = select(func.count()).select_from(InvoiceEntity)
        
        # Apply filters
        conditions = []
        
        if filters.get('invoice_number'):
            conditions.append(col(InvoiceEntity.invoice_number).ilike(f"%{filters['invoice_number']}%"))
        
        if filters.get('student_id') is not None:
            conditions.append(InvoiceEntity.student_id == filters['student_id'])
        
        if filters.get('school_id') is not None:
            conditions.append(InvoiceEntity.school_id == filters['school_id'])
        
        # Amount range filters
        if filters.get('amount_min') is not None:
            conditions.append(InvoiceEntity.amount >= filters['amount_min'])
        
        if filters.get('amount_max') is not None:
            conditions.append(InvoiceEntity.amount <= filters['amount_max'])
        
        if filters.get('tax_amount_min') is not None:
            conditions.append(InvoiceEntity.tax_amount >= filters['tax_amount_min'])
        
        if filters.get('tax_amount_max') is not None:
            conditions.append(InvoiceEntity.tax_amount <= filters['tax_amount_max'])
        
        if filters.get('total_amount_min') is not None:
            conditions.append(InvoiceEntity.total_amount >= filters['total_amount_min'])
        
        if filters.get('total_amount_max') is not None:
            conditions.append(InvoiceEntity.total_amount <= filters['total_amount_max'])
        
        if filters.get('description'):
            conditions.append(col(InvoiceEntity.description).ilike(f"%{filters['description']}%"))
        
        # Date range filters
        if filters.get('invoice_date_from'):
            conditions.append(InvoiceEntity.invoice_date >= filters['invoice_date_from'])
        
        if filters.get('invoice_date_to'):
            conditions.append(InvoiceEntity.invoice_date <= filters['invoice_date_to'])
        
        if filters.get('due_date_from'):
            conditions.append(InvoiceEntity.due_date >= filters['due_date_from'])
        
        if filters.get('due_date_to'):
            conditions.append(InvoiceEntity.due_date <= filters['due_date_to'])
        
        if filters.get('payment_date_from'):
            conditions.append(InvoiceEntity.payment_date >= filters['payment_date_from'])
        
        if filters.get('payment_date_to'):
            conditions.append(InvoiceEntity.payment_date <= filters['payment_date_to'])
        
        if filters.get('status'):
            conditions.append(InvoiceEntity.status == filters['status'])
        
        if filters.get('payment_method'):
            conditions.append(InvoiceEntity.payment_method == filters['payment_method'])
        
        # Apply conditions to both statements
        if conditions:
            from sqlmodel import and_
            filter_condition = and_(*conditions)
            statement = statement.where(filter_condition)
            count_statement = count_statement.where(filter_condition)
        
        # Get total count
        total = self.session.exec(count_statement).one()
        
        # Get paginated results
        statement = statement.offset(offset).limit(limit)
        result = self.session.exec(statement)
        entities = list(result.all())
        
        # Convert to domain models
        invoices = [InvoiceMapper.to_domain(entity) for entity in entities]
        return invoices, total
