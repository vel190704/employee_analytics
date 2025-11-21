"""
Employee API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import date
from database import get_db
from services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"])


# Pydantic models for request/response
class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    salary: float = Field(..., gt=0)
    department_id: int
    date_joined: date
    status: str = Field(default="active", pattern="^(active|resigned)$")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    salary: Optional[float] = Field(None, gt=0)
    department_id: Optional[int] = None
    status: Optional[str] = Field(None, pattern="^(active|resigned)$")


class EmployeeResponse(EmployeeBase):
    employee_id: int
    last_updated: Optional[str] = None

    class Config:
        from_attributes = True


class SalaryIncrement(BaseModel):
    increment: float = Field(..., gt=0)


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee"""
    try:
        employee_data = employee.model_dump()
        new_employee = EmployeeService.create_employee(db, employee_data)
        return new_employee
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating employee: {str(e)}"
        )


@router.get("/", response_model=List[EmployeeResponse])
def get_all_employees(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    department_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all employees with optional filters"""
    employees = EmployeeService.get_all_employees(
        db, skip=skip, limit=limit, status=status, department_id=department_id
    )
    return employees


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get employee by ID"""
    employee = EmployeeService.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    """Update employee information"""
    update_data = employee_update.model_dump(exclude_unset=True)
    employee = EmployeeService.update_employee(db, employee_id, update_data)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete (resign) an employee"""
    success = EmployeeService.delete_employee(db, employee_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )


@router.put("/{employee_id}/increment_salary", response_model=EmployeeResponse)
def increment_salary(
    employee_id: int,
    salary_increment: SalaryIncrement,
    db: Session = Depends(get_db)
):
    """Increment employee salary using stored function"""
    try:
        employee = EmployeeService.increment_salary(
            db, employee_id, salary_increment.increment
        )
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        return employee
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error incrementing salary: {str(e)}"
        )


@router.get("/stats/count")
def get_employee_count(status: Optional[str] = None, db: Session = Depends(get_db)):
    """Get employee count"""
    count = EmployeeService.get_employee_count(db, status=status)
    return {"count": count, "status": status or "all"}


@router.get("/stats/salary")
def get_salary_statistics(
    department_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get salary statistics"""
    stats = EmployeeService.get_salary_statistics(db, department_id=department_id)
    return stats

