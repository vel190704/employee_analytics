"""
Analytics service layer for KPI and reporting queries
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service class for analytics operations"""

    @staticmethod
    def get_top_departments_by_salary(db: Session, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top N departments by average salary using CTE"""
        query = text("""
            WITH avg_sal AS (
                SELECT 
                    department_id, 
                    AVG(salary) as avg_salary,
                    COUNT(*) as employee_count
                FROM employees
                WHERE status = 'active'
                GROUP BY department_id
            )
            SELECT 
                d.department_id,
                d.department_name,
                d.location,
                a.avg_salary,
                a.employee_count
            FROM avg_sal a
            JOIN departments d ON d.department_id = a.department_id
            ORDER BY a.avg_salary DESC
            LIMIT :limit
        """)
        
        result = db.execute(query, {"limit": limit})
        
        return [
            {
                "department_id": row.department_id,
                "department_name": row.department_name,
                "location": row.location,
                "avg_salary": float(row.avg_salary),
                "employee_count": row.employee_count
            }
            for row in result
        ]

    @staticmethod
    def get_department_statistics(db: Session, department_id: int) -> Dict[str, Any]:
        """Get comprehensive department statistics using stored function"""
        query = text("SELECT * FROM get_department_stats(:dept_id)")
        result = db.execute(query, {"dept_id": department_id}).first()
        
        if not result:
            return {}
        
        return {
            "department_name": result.department_name,
            "total_employees": result.total_employees,
            "active_employees": result.active_employees,
            "avg_salary": float(result.avg_salary) if result.avg_salary else 0,
            "max_salary": float(result.max_salary) if result.max_salary else 0,
            "min_salary": float(result.min_salary) if result.min_salary else 0
        }

    @staticmethod
    def get_salary_insights(db: Session) -> Dict[str, Any]:
        """Get overall salary insights and trends"""
        # Active vs Resigned
        active_count_query = text("SELECT COUNT(*) as count FROM employees WHERE status = 'active'")
        resigned_count_query = text("SELECT COUNT(*) as count FROM employees WHERE status = 'resigned'")
        
        active_count = db.execute(active_count_query).scalar()
        resigned_count = db.execute(resigned_count_query).scalar()
        
        # Salary statistics
        salary_stats_query = text("""
            SELECT 
                AVG(salary) as avg_salary,
                MAX(salary) as max_salary,
                MIN(salary) as min_salary,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as median_salary
            FROM employees
            WHERE status = 'active'
        """)
        
        salary_stats = db.execute(salary_stats_query).first()
        
        # Department distribution
        dept_dist_query = text("""
            SELECT 
                d.department_name,
                COUNT(e.employee_id) as employee_count,
                AVG(e.salary) as avg_salary
            FROM departments d
            LEFT JOIN employees e ON d.department_id = e.department_id AND e.status = 'active'
            GROUP BY d.department_id, d.department_name
            ORDER BY employee_count DESC
        """)
        
        dept_dist = db.execute(dept_dist_query)
        
        return {
            "active_employees": active_count,
            "resigned_employees": resigned_count,
            "total_employees": active_count + resigned_count,
            "salary_statistics": {
                "avg_salary": float(salary_stats.avg_salary) if salary_stats.avg_salary else 0,
                "max_salary": float(salary_stats.max_salary) if salary_stats.max_salary else 0,
                "min_salary": float(salary_stats.min_salary) if salary_stats.min_salary else 0,
                "median_salary": float(salary_stats.median_salary) if salary_stats.median_salary else 0
            },
            "department_distribution": [
                {
                    "department_name": row.department_name,
                    "employee_count": row.employee_count,
                    "avg_salary": float(row.avg_salary) if row.avg_salary else 0
                }
                for row in dept_dist
            ]
        }

    @staticmethod
    def get_salary_growth_trend(db: Session, employee_id: int, months_back: int = 12) -> Dict[str, Any]:
        """Get salary growth trend for an employee"""
        query = text("SELECT calculate_salary_growth(:emp_id, :months_back) as growth_percent")
        result = db.execute(query, {"emp_id": employee_id, "months_back": months_back}).first()
        
        return {
            "employee_id": employee_id,
            "growth_percent": float(result.growth_percent) if result.growth_percent else 0,
            "months_back": months_back
        }

    @staticmethod
    def get_audit_log_summary(db: Session, days: int = 30) -> Dict[str, Any]:
        """Get audit log summary for the last N days"""
        query = text("""
            SELECT 
                action_type,
                COUNT(*) as count
            FROM employee_audit_log
            WHERE timestamp >= NOW() - INTERVAL '1 day' * :days
            GROUP BY action_type
        """)
        
        result = db.execute(query, {"days": days})
        
        summary = {row.action_type: row.count for row in result}
        
        return {
            "period_days": days,
            "actions": summary,
            "total_actions": sum(summary.values())
        }

