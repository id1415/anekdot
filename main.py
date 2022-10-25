from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
from app import Search, data
from random import randint


app = Flask(__name__)


# поиск и пагинация результатов
@app.route('/')
@app.route('/about')
def search():
    q = Search(request.args.get('q'))  # запрос в поиске
    if q.status():

        results = []  # сюда помещаются результаты поиска
        for anekdot in data:
            if str(q.query).lower() in anekdot['anekdot'].lower():
                results.append(f"{anekdot['id']}\n{anekdot['anekdot']}")

        total = len(results)  # количество найденных анекдотов

        page, per_page, offset = get_page_args(page_parameter='page',
                                            per_page_parameter='per_page')

        pagination_anekdots = results[offset: offset + 10]  # сколько анекдотов выводить на страницу

        pagination = Pagination(page=page, 
                                per_page=per_page, 
                                total=total,
                                css_framework='Bootstrap3', 
                                display_msg=f'Найдено {total} анекдотов'
                                )

        return render_template('results.html', 
                    results=pagination_anekdots,
                    page=page,
                    per_page=per_page,
                    pagination=pagination
                    )
    else:
        return index()


@app.route('/')
def index():
    # код для главной страницы
    id = []
    anekdots = []
    for _ in range(10):  # выбираются 10 случайных чисел от 1 до 111707
        random_number = randint(1, 111707)
        id.append(random_number)
    for i in id:  # добавляются анекдоты с id - случайными числами
        newline = data[i]["anekdot"]
        anekdots.append(f'{i}\n{newline}')
    
    # вывод анекдотов на главную страницу
    return render_template('index.html', anekdots=anekdots)


 # страница О САЙТЕ
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
