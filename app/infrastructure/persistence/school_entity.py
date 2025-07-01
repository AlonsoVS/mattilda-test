from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .student_entity import StudentEntity
    from .invoice_entity import InvoiceEntity


class SchoolBase(SQLModel):
    """Base school entity with common fields"""
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone_number: str
    email: str
    principal_name: str
    established_year: int
    is_active: bool = True


class SchoolEntity(SchoolBase, table=True):
    """School persistence entity"""
    
    __tablename__ = "schools" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships  
    students: List["StudentEntity"] = Relationship(back_populates="school")
    invoices: List["InvoiceEntity"] = Relationship(back_populates="school")
