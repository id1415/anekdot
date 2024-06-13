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


# the function saves some data in cookies (from search field or tag)
def if_query(query, tag):
    resp = make_response(redirect(url_for('results')))
    if tag:
        resp.set_cookie('query', '')
        resp.set_cookie('tag', tag)
    else:
        resp.set_cookie('tag', '')
        resp.set_cookie('query', query)
    return resp


# results page
@app.route('/results', methods=['GET', 'POST'])
def results():
    # search query is stored in cookies
    query = request.args.get('search')  # getting data from the search field
    if query:                           # if user entered something into the search field
        return if_query(query, '')      # saving a search query in cookies

    tag = request.args.get('tags')      # the same for tag
    if tag:
        return if_query('', tag)

    # getting a string from cookie
    query_from_cookie = request.cookies.get('query')
    tag_from_cookie = request.cookies.get('tag')

    # database search is performed here
    if tag_from_cookie:
        title = tag_from_cookie
        results = search(tag_from_cookie, flag=1)
    if query_from_cookie:
        title = query_from_cookie
        results = search(query_from_cookie)

    # pagination results
    page = request.args.get('page', 1, type=int)
    results = results.paginate(page=page, per_page=10, error_out=True)

    return render_template('results.html',
                           menu=menu,                 # site menu
                           title=title,               # page title
                           search_form=SearchForm(),  # search field
                           results=results,           # search results
                           )

#TAGS page
@app.route('/tags')
def tags():
    query = request.args.get('search')
    if query:
        return if_query(query, tag='')

    results = tags_db()  # getting tag's list from db

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

    results = best_anecdotes()  # 100 jokes with the highest ratings

    # pagination
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

    results = new_anecdotes()  # 100 latest jokes

    # pagination
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

        if like:               # if user clicked like
            likes(like)        # rating increases by 1
        if dislike:            # if user clicked dislike
            dislikes(dislike)  # rating decreases by 1

    anekdots = random_anekdot()  # 10 random jokes from db

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
            new_tag = str.lower(tags_form.tags.data) # text from tag field
        new_anekdot = text_form.text.data    # text from form field

        # adding to db, the function returns the id of the new joke
        id = add_anekdot(new_anekdot, new_tag)

        # forms need to be cleaned
        # otherwise user will be able to send the same text infinit times
        # captcha does not prevent this
        text_form = TextForm(formdata=None)  # cleaning the text form
        tags_form = TagsForm(formdata=None)  # cleaning the tags form

        # flash message about successful sending
        flash(f'Анекдот добавлен, ему присвоен id - {id}', category='success')
    elif text_form.recaptcha.errors:  # if captcha hasn't worked
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
