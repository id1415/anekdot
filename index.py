import os
from dotenv import load_dotenv
from flask import render_template, request, flash, redirect, url_for, make_response
from db_module import app, random_anekdot, len_base, add_anekdot, \
    likes, dislikes, new_anecdotes, best_anecdotes, search, tags_db
from forms import TextForm, SearchForm, LikeForm, TagsForm

# environment variables
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

# site menu
menu = [{'name': 'ОБНОВИТЬ', 'url': '/'},
        {'name': 'Лучшие анекдоты', 'url': 'best'},
        {'name': 'Новые анекдоты', 'url': 'new'},
        {'name': 'Теги', 'url': 'tags'},
        {'name': 'Добавить анекдот', 'url': 'add'},
        {'name': 'О сайте', 'url': 'about'},
        ]


# the function saves the query from the search in cookies
def if_query(query, tag, flag=0):
    resp = make_response(redirect(url_for('results')))
    if flag == 1:
        resp.set_cookie('query', '')
        resp.set_cookie('tag', tag)
    else:
        resp.set_cookie('tag', '')
        resp.set_cookie('query', query, httponly=True)
    return resp


# results page
@app.route('/results', methods=['GET', 'POST'])
def results():
    # the following lines are copied for each page so that the search field works everywhere
    query = request.args.get('search')  # getting data from the search field
    if query:                           # if the user entered something into the search
        return if_query(query, tag='')          # saving a search query in cookies

    tag = request.args.get('tags')
    if tag:
        return if_query('', tag, flag=1)

    query_from_cookie = request.cookies.get('query')  # getting a string from a cookie
    tag_from_cookie = request.cookies.get('tag')
    if tag_from_cookie:
        #query_from_cookie = tag_from_cookie
        results = search(tag_from_cookie, flag=1)
    if query_from_cookie:
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

#TAGS page
@app.route('/tags')
def tags():
    query = request.args.get('search')
    if query:
        return if_query(query, tag='')

    tags_db()
    results = tags_db()

    return render_template('tags.html',
                           menu=menu,
                           title='Теги',
                           search_form=SearchForm(),
                           results=results,
                          )

# BEST page
@app.route('/best')
def best():
    query = request.args.get('search')
    if query:
        return if_query(query, tag='')

    results = best_anecdotes()  # 100 jokes with the highest ratings are displayed
    page = request.args.get('page', 1, type=int)
    results = results.paginate(page=page, per_page=10, error_out=True)

    return render_template('best.html',
                           menu=menu,
                           title='Лучшие анекдоты',
                           search_form=SearchForm(),
                           results=results,
                           )


# NEW page
@app.route('/new')
def new():
    query = request.args.get('search')
    if query:
        return if_query(query, tag='')

    results = new_anecdotes()  # 100 latest jokes are displayed
    page = request.args.get('page', 1, type=int)
    results = results.paginate(page=page, per_page=10, error_out=True)

    return render_template('new.html',
                           menu=menu,
                           title='Новые анекдоты',
                           search_form=SearchForm(),
                           results=results,
                           )


# MAIN page
@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('search')
    if query:
        return if_query(query, tag='')

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


# ABOUT page
@app.route('/about')
def about():
    query = request.args.get('search')
    if query:
        return if_query(query, tag='')

    return render_template('about.html',
                           menu=menu,
                           title='О сайте',
                           search_form=SearchForm(),
                           raw=len_base(),  # number of jokes in the database
                           )


# ADD page
@app.route('/add', methods=['GET', 'POST'])
def add():
    query = request.args.get('search')
    if query:
        return if_query(query, tag='')

    text_form = TextForm()                   # form for text
    tags_form = TagsForm()                   # form for tags
    if text_form.validate_on_submit():       # if the query is POST
        if tags_form.validate_on_submit():
            new_tag = str.lower(tags_form.tags.data)
        new_anekdot = text_form.text.data    # text from the form
        # adding to the database, the function returns the id of the new joke
        id = add_anekdot(new_anekdot, new_tag)
        text_form = TextForm(formdata=None)  # cleaning the text form
        tags_form = TagsForm(formdata=None)  # cleaning the tags form
        # if you don't clean the form, then
        # you'll be able to send the same text infinit times
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
                           tags_form=tags_form,
                           )


if __name__ == '__main__':
    app.run()
