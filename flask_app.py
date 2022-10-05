import sqlite3
from flask import Flask, render_template


def get_db_connection():
    conn = sqlite3.connect('anek.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('select * from anekdot order by random()').fetchmany(10)
    conn.close()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run()
