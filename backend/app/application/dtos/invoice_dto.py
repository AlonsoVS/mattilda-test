from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.domain.enums import InvoiceStatus, PaymentMethod


class InvoiceFilterDTO(BaseModel):
    """DTO for filtering invoices"""
    invoice_number: Optional[str] = None
    student_id: Optional[int] = None
    school_id: Optional[int] = None
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    tax_amount_min: Optional[float] = None
    tax_amount_max: Optional[float] = None
    total_amount_min: Optional[float] = None
    total_amount_max: Optional[float] = None
    description: Optional[str] = None
    invoice_date_from: Optional[date] = None
    invoice_date_to: Optional[date] = None
    due_date_from: Optional[date] = None
    due_date_to: Optional[date] = None
    payment_date_from: Optional[date] = None
    payment_date_to: Optional[date] = None
    status: Optional[InvoiceStatus] = None
    payment_method: Optional[PaymentMethod] = None


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
    status: InvoiceStatus = InvoiceStatus.PENDING
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
    status: Optional[InvoiceStatus] = None
    payment_method: Optional[PaymentMethod] = None
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
    status: InvoiceStatus
    payment_method: Optional[PaymentMethod] = None
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class PaymentRecordDTO(BaseModel):
    """DTO for recording payments"""
    payment_date: date
    payment_method: PaymentMethod
    notes: Optional[str] = None
