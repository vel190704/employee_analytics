"""
Analytics API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from database import get_db
from services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/top_departments")
def get_top_departments(limit: int = 5, db: Session = Depends(get_db)):
    """Get top N departments by average salary using CTE"""
    if limit < 1 or limit > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 50"
        )
    
    departments = AnalyticsService.get_top_departments_by_salary(db, limit=limit)
    return {
        "limit": limit,
        "departments": departments
    }


@router.get("/department/{department_id}/stats")
def get_department_statistics(department_id: int, db: Session = Depends(get_db)):
    """Get comprehensive department statistics"""
    stats = AnalyticsService.get_department_statistics(db, department_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID {department_id} not found"
        )
    return stats


@router.get("/salary_insights")
def get_salary_insights(db: Session = Depends(get_db)):
    """Get overall salary insights and trends"""
    insights = AnalyticsService.get_salary_insights(db)
    return insights


@router.get("/employee/{employee_id}/salary_growth")
def get_salary_growth(
    employee_id: int,
    months_back: int = 12,
    db: Session = Depends(get_db)
):
    """Get salary growth trend for an employee"""
    if months_back < 1 or months_back > 60:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="months_back must be between 1 and 60"
        )
    
    growth = AnalyticsService.get_salary_growth_trend(db, employee_id, months_back)
    return growth


@router.get("/audit_summary")
def get_audit_summary(days: int = 30, db: Session = Depends(get_db)):
    """Get audit log summary for the last N days"""
    if days < 1 or days > 365:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="days must be between 1 and 365"
        )
    
    summary = AnalyticsService.get_audit_log_summary(db, days=days)
    return summary

