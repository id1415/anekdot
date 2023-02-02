import os
from dotenv import load_dotenv
from flask import render_template, request, flash, redirect, url_for, make_response
from db_module import app, random_anekdot, len_base, add_anekdot, \
    likes, dislikes, new_anecdotes, best_anecdotes, search
from forms import TextForm, SearchForm, LikeForm

# environment variables
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

# site menu
menu = [{'name': 'ОБНОВИТЬ', 'url': '/'},
        {'name': 'Лучшие анекдоты', 'url': 'best'},
        {'name': 'Новые анекдоты', 'url': 'new'},
        {'name': 'Добавить анекдот', 'url': 'add'},
        {'name': 'О сайте', 'url': 'about'},
        ]


# the function saves the query from the search in cookies
def if_query(query):
    resp = make_response(redirect(url_for('results')))
    resp.set_cookie('query', query, httponly=True)
    return resp


# search results
@app.route('/results', methods=['GET', 'POST'])
def results():
    # the following lines are copied for each page so that the search field works everywhere
    query = request.args.get('search')  # getting data from the search field
    if query:                           # if the user entered something into the search
        return if_query(query)          # saving a search query in cookies

    query_from_cookie = request.cookies.get(
        'query')  # getting a string from a cookie
    results = search(query_from_cookie)               # database search

    # for pagination
    page = request.args.get('page', 1, type=int)
    results = results.paginate(
        page=page, per_page=10, error_out=True)  # pagination

    # everything inside the render_template functions,
    # used in jinja syntax in html files
    return render_template('results.html',
                           menu=menu,                 # site menu
                           title=query_from_cookie,   # page title
                           search_form=SearchForm(),  # search field
                           results=results,           # search results
                           )


# Best anecdotes page
@app.route('/best')
def best():
    query = request.args.get('search')
    if query:
        return if_query(query)

    results = best_anecdotes()  # 100 jokes with the highest ratings are displayed
    page = request.args.get('page', 1, type=int)
    results = results.paginate(page=page, per_page=10, error_out=True)

    return render_template('best.html',
                           menu=menu,
                           title='Лучшие анекдоты',
                           search_form=SearchForm(),
                           results=results,
                           )


# New anecdotes page
@app.route('/new')
def new():
    query = request.args.get('search')
    if query:
        return if_query(query)

    results = new_anecdotes()  # 100 latest jokes are displayed
    page = request.args.get('page', 1, type=int)
    results = results.paginate(page=page, per_page=10, error_out=True)

    return render_template('new.html',
                           menu=menu,
                           title='Новые анекдоты',
                           search_form=SearchForm(),
                           results=results,
                           )


# the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('search')
    if query:
        return if_query(query)

    # like, dislike forms
    like_form = LikeForm()
    if request.method == 'POST':
        # data from like.js, dislike.js is received here
        like = request.form['like']
        dislike = request.form['dislike']

        if like:               # if the user clicked on like
            likes(like)        # the number of rating in the database increases by 1
        if dislike:            # if the user clicked on dislike
            dislikes(dislike)  # the number is decreases by 1

    anekdots = random_anekdot()  # the function outputs 10 random jokes per page

    return render_template('index.html',
                           menu=menu,
                           title='Анекдоты',
                           search_form=SearchForm(),
                           like_form=like_form,  # like/dislike buttons
                           anekdots=anekdots,
                           )


# About page
@app.route('/about')
def about():
    query = request.args.get('search')
    if query:
        return if_query(query)

    return render_template('about.html',
                           menu=menu,
                           title='О сайте',
                           search_form=SearchForm(),
                           raw=len_base(),  # number of jokes in the database
                           )


# ADD ANECDOTE page
@app.route('/add', methods=['GET', 'POST'])
def add():
    query = request.args.get('search')
    if query:
        return if_query(query)

    text_form = TextForm()                   # form for adding jokes
    if text_form.validate_on_submit():       # if the query is POST
        new_anekdot = text_form.text.data    # text from the form
        # adding to the database, the function returns the id of the new joke
        id = add_anekdot(new_anekdot)
        text_form = TextForm(formdata=None)  # cleaning the form
        # if you don't clean the form, then
        # you will be able to send text infinitely
        # captcha does not prevent this

        # flash message about successful sending
        flash(f'Анекдот добавлен, ему присвоен id - {id}', category='success')
    elif text_form.recaptcha.errors:  # if the captcha hasn't worked
        flash('Ошибка валидации!', category='error')

    return render_template('add.html',
                           menu=menu,
                           title='Добавить анекдот',
                           search_form=SearchForm(),
                           text_form=text_form,
                           )


if __name__ == '__main__':
    app.run()
