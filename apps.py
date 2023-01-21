# этот модуль для работы с бд
# https://docs.sqlalchemy.org/en/14/index.html

import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, and_

load_dotenv()
app = Flask(__name__)
# использую БД postgresql
# app.config["SQLALCHEMY_DATABASE_URI"] = postgresql+psycopg2://username:password@host:port/mydatabase
# https://docs.sqlalchemy.org/en/14/core/engines.html
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# В БД одна таблица и три столбца (id, text, rating)
class Anek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2000), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'[{self.id}, {self.text}, {self.rating}]'

class Search:
    # если перейти на страницу results, то будут выведены анекдоты со словом none
    # либо будут анекдоты с последним поисковым запросом
    def __init__(self, title='None'):
        self._title = title

    # для чтения заголовка
    @property
    def title(self):
        return self._title

    # для записи нового заголовка
    @title.setter
    def title(self, value):
        self._title = value

    # поиск в БД
    def search(self):
        query = self.title
        try:  # если запрос в поиске можно перевести в int, то выводится анекдот с id = int
            query = int(query)
            '''SELECT * FROM anek 
            WHERE id = 12345;'''
            posts = Anek.query.filter(Anek.id == query)

        except ValueError:  # если запрос не переводится в int

            # если в запросе есть слова, разделённые ; то поиск работает по разбавочному вхождению
            if ';' in query and query[0] != ';' and query[-1] != ';':
                query = query.split(';')
                query = [i.strip() for i in query]

                posts = []
                # здесь составляется sql запрос
                for i in range(len(query)):
                    posts.append(Anek.text.ilike(f'%{query[i]}%'))  # text ILIKE '%query[i]%'

                # если в поиск ввести 'американец;немец;русский', то финальный sql запрос будет таким:
                '''SELECT * FROM anek
                WHERE text ILIKE '%американец%'
                AND text ILIKE '%немец%'
                AND text ILIKE '%русский%'
                ORDER BY id DESC;'''
                posts = Anek.query.filter(and_(*posts)).order_by(Anek.id.desc())

            # если ; нет то поиск работает по прямому вхождению
            else:
                '''SELECT * FROM anek
                WHERE text ILIKE '%американец%
                ORDER BY id DESC;'''
                posts = Anek.query.filter(Anek.text.ilike(f'%{query}%')).order_by(Anek.id.desc())

        return posts


# вывод 10 случайных анекдотов на главную страницу
def random_anekdot():
    '''SELECT * FROM anek
    ORDER BY random()
    LIMIT 10;'''
    lst = Anek.query.order_by(func.random()).limit(10).all()
    return lst


# функция выдаёт максимальный id = кол-во анекдотов в базе
def len_base():
    # SELECT max(id) FROM anek;
    result = db.session.query(func.max(Anek.id)).first()
    return result[0]  # на выходе кортеж типа (12345,) поэтому [0]


# добавление анекдота в базу
def add_anekdot(new_anekdot):
    # id прописывается автоматически, указывать его не нужно
    # rating по умолчанию 0 и тоже не указывается в синтаксисе SQLAlchemy
    # но, в моей бд, если составлять sql запрос, rating надо указывать
    # INSERT INTO anek VALUES ('text', 0)
    anekdot = Anek(text=new_anekdot)
    db.session.add(anekdot)
    db.session.commit()
    return anekdot.id


# лайк
def likes(id):
    '''SELECT * FROM anek
    WHERE id=12345;'''
    like = Anek.query.filter_by(id=id).first()
    '''UPDATE anek SET rating = rating + 1
    WHERE id = 12345;'''
    like.rating += 1  # цифра рейтинга увеличивается на 1
    db.session.commit()


# дизлайк
def dislikes(id):
    '''SELECT * FROM anek
    WHERE id=12345;'''
    dislike = Anek.query.filter_by(id=id).first()
    '''UPDATE anek SET rating = rating - 1
    WHERE id = 12345;'''
    dislike.rating -= 1  # цифра рейтинга уменьшается на 1
    db.session.commit()


# новые анекдоты
def new_anecdotes():
    '''SELECT * FROM anek
    ORDER BY id DESC
    LIMIT 100;'''
    # не знаю что такое from_self(), но без него пагинация не работает
    # https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.from_self
    new = Anek.query.order_by(Anek.id.desc()).limit(100).from_self()
    return new


# лучшие анекдоты
def best_anecdotes():
    '''SELECT * FROM anek
    ORDER BY rating DESC
    LIMIT 100;'''
    best = Anek.query.order_by(Anek.rating.desc()).limit(100).from_self()
    return best
