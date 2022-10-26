from json import load
from random import randint

data = load(open('anekdot.json', encoding='utf-8'))  # загрузка json файла с анекдотами


class Search:
    def __init__(self, query):
        self.query = query

    def status(self):  # ввёл ли пользователь запрос в поиск
        if self.query != None and self.query != ' ' and 101 > len(self.query) > 2:
            return True


def random_anekdot():
    id = []
    anekdots = []
    for _ in range(10):  # выбираются 10 случайных чисел от 1 до 111707
        random_number = randint(1, 111707)
        id.append(random_number)
    for i in id:  # добавляются анекдоты с id - случайными числами
        newline = data[i]["anekdot"]
        anekdots.append(f'{i}\n{newline}')
    
    return anekdots
