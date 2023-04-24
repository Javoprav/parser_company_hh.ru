SELECT company_name, count_vac FROM company;
SELECT company_name, vacancy_name, salary, url FROM vacancy;
SELECT round(AVG(salary),0) AS avg_salary from vacancy;
SELECT * from vacancy where salary > (SELECT round(AVG(salary),0) AS avg_salary from vacancy);
SELECT * from vacancy where salary > (SELECT round(AVG(salary),0) AS avg_salary from vacancy;