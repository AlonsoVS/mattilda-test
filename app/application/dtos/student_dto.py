from pydantic import BaseModel
from typing import Optional
from datetime import date


class StudentCreateDTO(BaseModel):
    """DTO for creating a student"""
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: date
    grade_level: int
    school_id: int
    student_id_number: str
    enrollment_date: date
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_email: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    is_active: bool = True


class StudentUpdateDTO(BaseModel):
    """DTO for updating a student"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    grade_level: Optional[int] = None
    school_id: Optional[int] = None
    student_id_number: Optional[str] = None
    enrollment_date: Optional[date] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    is_active: Optional[bool] = None


class StudentResponseDTO(BaseModel):
    """DTO for student responses"""
    id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: date
    grade_level: int
    school_id: int
    student_id_number: str
    enrollment_date: date
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_email: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    is_active: bool

    class Config:
        from_attributes = True
