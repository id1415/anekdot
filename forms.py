from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField
from wtforms import TextAreaField, SearchField
from wtforms.validators import DataRequired, Length

# Форма добавления анекдотов + капча
class TextForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired(), Length(min=10, max=500)])
    recaptcha = RecaptchaField()

# Форма поиска
class SearchForm(FlaskForm):
    search = SearchField(validators=[DataRequired(), Length(min=3, max=30)], render_kw={"placeholder": "Искать здесь..."})
