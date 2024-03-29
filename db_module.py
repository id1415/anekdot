# this module is for work with the database
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
# postgresql database is used here
# app.config["SQLALCHEMY_DATABASE_URI"] = postgresql+psycopg2://username:password@host:port/mydatabase
# https://docs.sqlalchemy.org/en/14/core/engines.html
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
Session = sessionmaker(bind=engine)
session = Session()

# there are forth columns in the table (id, text, rating, date)
class Anek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2000), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.Date, nullable=False, default=func.now())

    def __repr__(self):
        return f'[{self.id}, {self.text}, {self.rating}, {self.date}]'


def search(query):
    # if the search query is a number, then id=number is output
    if query.isdigit():
        query = int(query)
        '''SELECT * FROM anek 
        WHERE id = 12345;'''
        posts = Anek.query.filter(Anek.id == query)

    else:  # if the query is not a number
        # if there are words separated ; then the search works by a split occurrence
        if ';' in query and query[0] != ';' and query[-1] != ';':
            query = query.split(';')
            query = [i.strip() for i in query]

            posts = []
            # an sql query is compiled here
            for i in range(len(query)):
                # text ILIKE '%query[i]%'
                posts.append(Anek.text.ilike(f'%{query[i]}%'))

            # if you enter 'word1;word2;word3', then the final sql query will be like this:
            '''SELECT * FROM anek
            WHERE text ILIKE '%word1%'
            AND text ILIKE '%word2%'
            AND text ILIKE '%word3%'
            ORDER BY id DESC;'''
            posts = Anek.query.filter(and_(*posts)).order_by(Anek.id.desc())

        # if there is no ; then the search works by direct occurrence
        else:
            '''SELECT * FROM anek
            WHERE text ILIKE '%word%
            ORDER BY id DESC;'''
            posts = Anek.query.filter(Anek.text.ilike(
                f'%{query}%')).order_by(Anek.id.desc())

    return posts


# output of 10 random jokes to the main page
def random_anekdot():
    '''SELECT * FROM anek
    ORDER BY random()
    LIMIT 10;'''
    lst = Anek.query.order_by(func.random()).limit(10).all()
    return lst


# the function outputs the maximum id - number of jokes in the database
def len_base():
    # SELECT max(id) FROM anek;
    result = db.session.query(func.max(Anek.id)).first()
    return result[0]  # the output is a tuple (12345,) so the index is 0


# add an anecdote to the database
def add_anekdot(new_anekdot):
    # INSERT INTO anek VALUES ('text', 0)
    anekdot = Anek(text=new_anekdot)
    db.session.add(anekdot)
    db.session.commit()
    return anekdot.id


# like
def likes(id):
    '''SELECT * FROM anek
    WHERE id=12345;'''
    like = Anek.query.filter_by(id=id).first()
    '''UPDATE anek SET rating = rating + 1
    WHERE id = 12345;'''
    like.rating += 1  # the rating number increases by 1
    db.session.commit()


# dislike
def dislikes(id):
    '''SELECT * FROM anek
    WHERE id=12345;'''
    dislike = Anek.query.filter_by(id=id).first()
    '''UPDATE anek SET rating = rating - 1
    WHERE id = 12345;'''
    dislike.rating -= 1  # the rating number decreases by 1
    db.session.commit()


# last anecdotes
def new_anecdotes():
    '''SELECT * FROM anek
    ORDER BY date DESC
    LIMIT 100;'''
    # I don't know what from_self() is, but pagination doesn't work without it
    # https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.from_self
    # new = Anek.query.order_by(Anek.date).limit(100).from_self()
    new = Anek.query.filter(Anek.date.isnot(None)).order_by(Anek.date.desc()).limit(100).from_self()
    return new


# best anecdotes
def best_anecdotes():
    '''SELECT * FROM anek
    ORDER BY rating DESC
    LIMIT 100;'''
    best = Anek.query.order_by(Anek.rating.desc()).limit(100).from_self()
    return best
