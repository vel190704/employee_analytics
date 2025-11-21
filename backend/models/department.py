"""
Department model for Employee Analytics Platform
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(100), nullable=False, unique=True, index=True)
    location = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    employees = relationship("Employee", back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.department_id}, name={self.department_name}, location={self.location})>"

