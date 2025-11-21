-- Employee Analytics Platform - Triggers for Automation
-- PostgreSQL Triggers for Data Integrity and Audit Logging

-- Trigger Function: Log employee updates in audit log
CREATE OR REPLACE FUNCTION log_employee_update()
RETURNS TRIGGER AS $$
BEGIN
    -- Only log if salary or status changed
    IF OLD.salary IS DISTINCT FROM NEW.salary OR OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO employee_audit_log(
            employee_id, 
            action_type, 
            old_salary, 
            new_salary, 
            timestamp
        )
        VALUES(
            NEW.employee_id, 
            'UPDATE', 
            OLD.salary, 
            NEW.salary, 
            NOW()
        );
    END IF;
    
    -- Update last_updated timestamp
    NEW.last_updated = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Log updates on employees table
CREATE TRIGGER trg_employee_update
AFTER UPDATE ON employees
FOR EACH ROW 
EXECUTE FUNCTION log_employee_update();

-- Trigger Function: Log employee inserts
CREATE OR REPLACE FUNCTION log_employee_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO employee_audit_log(
        employee_id, 
        action_type, 
        old_salary, 
        new_salary, 
        timestamp
    )
    VALUES(
        NEW.employee_id, 
        'INSERT', 
        NULL, 
        NEW.salary, 
        NOW()
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Log inserts on employees table
CREATE TRIGGER trg_employee_insert
AFTER INSERT ON employees
FOR EACH ROW 
EXECUTE FUNCTION log_employee_insert();

-- Trigger Function: Log employee deletes
CREATE OR REPLACE FUNCTION log_employee_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO employee_audit_log(
        employee_id, 
        action_type, 
        old_salary, 
        new_salary, 
        timestamp
    )
    VALUES(
        OLD.employee_id, 
        'DELETE', 
        OLD.salary, 
        NULL, 
        NOW()
    );
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Log deletes on employees table
CREATE TRIGGER trg_employee_delete
AFTER DELETE ON employees
FOR EACH ROW 
EXECUTE FUNCTION log_employee_delete();

-- Trigger Function: Format employee names (capitalize first letter)
CREATE OR REPLACE FUNCTION format_employee_name()
RETURNS TRIGGER AS $$
BEGIN
    NEW.first_name = INITCAP(TRIM(NEW.first_name));
    NEW.last_name = INITCAP(TRIM(NEW.last_name));
    NEW.email = LOWER(TRIM(NEW.email));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Format names before insert
CREATE TRIGGER trg_name_format_insert
BEFORE INSERT ON employees
FOR EACH ROW 
EXECUTE FUNCTION format_employee_name();

-- Trigger: Format names before update
CREATE TRIGGER trg_name_format_update
BEFORE UPDATE ON employees
FOR EACH ROW 
EXECUTE FUNCTION format_employee_name();

-- Trigger Function: Validate email format
CREATE OR REPLACE FUNCTION validate_employee_email()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Invalid email format: %', NEW.email;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Validate email on insert and update
CREATE TRIGGER trg_validate_email_insert
BEFORE INSERT ON employees
FOR EACH ROW 
EXECUTE FUNCTION validate_employee_email();

CREATE TRIGGER trg_validate_email_update
BEFORE UPDATE ON employees
FOR EACH ROW 
EXECUTE FUNCTION validate_employee_email();

