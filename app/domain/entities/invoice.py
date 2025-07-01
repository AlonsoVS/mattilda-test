from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date, datetime

if TYPE_CHECKING:
    from .student import Student
    from .school import School


class InvoiceBase(SQLModel):
    """Base invoice model with common fields"""
    invoice_number: str
    student_id: int = Field(foreign_key="student.id")
    school_id: int = Field(foreign_key="school.id")
    amount: float
    tax_amount: float
    total_amount: float
    description: str
    invoice_date: date
    due_date: date
    payment_date: Optional[date] = None
    status: str = "pending"  # "pending", "paid", "overdue", "cancelled"
    payment_method: Optional[str] = None  # "cash", "credit_card", "bank_transfer", "check"
    notes: Optional[str] = None


class Invoice(InvoiceBase, table=True):
    """Invoice database entity"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    student: Optional["Student"] = Relationship(back_populates="invoices")
    school: Optional["School"] = Relationship(back_populates="invoices")
