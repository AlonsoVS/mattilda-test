from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

school_router = APIRouter(prefix="/schools", tags=["schools"])


class School(BaseModel):
    id: Optional[int] = None
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


class SchoolCreate(BaseModel):
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


class SchoolUpdate(BaseModel):
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


# In-memory storage for demonstration (replace with database in production)
schools_db = [
    School(
        id=1,
        name="Lincoln Elementary School",
        address="123 Main Street",
        city="Springfield",
        state="Illinois",
        zip_code="62701",
        phone="(217) 555-0101",
        email="info@lincoln.edu",
        principal="Sarah Johnson",
        student_count=450,
        is_active=True
    ),
    School(
        id=2,
        name="Washington High School",
        address="456 Oak Avenue",
        city="Madison",
        state="Wisconsin",
        zip_code="53703",
        phone="(608) 555-0202",
        email="admin@washington.edu",
        principal="Michael Chen",
        student_count=1200,
        is_active=True
    ),
    School(
        id=3,
        name="Roosevelt Middle School",
        address="789 Elm Street",
        city="Portland",
        state="Oregon",
        zip_code="97201",
        phone="(503) 555-0303",
        email="contact@roosevelt.edu",
        principal="Jennifer Davis",
        student_count=680,
        is_active=True
    ),
    School(
        id=4,
        name="Jefferson Academy",
        address="321 Pine Road",
        city="Austin",
        state="Texas",
        zip_code="73301",
        phone="(512) 555-0404",
        email="office@jefferson.edu",
        principal="Robert Martinez",
        student_count=890,
        is_active=True
    ),
    School(
        id=5,
        name="Franklin Preparatory School",
        address="654 Cedar Lane",
        city="Denver",
        state="Colorado",
        zip_code="80202",
        phone="(303) 555-0505",
        email="hello@franklin.edu",
        principal="Lisa Thompson",
        student_count=320,
        is_active=True
    ),
    School(
        id=6,
        name="Adams Charter School",
        address="987 Birch Boulevard",
        city="Phoenix",
        state="Arizona",
        zip_code="85001",
        phone="(602) 555-0606",
        email="info@adams.edu",
        principal="David Wilson",
        student_count=540,
        is_active=True
    ),
    School(
        id=7,
        name="Hamilton Institute",
        address="147 Maple Drive",
        city="Seattle",
        state="Washington",
        zip_code="98101",
        phone="(206) 555-0707",
        email="admin@hamilton.edu",
        principal="Amanda Garcia",
        student_count=750,
        is_active=False
    ),
    School(
        id=8,
        name="Madison Community School",
        address="258 Walnut Street",
        city="Madison",
        state="Wisconsin",
        zip_code="53704",
        phone="(608) 555-0808",
        email="contact@madison.edu",
        principal="James Anderson",
        student_count=410,
        is_active=True
    )
]
next_id = 9


@school_router.get("/", response_model=List[School])
async def get_schools():
    """Get all schools"""
    return schools_db


@school_router.get("/{school_id}", response_model=School)
async def get_school(school_id: int):
    """Get a school by ID"""
    school = next((school for school in schools_db if school.id == school_id), None)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


@school_router.post("/", response_model=School)
async def create_school(school: SchoolCreate):
    """Create a new school"""
    global next_id
    new_school = School(id=next_id, **school.dict())
    schools_db.append(new_school)
    next_id += 1
    return new_school


@school_router.put("/{school_id}", response_model=School)
async def update_school(school_id: int, school_update: SchoolUpdate):
    """Update a school by ID"""
    school = next((school for school in schools_db if school.id == school_id), None)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Update only provided fields
    for field, value in school_update.dict(exclude_unset=True).items():
        setattr(school, field, value)
    
    return school


@school_router.delete("/{school_id}")
async def delete_school(school_id: int):
    """Delete a school by ID"""
    global schools_db
    school = next((school for school in schools_db if school.id == school_id), None)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    schools_db = [s for s in schools_db if s.id != school_id]
    return {"message": "School deleted successfully"}


@school_router.get("/search/by-city/{city}", response_model=List[School])
async def get_schools_by_city(city: str):
    """Get schools by city"""
    schools_in_city = [school for school in schools_db if school.city.lower() == city.lower()]
    return schools_in_city


@school_router.get("/search/by-state/{state}", response_model=List[School])
async def get_schools_by_state(state: str):
    """Get schools by state"""
    schools_in_state = [school for school in schools_db if school.state.lower() == state.lower()]
    return schools_in_state
