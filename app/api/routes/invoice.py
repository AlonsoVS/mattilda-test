from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from datetime import datetime
from app.database import get_session
from app.models import Invoice, InvoiceCreate, InvoiceRead, InvoiceUpdate, PaymentRecord

invoice_router = APIRouter(prefix="/invoices", tags=["invoices"])


@invoice_router.get("/", response_model=List[InvoiceRead])
async def get_invoices(session: Session = Depends(get_session)):
    """Get all invoices"""
    invoices = session.exec(select(Invoice)).all()
    return invoices


@invoice_router.get("/{invoice_id}", response_model=InvoiceRead)
async def get_invoice(invoice_id: int, session: Session = Depends(get_session)):
    """Get an invoice by ID"""
    invoice = session.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@invoice_router.post("/", response_model=InvoiceRead)
async def create_invoice(invoice: InvoiceCreate, session: Session = Depends(get_session)):
    """Create a new invoice"""
    current_time = datetime.now()
    total_amount = invoice.amount + invoice.tax_amount
    
    invoice_data = invoice.model_dump()
    invoice_data.update({
        "total_amount": total_amount,
        "created_at": current_time,
        "updated_at": current_time
    })
    
    db_invoice = Invoice.model_validate(invoice_data)
    session.add(db_invoice)
    session.commit()
    session.refresh(db_invoice)
    return db_invoice


@invoice_router.put("/{invoice_id}", response_model=InvoiceRead)
async def update_invoice(
    invoice_id: int, 
    invoice_update: InvoiceUpdate, 
    session: Session = Depends(get_session)
):
    """Update an invoice by ID"""
    db_invoice = session.get(Invoice, invoice_id)
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Update only provided fields
    update_data = invoice_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_invoice, field, value)
    
    # Recalculate total if amount or tax changed
    if "amount" in update_data or "tax_amount" in update_data:
        db_invoice.total_amount = db_invoice.amount + db_invoice.tax_amount
    
    db_invoice.updated_at = datetime.now()
    session.add(db_invoice)
    session.commit()
    session.refresh(db_invoice)
    return db_invoice


@invoice_router.delete("/{invoice_id}")
async def delete_invoice(invoice_id: int, session: Session = Depends(get_session)):
    """Delete an invoice by ID"""
    db_invoice = session.get(Invoice, invoice_id)
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    session.delete(db_invoice)
    session.commit()
    return {"message": "Invoice deleted successfully"}


@invoice_router.get("/student/{student_id}", response_model=List[InvoiceRead])
async def get_invoices_by_student(student_id: int, session: Session = Depends(get_session)):
    """Get invoices by student ID"""
    statement = select(Invoice).where(Invoice.student_id == student_id)
    invoices = session.exec(statement).all()
    return invoices


@invoice_router.get("/school/{school_id}", response_model=List[InvoiceRead])
async def get_invoices_by_school(school_id: int, session: Session = Depends(get_session)):
    """Get invoices by school ID"""
    statement = select(Invoice).where(Invoice.school_id == school_id)
    invoices = session.exec(statement).all()
    return invoices


@invoice_router.get("/status/{status}", response_model=List[InvoiceRead])
async def get_invoices_by_status(status: str, session: Session = Depends(get_session)):
    """Get invoices by status (pending, paid, overdue, cancelled)"""
    statement = select(Invoice).where(Invoice.status == status.lower())
    invoices = session.exec(statement).all()
    return invoices


@invoice_router.post("/{invoice_id}/payment")
async def record_payment(
    invoice_id: int, 
    payment: PaymentRecord, 
    session: Session = Depends(get_session)
):
    """Record a payment for an invoice"""
    db_invoice = session.get(Invoice, invoice_id)
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    if db_invoice.status == "paid":
        raise HTTPException(status_code=400, detail="Invoice is already paid")
    
    db_invoice.payment_date = payment.payment_date
    db_invoice.payment_method = payment.payment_method
    db_invoice.status = "paid"
    db_invoice.updated_at = datetime.now()
    
    if payment.notes:
        db_invoice.notes = payment.notes
    
    session.add(db_invoice)
    session.commit()
    session.refresh(db_invoice)
    
    return {"message": "Payment recorded successfully", "invoice": db_invoice}
