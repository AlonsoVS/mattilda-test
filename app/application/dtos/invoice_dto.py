from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class InvoiceCreateDTO(BaseModel):
    """DTO for creating an invoice"""
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


class InvoiceUpdateDTO(BaseModel):
    """DTO for updating an invoice"""
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


class InvoiceResponseDTO(BaseModel):
    """DTO for invoice responses"""
    id: int
    invoice_number: str
    student_id: int
    school_id: int
    amount: float
    tax_amount: float
    total_amount: float
    description: str
    invoice_date: date
    due_date: date
    payment_date: Optional[date] = None
    status: str
    payment_method: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class PaymentRecordDTO(BaseModel):
    """DTO for recording payments"""
    payment_date: date
    payment_method: str
    notes: Optional[str] = None
