from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .student import Student
    from .invoice import Invoice


class SchoolBase(SQLModel):
    """Base school model with common fields"""
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: Optional[str] = None
    email: Optional[str] = None
    principal: Optional[str] = None
    student_count: Optional[int] = None
    is_active: bool = True


class School(SchoolBase, table=True):
    """School database entity"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    students: List["Student"] = Relationship(back_populates="school")
    invoices: List["Invoice"] = Relationship(back_populates="school")
