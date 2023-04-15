#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


import json
import click
import os


@click.group()
@click.argument("filename")
@click.pass_context
def main(ctx, filename):
    ctx.obj = {
        'filename': filename
    }


@main.command('add')
@click.pass_context
@click.option("-s", "--start")
@click.option("-f", "--finish")
@click.option("-n", "--num")
def get_student(ctx, start, finish, num):
    filename = ctx.obj['filename']
    ways = load_ways(filename)
    ways.append(
        {
            'start': start,
            'finish': finish,
            'num': num
        }
    )

    with open(filename, "w", encoding="utf-8") as fout:
        json.dump(ways, fout, ensure_ascii=False, indent=4)
    click.secho("Маршрут добавлен")


@main.command("display")
@click.pass_obj
@click.option("--display", "-d", is_flag=True)
def display_ways(filename, find):
    ways = load_ways(filename)
    if find:
        ways = find(ways)

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
            "№",
            "Название начального маршрута",
            "Название конечного маршрута",
            "Номер маршрута"
        )
    )
    print(line)

    for idx, way in enumerate(ways, 1):
        print(
            '| {:>4} | {:<30} | {:<30} | {:>15} |'.format(
                idx,
                way.get('start', ''),
                way.get('finish', ''),
                way.get('num', 0)
            )
        )
    print(line)


@main.command("find")
@click.pass_obj
@click.option("--find", "-f", is_flag=True)
def find_ways(ways, nw):
    result = []
    count = 0
    for h in ways:
        if nw in str(h.values()):
            result.append(h)

    return result


def load_ways(filename):
    result = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as fin:
            result = json.load(fin)
    return result


if __name__ == "__main__":
    main()