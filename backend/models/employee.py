"""
Employee model for Employee Analytics Platform
"""
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    salary = Column(Numeric(10, 2), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=False, index=True)
    date_joined = Column(Date, nullable=False)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(String(20), default="active", index=True)

    # Relationships
    department = relationship("Department", back_populates="employees")
    audit_logs = relationship("EmployeeAuditLog", back_populates="employee", cascade="all, delete-orphan")
    performance_data = relationship("PerformanceData", back_populates="employee", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("salary >= 0", name="check_salary_positive"),
        CheckConstraint("status IN ('active', 'resigned')", name="check_status_valid"),
    )

    def __repr__(self):
        return f"<Employee(id={self.employee_id}, name={self.first_name} {self.last_name}, email={self.email})>"

