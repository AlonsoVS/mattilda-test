from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class SchoolFilterDTO(BaseModel):
    """DTO for filtering schools"""
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    principal: Optional[str] = None
    is_active: Optional[bool] = None


class SchoolCreateDTO(BaseModel):
    """DTO for creating a school"""
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: Optional[str] = None
    email: Optional[str] = None
    principal: Optional[str] = None
    is_active: bool = True


class SchoolUpdateDTO(BaseModel):
    """DTO for updating a school"""
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    principal: Optional[str] = None
    is_active: Optional[bool] = None


class SchoolResponseDTO(BaseModel):
    """DTO for school responses"""
    id: int
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: Optional[str] = None
    email: Optional[str] = None
    principal: Optional[str] = None
    student_count: Optional[int] = None
    is_active: bool

    class Config:
        from_attributes = True


class StudentFinancialSummaryDTO(BaseModel):
    """DTO for student financial summary in school account statement"""
    student_id: int
    student_name: str
    total_charges: float
    total_payments: float
    current_balance: float
    pending_amount: float
    paid_amount: float
    overdue_amount: float
    total_invoices: int
    overdue_invoices: int

    class Config:
        from_attributes = True


class SchoolAccountStatementDTO(BaseModel):
    """DTO for school account statement"""
    school_id: int
    school_name: str
    school_address: str
    statement_period_from: date
    statement_period_to: date
    
    # Overall financial summary
    total_charges: float
    total_payments: float
    current_balance: float
    
    # Aggregated amounts
    pending_amount: float
    paid_amount: float
    overdue_amount: float
    
    # Student counts
    total_students: int
    students_with_invoices: int
    students_with_balance: int
    students_overdue: int
    
    # Invoice statistics
    total_invoices: int
    pending_invoices: int
    paid_invoices: int
    overdue_invoices: int
    
    # Student financial details
    student_summaries: List[StudentFinancialSummaryDTO]
    
    # Top statistics
    highest_balance_student: Optional[StudentFinancialSummaryDTO] = None
    most_overdue_student: Optional[StudentFinancialSummaryDTO] = None
    
    # Generated timestamp
    generated_at: date

    class Config:
        from_attributes = True
