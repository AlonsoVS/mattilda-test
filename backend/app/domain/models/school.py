from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class School:
    """Pure domain model for School"""
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone_number: str
    email: str
    principal_name: str
    established_year: int
    is_active: bool = True
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate business rules"""
        if not self.name.strip():
            raise ValueError("School name cannot be empty")
        if not self.address.strip():
            raise ValueError("Address cannot be empty")
        if not self.city.strip():
            raise ValueError("City cannot be empty")
        if not self.state.strip():
            raise ValueError("State cannot be empty")
        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")
        if self.established_year < 1800 or self.established_year > datetime.now().year:
            raise ValueError("Invalid establishment year")
        if len(self.zip_code) < 3:
            raise ValueError("Valid zip code is required")

    def deactivate(self) -> None:
        """Deactivate the school"""
        self.is_active = False

    def activate(self) -> None:
        """Activate the school"""
        self.is_active = True

    def update_contact_info(self, phone_number: str, email: str) -> None:
        """Update school contact information"""
        if phone_number:
            self.phone_number = phone_number
        if email and "@" in email:
            self.email = email

    def update_principal(self, principal_name: str) -> None:
        """Update principal name"""
        if principal_name.strip():
            self.principal_name = principal_name

    def update(self, **kwargs) -> 'School':
        """Update school fields and return new instance"""
        # Create a new school with updated values
        current_values = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone_number': self.phone_number,
            'email': self.email,
            'principal_name': self.principal_name,
            'established_year': self.established_year,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': datetime.now()
        }
        current_values.update(kwargs)
        return School(**current_values)
