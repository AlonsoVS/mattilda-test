from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date

student_router = APIRouter(prefix="/students", tags=["students"])


class Student(BaseModel):
    id: Optional[int] = None
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


class StudentCreate(BaseModel):
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


class StudentUpdate(BaseModel):
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


# In-memory storage for demonstration (replace with database in production)
students_db = [
    Student(
        id=1,
        first_name="Emma",
        last_name="Johnson",
        email="emma.johnson@email.com",
        phone="(217) 555-1001",
        date_of_birth=date(2010, 3, 15),
        grade_level=8,
        school_id=1,
        student_id_number="LIN001",
        enrollment_date=date(2023, 8, 15),
        guardian_name="Mary Johnson",
        guardian_phone="(217) 555-1000",
        guardian_email="mary.johnson@email.com",
        address="456 School Street",
        city="Springfield",
        state="Illinois",
        zip_code="62701",
        is_active=True
    ),
    Student(
        id=2,
        first_name="Liam",
        last_name="Chen",
        email="liam.chen@email.com",
        phone="(608) 555-2001",
        date_of_birth=date(2006, 7, 22),
        grade_level=12,
        school_id=2,
        student_id_number="WAS002",
        enrollment_date=date(2022, 8, 20),
        guardian_name="David Chen",
        guardian_phone="(608) 555-2000",
        guardian_email="david.chen@email.com",
        address="789 Student Avenue",
        city="Madison",
        state="Wisconsin",
        zip_code="53703",
        is_active=True
    ),
    Student(
        id=3,
        first_name="Sophia",
        last_name="Davis",
        email="sophia.davis@email.com",
        phone="(503) 555-3001",
        date_of_birth=date(2011, 11, 8),
        grade_level=7,
        school_id=3,
        student_id_number="ROO003",
        enrollment_date=date(2023, 9, 1),
        guardian_name="Jennifer Davis",
        guardian_phone="(503) 555-3000",
        guardian_email="jennifer.davis@email.com",
        address="321 Learning Lane",
        city="Portland",
        state="Oregon",
        zip_code="97201",
        is_active=True
    ),
    Student(
        id=4,
        first_name="Noah",
        last_name="Martinez",
        email="noah.martinez@email.com",
        phone="(512) 555-4001",
        date_of_birth=date(2008, 1, 30),
        grade_level=10,
        school_id=4,
        student_id_number="JEF004",
        enrollment_date=date(2023, 8, 25),
        guardian_name="Roberto Martinez",
        guardian_phone="(512) 555-4000",
        guardian_email="roberto.martinez@email.com",
        address="654 Education Drive",
        city="Austin",
        state="Texas",
        zip_code="73301",
        is_active=True
    ),
    Student(
        id=5,
        first_name="Olivia",
        last_name="Thompson",
        email="olivia.thompson@email.com",
        phone="(303) 555-5001",
        date_of_birth=date(2009, 9, 12),
        grade_level=9,
        school_id=5,
        student_id_number="FRA005",
        enrollment_date=date(2023, 8, 30),
        guardian_name="Lisa Thompson",
        guardian_phone="(303) 555-5000",
        guardian_email="lisa.thompson@email.com",
        address="987 Academy Road",
        city="Denver",
        state="Colorado",
        zip_code="80202",
        is_active=True
    ),
    Student(
        id=6,
        first_name="Ethan",
        last_name="Wilson",
        email="ethan.wilson@email.com",
        phone="(602) 555-6001",
        date_of_birth=date(2012, 5, 18),
        grade_level=6,
        school_id=6,
        student_id_number="ADA006",
        enrollment_date=date(2023, 8, 15),
        guardian_name="David Wilson",
        guardian_phone="(602) 555-6000",
        guardian_email="david.wilson@email.com",
        address="147 Charter Boulevard",
        city="Phoenix",
        state="Arizona",
        zip_code="85001",
        is_active=True
    ),
    Student(
        id=7,
        first_name="Ava",
        last_name="Garcia",
        email="ava.garcia@email.com",
        phone="(206) 555-7001",
        date_of_birth=date(2007, 12, 3),
        grade_level=11,
        school_id=7,
        student_id_number="HAM007",
        enrollment_date=date(2022, 9, 5),
        guardian_name="Amanda Garcia",
        guardian_phone="(206) 555-7000",
        guardian_email="amanda.garcia@email.com",
        address="258 Institute Street",
        city="Seattle",
        state="Washington",
        zip_code="98101",
        is_active=False
    ),
    Student(
        id=8,
        first_name="Mason",
        last_name="Anderson",
        email="mason.anderson@email.com",
        phone="(608) 555-8001",
        date_of_birth=date(2010, 4, 25),
        grade_level=8,
        school_id=8,
        student_id_number="MAD008",
        enrollment_date=date(2023, 8, 20),
        guardian_name="James Anderson",
        guardian_phone="(608) 555-8000",
        guardian_email="james.anderson@email.com",
        address="369 Community Circle",
        city="Madison",
        state="Wisconsin",
        zip_code="53704",
        is_active=True
    )
]
next_student_id = 9


@student_router.get("/", response_model=List[Student])
async def get_students():
    """Get all students"""
    return students_db


@student_router.get("/{student_id}", response_model=Student)
async def get_student(student_id: int):
    """Get a student by ID"""
    student = next((student for student in students_db if student.id == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@student_router.post("/", response_model=Student)
async def create_student(student: StudentCreate):
    """Create a new student"""
    global next_student_id
    new_student = Student(id=next_student_id, **student.dict())
    students_db.append(new_student)
    next_student_id += 1
    return new_student


@student_router.put("/{student_id}", response_model=Student)
async def update_student(student_id: int, student_update: StudentUpdate):
    """Update a student by ID"""
    student = next((student for student in students_db if student.id == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Update only provided fields
    for field, value in student_update.dict(exclude_unset=True).items():
        setattr(student, field, value)
    
    return student


@student_router.delete("/{student_id}")
async def delete_student(student_id: int):
    """Delete a student by ID"""
    global students_db
    student = next((student for student in students_db if student.id == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    students_db = [s for s in students_db if s.id != student_id]
    return {"message": "Student deleted successfully"}


@student_router.get("/school/{school_id}", response_model=List[Student])
async def get_students_by_school(school_id: int):
    """Get students by school ID"""
    students_in_school = [student for student in students_db if student.school_id == school_id]
    return students_in_school


@student_router.get("/grade/{grade_level}", response_model=List[Student])
async def get_students_by_grade(grade_level: int):
    """Get students by grade level"""
    students_in_grade = [student for student in students_db if student.grade_level == grade_level]
    return students_in_grade


@student_router.get("/search/by-name/{name}", response_model=List[Student])
async def search_students_by_name(name: str):
    """Search students by first or last name"""
    name_lower = name.lower()
    matching_students = [
        student for student in students_db 
        if name_lower in student.first_name.lower() or name_lower in student.last_name.lower()
    ]
    return matching_students
