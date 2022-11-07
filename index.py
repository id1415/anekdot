import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash
from apps import Search, random_anekdot, len_base, add_anekdot

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
exm = Search()  # для поиска
menu = [{'name': 'ОБНОВИТЬ', 'url': '/'},
        {'name': 'О САЙТЕ', 'url': 'about'},
        {'name': 'ДОБАВИТЬ АНЕКДОТ', 'url': 'add'}
        ]


# результаты поиска
def results():
    search = exm.search()

    return render_template('results.html',
                results=search[0],
                pagination=search[1],
                menu=menu,
                )


@app.route('/')
def index():

    global exm
    q = request.args.get('q')  # запрос в поиске
    exm = Search(q)
    if exm.status():
        return results()

    anekdots = random_anekdot()
    return render_template('index.html',
                            anekdots=anekdots,
                            menu=menu,
                            title='Анекдоты',
                            )


@app.route('/about')
def about():

    # копипаст поиска ¯\_(ツ)_/¯
    global exm
    q = request.args.get('q')  # запрос в поиске
    exm = Search(q)
    if exm.status():
        return results()

    return render_template('about.html',
                            menu=menu, 
                            title='О сайте',
                            raw=len_base(),
                            )


@app.route('/add', methods = ['POST', 'GET'])
def add():

    # копипаст поиска ¯\_(ツ)_/¯
    global exm
    q = request.args.get('q')  # запрос в поиске
    exm = Search(q)
    if exm.status():
        return results()
    
    # форма добавления анекдотов
    if request.method == 'POST':
        if 500 > len(request.form['message']) > 10:
            new_anekdot = request.form
            a = add_anekdot(new_anekdot['message'])
            if a:
                flash(f'Анекдот добавлен, ему присвоен id - {a}', category='success')
            else:
                flash('Ошибка', category='error')
        else:
            flash('Ошибка', category='error')

    return render_template('add.html',
                            menu=menu,
                            title='Добавить анекдот',
                            )


if __name__ == '__main__':
    app.run()
