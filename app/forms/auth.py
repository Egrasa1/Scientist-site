from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo

from app.models import User

class SignUpForm(FlaskForm):
    name = StringField(
        'Нікнейм', 
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Пароль', 
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        'Підтвердження пароля', 
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Зареєструватися')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            flash('Ця електронна адреса вже використовується. Виберіть інший.')
        

class LoginForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Пароль', 
        validators=[DataRequired()]
    )
    remember = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Увійти')


class ProfileForm(FlaskForm):
    name = StringField(
        'Нікнейм', 
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Пароль', 
        validators=[Length(min=6)]
    )
    description = StringField(
        'Опис профілю',
        validators=[Length(max=100)]
    )
    submit = SubmitField('Оновити')