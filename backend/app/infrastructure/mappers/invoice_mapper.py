from app.domain.models.invoice import Invoice
from app.infrastructure.persistence.invoice_entity import InvoiceEntity


class InvoiceMapper:
    """Mapper between Invoice domain model and InvoiceEntity persistence model"""

    @staticmethod
    def to_domain(entity: InvoiceEntity) -> Invoice:
        """Convert InvoiceEntity to Invoice domain model"""
        return Invoice(
            id=entity.id,
            invoice_number=entity.invoice_number,
            student_id=entity.student_id,
            school_id=entity.school_id,
            amount=entity.amount,
            tax_amount=entity.tax_amount,
            total_amount=entity.total_amount,
            description=entity.description,
            invoice_date=entity.invoice_date,
            due_date=entity.due_date,
            payment_date=entity.payment_date,
            status=entity.status,
            payment_method=entity.payment_method,
            notes=entity.notes,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_entity(domain: Invoice) -> InvoiceEntity:
        """Convert Invoice domain model to InvoiceEntity"""
        entity = InvoiceEntity(
            invoice_number=domain.invoice_number,
            student_id=domain.student_id,
            school_id=domain.school_id,
            amount=domain.amount,
            tax_amount=domain.tax_amount,
            total_amount=domain.total_amount,
            description=domain.description,
            invoice_date=domain.invoice_date,
            due_date=domain.due_date,
            payment_date=domain.payment_date,
            status=domain.status,
            payment_method=domain.payment_method,
            notes=domain.notes
        )
        
        if domain.id is not None:
            entity.id = domain.id
        if domain.created_at is not None:
            entity.created_at = domain.created_at
        if domain.updated_at is not None:
            entity.updated_at = domain.updated_at
            
        return entity

    @staticmethod
    def update_entity(entity: InvoiceEntity, domain: Invoice) -> InvoiceEntity:
        """Update existing entity with domain model data"""
        entity.invoice_number = domain.invoice_number
        entity.student_id = domain.student_id
        entity.school_id = domain.school_id
        entity.amount = domain.amount
        entity.tax_amount = domain.tax_amount
        entity.total_amount = domain.total_amount
        entity.description = domain.description
        entity.invoice_date = domain.invoice_date
        entity.due_date = domain.due_date
        entity.payment_date = domain.payment_date
        entity.status = domain.status
        entity.payment_method = domain.payment_method
        entity.notes = domain.notes
        
        return entity
