from json import load
from random import randint
from flask_paginate import Pagination, get_page_args

data = load(open('anekdot.json', encoding='utf-8'))  # загрузка json файла с анекдотами


class Search:

    def __init__(self, query=None):
        self.query = query

    def status(self):  # ввёл ли пользователь запрос в поиск
        if self.query != None and self.query != ' ' and 101 > len(self.query) > 2:
            return True

    # поиск и пагинация результатов
    def search(self):
        results = []  # сюда помещаются результаты поиска
        for anekdot in data:
            if self.query.lower() in anekdot['anekdot'].lower():
                results.append({anekdot['id']: anekdot['anekdot']})

        total = len(results)  # количество найденных анекдотов

        # page - номер страницы
        # per_page - результатов на страницу
        # offset = (page - 1) * per_page
        page, per_page, offset = get_page_args(page_parameter='page',
                                            per_page_parameter='per_page')
        
        results = results[offset: offset + 10]  # список из 10 анекдотов

        pagination = Pagination(page=page,
                                per_page=per_page,
                                total=total,
                                css_framework='Bootstrap3',
                                display_msg=f'Найдено {total} анекдотов'
                                )

        return results, pagination


def random_anekdot():

    anekdots = []
    for _ in range(10):
        random_number = randint(1, 111707)  # выбирается случайное число от 1 до 111707
        newline = data[random_number]["anekdot"]  # анекдот с id - случайным числом
        anekdots.append({random_number: newline})
    
    return anekdots
