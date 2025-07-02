import pytest
from datetime import datetime, date
from app.domain.models.student import Student


class TestStudentDomainModel:
    """Test suite for Student domain model"""

    def test_student_creation_valid(self):
        """Test successful student creation with valid data"""
        birth_date = date(2005, 5, 15)
        enrollment_date = date(2023, 9, 1)
        
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            phone_number="555-0123",
            date_of_birth=birth_date,
            grade_level=10,
            school_id=1,
            enrollment_date=enrollment_date,
            address="123 Main Street, Springfield, CA"
        )
        
        assert student.first_name == "John"
        assert student.last_name == "Doe"
        assert student.email == "john.doe@email.com"
        assert student.phone_number == "555-0123"
        assert student.date_of_birth == birth_date
        assert student.grade_level == 10
        assert student.school_id == 1
        assert student.enrollment_date == enrollment_date
        assert student.address == "123 Main Street, Springfield, CA"
        assert student.is_active is True  # Default value
        assert student.id is None  # Default value
        assert student.created_at is None  # Default value
        assert student.updated_at is None  # Default value

    def test_student_creation_with_optional_fields(self):
        """Test student creation with optional fields set"""
        current_time = datetime.now()
        birth_date = date(2005, 5, 15)
        enrollment_date = date(2023, 9, 1)
        
        student = Student(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@email.com",
            phone_number="555-9999",
            date_of_birth=birth_date,
            grade_level=11,
            school_id=2,
            enrollment_date=enrollment_date,
            address="456 Oak Ave, Testville, TX",
            is_active=False,
            id=1,
            created_at=current_time,
            updated_at=current_time
        )
        
        assert student.is_active is False
        assert student.id == 1
        assert student.created_at == current_time
        assert student.updated_at == current_time

    def test_student_creation_empty_first_name_raises_error(self):
        """Test that empty first name raises ValueError"""
        with pytest.raises(ValueError, match="First name cannot be empty"):
            Student(
                first_name="   ",  # Empty after strip
                last_name="Doe",
                email="john.doe@email.com",
                phone_number="555-0123",
                date_of_birth=date(2005, 5, 15),
                grade_level=10,
                school_id=1,
                enrollment_date=date(2023, 9, 1),
                address="123 Main Street"
            )

    def test_student_creation_empty_last_name_raises_error(self):
        """Test that empty last name raises ValueError"""
        with pytest.raises(ValueError, match="Last name cannot be empty"):
            Student(
                first_name="John",
                last_name="",
                email="john.doe@email.com",
                phone_number="555-0123",
                date_of_birth=date(2005, 5, 15),
                grade_level=10,
                school_id=1,
                enrollment_date=date(2023, 9, 1),
                address="123 Main Street"
            )

    def test_student_creation_invalid_email_raises_error(self):
        """Test that invalid email raises ValueError"""
        with pytest.raises(ValueError, match="Valid email is required"):
            Student(
                first_name="John",
                last_name="Doe",
                email="invalid-email",
                phone_number="555-0123",
                date_of_birth=date(2005, 5, 15),
                grade_level=10,
                school_id=1,
                enrollment_date=date(2023, 9, 1),
                address="123 Main Street"
            )

    def test_student_creation_empty_email_raises_error(self):
        """Test that empty email raises ValueError"""
        with pytest.raises(ValueError, match="Valid email is required"):
            Student(
                first_name="John",
                last_name="Doe",
                email="",
                phone_number="555-0123",
                date_of_birth=date(2005, 5, 15),
                grade_level=10,
                school_id=1,
                enrollment_date=date(2023, 9, 1),
                address="123 Main Street"
            )

    def test_student_creation_invalid_grade_level_too_low_raises_error(self):
        """Test that grade level below 1 raises ValueError"""
        with pytest.raises(ValueError, match="Grade level must be between 1 and 12"):
            Student(
                first_name="John",
                last_name="Doe",
                email="john.doe@email.com",
                phone_number="555-0123",
                date_of_birth=date(2005, 5, 15),
                grade_level=0,
                school_id=1,
                enrollment_date=date(2023, 9, 1),
                address="123 Main Street"
            )

    def test_student_creation_invalid_grade_level_too_high_raises_error(self):
        """Test that grade level above 12 raises ValueError"""
        with pytest.raises(ValueError, match="Grade level must be between 1 and 12"):
            Student(
                first_name="John",
                last_name="Doe",
                email="john.doe@email.com",
                phone_number="555-0123",
                date_of_birth=date(2005, 5, 15),
                grade_level=13,
                school_id=1,
                enrollment_date=date(2023, 9, 1),
                address="123 Main Street"
            )

    def test_student_creation_future_enrollment_date_raises_error(self):
        """Test that enrollment date in future raises ValueError"""
        future_date = date.today() + date.resolution
        with pytest.raises(ValueError, match="Enrollment date cannot be in the future"):
            Student(
                first_name="John",
                last_name="Doe",
                email="john.doe@email.com",
                phone_number="555-0123",
                date_of_birth=date(2005, 5, 15),
                grade_level=10,
                school_id=1,
                enrollment_date=future_date,
                address="123 Main Street"
            )

    def test_student_creation_birth_date_today_or_future_raises_error(self):
        """Test that birth date today or in future raises ValueError"""
        with pytest.raises(ValueError, match="Date of birth must be in the past"):
            Student(
                first_name="John",
                last_name="Doe",
                email="john.doe@email.com",
                phone_number="555-0123",
                date_of_birth=date.today(),
                grade_level=10,
                school_id=1,
                enrollment_date=date(2023, 9, 1),
                address="123 Main Street"
            )

    def test_student_full_name_property(self):
        """Test full_name property returns correct concatenation"""
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            phone_number="555-0123",
            date_of_birth=date(2005, 5, 15),
            grade_level=10,
            school_id=1,
            enrollment_date=date(2023, 9, 1),
            address="123 Main Street"
        )
        
        assert student.full_name == "John Doe"

    def test_student_age_property(self):
        """Test age property calculates correctly"""
        # Create a student born 18 years ago
        birth_date = date(2005, 5, 15)
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            phone_number="555-0123",
            date_of_birth=birth_date,
            grade_level=10,
            school_id=1,
            enrollment_date=date(2023, 9, 1),
            address="123 Main Street"
        )
        
        # Calculate expected age
        today = date.today()
        expected_age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
        
        assert student.age == expected_age

    def test_student_age_property_birthday_not_yet_this_year(self):
        """Test age calculation when birthday hasn't occurred this year"""
        # Create a birth date that hasn't occurred this year yet
        today = date.today()
        birth_date = date(today.year - 18, today.month + 1 if today.month < 12 else 1, today.day)
        
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            phone_number="555-0123",
            date_of_birth=birth_date,
            grade_level=10,
            school_id=1,
            enrollment_date=date(2023, 9, 1),
            address="123 Main Street"
        )
        
        # Should be 17, not 18, since birthday hasn't occurred
        expected_age = 17
        assert student.age == expected_age

    def test_student_deactivate(self):
        """Test student deactivation"""
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            phone_number="555-0123",
            date_of_birth=date(2005, 5, 15),
            grade_level=10,
            school_id=1,
            enrollment_date=date(2023, 9, 1),
            address="123 Main Street",
            is_active=True
        )
        
        student.deactivate()
        assert student.is_active is False

    def test_student_activate(self):
        """Test student activation"""
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            phone_number="555-0123",
            date_of_birth=date(2005, 5, 15),
            grade_level=10,
            school_id=1,
            enrollment_date=date(2023, 9, 1),
            address="123 Main Street",
            is_active=False
        )
        
        student.activate()
        assert student.is_active is True

    def test_student_update_contact_info_valid(self):
        """Test updating contact information with valid data"""
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            phone_number="555-0123",
            date_of_birth=date(2005, 5, 15),
            grade_level=10,
            school_id=1,
            enrollment_date=date(2023, 9, 1),
            address="123 Main Street"
        )
        
        student.update_contact_info("newemail@example.com", "555-9999", "456 Oak Ave")
        assert student.email == "newemail@example.com"
        assert student.phone_number == "555-9999"
        assert student.address == "456 Oak Ave"

    def test_student_update_contact_info_invalid_email_ignored(self):
        """Test that invalid email is ignored during update"""
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            phone_number="555-0123",
            date_of_birth=date(2005, 5, 15),
            grade_level=10,
            school_id=1,
            enrollment_date=date(2023, 9, 1),
            address="123 Main Street"
        )
        
        original_email = student.email
        student.update_contact_info("invalid-email", "555-9999", "456 Oak Ave")
        assert student.email == original_email  # Should remain unchanged
        assert student.phone_number == "555-9999"
        assert student.address == "456 Oak Ave"

    def test_student_update_method(self):
        """Test the update method returns new instance with updated fields"""
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            phone_number="555-0123",
            date_of_birth=date(2005, 5, 15),
            grade_level=10,
            school_id=1,
            enrollment_date=date(2023, 9, 1),
            address="123 Main Street"
        )
        
        updated_student = student.update(
            first_name="Johnny",
            grade_level=11,
            is_active=False
        )
        
        # Original student should remain unchanged
        assert student.first_name == "John"
        assert student.grade_level == 10
        assert student.is_active is True
        
        # Updated student should have new values
        assert updated_student.first_name == "Johnny"
        assert updated_student.grade_level == 11
        assert updated_student.is_active is False
        assert updated_student.last_name == student.last_name  # Unchanged fields preserved
        assert updated_student.updated_at is not None  # Should be set to current time

    def test_student_boundary_values(self):
        """Test boundary values for validation"""
        # Test minimum valid grade level
        student_grade_1 = Student(
            first_name="Young",
            last_name="Student",
            email="young@student.com",
            phone_number="555-0123",
            date_of_birth=date(2015, 5, 15),
            grade_level=1,
            school_id=1,
            enrollment_date=date(2023, 9, 1),
            address="123 Main Street"
        )
        assert student_grade_1.grade_level == 1
        
        # Test maximum valid grade level
        student_grade_12 = Student(
            first_name="Senior",
            last_name="Student",
            email="senior@student.com",
            phone_number="555-0123",
            date_of_birth=date(2005, 5, 15),
            grade_level=12,
            school_id=1,
            enrollment_date=date(2023, 9, 1),
            address="123 Main Street"
        )
        assert student_grade_12.grade_level == 12
        
        # Test enrollment date today (boundary case)
        student_today = Student(
            first_name="Today",
            last_name="Student",
            email="today@student.com",
            phone_number="555-0123",
            date_of_birth=date(2005, 5, 15),
            grade_level=10,
            school_id=1,
            enrollment_date=date.today(),
            address="123 Main Street"
        )
        assert student_today.enrollment_date == date.today()
