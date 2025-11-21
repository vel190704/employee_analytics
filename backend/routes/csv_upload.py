"""
CSV upload and bulk processing routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
import csv
import io
from database import get_db
from services.employee_service import EmployeeService
from models.department import Department

router = APIRouter(prefix="/upload", tags=["upload"])


class UploadResponse(BaseModel):
    total_rows: int
    successful: int
    failed: int
    errors: List[Dict[str, Any]]


@router.post("/csv/employees", response_model=UploadResponse)
async def upload_employees_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload CSV file with employee data and process automatically.
    Expected CSV format: first_name,last_name,email,salary,department_id,date_joined,status
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV file"
        )
    
    try:
        contents = await file.read()
        csv_content = io.StringIO(contents.decode('utf-8'))
        reader = csv.DictReader(csv_content)
        
        successful = 0
        failed = 0
        errors = []
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
            try:
                # Validate required fields
                required_fields = ['first_name', 'last_name', 'email', 'salary', 'department_id', 'date_joined']
                missing_fields = [field for field in required_fields if not row.get(field)]
                
                if missing_fields:
                    errors.append({
                        "row": row_num,
                        "error": f"Missing required fields: {', '.join(missing_fields)}",
                        "data": row
                    })
                    failed += 1
                    continue
                
                # Validate department exists
                department_id = int(row['department_id'])
                department = db.query(Department).filter(Department.department_id == department_id).first()
                if not department:
                    errors.append({
                        "row": row_num,
                        "error": f"Department with ID {department_id} not found",
                        "data": row
                    })
                    failed += 1
                    continue
                
                # Create employee
                employee_data = {
                    "first_name": row['first_name'].strip(),
                    "last_name": row['last_name'].strip(),
                    "email": row['email'].strip().lower(),
                    "salary": float(row['salary']),
                    "department_id": department_id,
                    "date_joined": row['date_joined'],
                    "status": row.get('status', 'active').strip()
                }
                
                EmployeeService.create_employee(db, employee_data)
                successful += 1
                
            except ValueError as e:
                errors.append({
                    "row": row_num,
                    "error": f"Invalid data format: {str(e)}",
                    "data": row
                })
                failed += 1
            except Exception as e:
                errors.append({
                    "row": row_num,
                    "error": str(e),
                    "data": row
                })
                failed += 1
        
        return UploadResponse(
            total_rows=successful + failed,
            successful=successful,
            failed=failed,
            errors=errors
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing CSV file: {str(e)}"
        )

