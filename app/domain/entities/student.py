from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from .school import School
    from .invoice import Invoice


class StudentBase(SQLModel):
    """Base student model with common fields"""
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: date
    grade_level: int
    school_id: int = Field(foreign_key="school.id")
    student_id_number: str
    enrollment_date: date
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_email: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    is_active: bool = True


class Student(StudentBase, table=True):
    """Student database entity"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    school: Optional["School"] = Relationship(back_populates="students")
    invoices: List["Invoice"] = Relationship(back_populates="student")
