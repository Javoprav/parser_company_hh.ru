import requests, json
from typing import Any
import psycopg2


class HH:
    id_company = [733, 565840, 67611, 6093775, 160748, 1329, 1532045, 681672, 1122462, 592442]

    def __init__(self):
        self.name = None

    @classmethod
    def get_request_company(cls) -> list[dict[str, int | None | Any]]:
        """Получает список с компаниями по api"""
        url: str = "https://api.hh.ru/vacancies"
        company_dict = []
        for i in range(len(cls.id_company)):
            id_range = cls.id_company[i]
            params = {'area': 113, 'page': 0, 'per_page': 100, 'employer_id': id_range}
            response = requests.get(url, params=params)
            if response.ok:
                data = response.json()
                vac_for_name = data['items']
                name_employer = None
                for vac in vac_for_name:
                    name_employer = vac['employer']['name']
                company_dict.append({
                    'company_name': name_employer,
                    'count_vac': data['found'],
                    'company_id': id_range})
        return company_dict

    @classmethod
    def get_request_vacancy(cls) -> list[dict[str, int | str | Any]]:
        """Получает список с вакансиями по api"""
        url: str = "https://api.hh.ru/vacancies"
        vacancy_dict = []
        for i in range(len(cls.id_company)):
            id_range = cls.id_company[i]
            params = {'area': 113, 'page': 0, 'per_page': 100, 'employer_id': id_range}
            response = requests.get(url, params=params)
            if response.ok:
                data = response.json()
                for vac in data['items']:
                    if vac['salary'] is None or vac['salary']['from'] is None:
                        salary = 'Не известно'
                    else:
                        salary = vac['salary']['from']
                    vacancy_dict.append({
                        'company_id': id_range,
                        'company_name': vac['employer']['name'],
                        'vacancy_name': vac['name'],
                        'salary': salary,
                        'url': vac['alternate_url']
                    })
            else:
                print(f"Ошибка {response.status_code}")
        return vacancy_dict

    @staticmethod
    def create_database(database_name: str, params: dict):
        """Создание базы данных и таблиц для сохранения данных о каналах и видео."""

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"DROP DATABASE {database_name}")
        except psycopg2.errors.InvalidCatalogName:
            print(f'psycopg2.errors.InvalidCatalogName: ОШИБКА:  база данных {database_name} не существует')

        cur.execute(f"CREATE DATABASE {database_name}")
        conn.close()
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE company (
                    company_name VARCHAR(255),
                    count_vac INTEGER,
                    company_id INTEGER
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancy (
                    company_id INTEGER,
                    company_name VARCHAR(255),
                    vacancy_name VARCHAR,
                    salary INTEGER,
                    url TEXT
                )
            """)
        conn.commit()
        conn.close()

    @staticmethod
    def save_data_company_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
        """Сохранение данных о компаниях в базу данных."""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            for comp in data:
                cur.execute(
                    """
                    INSERT INTO company (company_name, count_vac, company_id)
                    VALUES (%s, %s, %s)
                    """,
                    (comp['company_name'], comp['count_vac'], comp['company_id'])
                )
        conn.commit()
        conn.close()

    @staticmethod
    def save_data_vacancy_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
        """Сохранение данных о вакансиях в базу данных."""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            for vac in data:
                salary_vac = None
                if vac['salary'] == 'Не известно':
                    salary_vac = 0
                else:
                    salary_vac = vac['salary']
                cur.execute(
                    """
                    INSERT INTO vacancy (company_id, company_name, vacancy_name, salary, url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (vac['company_id'], vac['company_name'], vac['vacancy_name'], salary_vac, vac['url'])
                )
        conn.commit()
        conn.close()

