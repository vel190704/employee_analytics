# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Start the Services

```bash
cd E:\Projects\Employee
docker-compose up -d
```

This will:
- Start PostgreSQL database
- Start FastAPI backend
- Initialize database schema, functions, and triggers automatically

### Step 2: Wait for Services (30 seconds)

Check if services are ready:
```bash
docker-compose ps
```

### Step 3: Access the API

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Root**: http://localhost:8000

## 📝 Quick Test

### 1. Create a Department

```bash
curl -X POST "http://localhost:8000/departments/" \
  -H "Content-Type: application/json" \
  -d '{
    "department_name": "Engineering",
    "location": "San Francisco"
  }'
```

### 2. Create an Employee

```bash
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
```

### 3. Get Analytics

```bash
# Top departments by salary
curl "http://localhost:8000/analytics/top_departments?limit=5"

# Salary insights
curl "http://localhost:8000/analytics/salary_insights"
```

### 4. Upload CSV

```bash
curl -X POST "http://localhost:8000/upload/csv/employees" \
  -F "file=@sample_data/employees_sample.csv"
```

## 🛑 Stop Services

```bash
docker-compose down
```

To remove volumes (clean database):
```bash
docker-compose down -v
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API at http://localhost:8000/docs
- Check out the SQL files in the `sql/` directory
- Review the test files in `backend/tests/`

## 🐛 Troubleshooting

### Database not ready?
```bash
docker-compose logs db
```

### Backend errors?
```bash
docker-compose logs backend
```

### Port already in use?
Change ports in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

