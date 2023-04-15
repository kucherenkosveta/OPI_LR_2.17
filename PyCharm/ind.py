#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import sys


def get_way(ways, start, finish, num):
    """
    Запросить данные о маршруте.
    """
    # Создать словарь.
    ways.append(
        {
            'start': start,
            'finish': finish,
            'num': num,
        }
    )
    return ways


def display_way(numbers):
    """
    Отобразить список маршрутов.
    """
    if numbers:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 30,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^30} | {:^15} |'.format(
                "No",
                "Название начального маршрута",
                "Название конечного маршрута",
                "Номер маршрута"
            )
        )
        print(line)

        # Вывести данные о всех маршрутах.
        for idx, way in enumerate(numbers, 1):
            print(
                '| {:>4} | {:<30} | {:<30} | {:>15} |'.format(
                    idx,
                    way.get('start', ''),
                    way.get('finish', ''),
                    way.get('num', 0)
                )
            )
        print(line)

    else:
        print("Список пуст.")


def find_way(numbers, nw):
    """
    Выбрать маршрут с данным номером.
    """
    # Список маршрутов
    result = []
    for h in numbers:
        if nw in str(h.values()):
            result.append(h)

    # Возвратить список выбранных маршрутов.
    return result


def save_ways(file_name, ways):
    """
    Сохранить номера всех маршрутов в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(ways, fout, ensure_ascii=False, indent=4)


def load_ways(file_name):
    """
    Загрузить все маршруты из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("ways")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления маршрута.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new student"
    )

    add.add_argument(
        "-s",
        "--start",
        action="store",
        required=True,
        help="Start Route"
    )

    add.add_argument(
        "-f",
        "--finish",
        action="store",
        help="Final Route"
    )

    add.add_argument(
        "-n",
        "--num",
        action="store",
        required=True,
        help="Route number"
    )

    # Создать субпарсер для отображения всех маршрутов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all ways"
    )

    # Создать субпарсер для поиска маршрутов.
    find = subparsers.add_parser(
        "find",
        parents=[file_parser],
        help="find the ways"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить все маршруты из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        ways = load_ways(args.filename)
    else:
        ways = []

    # Добавить маршрут.
    if args.command == "add":
        ways = get_way(
            ways,
            args.start,
            args.finish,
            args.num
        )
        is_dirty = True

    # Отобразить всех студентов.
    elif args.command == "display":
        display_way(ways)

    # Выбрать требуемых студентов.
    elif args.command == "find":
        found = find_way(ways)
        display_way(found)

    # Сохранить данные в файл, если список студентов был изменен.
    if is_dirty:
        save_ways(args.filename, ways)


if __name__ == '__main__':
    main()
