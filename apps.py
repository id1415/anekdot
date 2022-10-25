from json import load

data = load(open('anekdot.json', encoding='utf-8'))  # загрузка json файла с анекдотами

class Search:
    def __init__(self, query):
        self.query = query

    def status(self):  # ввёл ли пользователь запрос в поиске
        if self.query != None and self.query != ' ' and 100 > len(self.query) > 2:
            return True
