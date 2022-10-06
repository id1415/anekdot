from flask import Flask, render_template
import json
import random


app = Flask(__name__)
data = json.load(open('anekdot.json', encoding='utf-8'))


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
