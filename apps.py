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
    anekdots = []
    for _ in range(10):
        random_number = randint(1, 111707)  # выбирается случайное число от 1 до 111707
        newline = data[random_number]["anekdot"]  # анекдот с id - случайным числом
        anekdots.append({random_number: newline})
    
    return anekdots
