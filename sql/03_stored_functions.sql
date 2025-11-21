-- Employee Analytics Platform - Stored Functions
-- PostgreSQL Stored Functions for Automation

-- Function: Update employee salary with increment
CREATE OR REPLACE FUNCTION update_salary(emp_id INTEGER, increment NUMERIC)
RETURNS VOID AS $$
BEGIN
    UPDATE employees
    SET salary = salary + increment,
        last_updated = NOW()
    WHERE employee_id = emp_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Employee with ID % not found', emp_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function: Get department statistics
CREATE OR REPLACE FUNCTION get_department_stats(dept_id INTEGER)
RETURNS TABLE(
    department_name VARCHAR,
    total_employees BIGINT,
    active_employees BIGINT,
    avg_salary NUMERIC,
    max_salary NUMERIC,
    min_salary NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        d.department_name,
        COUNT(e.employee_id)::BIGINT as total_employees,
        COUNT(CASE WHEN e.status = 'active' THEN 1 END)::BIGINT as active_employees,
        AVG(CASE WHEN e.status = 'active' THEN e.salary END) as avg_salary,
        MAX(CASE WHEN e.status = 'active' THEN e.salary END) as max_salary,
        MIN(CASE WHEN e.status = 'active' THEN e.salary END) as min_salary
    FROM departments d
    LEFT JOIN employees e ON d.department_id = e.department_id
    WHERE d.department_id = dept_id
    GROUP BY d.department_id, d.department_name;
END;
$$ LANGUAGE plpgsql;

-- Function: Get top N departments by average salary
CREATE OR REPLACE FUNCTION get_top_departments_by_salary(n INTEGER DEFAULT 5)
RETURNS TABLE(
    department_id INTEGER,
    department_name VARCHAR,
    avg_salary NUMERIC,
    employee_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    WITH avg_sal AS (
        SELECT 
            department_id, 
            AVG(salary) as avg_salary,
            COUNT(*)::BIGINT as employee_count
        FROM employees
        WHERE status = 'active'
        GROUP BY department_id
    )
    SELECT 
        d.department_id,
        d.department_name,
        a.avg_salary,
        a.employee_count
    FROM avg_sal a
    JOIN departments d ON d.department_id = a.department_id
    ORDER BY a.avg_salary DESC
    LIMIT n;
END;
$$ LANGUAGE plpgsql;

-- Function: Calculate salary growth percentage
CREATE OR REPLACE FUNCTION calculate_salary_growth(emp_id INTEGER, months_back INTEGER DEFAULT 12)
RETURNS NUMERIC AS $$
DECLARE
    current_salary NUMERIC;
    old_salary NUMERIC;
    growth_percent NUMERIC;
BEGIN
    -- Get current salary
    SELECT salary INTO current_salary
    FROM employees
    WHERE employee_id = emp_id AND status = 'active';
    
    IF current_salary IS NULL THEN
        RETURN NULL;
    END IF;
    
    -- Get salary from months_back ago
    SELECT old_salary INTO old_salary
    FROM employee_audit_log
    WHERE employee_id = emp_id
      AND action_type = 'UPDATE'
      AND timestamp >= NOW() - (months_back || ' months')::INTERVAL
    ORDER BY timestamp ASC
    LIMIT 1;
    
    IF old_salary IS NULL THEN
        RETURN 0;
    END IF;
    
    -- Calculate growth percentage
    growth_percent := ((current_salary - old_salary) / old_salary) * 100;
    
    RETURN ROUND(growth_percent, 2);
END;
$$ LANGUAGE plpgsql;

-- Function: Bulk insert employees from array
CREATE OR REPLACE FUNCTION bulk_insert_employees(
    emp_data JSONB
)
RETURNS TABLE(
    employee_id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    success BOOLEAN,
    error_message TEXT
) AS $$
DECLARE
    emp_record JSONB;
    new_emp_id INTEGER;
BEGIN
    FOR emp_record IN SELECT * FROM jsonb_array_elements(emp_data)
    LOOP
        BEGIN
            INSERT INTO employees (
                first_name, last_name, email, salary, 
                department_id, date_joined, status
            )
            VALUES (
                emp_record->>'first_name',
                emp_record->>'last_name',
                emp_record->>'email',
                (emp_record->>'salary')::NUMERIC,
                (emp_record->>'department_id')::INTEGER,
                (emp_record->>'date_joined')::DATE,
                COALESCE(emp_record->>'status', 'active')
            )
            RETURNING employee_id INTO new_emp_id;
            
            RETURN QUERY SELECT 
                new_emp_id,
                (emp_record->>'first_name')::VARCHAR,
                (emp_record->>'last_name')::VARCHAR,
                (emp_record->>'email')::VARCHAR,
                TRUE,
                NULL::TEXT;
        EXCEPTION WHEN OTHERS THEN
            RETURN QUERY SELECT 
                NULL::INTEGER,
                (emp_record->>'first_name')::VARCHAR,
                (emp_record->>'last_name')::VARCHAR,
                (emp_record->>'email')::VARCHAR,
                FALSE,
                SQLERRM::TEXT;
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

