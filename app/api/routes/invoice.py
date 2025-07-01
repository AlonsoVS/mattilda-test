from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal

invoice_router = APIRouter(prefix="/invoices", tags=["invoices"])


class Invoice(BaseModel):
    id: Optional[int] = None
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
    status: str  # "pending", "paid", "overdue", "cancelled"
    payment_method: Optional[str] = None  # "cash", "credit_card", "bank_transfer", "check"
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None


class InvoiceCreate(BaseModel):
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


class InvoiceUpdate(BaseModel):
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


class PaymentRecord(BaseModel):
    payment_date: date
    payment_method: str
    notes: Optional[str] = None


# In-memory storage for demonstration (replace with database in production)
invoices_db = [
    Invoice(
        id=1,
        invoice_number="INV-2024-001",
        student_id=1,
        school_id=1,
        amount=850.00,
        tax_amount=68.00,
        total_amount=918.00,
        description="Tuition fee for Spring semester 2024",
        invoice_date=date(2024, 1, 15),
        due_date=date(2024, 2, 15),
        payment_date=date(2024, 2, 10),
        status="paid",
        payment_method="bank_transfer",
        created_at=datetime(2024, 1, 15, 9, 0, 0),
        updated_at=datetime(2024, 2, 10, 14, 30, 0),
        notes="Payment received on time"
    ),
    Invoice(
        id=2,
        invoice_number="INV-2024-002",
        student_id=2,
        school_id=2,
        amount=1200.00,
        tax_amount=96.00,
        total_amount=1296.00,
        description="High school tuition and laboratory fees",
        invoice_date=date(2024, 1, 20),
        due_date=date(2024, 2, 20),
        payment_date=None,
        status="pending",
        payment_method=None,
        created_at=datetime(2024, 1, 20, 10, 0, 0),
        updated_at=datetime(2024, 1, 20, 10, 0, 0),
        notes="Reminder sent on 2024-02-15"
    ),
    Invoice(
        id=3,
        invoice_number="INV-2024-003",
        student_id=3,
        school_id=3,
        amount=750.00,
        tax_amount=60.00,
        total_amount=810.00,
        description="Middle school tuition and activity fees",
        invoice_date=date(2024, 1, 25),
        due_date=date(2024, 2, 25),
        payment_date=date(2024, 2, 22),
        status="paid",
        payment_method="credit_card",
        created_at=datetime(2024, 1, 25, 11, 0, 0),
        updated_at=datetime(2024, 2, 22, 16, 45, 0),
        notes="Paid via online portal"
    ),
    Invoice(
        id=4,
        invoice_number="INV-2024-004",
        student_id=4,
        school_id=4,
        amount=950.00,
        tax_amount=76.00,
        total_amount=1026.00,
        description="Academy tuition and technology fee",
        invoice_date=date(2024, 2, 1),
        due_date=date(2024, 3, 1),
        payment_date=None,
        status="overdue",
        payment_method=None,
        created_at=datetime(2024, 2, 1, 9, 30, 0),
        updated_at=datetime(2024, 3, 5, 8, 0, 0),
        notes="Second notice sent"
    ),
    Invoice(
        id=5,
        invoice_number="INV-2024-005",
        student_id=5,
        school_id=5,
        amount=1100.00,
        tax_amount=88.00,
        total_amount=1188.00,
        description="Preparatory school tuition",
        invoice_date=date(2024, 2, 5),
        due_date=date(2024, 3, 5),
        payment_date=date(2024, 3, 1),
        status="paid",
        payment_method="check",
        created_at=datetime(2024, 2, 5, 12, 0, 0),
        updated_at=datetime(2024, 3, 1, 10, 15, 0),
        notes="Check #1234 received"
    ),
    Invoice(
        id=6,
        invoice_number="INV-2024-006",
        student_id=6,
        school_id=6,
        amount=680.00,
        tax_amount=54.40,
        total_amount=734.40,
        description="Charter school tuition and supplies",
        invoice_date=date(2024, 2, 10),
        due_date=date(2024, 3, 10),
        payment_date=None,
        status="pending",
        payment_method=None,
        created_at=datetime(2024, 2, 10, 14, 0, 0),
        updated_at=datetime(2024, 2, 10, 14, 0, 0),
        notes="First notice"
    ),
    Invoice(
        id=7,
        invoice_number="INV-2024-007",
        student_id=7,
        school_id=7,
        amount=1050.00,
        tax_amount=84.00,
        total_amount=1134.00,
        description="Institute tuition and graduation fees",
        invoice_date=date(2024, 2, 15),
        due_date=date(2024, 3, 15),
        payment_date=None,
        status="cancelled",
        payment_method=None,
        created_at=datetime(2024, 2, 15, 15, 0, 0),
        updated_at=datetime(2024, 2, 20, 9, 0, 0),
        notes="Student transferred to another school"
    ),
    Invoice(
        id=8,
        invoice_number="INV-2024-008",
        student_id=8,
        school_id=8,
        amount=780.00,
        tax_amount=62.40,
        total_amount=842.40,
        description="Community school tuition",
        invoice_date=date(2024, 2, 20),
        due_date=date(2024, 3, 20),
        payment_date=date(2024, 3, 18),
        status="paid",
        payment_method="cash",
        created_at=datetime(2024, 2, 20, 16, 0, 0),
        updated_at=datetime(2024, 3, 18, 11, 30, 0),
        notes="Cash payment received at school office"
    )
]
next_invoice_id = 9


@invoice_router.get("/", response_model=List[Invoice])
async def get_invoices():
    """Get all invoices"""
    return invoices_db


@invoice_router.get("/{invoice_id}", response_model=Invoice)
async def get_invoice(invoice_id: int):
    """Get an invoice by ID"""
    invoice = next((invoice for invoice in invoices_db if invoice.id == invoice_id), None)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@invoice_router.post("/", response_model=Invoice)
async def create_invoice(invoice: InvoiceCreate):
    """Create a new invoice"""
    global next_invoice_id
    current_time = datetime.now()
    total_amount = invoice.amount + invoice.tax_amount
    
    new_invoice = Invoice(
        id=next_invoice_id,
        total_amount=total_amount,
        created_at=current_time,
        updated_at=current_time,
        **invoice.dict()
    )
    invoices_db.append(new_invoice)
    next_invoice_id += 1
    return new_invoice


@invoice_router.put("/{invoice_id}", response_model=Invoice)
async def update_invoice(invoice_id: int, invoice_update: InvoiceUpdate):
    """Update an invoice by ID"""
    invoice = next((invoice for invoice in invoices_db if invoice.id == invoice_id), None)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Update only provided fields
    update_data = invoice_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(invoice, field, value)
    
    # Recalculate total if amount or tax changed
    if "amount" in update_data or "tax_amount" in update_data:
        invoice.total_amount = invoice.amount + invoice.tax_amount
    
    invoice.updated_at = datetime.now()
    return invoice


@invoice_router.delete("/{invoice_id}")
async def delete_invoice(invoice_id: int):
    """Delete an invoice by ID"""
    global invoices_db
    invoice = next((invoice for invoice in invoices_db if invoice.id == invoice_id), None)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    invoices_db = [inv for inv in invoices_db if inv.id != invoice_id]
    return {"message": "Invoice deleted successfully"}


@invoice_router.get("/student/{student_id}", response_model=List[Invoice])
async def get_invoices_by_student(student_id: int):
    """Get invoices by student ID"""
    student_invoices = [invoice for invoice in invoices_db if invoice.student_id == student_id]
    return student_invoices


@invoice_router.get("/school/{school_id}", response_model=List[Invoice])
async def get_invoices_by_school(school_id: int):
    """Get invoices by school ID"""
    school_invoices = [invoice for invoice in invoices_db if invoice.school_id == school_id]
    return school_invoices


@invoice_router.get("/status/{status}", response_model=List[Invoice])
async def get_invoices_by_status(status: str):
    """Get invoices by status (pending, paid, overdue, cancelled)"""
    status_invoices = [invoice for invoice in invoices_db if invoice.status.lower() == status.lower()]
    return status_invoices


@invoice_router.post("/{invoice_id}/payment")
async def record_payment(invoice_id: int, payment: PaymentRecord):
    """Record a payment for an invoice"""
    invoice = next((invoice for invoice in invoices_db if invoice.id == invoice_id), None)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    if invoice.status == "paid":
        raise HTTPException(status_code=400, detail="Invoice is already paid")
    
    invoice.payment_date = payment.payment_date
    invoice.payment_method = payment.payment_method
    invoice.status = "paid"
    invoice.updated_at = datetime.now()
    
    if payment.notes:
        invoice.notes = payment.notes
    
    return {"message": "Payment recorded successfully", "invoice": invoice}
