from typing import Generic, List, TypeVar, Optional
from pydantic import BaseModel, model_validator
from math import ceil

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = 1
    size: int = 10
    
    @model_validator(mode='after')
    def validate_pagination(self):
        """Validate pagination parameters"""
        if self.page < 1:
            self.page = 1
        if self.size < 1:
            self.size = 10
        if self.size > 100:  # Max items per page
            self.size = 100
        return self
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries"""
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        """Get limit for database queries"""
        return self.size


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_previous: bool
    
    @classmethod
    def create(
        cls, 
        items: List[T], 
        total: int, 
        pagination: PaginationParams
    ) -> "PaginatedResponse[T]":
        """Create paginated response"""
        pages = ceil(total / pagination.size) if total > 0 else 1
        
        return cls(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=pages,
            has_next=pagination.page < pages,
            has_previous=pagination.page > 1
        )
