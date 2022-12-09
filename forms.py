from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField
from wtforms import TextAreaField, SearchField, SubmitField
from wtforms.validators import DataRequired, Length

# Форма добавления анекдотов + капча
class TextForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired(), Length(min=10, max=1000)])
    recaptcha = RecaptchaField()

# Форма поиска
class SearchForm(FlaskForm):
    search = SearchField(validators=[DataRequired(), Length(min=3, max=50)], 
                         render_kw={"placeholder": "Искать здесь..."}
                        )

# Кнопки лайк и дизлайк
class LikeForm(FlaskForm):
    like = SubmitField(render_kw={"class": 'like', "type": 'image', "alt": 'like'})
    dislike = SubmitField(render_kw={"class": 'dislike', "type": 'image', "alt": 'dislike'})
