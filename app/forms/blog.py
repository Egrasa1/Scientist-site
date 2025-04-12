from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length



class BlogForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Контент', validators=[DataRequired()])
    image = StringField('URL зображення', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Опублікувати')