import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, and_

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Anek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2000), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'[{self.id}, {self.text}, {self.rating}]'


# поиск и пагинация результатов
def search(query):
    try:  # если запрос в поиске можно перевести в int, то выводится анекдот с id = int
        query = int(query)
        posts = Anek.query.filter(Anek.id == query)

    except ValueError:  # если запрос не переводится в int

        # если в запросе есть слова, разделённые ; то поиск работает по разбавочному вхождению
        if ';' in query and query[0] != ';' and query[-1] != ';':
            query = query.split(';')
            query = [i.strip() for i in query]

            posts = []
            for i in range(len(query)):
                posts.append(Anek.text.like(f'%{query[i]}%'))

            posts = Anek.query.filter(and_(*posts)).order_by(Anek.id.desc())

        # если ; нет то поиск работает по прямому вхождению
        else:
            posts = Anek.query.filter(Anek.text.ilike(f'%{query}%')).order_by(Anek.id.desc())
    
    return posts


# вывод 10 случайных анекдотов на главную страницу
def random_anekdot():
    lst = Anek.query.order_by(func.random()).limit(10).all()
    return lst


# функция выдаёт максимальный id = кол-во анекдотов в базе
def len_base():
    result = db.session.query(func.max(Anek.id)).first()
    return result[0]


# добавление анекдота в базу
def add_anekdot(new_anekdot):
    anekdot = Anek(text=new_anekdot)
    db.session.add(anekdot)
    db.session.commit()
    return anekdot.id


# лайк
def likes(id):
    like = Anek.query.filter_by(id=id).first()
    like.rating += 1
    db.session.commit()


# дизлайк
def dislikes(id):
    dislike = Anek.query.filter_by(id=id).first()
    dislike.rating -= 1
    db.session.commit()


# новые анекдоты
def new_anecdotes():
    new = Anek.query.order_by(Anek.id.desc()).limit(100).from_self()
    return new


# лучшие анекдоты
def best_anecdotes():
    best = Anek.query.order_by(Anek.rating.desc()).limit(100).from_self()
    return best
