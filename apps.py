import os
from dotenv import load_dotenv
from flask import Flask
from random import randint
from flask_paginate import Pagination, get_page_args
from flaskext.mysql import MySQL

load_dotenv()
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv('mysql_user')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('mysql_password')
app.config['MYSQL_DATABASE_DB'] = os.getenv('mysql_db')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('mysql_host')
mysql.init_app(app)


class Search:

    def __init__(self, query=None):
        self.query = query  # тип запроса - строка

    def status(self):  # ввёл ли пользователь запрос в поиск
        if self.query != None and self.query != ' ' and 101 > len(self.query) > 2:
            return True

    # поиск и пагинация результатов
    def search(self):
        # results = []  # сюда помещаются результаты поиска
        con = mysql.connect()
        cur = con.cursor()
        # поиск
        mysql_query = cur.execute("SELECT id, text FROM anek WHERE text LIKE %s", ['%' + self.query + '%'])
        results = cur.fetchall()

        total = len(results)  # количество найденных анекдотов

        # page - номер страницы
        # per_page - результатов на страницу
        # offset = (page - 1) * per_page
        page, per_page, offset = get_page_args(page_parameter='page',
                                            per_page_parameter='per_page')
        
        results = results[offset: offset + 10]  # список из 10 анекдотов

        pagination = Pagination(page=page,
                                per_page=per_page,
                                total=total,
                                css_framework='Bootstrap3',
                                display_msg=f'Найдено {total} анекдотов'
                                )
        cur.close()
        con.close()
        return results, pagination


def random_anekdot():

    con = mysql.connect()
    cur = con.cursor()

    anekdots = []
    for _ in range(10):
        random_number = randint(1, 130263)  # выбирается случайное число 1-130263
        
        # вытаскивается анекдот из базы с id - случайным числом
        mysql_query = "SELECT id, text from anek WHERE id = %s"
        cur.execute(mysql_query, (random_number,))
        newline = cur.fetchone()

        anekdots.append({newline[0]: newline[1]})

    cur.close()
    con.close()
    
    return anekdots


# функция вычисляет кол-во анекдотов в базе
# число обновляется если пользователь добавит анекдот и перезайдёт на страницу about
def len_base():

    con = mysql.connect()
    cur = con.cursor()
    cur.execute("SELECT MAX(id) from anek")  # количество анекдотов в базе
    result = cur.fetchone()
    cur.close()
    con.close()
    return result[0]


# добавление анекдота в базу
def add_anekdot(new_anekdot):
    with app.app_context():
        con = mysql.connect()
        cur = con.cursor()
        cur.execute("INSERT INTO anek(cat, text) VALUES (100, %s)", (new_anekdot,))
        con.commit()
        cur.close()
        con.close()
    return cur.lastrowid
