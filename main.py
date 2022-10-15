from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
import json
import random


app = Flask(__name__)
data = json.load(open('anekdot.json', encoding='utf-8'))


@app.route('/')
def index():
    query = request.args.get('q')
    if query and query != ' ' and len(query) > 2:
        page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
        results = []
        for anekdot in data:
            if str(query).lower() in anekdot['anekdot'].lower():
                results.append(f"{anekdot['id']}\n{anekdot['anekdot']}")
        total = len(results)
        pagination_anekdots = results[offset: offset + 10]
        pagination = Pagination(page=page, 
                                per_page=per_page, 
                                total=total,
                                css_framework='Bootstrap3', 
                                display_msg=f'Найдено {total} анекдотов',
                                )

        return render_template('results.html', 
                                results=pagination_anekdots,
                                page=page,
                                per_page=per_page,
                                pagination=pagination,)

    id = []
    anekdots = []
    for _ in range(10):
        random_number = random.randint(1, 111707)
        id.append(random_number)
    for i in id:
        newline = data[i]["anekdot"]
        anekdots.append(f'{i}\n{newline}')
        
    return render_template('index.html', anekdots=anekdots)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
