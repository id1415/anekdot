from flask import Flask
from flask_paginate import Pagination, get_page_args
from flaskext.mysql import MySQL

app = Flask(__name__)  # инициализатор фреймворка Flask
mysql = MySQL()        # инициализатор бд MySQL
mysql.init_app(app)    # ещё один инициализатор


# поиск и пагинация результатов
def search(query):

    # соединение с базой данных
    con = mysql.connect()
    cur = con.cursor()

    try:  # если запрос в поиске можно перевести в int...
        query = int(query)
        cur.execute("SELECT id, text FROM anek where id=%s", query)
        results = cur.fetchall()  # ...то выводится анекдот с id = int
    except ValueError:  # если нельзя...
        cur.execute("SELECT id, text FROM anek WHERE text LIKE %s ORDER BY id DESC", ['%' + query + '%'])
        results = cur.fetchall()  # ...то поиск работает по прямому вхождению

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
                            display_msg=f'Найдено {total} анекдотов',
                            )

    return results, pagination


# вывод 10 случайных анекдотов на главную страницу
def random_anekdot():

    # соединение с базой данных
    con = mysql.connect()
    cur = con.cursor()

    # SQL запросы
    cur.execute("SELECT @min := MIN(id), @max := MAX(id) FROM anek")
    cur.fetchone()
    cur.execute("""
                SELECT DISTINCT id, text 
                FROM anek AS a 
                JOIN ( SELECT FLOOR(@min + (@max - @min + 1) * RAND()) AS id 
                FROM anek LIMIT 11) 
                b USING (id)
                LIMIT 10
                """)
    anekdots = cur.fetchall()
    
    return anekdots


# функция вычисляет кол-во анекдотов в базе
def len_base():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute("SELECT count(*) from anek")  # количество анекдотов в базе
    result = cur.fetchone()
    return result[0]


# добавление анекдота в базу
def add_anekdot(new_anekdot):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute("INSERT INTO anek(cat, text) VALUES (100, %s)", (new_anekdot,))
    con.commit()
    return cur.lastrowid
