"""
Employee service layer for business logic
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional, Dict, Any
from models.employee import Employee
from models.department import Department
from models.audit_log import EmployeeAuditLog
import logging

logger = logging.getLogger(__name__)


class EmployeeService:
    """Service class for employee operations"""

    @staticmethod
    def create_employee(db: Session, employee_data: Dict[str, Any]) -> Employee:
        """Create a new employee"""
        employee = Employee(**employee_data)
        db.add(employee)
        db.commit()
        db.refresh(employee)
        logger.info(f"Created employee: {employee.employee_id}")
        return employee

    @staticmethod
    def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        return db.query(Employee).filter(Employee.employee_id == employee_id).first()

    @staticmethod
    def get_all_employees(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        department_id: Optional[int] = None
    ) -> List[Employee]:
        """Get all employees with optional filters"""
        query = db.query(Employee)
        
        if status:
            query = query.filter(Employee.status == status)
        if department_id:
            query = query.filter(Employee.department_id == department_id)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_employee(db: Session, employee_id: int, update_data: Dict[str, Any]) -> Optional[Employee]:
        """Update employee information"""
        employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if not employee:
            return None
        
        for key, value in update_data.items():
            setattr(employee, key, value)
        
        db.commit()
        db.refresh(employee)
        logger.info(f"Updated employee: {employee_id}")
        return employee

    @staticmethod
    def delete_employee(db: Session, employee_id: int) -> bool:
        """Delete (resign) an employee"""
        employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if not employee:
            return False
        
        db.delete(employee)
        db.commit()
        logger.info(f"Deleted employee: {employee_id}")
        return True

    @staticmethod
    def increment_salary(db: Session, employee_id: int, increment: float) -> Optional[Employee]:
        """Increment employee salary using stored function"""
        try:
            # Call stored function
            db.execute(
                "SELECT update_salary(:emp_id, :increment)",
                {"emp_id": employee_id, "increment": increment}
            )
            db.commit()
            
            # Return updated employee
            return db.query(Employee).filter(Employee.employee_id == employee_id).first()
        except Exception as e:
            db.rollback()
            logger.error(f"Error incrementing salary: {e}")
            raise

    @staticmethod
    def get_employee_count(db: Session, status: Optional[str] = None) -> int:
        """Get total employee count"""
        query = db.query(Employee)
        if status:
            query = query.filter(Employee.status == status)
        return query.count()

    @staticmethod
    def get_salary_statistics(db: Session, department_id: Optional[int] = None) -> Dict[str, Any]:
        """Get salary statistics"""
        query = db.query(
            func.avg(Employee.salary).label('avg_salary'),
            func.max(Employee.salary).label('max_salary'),
            func.min(Employee.salary).label('min_salary'),
            func.sum(Employee.salary).label('total_salary')
        ).filter(Employee.status == 'active')
        
        if department_id:
            query = query.filter(Employee.department_id == department_id)
        
        result = query.first()
        
        return {
            "avg_salary": float(result.avg_salary) if result.avg_salary else 0,
            "max_salary": float(result.max_salary) if result.max_salary else 0,
            "min_salary": float(result.min_salary) if result.min_salary else 0,
            "total_salary": float(result.total_salary) if result.total_salary else 0
        }

