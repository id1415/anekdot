from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField
from wtforms import TextAreaField, SearchField, SubmitField
from wtforms.validators import DataRequired, Length

# form for adding jokes and captcha
# the minimum text length is 10 characters, the maximum is 2000
class TextForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired(), Length(min=10, max=2000)])
    recaptcha = RecaptchaField()

# search form
# the minimum text length is 3 characters, the maximum is 50
class SearchForm(FlaskForm):
    search = SearchField(validators=[DataRequired(), Length(min=3, max=50)], 
                         render_kw={"placeholder": "Искать здесь..."})

# like and dislike buttons
class LikeForm(FlaskForm):
    like = SubmitField(render_kw={"class": 'like', "type": 'image', "alt": 'like'})
    dislike = SubmitField(render_kw={"class": 'dislike', "type": 'image', "alt": 'dislike'})

# tag form
# max length = 30
class TagsForm(FlaskForm):
    tags = SearchField(validators=[Length(max=30)])
