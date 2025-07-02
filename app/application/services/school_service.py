from typing import List, Optional
from app.domain.models.school import School
from app.domain.repositories.school_repository import SchoolRepositoryInterface
from app.domain.repositories.student_repository import StudentRepositoryInterface
from app.domain.repositories.invoice_repository import InvoiceRepositoryInterface
from app.application.dtos.school_dto import (
    SchoolCreateDTO, 
    SchoolUpdateDTO, 
    SchoolResponseDTO, 
    SchoolFilterDTO,
    SchoolAccountStatementDTO,
    StudentFinancialSummaryDTO
)
from app.domain.enums import InvoiceStatus
from app.core.pagination import PaginationParams, PaginatedResponse
from datetime import datetime, date


class SchoolService:
    """Service layer for school operations"""

    def __init__(
        self, 
        school_repository: SchoolRepositoryInterface, 
        student_repository: StudentRepositoryInterface,
        invoice_repository: Optional[InvoiceRepositoryInterface] = None
    ):
        self.school_repository = school_repository
        self.student_repository = student_repository
        self.invoice_repository = invoice_repository

    async def get_all_schools(self, pagination: PaginationParams) -> PaginatedResponse[SchoolResponseDTO]:
        """Get all schools with pagination"""
        schools, total = await self.school_repository.get_all(pagination.offset, pagination.limit)
        school_dtos = []
        for school in schools:
            dto = await self._to_response_dto(school)
            school_dtos.append(dto)
        return PaginatedResponse.create(school_dtos, total, pagination)

    async def get_schools_with_filters(self, filters: SchoolFilterDTO, pagination: PaginationParams) -> PaginatedResponse[SchoolResponseDTO]:
        """Get schools with flexible filtering and pagination"""
        # Convert DTO to dict, excluding None values
        filter_dict = {k: v for k, v in filters.model_dump().items() if v is not None}
        
        schools, total = await self.school_repository.get_with_filters(filter_dict, pagination.offset, pagination.limit)
        school_dtos = []
        for school in schools:
            dto = await self._to_response_dto(school)
            school_dtos.append(dto)
        return PaginatedResponse.create(school_dtos, total, pagination)

    async def get_school_by_id(self, school_id: int) -> Optional[SchoolResponseDTO]:
        """Get school by ID"""
        school = await self.school_repository.get_by_id(school_id)
        if school:
            return await self._to_response_dto(school)
        return None

    async def create_school(self, school_data: SchoolCreateDTO) -> SchoolResponseDTO:
        """Create a new school"""
        school = School(
            name=school_data.name,
            address=school_data.address,
            city=school_data.city,
            state=school_data.state,
            zip_code=school_data.zip_code,
            phone_number=school_data.phone or "",
            email=school_data.email or "",
            principal_name=school_data.principal or "",
            established_year=getattr(school_data, "established_year", None) or datetime.now().year,
            is_active=school_data.is_active
        )
        created_school = await self.school_repository.create(school)
        return await self._to_response_dto(created_school)

    async def update_school(self, school_id: int, school_data: SchoolUpdateDTO) -> Optional[SchoolResponseDTO]:
        """Update an existing school"""
        school = await self.school_repository.get_by_id(school_id)
        if not school:
            return None

        # Map DTO fields to domain model fields
        update_data = {}
        dto_data = school_data.model_dump(exclude_unset=True)
        
        if 'phone' in dto_data:
            update_data['phone_number'] = dto_data['phone']
        if 'principal' in dto_data:
            update_data['principal_name'] = dto_data['principal']
        if 'name' in dto_data:
            update_data['name'] = dto_data['name']
        if 'address' in dto_data:
            update_data['address'] = dto_data['address']
        if 'city' in dto_data:
            update_data['city'] = dto_data['city']
        if 'state' in dto_data:
            update_data['state'] = dto_data['state']
        if 'zip_code' in dto_data:
            update_data['zip_code'] = dto_data['zip_code']
        if 'email' in dto_data:
            update_data['email'] = dto_data['email']
        if 'is_active' in dto_data:
            update_data['is_active'] = dto_data['is_active']

        updated_school = school.update(**update_data)
        updated_school = await self.school_repository.update(updated_school)
        return await self._to_response_dto(updated_school)

    async def delete_school(self, school_id: int) -> bool:
        """Delete a school"""
        return await self.school_repository.delete(school_id)

    async def get_school_account_statement(
        self, 
        school_id: int, 
        date_from: Optional[date] = None, 
        date_to: Optional[date] = None
    ) -> Optional[SchoolAccountStatementDTO]:
        """Generate a comprehensive account statement for a school including all students"""
        if not self.invoice_repository:
            raise ValueError("Invoice repository is required for account statements")
        
        # Get school details
        school = await self.school_repository.get_by_id(school_id)
        if not school:
            return None
        
        # Set default date range if not provided
        if not date_from:
            date_from = date(datetime.now().year, 1, 1)  # Beginning of current year
        if not date_to:
            date_to = date.today()
        
        # Get all students for this school
        all_students, _ = await self.student_repository.get_with_filters(
            {'school_id': school_id}, 0, 1000
        )
        
        # Initialize aggregated totals
        total_charges = 0.0
        total_payments = 0.0
        pending_amount = 0.0
        paid_amount = 0.0
        overdue_amount = 0.0
        total_invoices = 0
        pending_invoices_count = 0
        paid_invoices_count = 0
        overdue_invoices_count = 0
        
        student_summaries = []
        students_with_invoices = 0
        students_with_balance = 0
        students_overdue = 0
        
        current_date = date.today()
        
        # Process each student
        for student in all_students:
            # Get student invoices in date range
            filter_dict = {
                'student_id': student.id,
                'invoice_date_from': date_from,
                'invoice_date_to': date_to
            }
            student_invoices, _ = await self.invoice_repository.get_with_filters(filter_dict, 0, 1000)
            
            # Calculate student financial summary
            student_charges = 0.0
            student_payments = 0.0
            student_pending = 0.0
            student_paid = 0.0
            student_overdue = 0.0
            student_overdue_count = 0
            
            for invoice in student_invoices:
                student_charges += invoice.total_amount
                total_charges += invoice.total_amount
                total_invoices += 1
                
                if invoice.status == InvoiceStatus.PAID:
                    student_payments += invoice.total_amount
                    student_paid += invoice.total_amount
                    total_payments += invoice.total_amount
                    paid_amount += invoice.total_amount
                    paid_invoices_count += 1
                elif invoice.status == InvoiceStatus.PENDING:
                    if invoice.due_date < current_date:
                        student_overdue += invoice.total_amount
                        overdue_amount += invoice.total_amount
                        overdue_invoices_count += 1
                        student_overdue_count += 1
                    else:
                        student_pending += invoice.total_amount
                        pending_amount += invoice.total_amount
                        pending_invoices_count += 1
                else:  # Other statuses
                    student_pending += invoice.total_amount
                    pending_amount += invoice.total_amount
                    pending_invoices_count += 1
            
            student_balance = student_charges - student_payments
            
            # Only include students with invoices
            if student_invoices:
                students_with_invoices += 1
                
                if student_balance > 0:
                    students_with_balance += 1
                
                if student_overdue_count > 0:
                    students_overdue += 1
                
                student_summary = StudentFinancialSummaryDTO(
                    student_id=student.id or 0,
                    student_name=f"{student.first_name} {student.last_name}",
                    total_charges=student_charges,
                    total_payments=student_payments,
                    current_balance=student_balance,
                    pending_amount=student_pending,
                    paid_amount=student_paid,
                    overdue_amount=student_overdue,
                    total_invoices=len(student_invoices),
                    overdue_invoices=student_overdue_count
                )
                student_summaries.append(student_summary)
        
        # Sort students by balance (highest first)
        student_summaries.sort(key=lambda x: x.current_balance, reverse=True)
        
        # Find top statistics
        highest_balance_student = None
        most_overdue_student = None
        
        if student_summaries:
            highest_balance_student = max(student_summaries, key=lambda x: x.current_balance)
            overdue_students = [s for s in student_summaries if s.overdue_amount > 0]
            if overdue_students:
                most_overdue_student = max(overdue_students, key=lambda x: x.overdue_amount)
        
        current_balance = total_charges - total_payments
        
        return SchoolAccountStatementDTO(
            school_id=school_id,
            school_name=school.name,
            school_address=f"{school.address}, {school.city}, {school.state} {school.zip_code}",
            statement_period_from=date_from,
            statement_period_to=date_to,
            total_charges=total_charges,
            total_payments=total_payments,
            current_balance=current_balance,
            pending_amount=pending_amount,
            paid_amount=paid_amount,
            overdue_amount=overdue_amount,
            total_students=len(all_students),
            students_with_invoices=students_with_invoices,
            students_with_balance=students_with_balance,
            students_overdue=students_overdue,
            total_invoices=total_invoices,
            pending_invoices=pending_invoices_count,
            paid_invoices=paid_invoices_count,
            overdue_invoices=overdue_invoices_count,
            student_summaries=student_summaries,
            highest_balance_student=highest_balance_student,
            most_overdue_student=most_overdue_student,
            generated_at=date.today()
        )

    async def _to_response_dto(self, school: School) -> SchoolResponseDTO:
        """Convert domain model to response DTO"""
        # Get student count for this school
        student_count = await self.student_repository.count_by_school_id(school.id or 0)
        
        return SchoolResponseDTO(
            id=school.id or 0,  # Handle None case
            name=school.name,
            address=school.address,
            city=school.city,
            state=school.state,
            zip_code=school.zip_code,
            phone=school.phone_number,
            email=school.email,
            principal=school.principal_name,
            student_count=student_count,
            is_active=school.is_active
        )
