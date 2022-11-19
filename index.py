import os
from dotenv import load_dotenv
from flask import render_template, request, flash
from apps import app, search, random_anekdot, len_base, add_anekdot
from forms import TextForm, SearchForm

load_dotenv()

app.secret_key = os.getenv('SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

menu = [{'name': 'ОБНОВИТЬ', 'url': '/'},
        {'name': 'О САЙТЕ', 'url': 'about'},
        {'name': 'ДОБАВИТЬ АНЕКДОТ', 'url': 'add'},
        ]


# результаты поиска
def results(s):
    search1 = search(s)

    return render_template('results.html',
                results=search1[0],
                pagination=search1[1],
                menu=menu,
                search_form=SearchForm(),
                )


@app.route('/')
def index():
    search = request.args.get('search')
    if search:
        return results(search)

    anekdots = random_anekdot()
    return render_template('index.html',
                            anekdots=anekdots,
                            menu=menu,
                            title='Анекдоты',
                            search_form=SearchForm(),
                            )


@app.route('/about')
def about():
    search = request.args.get('search')
    if search:
        return results(search)

    return render_template('about.html',
                            menu=menu, 
                            title='О сайте',
                            raw=len_base(),
                            search_form=SearchForm(),
                            )


@app.route('/add', methods = ['GET', 'POST'])
def add():
    search = request.args.get('search')
    if search:
        return results(search)
    
    # форма добавления анекдотов
    text_form = TextForm()
    if text_form.validate_on_submit():
        new_anekdot = text_form.text.data
        a = add_anekdot(new_anekdot)
        flash(f'Анекдот добавлен, ему присвоен id - {a}', category='success')
    elif text_form.recaptcha.errors:
        flash('Ошибка валидации!', category='error')

    return render_template('add.html',
                            menu=menu,
                            title='Добавить анекдот',
                            text_form=text_form,
                            search_form=SearchForm(),
                            )


if __name__ == '__main__':
    app.run()
