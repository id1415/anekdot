from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField
from wtforms import TextAreaField, SearchField
from wtforms.validators import DataRequired, Length
 
 
class TextForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired(), Length(min=10, max=500)])
    recaptcha = RecaptchaField()
