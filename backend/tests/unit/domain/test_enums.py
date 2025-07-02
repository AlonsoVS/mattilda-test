import pytest
from app.domain.enums import InvoiceStatus, PaymentMethod


class TestDomainEnums:
    """Test suite for domain enums"""

    def test_invoice_status_enum_values(self):
        """Test that InvoiceStatus enum has correct values"""
        assert InvoiceStatus.PENDING == "pending"
        assert InvoiceStatus.PAID == "paid"
        assert InvoiceStatus.OVERDUE == "overdue"
        assert InvoiceStatus.CANCELLED == "cancelled"

    def test_invoice_status_enum_membership(self):
        """Test InvoiceStatus enum membership"""
        # Test that enum members exist
        assert InvoiceStatus.PENDING in InvoiceStatus
        assert InvoiceStatus.PAID in InvoiceStatus
        assert InvoiceStatus.OVERDUE in InvoiceStatus
        assert InvoiceStatus.CANCELLED in InvoiceStatus
        
        # Test value lookup
        status_values = [status.value for status in InvoiceStatus]
        assert "pending" in status_values
        assert "paid" in status_values
        assert "overdue" in status_values
        assert "cancelled" in status_values
        assert "invalid_status" not in status_values

    def test_invoice_status_enum_iteration(self):
        """Test InvoiceStatus enum iteration"""
        expected_values = {"pending", "paid", "overdue", "cancelled"}
        actual_values = {status.value for status in InvoiceStatus}
        assert actual_values == expected_values

    def test_invoice_status_enum_count(self):
        """Test InvoiceStatus enum has correct number of values"""
        assert len(list(InvoiceStatus)) == 4

    def test_payment_method_enum_values(self):
        """Test that PaymentMethod enum has correct values"""
        assert PaymentMethod.CASH == "cash"
        assert PaymentMethod.CREDIT_CARD == "credit_card"
        assert PaymentMethod.BANK_TRANSFER == "bank_transfer"
        assert PaymentMethod.CHECK == "check"

    def test_payment_method_enum_membership(self):
        """Test PaymentMethod enum membership"""
        # Test that enum members exist
        assert PaymentMethod.CASH in PaymentMethod
        assert PaymentMethod.CREDIT_CARD in PaymentMethod
        assert PaymentMethod.BANK_TRANSFER in PaymentMethod
        assert PaymentMethod.CHECK in PaymentMethod
        
        # Test value lookup
        method_values = [method.value for method in PaymentMethod]
        assert "cash" in method_values
        assert "credit_card" in method_values
        assert "bank_transfer" in method_values
        assert "check" in method_values
        assert "invalid_method" not in method_values

    def test_payment_method_enum_iteration(self):
        """Test PaymentMethod enum iteration"""
        expected_values = {"cash", "credit_card", "bank_transfer", "check"}
        actual_values = {method.value for method in PaymentMethod}
        assert actual_values == expected_values

    def test_payment_method_enum_count(self):
        """Test PaymentMethod enum has correct number of values"""
        assert len(list(PaymentMethod)) == 4

    def test_invoice_status_string_conversion(self):
        """Test that InvoiceStatus values convert to strings correctly"""
        assert InvoiceStatus.PENDING.value == "pending"
        assert InvoiceStatus.PAID.value == "paid"
        assert InvoiceStatus.OVERDUE.value == "overdue"
        assert InvoiceStatus.CANCELLED.value == "cancelled"

    def test_payment_method_string_conversion(self):
        """Test that PaymentMethod values convert to strings correctly"""
        assert PaymentMethod.CASH.value == "cash"
        assert PaymentMethod.CREDIT_CARD.value == "credit_card"
        assert PaymentMethod.BANK_TRANSFER.value == "bank_transfer"
        assert PaymentMethod.CHECK.value == "check"

    def test_enum_comparison(self):
        """Test enum value comparison"""
        # Test equality
        assert InvoiceStatus.PENDING == InvoiceStatus.PENDING
        assert PaymentMethod.CASH == PaymentMethod.CASH
        
        # Test inequality
        assert InvoiceStatus.PENDING != InvoiceStatus.PAID
        assert PaymentMethod.CASH != PaymentMethod.CREDIT_CARD
        
        # Test comparison with string values
        assert InvoiceStatus.PENDING == "pending"
        assert PaymentMethod.CASH == "cash"

    def test_enum_uniqueness(self):
        """Test that all enum values are unique"""
        # Test InvoiceStatus uniqueness
        status_values = [status.value for status in InvoiceStatus]
        assert len(status_values) == len(set(status_values))
        
        # Test PaymentMethod uniqueness
        method_values = [method.value for method in PaymentMethod]
        assert len(method_values) == len(set(method_values))

    def test_enum_case_sensitivity(self):
        """Test enum case sensitivity"""
        # Enums should be case sensitive
        assert InvoiceStatus.PENDING != "PENDING"
        assert InvoiceStatus.PENDING != "Pending"
        assert PaymentMethod.CASH != "CASH"
        assert PaymentMethod.CREDIT_CARD != "Credit_Card"
