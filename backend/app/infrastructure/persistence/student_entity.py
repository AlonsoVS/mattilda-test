from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, date

if TYPE_CHECKING:
    from .invoice_entity import InvoiceEntity
    from .school_entity import SchoolEntity


class StudentBase(SQLModel):
    """Base student entity with common fields"""
    first_name: str
    last_name: str
    email: str
    phone_number: str
    date_of_birth: date
    grade_level: int
    school_id: int = Field(foreign_key="schools.id")
    enrollment_date: date
    address: str
    is_active: bool = True


class StudentEntity(StudentBase, table=True):
    """Student persistence entity"""
    
    __tablename__ = "students" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    school: Optional["SchoolEntity"] = Relationship(back_populates="students")
    invoices: List["InvoiceEntity"] = Relationship(back_populates="student")
