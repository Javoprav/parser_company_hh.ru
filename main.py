from classes import *
from pprint import pprint
from config import config

if __name__ == '__main__':
    hh = HH()
    params = config()
    start_input = input('Введите "1" для запуска: ')
    if start_input.lower() == 'stop':
        print("Выход!")
        exit()
    elif start_input == '1':
        data_company = hh.get_request_company()
        data_vacancy = hh.get_request_vacancy()
        hh.create_database('hh_ru', params)
        hh.save_data_company_to_database(data_company, 'hh_ru', params)
        # hh.save_data_vacancy_to_database(data_company, 'vacancy', params)
    else:
        print("Не верный ввод! Выход!")
        exit()
