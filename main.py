from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
from json import load
from random import randint


app = Flask(__name__)
data = load(open('anekdot.json', encoding='utf-8'))  # загрузка json файла с анекдотами


@app.route('/')
def index():
    
    # блок для поиска
    # как отделить поиск от основной функции - не знаю, пока будет так
    query = request.args.get('q')  #  запрос в поиске
    if query and query != ' ' and 100 > len(query) > 2:
        results = []  # сюда помещаются результаты поиска
        for anekdot in data:  # поиск
            if str(query).lower() in anekdot['anekdot'].lower():
                results.append(f"{anekdot['id']}\n{anekdot['anekdot']}")

        total = len(results)  # количество найденных анекдотов

        # настройка для пагинации страницы с результатами поиска
        page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

        pagination_anekdots = results[offset: offset + 10]  # сколько анекдотов выводить на страницу

        # пагинация
        pagination = Pagination(page=page, 
                                per_page=per_page, 
                                total=total,
                                css_framework='Bootstrap3', 
                                display_msg=f'Найдено {total} анекдотов',
                                )
        
        # возврат результов
        return render_template('results.html', 
                                results=pagination_anekdots,
                                page=page,
                                per_page=per_page,
                                pagination=pagination,)

    # код для главной страницы
    id = []
    anekdots = []
    for _ in range(10):  # выбираются 10 случайных чисел от 1 до 111707
        random_number = randint(1, 111707)
        id.append(random_number)
    for i in id:  # добавляются анекдоты с id - случайными числами
        newline = data[i]["anekdot"]
        anekdots.append(f'{i}\n{newline}')
    
    # возврат анекдотов на главную страницу
    return render_template('index.html', anekdots=anekdots)

 # страница О САЙТЕ
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
