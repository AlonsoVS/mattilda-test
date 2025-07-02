from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class StudentFilterDTO(BaseModel):
    """DTO for filtering students"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    grade_level: Optional[int] = None
    school_id: Optional[int] = None
    enrollment_date: Optional[date] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class StudentCreateDTO(BaseModel):
    """DTO for creating a student"""
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: date
    grade_level: int
    school_id: int
    enrollment_date: date
    address: str
    is_active: bool = True


class StudentUpdateDTO(BaseModel):
    """DTO for updating a student"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    grade_level: Optional[int] = None
    school_id: Optional[int] = None
    enrollment_date: Optional[date] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class StudentResponseDTO(BaseModel):
    """DTO for student responses"""
    id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: date
    grade_level: int
    school_id: int
    enrollment_date: date
    address: str
    is_active: bool

    class Config:
        from_attributes = True


class InvoiceSummaryDTO(BaseModel):
    """DTO for invoice summary in account statement"""
    id: int
    invoice_number: str
    description: str
    invoice_date: date
    due_date: date
    amount: float
    tax_amount: float
    total_amount: float
    status: str
    payment_date: Optional[date] = None
    payment_method: Optional[str] = None

    class Config:
        from_attributes = True


class StudentAccountStatementDTO(BaseModel):
    """DTO for student account statement"""
    student_id: int
    student_name: str
    school_name: str
    statement_period_from: date
    statement_period_to: date
    
    # Financial summary
    total_charges: float
    total_payments: float
    current_balance: float
    
    # Detailed breakdown
    pending_invoices: List[InvoiceSummaryDTO]
    paid_invoices: List[InvoiceSummaryDTO]
    overdue_invoices: List[InvoiceSummaryDTO]
    
    # Account statistics
    total_invoices: int
    pending_amount: float
    paid_amount: float
    overdue_amount: float
    
    # Generated timestamp
    generated_at: date

    class Config:
        from_attributes = True
