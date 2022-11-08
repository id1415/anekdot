import sqlite3
from random import randint
from flask_paginate import Pagination, get_page_args

# подключение к базе данных
con = sqlite3.connect("a.db", check_same_thread=False)
cur = con.cursor()

sqlite_query = cur.execute("SELECT Count(*) from anekdot")
raw = cur.fetchone() # raw[0] - количество анекдотов в базе

class Search:

    def __init__(self, query=None):
        self.query = query  # тип запроса - строка

    def status(self):  # ввёл ли пользователь запрос в поиск
        if self.query != None and self.query != ' ' and 101 > len(self.query) > 2:
            return True

    # поиск и пагинация результатов
    def search(self):
        results = []  # сюда помещаются результаты поиска

        # поиск
        sqlite_query = "SELECT id, text FROM anekdot"
        cur.execute(sqlite_query)
        records = cur.fetchall()
        for record in records:
            if self.query.lower() in record[1].lower():
                results.append({record[0]: record[1]})

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

        return results, pagination


def random_anekdot():

    anekdots = []
    for _ in range(10):
        random_number = randint(1, 114060)  # выбирается случайное число от 1 до 111707
        
        # вытаскивается анекдот из базы с id - случайным числом
        sqlite_query = "SELECT text from anekdot WHERE id = ?"
        cur.execute(sqlite_query, (random_number,))
        newline = cur.fetchone()

        anekdots.append({random_number: newline[0]})
    
    return anekdots


# функция вычисляет кол-во анекдотов в базе
# число обновляется если пользователь добавит анекдот и перезайдёт на страницу about
def len_base():
    con = sqlite3.connect("a.db", check_same_thread=False)
    cur = con.cursor()
    sqlite_query = cur.execute("SELECT Count(*) from anekdot")
    raw = cur.fetchone() # raw[0] - количество анекдотов в базе

    return raw


# добавление анекдота в базу
def add_anekdot(new_anekdot):
    try:
        cur.execute("INSERT INTO anekdot(text) VALUES (?)", (new_anekdot,))
        con.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return False
    except sqlite3.OperationalError:
        return False
