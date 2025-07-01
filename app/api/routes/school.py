from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select, col
from app.database import get_session
from app.models import School, SchoolCreate, SchoolRead, SchoolUpdate

school_router = APIRouter(prefix="/schools", tags=["schools"])


@school_router.get("/", response_model=List[SchoolRead])
async def get_schools(session: Session = Depends(get_session)):
    """Get all schools"""
    schools = session.exec(select(School)).all()
    return schools


@school_router.get("/{school_id}", response_model=SchoolRead)
async def get_school(school_id: int, session: Session = Depends(get_session)):
    """Get a school by ID"""
    school = session.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


@school_router.post("/", response_model=SchoolRead)
async def create_school(school: SchoolCreate, session: Session = Depends(get_session)):
    """Create a new school"""
    db_school = School.model_validate(school)
    session.add(db_school)
    session.commit()
    session.refresh(db_school)
    return db_school


@school_router.put("/{school_id}", response_model=SchoolRead)
async def update_school(
    school_id: int, 
    school_update: SchoolUpdate, 
    session: Session = Depends(get_session)
):
    """Update a school by ID"""
    db_school = session.get(School, school_id)
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Update only provided fields
    update_data = school_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_school, field, value)
    
    session.add(db_school)
    session.commit()
    session.refresh(db_school)
    return db_school


@school_router.delete("/{school_id}")
async def delete_school(school_id: int, session: Session = Depends(get_session)):
    """Delete a school by ID"""
    db_school = session.get(School, school_id)
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    
    session.delete(db_school)
    session.commit()
    return {"message": "School deleted successfully"}


@school_router.get("/search/by-city/{city}", response_model=List[SchoolRead])
async def get_schools_by_city(city: str, session: Session = Depends(get_session)):
    """Get schools by city"""
    statement = select(School).where(col(School.city).ilike(f"%{city}%"))
    schools = session.exec(statement).all()
    return schools


@school_router.get("/search/by-state/{state}", response_model=List[SchoolRead])
async def get_schools_by_state(state: str, session: Session = Depends(get_session)):
    """Get schools by state"""
    statement = select(School).where(col(School.state).ilike(f"%{state}%"))
    schools = session.exec(statement).all()
    return schools
