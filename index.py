from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
from apps import data, Search, random_anekdot


app = Flask(__name__)


# результаты поиска и пагинация
def results(q):
    results = []  # сюда помещаются результаты поиска
    for anekdot in data:
        if q.lower() in anekdot['anekdot'].lower():
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

    return render_template('results.html', 
                results=results,
                pagination=pagination
                )


@app.route('/')
def index():

    q = Search(request.args.get('q'))  # запрос в поиске
    if q.status():
        return results(q.query)

    anekdots = random_anekdot()
    return render_template('index.html', anekdots=anekdots)


@app.route('/about')
def about():

    q = Search(request.args.get('q'))  # запрос в поиске
    if q.status():
        return results(q.query)

    return render_template('about.html')


if __name__ == '__main__':
    app.run()
