from typing import Optional
from datetime import datetime, date
from dataclasses import dataclass


@dataclass
class Student:
    """Pure domain model for Student"""
    first_name: str
    last_name: str
    email: str
    phone_number: str
    date_of_birth: date
    grade_level: int
    school_id: int
    enrollment_date: date
    address: str
    guardian_name: str
    guardian_phone: str
    is_active: bool = True
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate business rules"""
        if not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")
        if self.grade_level < 1 or self.grade_level > 12:
            raise ValueError("Grade level must be between 1 and 12")
        if self.enrollment_date > date.today():
            raise ValueError("Enrollment date cannot be in the future")
        if self.date_of_birth >= date.today():
            raise ValueError("Date of birth must be in the past")

    @property
    def full_name(self) -> str:
        """Get full name of the student"""
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        """Calculate student's age"""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def deactivate(self) -> None:
        """Deactivate the student"""
        self.is_active = False

    def activate(self) -> None:
        """Activate the student"""
        self.is_active = True

    def update_contact_info(self, email: str, phone_number: str, address: str) -> None:
        """Update student contact information"""
        if email and "@" in email:
            self.email = email
        if phone_number:
            self.phone_number = phone_number
        if address:
            self.address = address

    def update(self, **kwargs) -> 'Student':
        """Update student fields and return new instance"""
        # Create a new student with updated values
        current_values = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'date_of_birth': self.date_of_birth,
            'grade_level': self.grade_level,
            'school_id': self.school_id,
            'enrollment_date': self.enrollment_date,
            'address': self.address,
            'guardian_name': self.guardian_name,
            'guardian_phone': self.guardian_phone,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': datetime.now()
        }
        current_values.update(kwargs)
        return Student(**current_values)
