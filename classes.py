import json, requests, os
from pprint import pprint


class HH:
    def __init__(self):
        self.name = None

    def get_request(self, name='Python'):
        """Получает json с вакансиями по api"""
        self.name = name
        url: str = "https://api.hh.ru/employers"
        params = {"area": 1, "per_page": 100}
        # params = {'text': self.name, 'area': 113, 'page': 0, 'per_page': 100}
        response = requests.get(url, params=params)
        if response.ok:
            data = response.json()
            # pprint(data)
            employers = data["items"]
            for employer in employers:
                pprint(employer["name"])
        else:
            print(f"Ошибка {response.status_code}")


hh = HH()
hh.get_request()