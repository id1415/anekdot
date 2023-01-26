import os
from dotenv import load_dotenv
from flask import render_template, request, flash, redirect, url_for, make_response
from apps import app, random_anekdot, len_base, add_anekdot, \
                likes, dislikes, new_anecdotes, best_anecdotes, search
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


# функция сохраняет запрос в поиске в куки
def if_query(query):
    resp = make_response(redirect(url_for('results')))
    resp.set_cookie('query', query)
    return resp


# результаты поиска
@app.route('/results', methods = ['GET', 'POST'])
def results():
    # следующие строки копируются для каждой страницы чтобы поле поиска работало везде
    query = request.args.get('search')  # получение данных из поля поиска
    if query:                           # если пользователь что-то ввёл в поиск
        return if_query(query)
    
    query_from_cookie = request.cookies.get('query')  # получение строки из куки
    results = search(query_from_cookie)               # поиск в БД

    page = request.args.get('page', 1, type=int)                        # для пагинации
    results = results.paginate(page=page, per_page=10, error_out=True)  # пагинация

    return render_template('results.html',
                menu=menu,                 # меню сайта
                title=query_from_cookie,   # заголовок страницы
                search_form=SearchForm(),  # поле поиска
                results=results,           # результаты поиска
                )


# Страница лучшие анекдоты
@app.route('/best')
def best():
    query = request.args.get('search')
    if query:
        return if_query(query)

    results = best_anecdotes()  # функция выводит 100 анекдотов с наивысшими рейтингами
    page = request.args.get('page', 1, type=int)
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
    query = request.args.get('search')
    if query:
        return if_query(query)
    
    results = new_anecdotes()  # функция выводит 100 последних анекдотов из базы данных
    page = request.args.get('page', 1, type=int)
    results = results.paginate(page=page, per_page=10, error_out=True)

    return render_template('new.html',
                            menu=menu,
                            title='Новые анекдоты',
                            search_form=SearchForm(),
                            results=results,
                            )


@app.route('/setcookie')
def setcookie():
    dh = request.cookies.get('query')
    print(dh)
    return f'asadasd {dh}'
 

# главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('search')
    if query:
        return if_query(query)

    # Лайк, дизлайк
    like_form = LikeForm()
    if request.method == 'POST':
        # здесь принимаются данные из JS кода, который находится в index.html
        like = request.form['like']
        dislike = request.form['dislike']

        if like:               # если пользователь нажал на лайк
            likes(like)        # число рейтинга в БД увеличивается на 1
        if dislike:            # если пользователь нажал на дизлайк
            dislikes(dislike)  # число уменьшается на 1

    anekdots = random_anekdot()  # функция выводит 10 случайных анекдотов на страницу

    # всё, что находится внутри всех функций render_template, используется в jinja синтаксисе в html файлах
    return render_template('index.html',
                            menu=menu,
                            title='Анекдоты',
                            search_form=SearchForm(),
                            like_form=like_form,  # кнопки лайк/дизлайк
                            anekdots=anekdots,
                            )


# страница О САЙТЕ
@app.route('/about')
def about():
    query = request.args.get('search')
    if query:
        return if_query(query)

    return render_template('about.html',
                            menu=menu,
                            title='О сайте',
                            search_form=SearchForm(),
                            raw=len_base(),  # количество анекдотов в базе
                            )


# страница ДОБАВИТЬ АНЕКДОТ
@app.route('/add', methods = ['GET', 'POST'])
def add():
    query = request.args.get('search')
    if query:
        return if_query(query)
    
    text_form = TextForm()                   # форма добавления анекдотов
    if text_form.validate_on_submit():       # если запрос - POST
        new_anekdot = text_form.text.data    # текст из формы
        id = add_anekdot(new_anekdot)        # добавление в базу, функция возвращает id нового анекдота
        text_form = TextForm(formdata=None)  # очищение формы
                                             # если не очищать форму, то
                                             # отправлять текст можно будет много раз,
                                             # капча этому не препятствует
        # флэш сообщение об успешной отправке
        flash(f'Анекдот добавлен, ему присвоен id - {id}', category='success')
    elif text_form.recaptcha.errors:  # если капча не сработала
        flash('Ошибка валидации!', category='error')

    return render_template('add.html',
                            menu=menu,
                            title='Добавить анекдот',
                            search_form=SearchForm(),
                            text_form=text_form,
                            )


if __name__ == '__main__':
    app.run(debug=True)
