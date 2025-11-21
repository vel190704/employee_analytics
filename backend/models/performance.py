"""
Performance Data model for Employee Analytics Platform
"""
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class PerformanceData(Base):
    __tablename__ = "performance_data"

    performance_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False, index=True)
    rating_year = Column(Integer, nullable=False, index=True)
    rating_value = Column(Numeric(3, 1), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="performance_data")

    __table_args__ = (
        CheckConstraint("rating_year >= 2000 AND rating_year <= 2100", name="check_rating_year_valid"),
        CheckConstraint("rating_value >= 0 AND rating_value <= 10", name="check_rating_value_valid"),
        UniqueConstraint("employee_id", "rating_year", name="unique_employee_year"),
    )

    def __repr__(self):
        return f"<PerformanceData(id={self.performance_id}, employee_id={self.employee_id}, year={self.rating_year}, rating={self.rating_value})>"

