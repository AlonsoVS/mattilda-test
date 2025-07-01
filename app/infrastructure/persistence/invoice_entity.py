from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date, datetime

if TYPE_CHECKING:
    from .student_entity import StudentEntity
    from .school_entity import SchoolEntity


class InvoiceBase(SQLModel):
    """Base invoice entity with common fields"""
    invoice_number: str
    student_id: int = Field(foreign_key="students.id")
    school_id: int = Field(foreign_key="schools.id")
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


class InvoiceEntity(InvoiceBase, table=True):
    """Invoice persistence entity"""
    
    __tablename__ = "invoices" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    student: Optional["StudentEntity"] = Relationship(back_populates="invoices")
    school: Optional["SchoolEntity"] = Relationship(back_populates="invoices")
