from pydantic import BaseModel
from typing import Optional
from datetime import date


class StudentFilterDTO(BaseModel):
    """DTO for filtering students"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    grade_level: Optional[int] = None
    school_id: Optional[int] = None
    enrollment_date: Optional[date] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class StudentCreateDTO(BaseModel):
    """DTO for creating a student"""
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: date
    grade_level: int
    school_id: int
    enrollment_date: date
    address: str
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
    enrollment_date: Optional[date] = None
    address: Optional[str] = None
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
    enrollment_date: date
    address: str
    is_active: bool

    class Config:
        from_attributes = True
