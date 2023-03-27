#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import marshmallow
from marshmallow import Schema, fields


class Man(Schema):
    name = fields.String(required=True)
    zodiac_sign = fields.String(required=True)
    birth = fields.String(required=True)


man_Schema = Man()


def validate_json_marshmallow(d):
    try:
        man_Schema.load(d)
    except marshmallow.exceptions.ValidationError as err:
        return False, err
    message = "JSON data is correct"
    return True, message


def help_inf():
    # Вывести справку о работе с программой.
    print("\033[32mСписок команд:\n")
    print("add - добавить человека;")
    print("select <ЗЗ> - запросить людей с определенным ЗЗ;")
    print("show - показать список людей;")
    print("help - отобразить справку;")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")
    print("exit - завершить работу с программой.")


def add_human():
    # Кортеж ЗЗ
    zodiac_signs = (
        03.21,
        "овен",
        04.21,
        "телец",
        05.22,
        "близнецы",
        06.22,
        "рак",
        07.23,
        "лев",
        08.23,
        "дева",
        09.24,
        "весы",
        10.24,
        "скорпион",
        11.23,
        "стрелец",
        12.22,
        "козерог",
        01.21,
        "водолей",
        02.19,
        "рыбы",
        03.21
    )

    zs_ny = (
        12.22,
        "козерог",
        01.21,
        "водолей",
        02.19,
        "рыбы",
        03.21
    )

    # Запросить данные человека
    name = input("Enter name: ")
    # Проверка ЗЗ
    while True:
        zodiac_sign = input("\033[0mEnter zodiac sign: ").lower()
        if zodiac_sign not in zodiac_signs \
                and zodiac_sign not in zs_ny:
            print("\033[31mIncorrect zodiac sign")
        else:
            break

    # Проверка Даты Рождения
    while True:
        birth = input("\033[0mEnter date of birth (yyyy.mm.dd): ")
        # Обработка исключения (проверка правильности даты)
        try:
            birth_data = datetime.datetime.strptime(birth, '%Y.%m.%d')
        except Exception:
            print("\033[31mIncorrect data format")
        # Если ДР введен корректно относительно формата,
        # проверяем дату согласно ЗЗ
        else:
            # Получаем из кортежа начальную дату введенного ЗЗ
            # и преобразуем к нужному формату даты
            if zodiac_sign in zs_ny:
                beg_zs_data = datetime.datetime.strptime(
                    str(birth_data.year - 1) + '.' +
                    str(zs_ny[zs_ny.index(zodiac_sign) - 1]),
                    '%Y.%m.%d'
                )
                # Получаем из кортежа конечную дату введенного ЗЗ
                # и преобразуем к нужному формату даты
                end_zs_data = datetime.datetime.strptime(
                    str(birth_data.year) + '.' +
                    str(zs_ny[zs_ny.index(zodiac_sign) + 1]),
                    '%Y.%m.%d'
                )
                # Сравнение введенной даты с промежутком дат ЗЗ
                if beg_zs_data <= birth_data < end_zs_data:
                    break
                else:
                    print("\033[31mEnter CORRECR date of birth "
                          "(yyyy.mm.dd): ")
            else:
                beg_zs_data = datetime.datetime.strptime(
                    str(birth_data.year) + '.' +
                    str(zodiac_signs[zodiac_signs.index(zodiac_sign) - 1]),
                    '%Y.%m.%d'
                )
                # Получаем из кортежа конечную дату введенного ЗЗ
                # и преобразуем к нужному формату даты
                end_zs_data = datetime.datetime.strptime(
                    str(birth_data.year) + '.' +
                    str(zodiac_signs[zodiac_signs.index(zodiac_sign) + 1]),
                    '%Y.%m.%d'
                )
                # Сравнение введенной даты с промежутком дат ЗЗ
                if beg_zs_data <= birth_data < end_zs_data:
                    break
                else:
                    print("\033[31mEnter CORRECR date of birth "
                          "(yyyy.mm.dd): ")
    # Вернуть словарь
    return {
        'name': name,
        'zodiac_sign': zodiac_sign,
        'birth': birth,
    }


def display_people(people_list):
    # Заголовок таблицы.
    line = (f'{"+" + "-" * 15 + "+" + "-" * 12 + "+"}'
            f'{"-" * 15 + "+"}')
    print(line)
    print(f"|{'Name' :^15}|{'Birth ' :^12}|{'Zodiac_sign ' :^15}|")
    print(line)

    # Вывести данные о всех людях.
    for idx, man in enumerate(people_list):
        print(
            f'|{man.get("name", "") :^15}'
            f'|{man.get("birth", "") :^12}'
            f'|{man.get("zodiac_sign", "") :^15}|'
        )
        print(line)


def select_zz(com, people_list):
    # Разбить команду на части для выделения номера года.
    # Параметр maxsplit - int, сколько раз делить строку.
    while True:
        parts = com.split(' ', maxsplit=1)
        if len(parts) == 1:
            com = input("\033[31mEnter command "
                        "select and Zodiac_sign: ").lower()
            # Получить требуемый ЗЗ.
        else:
            break

    # Инициализировать счетчик.
    count = 0
    zz = parts[1]
    # Заголовок таблицы.
    line = (f'\033[0m{"+" + "-" * 12 + "+" + "-" * 12 + "+"}'
            f'{"-" * 15 + "+"}')
    print(line)
    print(
        f"|{'Name' :^12}|{'Birth ' :^12}"
        f"|{'Zodiac_sign ' :^15}|"
    )
    print(line)
    # Таблица с людьми
    for p in people_list:
        if zz == p.get('zodiac_sign'):
            count += 1
            print(
                f'|{p.get("name", "") :^12}|'
                f'{p.get("birth", "") :^12}|'
                f'{p.get("zodiac_sign", "") :^15}|'
            )
            print(line)

    # Если счетчик равен 0, то люди не найдены.
    if count == 0:
        print("Люди с заданным ЗЗ не найдены")


def save_people(file_name, people_list):
    """
    Сохранить всех людей в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(people_list, fout, ensure_ascii=False, indent=4)


def load_people(file_name):
    """
    Загрузить всех людей из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


if __name__ == '__main__':
    # Список людей
    people = []

    # zodiac_signs = {
    #             'name': "овен",
    #             'data_beg': datetime.datetime.strptime("11.11", "%d.%m"),
    #             'data_end': "birth"
    #         }
    # print(zodiac_signs.get("data_beg"))

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        # На Python с помощью ANSI-код можно делать цвет, фон и т.д.
        # \033[0m - сброс форматирования
        command = input("\033[0mEnter command: ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        # Добавить нового человека
        elif command == 'add':
            human = add_human()
            # Добавить словарь в список.
            people.append(human)

            # Отсортировать список в случае необходимости.
            # Сортировка по дате рождения (от старшего к младшим)
            if len(people) > 1:
                people.sort(key=lambda item: item.get('birth', ''))

        # Показать список людей
        elif command == 'show':
            display_people(people)

        # .startswith - Поиск строк с заданным началом строки
        elif command.startswith('select'):
            select_zz(command, people)

        # Список команд с описанием
        elif command == 'help':
            help_inf()

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            save_people(file_name, people)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Получить данные из файла
            people = load_people(file_name)
            # Валидация
            for elem in people:
                is_valid, msg = validate_json_marshmallow(elem)
                print(elem)
                print(msg)
        # Неопознанная команда
        else:
            print("\033[31mUnknown command")
