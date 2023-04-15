from classes import *


if __name__ == '__main__':
    hh = HH()
    user_input = input('Введите название вакансии: ')
    if user_input:
        hh.get_request(user_input)
    elif user_input.lower() == 'stop':
        print("Выход!")
        exit()
    else:
        print("Не верный ввод! Выход!")
        exit()
