from wtforms import Form, StringField, SelectField

# Форма поиска
class SearchForm(Form):
    
    search = StringField('')
    