-- Employee Analytics Platform - Indexes for Query Optimization
-- Additional indexes for analytics performance

-- Basic indexes (also in schema, but ensuring they exist)
CREATE INDEX IF NOT EXISTS idx_emp_dept ON employees(department_id);
CREATE INDEX IF NOT EXISTS idx_emp_status ON employees(status);
CREATE INDEX IF NOT EXISTS idx_emp_salary ON employees(salary);
CREATE INDEX IF NOT EXISTS idx_emp_email ON employees(email);
CREATE INDEX IF NOT EXISTS idx_audit_employee ON employee_audit_log(employee_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON employee_audit_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_perf_employee ON performance_data(employee_id);
CREATE INDEX IF NOT EXISTS idx_perf_year ON performance_data(rating_year);

-- Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_emp_dept_status ON employees(department_id, status);
CREATE INDEX IF NOT EXISTS idx_emp_status_salary ON employees(status, salary);
CREATE INDEX IF NOT EXISTS idx_emp_joined_date ON employees(date_joined);

-- Index for department lookups
CREATE INDEX IF NOT EXISTS idx_dept_name ON departments(department_name);

-- Index for audit log queries by action type
CREATE INDEX IF NOT EXISTS idx_audit_action ON employee_audit_log(action_type);

-- Index for performance data queries
CREATE INDEX IF NOT EXISTS idx_perf_employee_year ON performance_data(employee_id, rating_year);

-- Partial indexes for active employees (most common query)
CREATE INDEX IF NOT EXISTS idx_emp_active ON employees(employee_id, salary, department_id) 
WHERE status = 'active';

-- Index for salary range queries
CREATE INDEX IF NOT EXISTS idx_emp_salary_range ON employees(salary) 
WHERE status = 'active';

