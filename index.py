import os
from dotenv import load_dotenv
from flask import render_template, request, flash, redirect, url_for
from apps import app, search, random_anekdot, len_base, add_anekdot, \
                        likes, dislikes, new_anecdotes, best_anecdotes
from forms import TextForm, SearchForm, LikeForm

# переменные окружения
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

# меню сайта
menu = [{'name': 'ОБНОВИТЬ', 'url': '/'},
        {'name': 'Лучшие анекдоты', 'url': 'best'},
        {'name': 'Новые анекдоты', 'url': 'new'},
        {'name': 'Добавить анекдот', 'url': 'add'},
        {'name': 'О сайте', 'url': 'about'},
        ]
title = ''


# результаты поиска
@app.route('/results', methods = ['GET', 'POST'])
def results():
    query = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    if query:
        global title
        title = query
        results = search(title)
    else:
        results = search(title)
    results = results.paginate(page=page, per_page=10, error_out=True)

    return render_template('results.html',
                results=results,
                menu=menu,
                search_form=SearchForm(),
                title=title,
                )


# Страница лучшие анекдоты
@app.route('/best')
def best():
    # запрос в поле поиска
    query = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    if query:
        global title
        title = query
        return redirect(url_for('results'))

    results = best_anecdotes()
    results = results.paginate(page=page, per_page=10, error_out=True)

    return render_template('best.html',
                            menu=menu,
                            title='Лучшие анекдоты',
                            search_form=SearchForm(),
                            results=results,
                            )


# страница Новые анекдоты
@app.route('/new')
def new():
    # запрос в поле поиска
    query = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    if query:
        global title
        title = query
        return redirect(url_for('results'))
    
    results = new_anecdotes()
    results = results.paginate(page=page, per_page=10, error_out=True)

    return render_template('new.html',
                            menu=menu,
                            title='Новые анекдоты',
                            search_form=SearchForm(),
                            results=results,
                            )


# главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    # запрос в поле поиска
    query = request.args.get('search')
    if query:
        global title
        title = query
        return redirect(url_for('results'))

    # Лайк, дизлайк
    like_form = LikeForm()
    if request.method == 'POST':
        like = request.form['like']
        dislike = request.form['dislike']

        if like:
            likes(like)
        if dislike:
            dislikes(dislike)

    anekdots = random_anekdot()  # функция выводит 10 случайных анекдотов на страницу

    return render_template('index.html',
                            anekdots=anekdots,
                            menu=menu,
                            title='Анекдоты',
                            search_form=SearchForm(),
                            like_form=like_form,
                            )


# страница О САЙТЕ
@app.route('/about')
def about():
    # запрос в поле поиска
    query = request.args.get('search')
    if query:
        global title
        title = query
        return redirect(url_for('results'))

    return render_template('about.html',
                            menu=menu, 
                            title='О сайте',
                            raw=len_base(),  # количество анекдотов в базе
                            search_form=SearchForm(),
                            )


# страница ДОБАВИТЬ АНЕКДОТ
@app.route('/add', methods = ['GET', 'POST'])
def add():
    # запрос в поле поиска
    query = request.args.get('search')
    if query:
        global title
        title = query
        return redirect(url_for('results'))
    
    text_form = TextForm()  # форма добавления анекдотов
    if text_form.validate_on_submit():     # если запрос - POST
        new_anekdot = text_form.text.data  # текст из формы
        a = add_anekdot(new_anekdot)       # добавление в базу
        text_form = TextForm(formdata=None)
        flash(f'Анекдот добавлен, ему присвоен id - {a}', category='success')
    elif text_form.recaptcha.errors:  # если капча не сработала
        flash('Ошибка валидации!', category='error')

    return render_template('add.html',
                            menu=menu,
                            title='Добавить анекдот',
                            text_form=text_form,
                            search_form=SearchForm(),
                            )


if __name__ == '__main__':
    app.run()