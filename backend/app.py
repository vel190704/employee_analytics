"""
Employee Analytics Platform - FastAPI Application
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from database import init_db, engine
from models import Employee, Department, EmployeeAuditLog, PerformanceData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Employee Analytics Platform",
    description="A comprehensive platform for storing, analyzing, and managing employee data with automated processing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")


# Include routers
from routes import employees, analytics, departments, csv_upload

app.include_router(employees.router)
app.include_router(analytics.router)
app.include_router(departments.router)
app.include_router(csv_upload.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Employee Analytics Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "employees": "/employees",
            "analytics": "/analytics",
            "departments": "/departments",
            "upload": "/upload"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "employee-analytics-platform"}

