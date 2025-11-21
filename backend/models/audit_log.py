"""
Employee Audit Log model for Employee Analytics Platform
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class EmployeeAuditLog(Base):
    __tablename__ = "employee_audit_log"

    log_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False, index=True)
    action_type = Column(String(20), nullable=False, index=True)
    old_salary = Column(Numeric(10, 2), nullable=True)
    new_salary = Column(Numeric(10, 2), nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), index=True)

    # Relationships
    employee = relationship("Employee", back_populates="audit_logs")

    __table_args__ = (
        CheckConstraint("action_type IN ('INSERT', 'UPDATE', 'DELETE')", name="check_action_type_valid"),
    )

    def __repr__(self):
        return f"<EmployeeAuditLog(id={self.log_id}, employee_id={self.employee_id}, action={self.action_type})>"

