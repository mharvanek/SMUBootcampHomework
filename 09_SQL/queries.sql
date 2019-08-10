--1. List the following details of each employee: employee number, last name, first name, gender, and salary.
SELECT e.emp_no, last_name, first_name, gender, salary
FROM "Employees" e
INNER JOIN "Salaries" s ON e.emp_no = s.emp_no
;
--2. List employees who were hired in 1986.
SELECT *
FROM "Employees"
WHERE hire_date >= '1986-01-01'
and hire_date <= '1986-12-31'
;
--3. List the manager of each department with the following information:
-- department number, department name, the manager's employee number, last name, first name, and start and end employment dates.
--TODO: 1. Are we listing the current managers or all of them?
--TODO: 2. There is no employee end date? Show department to_date?
SELECT d.dept_no, d.dept_name, dm.emp_no, e.last_name, e.first_name, dm.from_date, dm.to_date, e.hire_date
FROM "Departments" d
INNER JOIN "Dept_Managers" dm on d.dept_no = dm.dept_no
INNER JOIN "Employees" e on dm.emp_no = e.emp_no
where dm.to_date = '9999-01-01'
;
--4. List the department of each employee with the following information: employee number, last name, first name, and department name.
SELECT e.emp_no, e.last_name, e.first_name, d.dept_name
FROM "Employees" e
INNER JOIN "Dept_Employees" de on e.emp_no = de.emp_no
INNER JOIN "Departments" d on de.dept_no = d.dept_no
;
--5. List all employees whose first name is "Hercules" and last names begin with "B."
SELECT *
FROM "Employees"
WHERE first_name = 'Hercules'
AND last_name like 'B%'
ORDER BY last_name
;
--6. List all employees in the Sales department, including their employee number, last name, first name, and department name.
SELECT e.emp_no, e.last_name, e.first_name, d.dept_name
FROM "Employees" e
INNER JOIN "Dept_Employees" de on e.emp_no = de.emp_no
INNER JOIN "Departments" d on de.dept_no = d.dept_no
WHERE d.dept_name = 'Sales'
;
--7. List all employees in the Sales and Development departments, including their employee number, last name, first name, and department name.
SELECT e.emp_no, e.last_name, e.first_name, d.dept_name
FROM "Employees" e
INNER JOIN "Dept_Employees" de on e.emp_no = de.emp_no
INNER JOIN "Departments" d on de.dept_no = d.dept_no
WHERE d.dept_name IN ('Sales', 'Development')
;
--8. In descending order, list the frequency count of employee last names, i.e., how many employees share each last name.
SELECT last_name, count(last_name)
FROM "Employees"
GROUP BY last_name
ORDER BY count(*) DESC
;
--BONUS:
SELECT title, AVG(salary)
FROM "Titles" t
INNER JOIN "Salaries" s on t.emp_no = s.emp_no
GROUP BY title
ORDER BY title