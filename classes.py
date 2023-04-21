import json, requests, os
from pprint import pprint


class HH:
    id_company = [733, 565840, 67611, 6093775, 160748, 1329, 1532045, 681672, 1122462, 592442]

    def __init__(self):
        self.name = None

    @classmethod
    def get_request_company(cls):
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
                    'count-vac': data['found'],
                    'company_id': id_range})
        with open('employer.json', 'w', encoding='utf8') as f:
            json.dump(company_dict, f, ensure_ascii=False)
            f.close()
        return company_dict

    @classmethod
    def get_request_vacancy(cls):
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
                        'vacancy_name': vac['professional_roles']['name'],
                        'salary': salary
                    })
            else:
                print(f"Ошибка {response.status_code}")


hhh = HH()
pprint(hhh.get_request_vacancy())