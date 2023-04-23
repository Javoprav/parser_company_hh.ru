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
        hh.save_data_vacancy_to_database(data_vacancy, 'hh_ru', params)

        print("Данные записаны!")

        manager = DBManager('hh_ru', params)
        print('Если хотите увидеть список всех компаний'
              ' и количество вакансий у каждой компании введите "2"')
        print('Если хотите увидеть список всех вакансий с указанием названия компании,'
              ' названия вакансии и зарплаты и ссылки на вакансию введите "3"')
        print('Если хотите увидеть среднюю зарплату по вакансиям "4"')
        print('Если хотите увидеть список всех вакансий, '
              'у которых зарплата выше средней по всем вакансиям "5"')
        print('Если хотите увидеть список всех вакансий, '
              'в названии которых содержатся слова, например “python” введите слово: ')

        next_input = input()
        if next_input == '2':
            print(manager.get_companies_and_vacancies_count())
        elif next_input == '3':
            manager.get_all_vacancies()
        elif next_input == '4':
            manager.get_avg_salary()
        elif next_input == '5':
            manager.get_vacancies_with_higher_salary()
        else:
            manager.get_vacancies_with_keyword(next_input)
    else:
        print("Не верный ввод! Выход!")
        exit()
