import psycopg2


class DBManager:

    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        company_dict = []
        fd = open('queries.sql', 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')
        res = [ele.replace("\n", '') for ele in sqlCommands]
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"{res[0]}")
            rows = cur.fetchall()
            for row in rows:
                company_dict.append(f'Компания - {row[0]}, количество вакансий: {row[1]}')
        return '\n'.join(company_dict)
        conn.commit()
        conn.close()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию."""
        vac_dict = []
        fd = open('queries.sql', 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')
        res = [ele.replace("\n", '') for ele in sqlCommands]
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"{res[1]}")
            rows = cur.fetchall()
            for row in rows:
                vac_dict.append(f'Компания: {row[0]}, названия вакансии: {row[1]}, зарплата: {row[2]}, Ссылка: {row[3]}')
        return '\n'.join(vac_dict)
        conn.commit()
        conn.close()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        fd = open('queries.sql', 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')
        res = [ele.replace("\n", '') for ele in sqlCommands]
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"{res[2]}")
            rows = cur.fetchall()
            for row in rows:
                return f'Средняя зарплата: {row[0]}'
        conn.commit()
        conn.close()


    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        vac_dict = []
        fd = open('queries.sql', 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')
        res = [ele.replace("\n", '') for ele in sqlCommands]
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"{res[3]}")
            rows = cur.fetchall()
            for row in rows:
                vac_dict.append(f'Компания: {row[1]}, названия вакансии: {row[2]}, зарплата: {row[3]}, Ссылка: {row[4]}')
        return '\n'.join(vac_dict)
        conn.commit()
        conn.close()

    def get_vacancies_with_keyword(self, word=''):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        vac_dict = []
        fd = open('queries.sql', 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')
        res = [ele.replace("\n", '') for ele in sqlCommands]
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("SELECT * from vacancy where salary > (SELECT round(AVG(salary),0) AS avg_salary from vacancy)")
            rows = cur.fetchall()
            for row in rows:
                if word in row[2]:
                    vac_dict.append(f'Компания: {row[1]}, названия вакансии: {row[2]}, зарплата: {row[3]}, Ссылка: {row[4]}')
        return '\n'.join(vac_dict)
        conn.commit()
        conn.close()

