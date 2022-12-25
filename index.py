import os
from dotenv import load_dotenv
from flask import render_template, request, flash, redirect, url_for
from apps import app, search, random_anekdot, len_base, add_anekdot, \
                        likes, dislikes, new_anecdotes, best_anecdotes
from forms import TextForm, SearchForm, LikeForm

# переменные окружения
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')  # секретный ключ
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')   # публичный ключ для капчи
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY') # приватный ключ для капчи

# меню сайта
menu = [{'name': 'ОБНОВИТЬ', 'url': '/'},
        {'name': 'Лучшие анекдоты', 'url': 'best'},
        {'name': 'Новые анекдоты', 'url': 'new'},
        {'name': 'Добавить анекдот', 'url': 'add'},
        {'name': 'О сайте', 'url': 'about'},
        ]

 # костыль для поиска, если пользователь вводит запрос в поиск, этот запрос сохраняется сюда
 # нужен для функции results() и для заголовка результатов поиска
title = ''


# результаты поиска
@app.route('/results', methods = ['GET', 'POST'])
def results():
    # строки ниже присутствуют для каждой страницы, чтобы поиск работал везде
    # пока не знаю как избавиться от копипаста
    query = request.args.get('search')            # получение данных из поля поиска
    if query:                                     # если пользователь что-то ввёл в поиск
        global title
        title = query                             # глобальной переменной присваивается запрос из поиска
        results = search(title)
    else:
        results = search(title)                   # костыль вставляется сюда

    page = request.args.get('page', 1, type=int)  # для пагинации
    results = results.paginate(page=page, per_page=10, error_out=True)  # пагинация

    return render_template('results.html',
                menu=menu,                 # меню сайта
                title=title,               # заголовок, совпадает с запросом пользователя в поиске
                search_form=SearchForm(),  # поле поиска
                results=results,           # результаты поиска
                )


# Страница лучшие анекдоты
@app.route('/best')
def best():
    # запрос в поле поиска
    query = request.args.get('search')            # получение данных из поля поиска
    if query:                                     # если пользователь что-то ввёл в поиск
        global title
        title = query                             # глобальной переменной присваивается запрос из поиска
        return redirect(url_for('results'))

    results = best_anecdotes()                    # функция выводит 100 анекдотов с наивысшими рейтингами
    page = request.args.get('page', 1, type=int)  # для пагинации
    results = results.paginate(page=page, per_page=10, error_out=True)  # пагинация 100 анекдотов

    return render_template('best.html',
                            menu=menu,                 # меню сайта
                            title='Лучшие анекдоты',   # заголовок страницы
                            search_form=SearchForm(),  # поле поиска
                            results=results,           # результаты поиска
                            )


# страница Новые анекдоты
@app.route('/new')
def new():
    # запрос в поле поиска
    query = request.args.get('search')            # получение данных из поля поиска
    if query:                                     # если пользователь что-то ввёл в поиск
        global title
        title = query                             # глобальной переменной присваивается запрос из поиска
        return redirect(url_for('results'))
    
    results = new_anecdotes()                     # функция выводит 100 последних анекдотов из базы данных
    page = request.args.get('page', 1, type=int)  # для пагинации
    results = results.paginate(page=page, per_page=10, error_out=True)  # пагинация

    return render_template('new.html',
                            menu=menu,                 # меню сайта
                            title='Новые анекдоты',    # заголовок страницы
                            search_form=SearchForm(),  # поле поиска
                            results=results,           # результаты поиска
                            )


# главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    # запрос в поле поиска
    query = request.args.get('search')  # получение данных из поля поиска
    if query:                           # если пользователь что-то ввёл в поиск
        global title
        title = query                   # глобальной переменной присваивается запрос из поиска
        return redirect(url_for('results'))

    # Лайк, дизлайк
    like_form = LikeForm()
    if request.method == 'POST':
        # здесь принимаются данные из JS кода, который находится в index.html
        like = request.form['like']
        dislike = request.form['dislike']

        if like:               # если пользователь нажал на лайк
            likes(like)        # число рейтинга в БД увеличивается на 1
        if dislike:            # или на дизлайк
            dislikes(dislike)  # число уменьшается на 1

    anekdots = random_anekdot()  # функция выводит 10 случайных анекдотов на страницу

    # всё, что находится внутри всех функций render_template, используется в jinja синтаксисе в html файлах
    return render_template('index.html',
                            menu=menu,                 # меню сайта
                            title='Анекдоты',          # заголовок страницы
                            search_form=SearchForm(),  # поле поиска
                            like_form=like_form,       # кнопки лайк/дизлайк
                            anekdots=anekdots,         # 10 случайных анекдотов
                            )


# страница О САЙТЕ
@app.route('/about')
def about():
    # запрос в поле поиска
    query = request.args.get('search')  # получение данных из поля поиска
    if query:                           # если пользователь что-то ввёл в поиск
        global title
        title = query                   # глобальной переменной присваивается запрос из поиска
        return redirect(url_for('results'))

    return render_template('about.html',
                            menu=menu,                 # меню сайта
                            title='О сайте',           # заголовок страницы
                            search_form=SearchForm(),  # поле поиска
                            raw=len_base(),            # количество анекдотов в базе
                            )


# страница ДОБАВИТЬ АНЕКДОТ
@app.route('/add', methods = ['GET', 'POST'])
def add():
    # запрос в поле поиска
    query = request.args.get('search')  # получение данных из поля поиска
    if query:                           # если пользователь что-то ввёл в поиск
        global title
        title = query                   # глобальной переменной присваивается запрос из поиска
        return redirect(url_for('results'))
    
    text_form = TextForm()                   # форма добавления анекдотов
    if text_form.validate_on_submit():       # если запрос - POST
        new_anekdot = text_form.text.data    # текст из формы
        id = add_anekdot(new_anekdot)        # добавление в базу, функция возвращает id нового анекдота
        text_form = TextForm(formdata=None)  # очищение формы
                                             # форму надо очищать, иначе
                                             # отправлять текст можно будет бесконечное число раз,
                                             # и капча всегда будет срабатывать
        # флэш сообщение об успешной отправке
        flash(f'Анекдот добавлен, ему присвоен id - {id}', category='success')
    elif text_form.recaptcha.errors:  # если капча не сработала
        flash('Ошибка валидации!', category='error')

    return render_template('add.html',
                            menu=menu,                 # меню сайта
                            title='Добавить анекдот',  # заголовок страницы
                            search_form=SearchForm(),  # поле поиска
                            text_form=text_form,       # текстовое поле для добавления анекдота
                            )


if __name__ == '__main__':
    app.run()