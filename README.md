# Employee Analytics Platform

A comprehensive platform for storing, analyzing, and managing employee data with automated processing capabilities. This system reduces manual SQL work by 75% through automation using stored functions, triggers, and optimized queries.

## 🎯 Features

- **Employee Management**: Full CRUD operations for employee data
- **Automated Processing**: Triggers and stored functions for automatic data updates
- **Analytics Dashboard**: KPI queries and insights via REST API
- **CSV Upload**: Bulk employee data processing from CSV files
- **Audit Logging**: Complete audit trail of all employee changes
- **Performance Optimization**: Indexed queries and CTEs for fast analytics
- **Docker Deployment**: Easy setup with Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 15+ (included in Docker)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Navigate to the project directory:**
   ```bash
   cd E:\Projects\Employee
   ```

2. **Start the services:**
   ```bash
   docker-compose up -d
   ```

3. **Wait for services to initialize** (about 30 seconds)

4. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - API Root: http://localhost:8000
   - Health Check: http://localhost:8000/health

### Local Development Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database:**
   - Create a database named `employee_analytics`
   - Update `DATABASE_URL` in `backend/database.py` or set environment variable

4. **Initialize database schema:**
   ```bash
   # Connect to PostgreSQL and run SQL files in order:
   # 1. sql/01_schema.sql
   # 2. sql/02_indexes.sql
   # 3. sql/03_stored_functions.sql
   # 4. sql/04_triggers.sql
   ```

5. **Run the application:**
   ```bash
   cd backend
   uvicorn app:app --reload
   ```

## 📁 Project Structure

```
Employee/
│── backend/
│   ├── app.py                 # FastAPI application entry point
│   ├── database.py            # Database connection and session management
│   ├── models/                # SQLAlchemy models
│   │   ├── employee.py
│   │   ├── department.py
│   │   ├── audit_log.py
│   │   └── performance.py
│   ├── routes/                # API route handlers
│   │   ├── employees.py
│   │   ├── analytics.py
│   │   ├── departments.py
│   │   └── csv_upload.py
│   ├── services/              # Business logic layer
│   │   ├── employee_service.py
│   │   └── analytics_service.py
│   └── Dockerfile
│── sql/
│   ├── 01_schema.sql          # Database schema
│   ├── 02_indexes.sql         # Performance indexes
│   ├── 03_stored_functions.sql # Stored procedures
│   └── 04_triggers.sql        # Automated triggers
│── docker-compose.yml
│── requirements.txt
└── README.md
```

## 🔌 API Endpoints

### Employees

- `POST /employees/` - Create a new employee
- `GET /employees/` - Get all employees (with filters)
- `GET /employees/{id}` - Get employee by ID
- `PUT /employees/{id}` - Update employee
- `DELETE /employees/{id}` - Delete employee
- `PUT /employees/{id}/increment_salary` - Increment salary using stored function
- `GET /employees/stats/count` - Get employee count
- `GET /employees/stats/salary` - Get salary statistics

### Analytics

- `GET /analytics/top_departments?limit=5` - Top departments by average salary
- `GET /analytics/department/{id}/stats` - Department statistics
- `GET /analytics/salary_insights` - Overall salary insights
- `GET /analytics/employee/{id}/salary_growth?months_back=12` - Salary growth trend
- `GET /analytics/audit_summary?days=30` - Audit log summary

### Departments

- `POST /departments/` - Create a new department
- `GET /departments/` - Get all departments
- `GET /departments/{id}` - Get department by ID

### Upload

- `POST /upload/csv/employees` - Upload CSV file with employee data

## 📊 Database Schema

### Tables

1. **departments** - Department information
2. **employees** - Employee data with foreign key to departments
3. **employee_audit_log** - Audit trail of all changes
4. **performance_data** - Optional performance ratings

### Automation Features

#### Triggers
- **Name Formatting**: Automatically capitalizes names on insert/update
- **Email Validation**: Validates email format
- **Audit Logging**: Logs all INSERT, UPDATE, DELETE operations

#### Stored Functions
- `update_salary(emp_id, increment)` - Update employee salary
- `get_department_stats(dept_id)` - Get department statistics
- `get_top_departments_by_salary(n)` - Top N departments by salary
- `calculate_salary_growth(emp_id, months_back)` - Calculate salary growth
- `bulk_insert_employees(emp_data)` - Bulk insert employees

## 📝 CSV Upload Format

When uploading employee data via CSV, use the following format:

```csv
first_name,last_name,email,salary,department_id,date_joined,status
John,Doe,john.doe@example.com,75000,1,2023-01-15,active
Jane,Smith,jane.smith@example.com,80000,2,2023-02-20,active
```

**Required fields:**
- first_name
- last_name
- email
- salary
- department_id
- date_joined (YYYY-MM-DD format)

**Optional fields:**
- status (defaults to 'active')

## 🧪 Testing

### Manual Testing

Use the interactive API documentation at http://localhost:8000/docs to test endpoints.

### Example API Calls

```bash
# Create a department
curl -X POST "http://localhost:8000/departments/" \
  -H "Content-Type: application/json" \
  -d '{
    "department_name": "Engineering",
    "location": "San Francisco"
  }'

# Create an employee
curl -X POST "http://localhost:8000/employees/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "salary": 75000,
    "department_id": 1,
    "date_joined": "2023-01-15",
    "status": "active"
  }'

# Get analytics
curl "http://localhost:8000/analytics/top_departments?limit=5"

# Increment salary
curl -X PUT "http://localhost:8000/employees/1/increment_salary" \
  -H "Content-Type: application/json" \
  -d '{"increment": 5000}'
```

## 🔧 Configuration

### Environment Variables

- `DATABASE_URL` - PostgreSQL connection string (default: `postgresql://postgres:admin123@db:5432/employee_analytics`)

### Docker Configuration

Edit `docker-compose.yml` to customize:
- Database credentials
- Port mappings
- Volume mounts

## 📈 Performance Optimizations

- **Indexes**: Created on frequently queried columns (department_id, status, salary, email)
- **Composite Indexes**: For common query patterns
- **Partial Indexes**: For active employees (most common query)
- **CTEs**: Used in analytics queries for better performance
- **Connection Pooling**: SQLAlchemy connection pool configured

## 🚢 Deployment

### Production Considerations

1. **Security**:
   - Change default database password
   - Use environment variables for sensitive data
   - Enable HTTPS
   - Configure CORS properly

2. **Database**:
   - Use managed PostgreSQL service (AWS RDS, Google Cloud SQL)
   - Set up regular backups
   - Configure connection pooling

3. **Scaling**:
   - Use load balancer for multiple backend instances
   - Consider read replicas for analytics queries
   - Implement caching for frequently accessed data

### Cloud Deployment Options

- **AWS**: EC2 + RDS PostgreSQL
- **Google Cloud**: Cloud Run + Cloud SQL
- **Azure**: App Service + Azure Database for PostgreSQL
- **Render/Railway**: One-click deployment platforms

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🎯 Project Goals Achieved

✅ Store and analyze employee data from multiple departments
✅ Automatically process updates (new employees, resignations, salary changes)
✅ Provide API endpoints to fetch analytics (count, salary stats, department trends)
✅ Automate repetitive SQL tasks (cleaning, aggregations, audit logs)
✅ Reduce manual processing by 75% through automation
✅ Docker deployment ready
✅ Production-ready code structure

---

**Built with ❤️ using FastAPI, PostgreSQL, and SQLAlchemy**

