from pydantic import BaseModel
from typing import Optional
from datetime import date


class SchoolCreateDTO(BaseModel):
    """DTO for creating a school"""
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: Optional[str] = None
    email: Optional[str] = None
    principal: Optional[str] = None
    student_count: Optional[int] = None
    is_active: bool = True


class SchoolUpdateDTO(BaseModel):
    """DTO for updating a school"""
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    principal: Optional[str] = None
    student_count: Optional[int] = None
    is_active: Optional[bool] = None


class SchoolResponseDTO(BaseModel):
    """DTO for school responses"""
    id: int
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: Optional[str] = None
    email: Optional[str] = None
    principal: Optional[str] = None
    student_count: Optional[int] = None
    is_active: bool

    class Config:
        from_attributes = True
