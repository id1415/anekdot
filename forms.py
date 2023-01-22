from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField
from wtforms import TextAreaField, SearchField, SubmitField
from wtforms.validators import DataRequired, Length

# форма добавления анекдотов и капча
# минимальная длина текста - 10 символов, максимальная - 2000
class TextForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired(), Length(min=10, max=2000)])
    recaptcha = RecaptchaField()

# форма поиска
# минимальная длина текста - 3 символа, максимальная - 50
class SearchForm(FlaskForm):
    search = SearchField(validators=[DataRequired(), Length(min=3, max=50)], 
                         render_kw={"placeholder": "Искать здесь..."})

# кнопки лайк и дизлайк
class LikeForm(FlaskForm):
    like = SubmitField(render_kw={"class": 'like', "type": 'image', "alt": 'like'})
    dislike = SubmitField(render_kw={"class": 'dislike', "type": 'image', "alt": 'dislike'})
