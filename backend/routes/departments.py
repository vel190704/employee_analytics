"""
Department API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field
from database import get_db
from models.department import Department

router = APIRouter(prefix="/departments", tags=["departments"])


class DepartmentBase(BaseModel):
    department_name: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=100)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    department_id: int
    created_at: str

    class Config:
        from_attributes = True


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    """Create a new department"""
    try:
        db_department = Department(**department.model_dump())
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
        return db_department
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating department: {str(e)}"
        )


@router.get("/", response_model=List[DepartmentResponse])
def get_all_departments(db: Session = Depends(get_db)):
    """Get all departments"""
    departments = db.query(Department).all()
    return departments


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(department_id: int, db: Session = Depends(get_db)):
    """Get department by ID"""
    department = db.query(Department).filter(Department.department_id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID {department_id} not found"
        )
    return department

