import pytest
from datetime import datetime, date
from app.domain.models.school import School


class TestSchoolDomainModel:
    """Test suite for School domain model"""

    def test_school_creation_valid(self):
        """Test successful school creation with valid data"""
        school = School(
            name="Springfield Elementary",
            address="123 Main Street",
            city="Springfield",
            state="CA",
            zip_code="90210",
            phone_number="555-0123",
            email="admin@springfield.edu",
            principal_name="John Smith",
            established_year=1995
        )
        
        assert school.name == "Springfield Elementary"
        assert school.address == "123 Main Street"
        assert school.city == "Springfield"
        assert school.state == "CA"
        assert school.zip_code == "90210"
        assert school.phone_number == "555-0123"
        assert school.email == "admin@springfield.edu"
        assert school.principal_name == "John Smith"
        assert school.established_year == 1995
        assert school.is_active is True  # Default value
        assert school.id is None  # Default value
        assert school.created_at is None  # Default value
        assert school.updated_at is None  # Default value

    def test_school_creation_with_optional_fields(self):
        """Test school creation with optional fields set"""
        current_time = datetime.now()
        school = School(
            name="Test School",
            address="456 Oak Ave",
            city="Testville",
            state="TX",
            zip_code="12345",
            phone_number="555-9999",
            email="test@testschool.edu",
            principal_name="Jane Doe",
            established_year=2000,
            is_active=False,
            id=1,
            created_at=current_time,
            updated_at=current_time
        )
        
        assert school.is_active is False
        assert school.id == 1
        assert school.created_at == current_time
        assert school.updated_at == current_time

    def test_school_creation_empty_name_raises_error(self):
        """Test that empty name raises ValueError"""
        with pytest.raises(ValueError, match="School name cannot be empty"):
            School(
                name="   ",  # Empty after strip
                address="123 Main Street",
                city="Springfield",
                state="CA",
                zip_code="90210",
                phone_number="555-0123",
                email="admin@springfield.edu",
                principal_name="John Smith",
                established_year=1995
            )

    def test_school_creation_empty_address_raises_error(self):
        """Test that empty address raises ValueError"""
        with pytest.raises(ValueError, match="Address cannot be empty"):
            School(
                name="Test School",
                address="",
                city="Springfield",
                state="CA",
                zip_code="90210",
                phone_number="555-0123",
                email="admin@springfield.edu",
                principal_name="John Smith",
                established_year=1995
            )

    def test_school_creation_empty_city_raises_error(self):
        """Test that empty city raises ValueError"""
        with pytest.raises(ValueError, match="City cannot be empty"):
            School(
                name="Test School",
                address="123 Main Street",
                city="   ",
                state="CA",
                zip_code="90210",
                phone_number="555-0123",
                email="admin@springfield.edu",
                principal_name="John Smith",
                established_year=1995
            )

    def test_school_creation_empty_state_raises_error(self):
        """Test that empty state raises ValueError"""
        with pytest.raises(ValueError, match="State cannot be empty"):
            School(
                name="Test School",
                address="123 Main Street",
                city="Springfield",
                state="",
                zip_code="90210",
                phone_number="555-0123",
                email="admin@springfield.edu",
                principal_name="John Smith",
                established_year=1995
            )

    def test_school_creation_invalid_email_raises_error(self):
        """Test that invalid email raises ValueError"""
        with pytest.raises(ValueError, match="Valid email is required"):
            School(
                name="Test School",
                address="123 Main Street",
                city="Springfield",
                state="CA",
                zip_code="90210",
                phone_number="555-0123",
                email="invalid-email",
                principal_name="John Smith",
                established_year=1995
            )

    def test_school_creation_empty_email_raises_error(self):
        """Test that empty email raises ValueError"""
        with pytest.raises(ValueError, match="Valid email is required"):
            School(
                name="Test School",
                address="123 Main Street",
                city="Springfield",
                state="CA",
                zip_code="90210",
                phone_number="555-0123",
                email="",
                principal_name="John Smith",
                established_year=1995
            )

    def test_school_creation_invalid_establishment_year_too_old_raises_error(self):
        """Test that establishment year before 1800 raises ValueError"""
        with pytest.raises(ValueError, match="Invalid establishment year"):
            School(
                name="Test School",
                address="123 Main Street",
                city="Springfield",
                state="CA",
                zip_code="90210",
                phone_number="555-0123",
                email="admin@test.edu",
                principal_name="John Smith",
                established_year=1799
            )

    def test_school_creation_invalid_establishment_year_future_raises_error(self):
        """Test that establishment year in future raises ValueError"""
        future_year = datetime.now().year + 1
        with pytest.raises(ValueError, match="Invalid establishment year"):
            School(
                name="Test School",
                address="123 Main Street",
                city="Springfield",
                state="CA",
                zip_code="90210",
                phone_number="555-0123",
                email="admin@test.edu",
                principal_name="John Smith",
                established_year=future_year
            )

    def test_school_creation_short_zip_code_raises_error(self):
        """Test that short zip code raises ValueError"""
        with pytest.raises(ValueError, match="Valid zip code is required"):
            School(
                name="Test School",
                address="123 Main Street",
                city="Springfield",
                state="CA",
                zip_code="12",  # Too short
                phone_number="555-0123",
                email="admin@test.edu",
                principal_name="John Smith",
                established_year=1995
            )

    def test_school_deactivate(self):
        """Test school deactivation"""
        school = School(
            name="Test School",
            address="123 Main Street",
            city="Springfield",
            state="CA",
            zip_code="90210",
            phone_number="555-0123",
            email="admin@test.edu",
            principal_name="John Smith",
            established_year=1995,
            is_active=True
        )
        
        school.deactivate()
        assert school.is_active is False

    def test_school_activate(self):
        """Test school activation"""
        school = School(
            name="Test School",
            address="123 Main Street",
            city="Springfield",
            state="CA",
            zip_code="90210",
            phone_number="555-0123",
            email="admin@test.edu",
            principal_name="John Smith",
            established_year=1995,
            is_active=False
        )
        
        school.activate()
        assert school.is_active is True

    def test_school_update_contact_info_valid(self):
        """Test updating contact information with valid data"""
        school = School(
            name="Test School",
            address="123 Main Street",
            city="Springfield",
            state="CA",
            zip_code="90210",
            phone_number="555-0123",
            email="admin@test.edu",
            principal_name="John Smith",
            established_year=1995
        )
        
        school.update_contact_info("555-9999", "newemail@test.edu")
        assert school.phone_number == "555-9999"
        assert school.email == "newemail@test.edu"

    def test_school_update_contact_info_invalid_email_ignored(self):
        """Test that invalid email is ignored during update"""
        school = School(
            name="Test School",
            address="123 Main Street",
            city="Springfield",
            state="CA",
            zip_code="90210",
            phone_number="555-0123",
            email="admin@test.edu",
            principal_name="John Smith",
            established_year=1995
        )
        
        original_email = school.email
        school.update_contact_info("555-9999", "invalid-email")
        assert school.phone_number == "555-9999"
        assert school.email == original_email  # Should remain unchanged

    def test_school_update_principal(self):
        """Test updating principal name"""
        school = School(
            name="Test School",
            address="123 Main Street",
            city="Springfield",
            state="CA",
            zip_code="90210",
            phone_number="555-0123",
            email="admin@test.edu",
            principal_name="John Smith",
            established_year=1995
        )
        
        school.update_principal("Jane Doe")
        assert school.principal_name == "Jane Doe"

    def test_school_update_principal_empty_ignored(self):
        """Test that empty principal name is ignored"""
        school = School(
            name="Test School",
            address="123 Main Street",
            city="Springfield",
            state="CA",
            zip_code="90210",
            phone_number="555-0123",
            email="admin@test.edu",
            principal_name="John Smith",
            established_year=1995
        )
        
        original_principal = school.principal_name
        school.update_principal("   ")  # Empty after strip
        assert school.principal_name == original_principal

    def test_school_update_method(self):
        """Test the update method returns new instance with updated fields"""
        school = School(
            name="Test School",
            address="123 Main Street",
            city="Springfield",
            state="CA",
            zip_code="90210",
            phone_number="555-0123",
            email="admin@test.edu",
            principal_name="John Smith",
            established_year=1995
        )
        
        updated_school = school.update(
            name="Updated School",
            principal_name="Jane Doe",
            is_active=False
        )
        
        # Original school should remain unchanged
        assert school.name == "Test School"
        assert school.principal_name == "John Smith"
        assert school.is_active is True
        
        # Updated school should have new values
        assert updated_school.name == "Updated School"
        assert updated_school.principal_name == "Jane Doe"
        assert updated_school.is_active is False
        assert updated_school.address == school.address  # Unchanged fields preserved
        assert updated_school.updated_at is not None  # Should be set to current time

    def test_school_boundary_values(self):
        """Test boundary values for validation"""
        # Test minimum valid establishment year
        school_1800 = School(
            name="Historic School",
            address="123 Main Street",
            city="Springfield",
            state="CA",
            zip_code="90210",
            phone_number="555-0123",
            email="admin@historic.edu",
            principal_name="John Smith",
            established_year=1800
        )
        assert school_1800.established_year == 1800
        
        # Test current year
        current_year = datetime.now().year
        school_current = School(
            name="New School",
            address="123 Main Street",
            city="Springfield",
            state="CA",
            zip_code="90210",
            phone_number="555-0123",
            email="admin@new.edu",
            principal_name="John Smith",
            established_year=current_year
        )
        assert school_current.established_year == current_year
        
        # Test minimum valid zip code length
        school_min_zip = School(
            name="Min Zip School",
            address="123 Main Street",
            city="Springfield",
            state="CA",
            zip_code="123",  # Minimum length
            phone_number="555-0123",
            email="admin@minzip.edu",
            principal_name="John Smith",
            established_year=1995
        )
        assert school_min_zip.zip_code == "123"
