import pytest
from datetime import datetime, date
from app.domain.models.invoice import Invoice
from app.domain.enums import InvoiceStatus, PaymentMethod


class TestInvoiceDomainModel:
    """Test suite for Invoice domain model"""

    def test_invoice_creation_valid(self):
        """Test successful invoice creation with valid data"""
        invoice_date = date(2024, 1, 15)
        due_date = date(2024, 2, 15)
        
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=invoice_date,
            due_date=due_date
        )
        
        assert invoice.invoice_number == "INV-2024-001"
        assert invoice.student_id == 1
        assert invoice.school_id == 1
        assert invoice.amount == 100.0
        assert invoice.tax_amount == 10.0
        assert invoice.total_amount == 110.0
        assert invoice.description == "Tuition fee"
        assert invoice.invoice_date == invoice_date
        assert invoice.due_date == due_date
        assert invoice.status == InvoiceStatus.PENDING  # Default value
        assert invoice.payment_date is None  # Default value
        assert invoice.payment_method is None  # Default value
        assert invoice.notes is None  # Default value
        assert invoice.id is None  # Default value
        assert invoice.created_at is None  # Default value
        assert invoice.updated_at is None  # Default value

    def test_invoice_creation_with_optional_fields(self):
        """Test invoice creation with optional fields set"""
        current_time = datetime.now()
        invoice_date = date(2024, 1, 15)
        due_date = date(2024, 2, 15)
        payment_date = date(2024, 1, 20)
        
        invoice = Invoice(
            invoice_number="INV-2024-002",
            student_id=2,
            school_id=2,
            amount=200.0,
            tax_amount=20.0,
            total_amount=220.0,
            description="Lab fee",
            invoice_date=invoice_date,
            due_date=due_date,
            status=InvoiceStatus.PAID,
            payment_date=payment_date,
            payment_method=PaymentMethod.CREDIT_CARD,
            notes="Paid via online portal",
            id=1,
            created_at=current_time,
            updated_at=current_time
        )
        
        assert invoice.status == InvoiceStatus.PAID
        assert invoice.payment_date == payment_date
        assert invoice.payment_method == PaymentMethod.CREDIT_CARD
        assert invoice.notes == "Paid via online portal"
        assert invoice.id == 1
        assert invoice.created_at == current_time
        assert invoice.updated_at == current_time

    def test_invoice_creation_negative_amount_raises_error(self):
        """Test that negative amount raises ValueError"""
        with pytest.raises(ValueError, match="Invoice amount must be positive"):
            Invoice(
                invoice_number="INV-2024-001",
                student_id=1,
                school_id=1,
                amount=-100.0,
                tax_amount=10.0,
                total_amount=-90.0,
                description="Invalid amount",
                invoice_date=date(2024, 1, 15),
                due_date=date(2024, 2, 15)
            )

    def test_invoice_creation_zero_amount_raises_error(self):
        """Test that zero amount raises ValueError"""
        with pytest.raises(ValueError, match="Invoice amount must be positive"):
            Invoice(
                invoice_number="INV-2024-001",
                student_id=1,
                school_id=1,
                amount=0.0,
                tax_amount=0.0,
                total_amount=0.0,
                description="Zero amount",
                invoice_date=date(2024, 1, 15),
                due_date=date(2024, 2, 15)
            )

    def test_invoice_creation_negative_tax_amount_raises_error(self):
        """Test that negative tax amount raises ValueError"""
        with pytest.raises(ValueError, match="Tax amount cannot be negative"):
            Invoice(
                invoice_number="INV-2024-001",
                student_id=1,
                school_id=1,
                amount=100.0,
                tax_amount=-10.0,
                total_amount=90.0,
                description="Negative tax",
                invoice_date=date(2024, 1, 15),
                due_date=date(2024, 2, 15)
            )

    def test_invoice_creation_incorrect_total_amount_raises_error(self):
        """Test that incorrect total amount calculation raises ValueError"""
        with pytest.raises(ValueError, match="Total amount must equal amount plus tax amount"):
            Invoice(
                invoice_number="INV-2024-001",
                student_id=1,
                school_id=1,
                amount=100.0,
                tax_amount=10.0,
                total_amount=100.0,  # Should be 110.0
                description="Wrong total",
                invoice_date=date(2024, 1, 15),
                due_date=date(2024, 2, 15)
            )

    def test_invoice_creation_due_date_before_invoice_date_raises_error(self):
        """Test that due date before invoice date raises ValueError"""
        with pytest.raises(ValueError, match="Due date cannot be before invoice date"):
            Invoice(
                invoice_number="INV-2024-001",
                student_id=1,
                school_id=1,
                amount=100.0,
                tax_amount=10.0,
                total_amount=110.0,
                description="Invalid dates",
                invoice_date=date(2024, 2, 15),
                due_date=date(2024, 1, 15)  # Before invoice date
            )

    def test_invoice_mark_as_paid_valid(self):
        """Test marking invoice as paid with valid data"""
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2024, 1, 15),
            due_date=date(2024, 2, 15),
            status=InvoiceStatus.PENDING
        )
        
        payment_date = date(2024, 1, 20)
        payment_method = PaymentMethod.CREDIT_CARD
        notes = "Paid online"
        
        invoice.mark_as_paid(payment_date, payment_method, notes)
        
        assert invoice.status == InvoiceStatus.PAID
        assert invoice.payment_date == payment_date
        assert invoice.payment_method == payment_method
        assert invoice.notes == notes

    def test_invoice_mark_as_paid_without_notes(self):
        """Test marking invoice as paid without notes"""
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2024, 1, 15),
            due_date=date(2024, 2, 15),
            status=InvoiceStatus.PENDING
        )
        
        payment_date = date(2024, 1, 20)
        payment_method = PaymentMethod.CASH
        
        invoice.mark_as_paid(payment_date, payment_method)
        
        assert invoice.status == InvoiceStatus.PAID
        assert invoice.payment_date == payment_date
        assert invoice.payment_method == payment_method
        assert invoice.notes is None

    def test_invoice_mark_as_paid_already_paid_raises_error(self):
        """Test that marking already paid invoice raises ValueError"""
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2024, 1, 15),
            due_date=date(2024, 2, 15),
            status=InvoiceStatus.PAID
        )
        
        with pytest.raises(ValueError, match="Invoice is already paid"):
            invoice.mark_as_paid(date(2024, 1, 25), PaymentMethod.CASH)

    def test_invoice_mark_as_paid_cancelled_raises_error(self):
        """Test that marking cancelled invoice as paid raises ValueError"""
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2024, 1, 15),
            due_date=date(2024, 2, 15),
            status=InvoiceStatus.CANCELLED
        )
        
        with pytest.raises(ValueError, match="Cannot pay a cancelled invoice"):
            invoice.mark_as_paid(date(2024, 1, 25), PaymentMethod.CASH)

    def test_invoice_cancel_valid(self):
        """Test cancelling a pending invoice"""
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2024, 1, 15),
            due_date=date(2024, 2, 15),
            status=InvoiceStatus.PENDING
        )
        
        reason = "Student transferred"
        invoice.cancel(reason)
        
        assert invoice.status == InvoiceStatus.CANCELLED
        assert invoice.notes == reason

    def test_invoice_cancel_without_reason(self):
        """Test cancelling invoice without reason"""
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2024, 1, 15),
            due_date=date(2024, 2, 15),
            status=InvoiceStatus.PENDING
        )
        
        invoice.cancel()
        
        assert invoice.status == InvoiceStatus.CANCELLED
        assert invoice.notes is None

    def test_invoice_cancel_paid_raises_error(self):
        """Test that cancelling paid invoice raises ValueError"""
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2024, 1, 15),
            due_date=date(2024, 2, 15),
            status=InvoiceStatus.PAID
        )
        
        with pytest.raises(ValueError, match="Cannot cancel a paid invoice"):
            invoice.cancel("Attempt to cancel")

    def test_invoice_is_overdue_true(self):
        """Test is_overdue returns True for overdue pending invoice"""
        past_due_date = date(2024, 1, 15)
        current_date = date(2024, 2, 15)  # After due date
        
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2024, 1, 1),
            due_date=past_due_date,
            status=InvoiceStatus.PENDING
        )
        
        assert invoice.is_overdue(current_date) is True

    def test_invoice_is_overdue_false_not_due_yet(self):
        """Test is_overdue returns False for not yet due invoice"""
        future_due_date = date(2024, 3, 15)
        current_date = date(2024, 2, 15)  # Before due date
        
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2024, 1, 1),
            due_date=future_due_date,
            status=InvoiceStatus.PENDING
        )
        
        assert invoice.is_overdue(current_date) is False

    def test_invoice_is_overdue_false_paid_invoice(self):
        """Test is_overdue returns False for paid invoice even if past due date"""
        past_due_date = date(2024, 1, 15)
        current_date = date(2024, 2, 15)  # After due date
        
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2024, 1, 1),
            due_date=past_due_date,
            status=InvoiceStatus.PAID
        )
        
        assert invoice.is_overdue(current_date) is False

    def test_invoice_is_overdue_uses_today_by_default(self):
        """Test is_overdue uses today's date when no date provided"""
        # Create invoice with due date in the past
        past_due_date = date(2020, 1, 1)  # Definitely in the past
        
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2019, 12, 1),
            due_date=past_due_date,
            status=InvoiceStatus.PENDING
        )
        
        # Should be overdue based on today's date
        assert invoice.is_overdue() is True

    def test_invoice_update_method(self):
        """Test the update method returns new instance with updated fields"""
        invoice = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Tuition fee",
            invoice_date=date(2024, 1, 15),
            due_date=date(2024, 2, 15)
        )
        
        updated_invoice = invoice.update(
            description="Updated tuition fee",
            status=InvoiceStatus.PAID,
            notes="Payment received"
        )
        
        # Original invoice should remain unchanged
        assert invoice.description == "Tuition fee"
        assert invoice.status == InvoiceStatus.PENDING
        assert invoice.notes is None
        
        # Updated invoice should have new values
        assert updated_invoice.description == "Updated tuition fee"
        assert updated_invoice.status == InvoiceStatus.PAID
        assert updated_invoice.notes == "Payment received"
        assert updated_invoice.amount == invoice.amount  # Unchanged fields preserved
        assert updated_invoice.updated_at is not None  # Should be set to current time

    def test_invoice_boundary_values(self):
        """Test boundary values for validation"""
        # Test minimum positive amount
        invoice_min_amount = Invoice(
            invoice_number="INV-2024-001",
            student_id=1,
            school_id=1,
            amount=0.01,  # Minimum positive value
            tax_amount=0.0,
            total_amount=0.01,
            description="Minimum amount",
            invoice_date=date(2024, 1, 15),
            due_date=date(2024, 2, 15)
        )
        assert invoice_min_amount.amount == 0.01
        
        # Test zero tax amount (boundary case)
        invoice_zero_tax = Invoice(
            invoice_number="INV-2024-002",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=0.0,  # Zero tax
            total_amount=100.0,
            description="No tax",
            invoice_date=date(2024, 1, 15),
            due_date=date(2024, 2, 15)
        )
        assert invoice_zero_tax.tax_amount == 0.0
        
        # Test due date same as invoice date (boundary case)
        same_date = date(2024, 1, 15)
        invoice_same_dates = Invoice(
            invoice_number="INV-2024-003",
            student_id=1,
            school_id=1,
            amount=100.0,
            tax_amount=10.0,
            total_amount=110.0,
            description="Same dates",
            invoice_date=same_date,
            due_date=same_date
        )
        assert invoice_same_dates.invoice_date == invoice_same_dates.due_date

    def test_invoice_all_enum_values(self):
        """Test that all enum values work correctly"""
        invoice_date = date(2024, 1, 15)
        due_date = date(2024, 2, 15)
        
        # Test all status values
        for status in InvoiceStatus:
            invoice = Invoice(
                invoice_number=f"INV-{status.value}",
                student_id=1,
                school_id=1,
                amount=100.0,
                tax_amount=10.0,
                total_amount=110.0,
                description=f"Status {status.value}",
                invoice_date=invoice_date,
                due_date=due_date,
                status=status
            )
            assert invoice.status == status
        
        # Test all payment method values
        for payment_method in PaymentMethod:
            invoice = Invoice(
                invoice_number=f"INV-{payment_method.value}",
                student_id=1,
                school_id=1,
                amount=100.0,
                tax_amount=10.0,
                total_amount=110.0,
                description=f"Payment {payment_method.value}",
                invoice_date=invoice_date,
                due_date=due_date,
                payment_method=payment_method
            )
            assert invoice.payment_method == payment_method
