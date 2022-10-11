from flask import Flask, render_template, request
import json
import random


app = Flask(__name__)
data = json.load(open('anekdot.json', encoding='utf-8'))


@app.route('/')
def index():
    query = request.args.get('q')
    if query != None:
        return render_template('results.html', results=search(query))

    s = []
    anekdots = []
    for _ in range(10):
        random_number = random.randint(1, 71360)
        s.append(random_number)
    for id in s:
        newline = data[id]["anekdot"]
        anekdots.append(f'{id}\n{newline}')
        
    return render_template('index.html', anekdots=anekdots)


def search(q):
    q = request.args.get('q')
    s1 = []
    for anekdot in data:
        if str(q).lower() in anekdot['anekdot'].lower():
            s1.append(anekdot['anekdot'])
    return s1


if __name__ == '__main__':
    app.run()
