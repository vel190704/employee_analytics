"""
Script to initialize database with sample data
Run this after setting up the database to populate with test data
"""
from database import SessionLocal, init_db
from models.department import Department
from models.employee import Employee
from datetime import date, timedelta
import random

def init_sample_data():
    """Initialize database with sample departments and employees"""
    db = SessionLocal()
    
    try:
        # Initialize database tables
        init_db()
        
        # Create departments
        departments_data = [
            {"department_name": "Engineering", "location": "San Francisco"},
            {"department_name": "Sales", "location": "New York"},
            {"department_name": "Marketing", "location": "Los Angeles"},
            {"department_name": "HR", "location": "Chicago"},
            {"department_name": "Finance", "location": "Boston"},
        ]
        
        departments = []
        for dept_data in departments_data:
            dept = Department(**dept_data)
            db.add(dept)
            departments.append(dept)
        
        db.commit()
        
        # Refresh to get IDs
        for dept in departments:
            db.refresh(dept)
        
        # Create sample employees
        first_names = ["John", "Jane", "Bob", "Alice", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        
        employees_data = []
        for i in range(50):
            dept = random.choice(departments)
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
            salary = random.randint(50000, 150000)
            date_joined = date.today() - timedelta(days=random.randint(0, 1000))
            status = random.choice(["active", "active", "active", "resigned"])  # 75% active
            
            emp = Employee(
                first_name=first_name,
                last_name=last_name,
                email=email,
                salary=salary,
                department_id=dept.department_id,
                date_joined=date_joined,
                status=status
            )
            db.add(emp)
            employees_data.append(emp)
        
        db.commit()
        
        print(f"✅ Created {len(departments)} departments")
        print(f"✅ Created {len(employees_data)} employees")
        print("\nSample data initialized successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error initializing data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_sample_data()

