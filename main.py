from flask import Flask, render_template, request
import json
import random
from forms import SearchForm


app = Flask(__name__)
data = json.load(open('anekdot.json', encoding='utf-8'))
s1 = []

# Ввод в поиск
@app.route('/search', methods=['GET', 'POST'])
def search():
    global s1
    search = SearchForm(request.form)
    s1 = []
    if request.method == 'POST':
        for anekdot in data:
            if search.data['search'] in anekdot['anekdot']:
                s1.append(anekdot['anekdot'])
        return search_results(search)

    return render_template('search.html', form=search)

# Результат поиска
@app.route('/results')
def search_results(search):
    results = s1
    return render_template('results.html', results=results)


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
