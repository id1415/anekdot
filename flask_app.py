import sqlite3
from flask import Flask, render_template
import json
import random


# def get_db_connection():
#     conn = sqlite3.connect('anek.db')
#     conn.row_factory = sqlite3.Row
#     return conn


app = Flask(__name__)


# @app.route('/')
# def index():
#     conn = get_db_connection()
#     posts = conn.execute('select * from anekdot order by random()').fetchmany(10)
#     print(type(posts))
#     conn.close()
#     return render_template('index.html', posts=posts)
data = json.load(open('anekdot.json', encoding='utf-8'))

# @app.route('/search/<title>')
# def search(word):
#     s1 = []
#     for i in data:
#         if word in i['anekdot']:
#             s1.append(i['anekdot'])
#     # return s1
#     return render_template('search.html', s1=s1)


@app.route('/')
def index():
    s = []
    anekdots = []

    for _ in range(10):
        random_number = random.randint(1, 71360)
        s.append(random_number)
    
    for id in s:
        anekdots.append(f'{id} {data[id]["anekdot"]}')
    return render_template('index.html', posts=anekdots)


if __name__ == '__main__':
    app.run()
