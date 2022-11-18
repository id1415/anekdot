import os
from dotenv import load_dotenv
from flask import render_template, request, flash
from apps import app, Search, random_anekdot, len_base, add_anekdot
from forms import TextForm

load_dotenv()

app.secret_key = os.getenv('SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')
 
exm = Search()  # для поиска

menu = [{'name': 'ОБНОВИТЬ', 'url': '/'},
        {'name': 'О САЙТЕ', 'url': 'about'},
        {'name': 'ДОБАВИТЬ АНЕКДОТ', 'url': 'add'},
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


@app.route('/add', methods = ['GET', 'POST'])
def add():

    # копипаст поиска ¯\_(ツ)_/¯
    global exm
    q = request.args.get('q')  # запрос в поиске
    exm = Search(q)
    if exm.status():
        return results()
    
    # форма добавления анекдотов
    form = TextForm()
    a = 0
    if form.validate_on_submit():
        new_anekdot = form.text.data
        a = add_anekdot(new_anekdot)
        flash(f'Анекдот добавлен, ему присвоен id - {a}', category='success')
    elif form.recaptcha.errors:
        flash('Ошибка валидации!', category='error')

    return render_template('add.html',
                            menu=menu,
                            title='Добавить анекдот',
                            form=form,
                            )


if __name__ == '__main__':
    app.run()
