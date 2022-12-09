import os
from dotenv import load_dotenv
from flask import render_template, request, flash
from apps import app, search, random_anekdot, len_base, add_anekdot, likes, dislikes
from forms import TextForm, SearchForm, LikeForm

# переменные окружения
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')
app.config['MYSQL_DATABASE_USER'] = os.getenv('mysql_user')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('mysql_password')
app.config['MYSQL_DATABASE_DB'] = os.getenv('mysql_db')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('mysql_host')

# меню сайта
menu = [{'name': 'ОБНОВИТЬ', 'url': '/'},
        {'name': 'О САЙТЕ', 'url': 'about'},
        {'name': 'ДОБАВИТЬ АНЕКДОТ', 'url': 'add'},
        ]


# результаты поиска
def results(s):
    results = search(s)

    return render_template('results.html',
                results=results[0],
                pagination=results[1],
                menu=menu,
                search_form=SearchForm(),
                title=s,
                )


# главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    # запрос в поле поиска
    query = request.args.get('search')
    if query:
        return results(query)

    anekdots = random_anekdot()  # функция выводит 10 случайных анекдотов на страницу

    # Лайк, дизлайк
    like_form = LikeForm()
    if request.method == 'POST':
        like = request.form['like']
        dislike = request.form['dislike']
        if like:
            likes(like)
        if dislike:
            dislikes(dislike)

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
        return results(query)

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
        return results(query)
    
    text_form = TextForm()  # форма добавления анекдотов
    if text_form.validate_on_submit():     # если запрос - POST
        new_anekdot = text_form.text.data  # текст из формы
        a = add_anekdot(new_anekdot)       # добавление в базу
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
