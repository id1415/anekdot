import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, and_

load_dotenv()
app = Flask(__name__)
# использую БД postgresql
# мой доступ выглядит так: postgresql+psycopg2://username:password@host:port/mydatabase
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


# поиск в БД
def search(query):
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
                posts.append(Anek.text.ilike(f'%{query[i]}%'))  # text LIKE '%query[i]%'

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
    # чтобы добавить анекдот в базу, достаточно прописать только text
    # id, rating прописываются автоматически
    anekdot = Anek(text=new_anekdot)
    db.session.add(anekdot)
    db.session.commit()
    return anekdot.id


# лайк
def likes(id):
    '''SELECT * FROM anek
    WHERE id=12345;'''
    like = Anek.query.filter_by(id=id).first()
    like.rating += 1  # цифра рейтинга увеличивается на 1
    db.session.commit()


# дизлайк
def dislikes(id):
    '''SELECT * FROM anek
    WHERE id=12345;'''
    dislike = Anek.query.filter_by(id=id).first()
    dislike.rating -= 1  # цифра рейтинга уменьшается на 1
    db.session.commit()


# новые анекдоты
def new_anecdotes():
    '''SELECT * FROM anek
    ORDER BY id DESC
    LIMIT 100;'''
    # не знаю что такое from_self(), но без него пагинация не работает
    new = Anek.query.order_by(Anek.id.desc()).limit(100).from_self()
    return new


# лучшие анекдоты
def best_anecdotes():
    '''SELECT * FROM anek
    ORDER BY rating DESC
    LIMIT 100;'''
    # не знаю что такое from_self(), но без него пагинация не работает
    best = Anek.query.order_by(Anek.rating.desc()).limit(100).from_self()
    return best
