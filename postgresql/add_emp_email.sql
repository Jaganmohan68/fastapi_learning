ALTER TABLE employees
ADD COLUMN emp_email VARCHAR(254);

CREATE UNIQUE INDEX ix_employees_emp_email
ON employees (emp_email);
