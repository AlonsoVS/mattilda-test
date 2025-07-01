from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date, datetime


class SchoolBase(SQLModel):
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
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    students: List["Student"] = Relationship(back_populates="school")
    invoices: List["Invoice"] = Relationship(back_populates="school")


class SchoolCreate(SchoolBase):
    pass


class SchoolRead(SchoolBase):
    id: int


class SchoolUpdate(SQLModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    principal: Optional[str] = None
    student_count: Optional[int] = None
    is_active: Optional[bool] = None


class StudentBase(SQLModel):
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
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    school: Optional[School] = Relationship(back_populates="students")
    invoices: List["Invoice"] = Relationship(back_populates="student")


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int


class StudentUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    grade_level: Optional[int] = None
    school_id: Optional[int] = None
    student_id_number: Optional[str] = None
    enrollment_date: Optional[date] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    is_active: Optional[bool] = None


class InvoiceBase(SQLModel):
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
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    student: Optional[Student] = Relationship(back_populates="invoices")
    school: Optional[School] = Relationship(back_populates="invoices")


class InvoiceCreate(SQLModel):
    invoice_number: str
    student_id: int
    school_id: int
    amount: float
    tax_amount: float
    description: str
    invoice_date: date
    due_date: date
    status: str = "pending"
    notes: Optional[str] = None


class InvoiceRead(InvoiceBase):
    id: int
    created_at: datetime
    updated_at: datetime


class InvoiceUpdate(SQLModel):
    invoice_number: Optional[str] = None
    student_id: Optional[int] = None
    school_id: Optional[int] = None
    amount: Optional[float] = None
    tax_amount: Optional[float] = None
    description: Optional[str] = None
    invoice_date: Optional[date] = None
    due_date: Optional[date] = None
    payment_date: Optional[date] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class PaymentRecord(SQLModel):
    payment_date: date
    payment_method: str
    notes: Optional[str] = None
