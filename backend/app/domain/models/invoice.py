from typing import Optional
from datetime import date, datetime
from dataclasses import dataclass
from app.domain.enums import InvoiceStatus, PaymentMethod


@dataclass
class Invoice:
    """Pure domain model for Invoice"""
    invoice_number: str
    student_id: int
    school_id: int
    amount: float
    tax_amount: float
    total_amount: float
    description: str
    invoice_date: date
    due_date: date
    status: InvoiceStatus = InvoiceStatus.PENDING
    payment_date: Optional[date] = None
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate business rules"""
        if self.amount <= 0:
            raise ValueError("Invoice amount must be positive")
        if self.tax_amount < 0:
            raise ValueError("Tax amount cannot be negative")
        if self.total_amount != self.amount + self.tax_amount:
            raise ValueError("Total amount must equal amount plus tax amount")
        if self.due_date < self.invoice_date:
            raise ValueError("Due date cannot be before invoice date")
        if self.status not in [InvoiceStatus.PENDING, InvoiceStatus.PAID, InvoiceStatus.OVERDUE, InvoiceStatus.CANCELLED]:
            raise ValueError("Invalid invoice status")

    def mark_as_paid(self, payment_date: date, payment_method: PaymentMethod, notes: Optional[str] = None) -> None:
        """Mark invoice as paid"""
        if self.status == InvoiceStatus.PAID:
            raise ValueError("Invoice is already paid")
        if self.status == InvoiceStatus.CANCELLED:
            raise ValueError("Cannot pay a cancelled invoice")
        
        self.status = InvoiceStatus.PAID
        self.payment_date = payment_date
        self.payment_method = payment_method
        if notes:
            self.notes = notes

    def cancel(self, reason: Optional[str] = None) -> None:
        """Cancel the invoice"""
        if self.status == InvoiceStatus.PAID:
            raise ValueError("Cannot cancel a paid invoice")
        
        self.status = InvoiceStatus.CANCELLED
        if reason:
            self.notes = reason

    def is_overdue(self, current_date: Optional[date] = None) -> bool:
        """Check if invoice is overdue"""
        if current_date is None:
            current_date = date.today()
        return self.status == InvoiceStatus.PENDING and self.due_date < current_date

    def update(self, **kwargs) -> 'Invoice':
        """Update invoice fields and return new instance"""
        # Create a new invoice with updated values
        current_values = {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'student_id': self.student_id,
            'school_id': self.school_id,
            'amount': self.amount,
            'tax_amount': self.tax_amount,
            'total_amount': self.total_amount,
            'description': self.description,
            'invoice_date': self.invoice_date,
            'due_date': self.due_date,
            'status': self.status,
            'payment_date': self.payment_date,
            'payment_method': self.payment_method,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': datetime.now()
        }
        current_values.update(kwargs)
        return Invoice(**current_values)
