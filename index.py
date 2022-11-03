from flask import Flask, render_template, request
from apps import Search, random_anekdot


app = Flask(__name__)
exm = Search()
menu = [{'name': 'ОБНОВИТЬ', 'url': '/'},
        {'name': 'О САЙТЕ', 'url': 'about'},
        ]


# результаты поиска
def results():
    search = exm.search()

    return render_template('results.html',
                results=search[0],
                pagination=search[1],
                menu=menu,
                )


@app.route('/')
def index():

    global exm
    q = request.args.get('q')  # запрос в поиске
    exm = Search(q)
    if exm.status():
        return results()

    anekdots = random_anekdot()
    return render_template('index.html',
                            anekdots=anekdots,
                            menu=menu,
                            title='Анекдоты',
                            )


@app.route('/about')
def about():

    # копипаст ¯\_(ツ)_/¯
    global exm
    q = request.args.get('q')  # запрос в поиске
    exm = Search(q)
    if exm.status():
        return results()

    return render_template('about.html',
                            menu=menu, 
                            title='О сайте',
                            )


if __name__ == '__main__':
    app.run()
