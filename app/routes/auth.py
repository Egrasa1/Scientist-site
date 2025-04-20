from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_user, logout_user

from app.forms import SignUpForm, LoginForm
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    register_form = SignUpForm(request.form)
    if register_form.validate_on_submit():
        user = User (
            name = register_form.name.data,
            email = register_form.email.data,
            password = register_form.password.data
        )
        user.save()
        login_user(user)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', register_form=register_form)



@auth_bp.route('/login', methods=['POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return redirect(url_for('main.index'))
    return render_template('login.html', login_form=login_form)

