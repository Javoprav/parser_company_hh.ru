from classes import *
from pprint import pprint


if __name__ == '__main__':
    hh = HH()
    start_input = input('Введите "1" для запуска: ')
    if start_input.lower() == 'stop':
        print("Выход!")
        exit()
    elif start_input == '1':
        pprint(hh.get_request_company())
    else:
        print("Не верный ввод! Выход!")
        exit()
