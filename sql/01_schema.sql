-- Employee Analytics Platform - Database Schema
-- PostgreSQL Database Schema

-- Create departments table
CREATE TABLE IF NOT EXISTS departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    salary NUMERIC(10, 2) NOT NULL CHECK (salary >= 0),
    department_id INTEGER NOT NULL,
    date_joined DATE NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'resigned')),
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE RESTRICT
);

-- Create employee_audit_log table
CREATE TABLE IF NOT EXISTS employee_audit_log (
    log_id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    action_type VARCHAR(20) NOT NULL CHECK (action_type IN ('INSERT', 'UPDATE', 'DELETE')),
    old_salary NUMERIC(10, 2),
    new_salary NUMERIC(10, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

-- Create performance_data table (optional)
CREATE TABLE IF NOT EXISTS performance_data (
    performance_id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    rating_year INTEGER NOT NULL CHECK (rating_year >= 2000 AND rating_year <= 2100),
    rating_value NUMERIC(3, 1) NOT NULL CHECK (rating_value >= 0 AND rating_value <= 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    UNIQUE(employee_id, rating_year)
);

