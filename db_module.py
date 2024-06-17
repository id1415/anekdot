# this module is for work with db
# https://docs.sqlalchemy.org/en/14/index.html

import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, and_
from sqlalchemy import create_engine, case, desc
from sqlalchemy.orm import sessionmaker

load_dotenv()
app = Flask(__name__)
# postgres is used here
# app.config["SQLALCHEMY_DATABASE_URI"] = postgresql+psycopg2://username:password@host:port/mydatabase
# https://docs.sqlalchemy.org/en/14/core/engines.html
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
Session = sessionmaker(bind=engine)
session = Session()

# there are five columns in the table (id, text, rating, date, tags)
class Anek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2000), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.Date, nullable=False, default=func.now())
    tags = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f'[{self.id}, {self.text}, {self.rating}, {self.date}, {self.tags}]'

#copy table to file
'''
with app.app_context():
    posts = Anek.query.all()
    with open('db_copy.txt', 'w') as file:
        for post in posts:
            file.write(f'({post.id}, {post.text}, {post.rating}, {post.date}, {post.tags}),\n')
'''

def search(query, flag=0): #flag for tags
    if flag == 1:
        '''
        SELECT * FROM anek
        WHERE tags = 'query';
        '''
        posts = Anek.query.filter(Anek.tags == query)

    # if search query is a number then id=number is output
    elif query.isdigit() and type(query.isdigit()) != None:
        query = int(query)
        '''
        SELECT * FROM anek 
        WHERE id = 12345;
        '''
        posts = Anek.query.filter(Anek.id == query)

    # if the query is not a number
    else:
        # if there are words separated ; then search works by a split occurrence
        if ';' in query and query[0] != ';' and query[-1] != ';':
            query = query.split(';')
            query = [i.strip() for i in query]

            posts = []
            # sql query is created here
            for i in range(len(query)):
                # text ILIKE '%query[i]%'
                posts.append(Anek.text.ilike(f'%{query[i]}%'))

            # if you enter 'word1;word2;word3' then the final sql query will be like this:
            '''
            SELECT * FROM anek
            WHERE text ILIKE '%word1%'
            AND text ILIKE '%word2%'
            AND text ILIKE '%word3%'
            ORDER BY id DESC;
            '''
            posts = Anek.query.filter(and_(*posts)).order_by(Anek.id.desc())

        # if there is no ; then the search works by direct occurrence
        else:
            '''
            SELECT * FROM anek
            WHERE text ILIKE '%word%
            ORDER BY id DESC;
            '''
            posts = Anek.query.filter(Anek.text.ilike(
                f'%{query}%')).order_by(Anek.id.desc())

    return posts

# List of tags
def tags_db():
    '''
    SELECT DISTINCT tags from anek
    WHERE tags != '';
    '''
    lst = []
    for tag in session.query(Anek.tags.distinct()):
        if tag[0] != '':
            lst.extend(tag)

    lst.sort() # sort by alphabet
    return lst

# output of 10 random jokes to the main page
def random_anekdot():
    '''
    SELECT * FROM anek
    ORDER BY random()
    LIMIT 10;
    '''
    lst = Anek.query.order_by(func.random()).limit(10).all()
    return lst


# the function outputs the maximum id - number of jokes in the database
def len_base():
    # SELECT max(id) FROM anek;
    result = db.session.query(func.max(Anek.id)).first()
    return result[0]  # the output is a tuple (12345,) so the index is 0


# add an anecdote to the database
def add_anekdot(new_anekdot, new_tag):
    # INSERT INTO anek VALUES ('text', 0, new_tag)
    # id and date are put automatically according to the field settings in db
    anekdot = Anek(text=new_anekdot, tags=new_tag)
    db.session.add(anekdot)
    db.session.commit()
    return anekdot.id


# like
def likes(id):
    '''
    SELECT * FROM anek
    WHERE id=12345;
    '''
    like = Anek.query.filter_by(id=id).first()
    '''
    UPDATE anek SET rating = rating + 1
    WHERE id = 12345;
    '''
    like.rating += 1  # the rating number increases by 1
    db.session.commit()


# dislike
def dislikes(id):
    '''
    SELECT * FROM anek
    WHERE id=12345;
    '''
    dislike = Anek.query.filter_by(id=id).first()
    '''
    UPDATE anek SET rating = rating - 1
    WHERE id = 12345;
    '''
    dislike.rating -= 1  # the rating number decreases by 1
    db.session.commit()


# last anecdotes
def new_anecdotes():
    '''
    SELECT * FROM anek
    ORDER BY date DESC
    LIMIT 100;
    '''
    # I don't know what from_self() is but pagination doesn't work without it
    # https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.from_self
    # some lines are without date in my db so I use .isnot(None)
    new = Anek.query.filter(Anek.date.isnot(None)).order_by(Anek.date.desc()).limit(100).from_self()
    return new


# best anecdotes
def best_anecdotes():
    '''
    SELECT * FROM anek
    ORDER BY rating DESC
    LIMIT 100;
    '''
    best = Anek.query.order_by(Anek.rating.desc()).limit(100).from_self()
    return best
