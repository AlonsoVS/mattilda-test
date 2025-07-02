from typing import List, Optional
from datetime import date, datetime
from app.domain.models.student import Student
from app.domain.repositories.student_repository import StudentRepositoryInterface
from app.domain.repositories.invoice_repository import InvoiceRepositoryInterface
from app.domain.repositories.school_repository import SchoolRepositoryInterface
from app.application.dtos.student_dto import (
    StudentCreateDTO, 
    StudentUpdateDTO, 
    StudentResponseDTO, 
    StudentFilterDTO,
    StudentAccountStatementDTO,
    InvoiceSummaryDTO
)
from app.domain.enums import InvoiceStatus
from app.core.pagination import PaginationParams, PaginatedResponse


class StudentService:
    """Service layer for student operations"""

    def __init__(
        self, 
        student_repository: StudentRepositoryInterface,
        invoice_repository: Optional[InvoiceRepositoryInterface] = None,
        school_repository: Optional[SchoolRepositoryInterface] = None
    ):
        self.student_repository = student_repository
        self.invoice_repository = invoice_repository
        self.school_repository = school_repository

    async def get_all_students(self, pagination: PaginationParams) -> PaginatedResponse[StudentResponseDTO]:
        """Get all students with pagination"""
        students, total = await self.student_repository.get_all(pagination.offset, pagination.limit)
        student_dtos = [self._to_response_dto(student) for student in students]
        return PaginatedResponse.create(student_dtos, total, pagination)

    async def get_students_with_filters(self, filters: StudentFilterDTO, pagination: PaginationParams) -> PaginatedResponse[StudentResponseDTO]:
        """Get students with flexible filtering and pagination"""
        # Convert DTO to dict, excluding None values
        filter_dict = {k: v for k, v in filters.model_dump().items() if v is not None}
        
        students, total = await self.student_repository.get_with_filters(filter_dict, pagination.offset, pagination.limit)
        student_dtos = [self._to_response_dto(student) for student in students]
        return PaginatedResponse.create(student_dtos, total, pagination)

    async def get_student_by_id(self, student_id: int) -> Optional[StudentResponseDTO]:
        """Get student by ID"""
        student = await self.student_repository.get_by_id(student_id)
        if student:
            return self._to_response_dto(student)
        return None

    async def create_student(self, student_data: StudentCreateDTO) -> StudentResponseDTO:
        """Create a new student"""
        student = Student(
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            email=student_data.email or "",
            phone_number=student_data.phone or "",
            date_of_birth=student_data.date_of_birth,
            grade_level=student_data.grade_level,
            school_id=student_data.school_id,
            enrollment_date=student_data.enrollment_date,
            address=student_data.address,
            is_active=student_data.is_active
        )
        created_student = await self.student_repository.create(student)
        return self._to_response_dto(created_student)

    async def update_student(self, student_id: int, student_data: StudentUpdateDTO) -> Optional[StudentResponseDTO]:
        """Update an existing student"""
        student = await self.student_repository.get_by_id(student_id)
        if not student:
            return None

        # Map DTO fields to domain model fields
        update_data = {}
        dto_data = student_data.model_dump(exclude_unset=True)
        
        if 'phone' in dto_data:
            update_data['phone_number'] = dto_data['phone']
        
        # Map other fields directly
        for field in ['first_name', 'last_name', 'email', 'date_of_birth', 'grade_level', 
                     'school_id', 'enrollment_date', 'address', 'is_active']:
            if field in dto_data:
                update_data[field] = dto_data[field]

        updated_student = student.update(**update_data)
        updated_student = await self.student_repository.update(updated_student)
        return self._to_response_dto(updated_student)

    async def delete_student(self, student_id: int) -> bool:
        """Delete a student"""
        return await self.student_repository.delete(student_id)

    async def get_student_account_statement(
        self, 
        student_id: int, 
        date_from: Optional[date] = None, 
        date_to: Optional[date] = None
    ) -> Optional[StudentAccountStatementDTO]:
        """Generate a comprehensive account statement for a student"""
        if not self.invoice_repository or not self.school_repository:
            raise ValueError("Invoice and School repositories are required for account statements")
        
        # Get student details
        student = await self.student_repository.get_by_id(student_id)
        if not student:
            return None
        
        # Get school details
        school = await self.school_repository.get_by_id(student.school_id)
        school_name = school.name if school else "Unknown School"
        
        # Set default date range if not provided
        if not date_from:
            date_from = date(datetime.now().year, 1, 1)  # Beginning of current year
        if not date_to:
            date_to = date.today()
        
        # Get all invoices for the student in the date range
        filter_dict = {
            'student_id': student_id,
            'invoice_date_from': date_from,
            'invoice_date_to': date_to
        }
        all_invoices, _ = await self.invoice_repository.get_with_filters(filter_dict, 0, 1000)
        
        # Categorize invoices
        pending_invoices = []
        paid_invoices = []
        overdue_invoices = []
        
        total_charges = 0.0
        total_payments = 0.0
        pending_amount = 0.0
        paid_amount = 0.0
        overdue_amount = 0.0
        
        current_date = date.today()
        
        for invoice in all_invoices:
            invoice_summary = InvoiceSummaryDTO(
                id=invoice.id or 0,
                invoice_number=invoice.invoice_number,
                description=invoice.description,
                invoice_date=invoice.invoice_date,
                due_date=invoice.due_date,
                amount=invoice.amount,
                tax_amount=invoice.tax_amount,
                total_amount=invoice.total_amount,
                status=invoice.status.value,
                payment_date=invoice.payment_date,
                payment_method=invoice.payment_method.value if invoice.payment_method else None
            )
            
            total_charges += invoice.total_amount
            
            if invoice.status == InvoiceStatus.PAID:
                paid_invoices.append(invoice_summary)
                paid_amount += invoice.total_amount
                total_payments += invoice.total_amount
            elif invoice.status == InvoiceStatus.PENDING:
                if invoice.due_date < current_date:
                    overdue_invoices.append(invoice_summary)
                    overdue_amount += invoice.total_amount
                else:
                    pending_invoices.append(invoice_summary)
                    pending_amount += invoice.total_amount
            else:  # Other statuses like CANCELLED, etc.
                pending_invoices.append(invoice_summary)
                pending_amount += invoice.total_amount
        
        # Calculate current balance
        current_balance = total_charges - total_payments
        
        return StudentAccountStatementDTO(
            student_id=student_id,
            student_name=f"{student.first_name} {student.last_name}",
            school_name=school_name,
            statement_period_from=date_from,
            statement_period_to=date_to,
            total_charges=total_charges,
            total_payments=total_payments,
            current_balance=current_balance,
            pending_invoices=pending_invoices,
            paid_invoices=paid_invoices,
            overdue_invoices=overdue_invoices,
            total_invoices=len(all_invoices),
            pending_amount=pending_amount,
            paid_amount=paid_amount,
            overdue_amount=overdue_amount,
            generated_at=date.today()
        )

    def _to_response_dto(self, student: Student) -> StudentResponseDTO:
        """Convert domain model to response DTO"""
        return StudentResponseDTO(
            id=student.id or 0,  # Handle None case
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            phone=student.phone_number,
            date_of_birth=student.date_of_birth,
            grade_level=student.grade_level,
            school_id=student.school_id,
            enrollment_date=student.enrollment_date,
            address=student.address,
            is_active=student.is_active
        )
