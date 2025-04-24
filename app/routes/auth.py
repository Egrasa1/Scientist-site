from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_user, logout_user

from app.forms import SignUpForm, LoginForm
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', register_form=register_form)

@auth_bp.route("/sign-out", methods=["GET"])
def signout():
    logout_user()
    flash("Вихід успішний.", "success")
    return redirect(url_for("main.index"))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if login_form.validate_on_submit():
        user = User.authenticate(login_form.email.data, login_form.password.data)
        if user:
            login_user(user, remember=login_form.remember.data)
            flash("Вхід успішний.", "success")
            return redirect(url_for('main.index'))
        else:
            flash("Неправильний емейл або пароль.", "danger")
    return render_template('auth/login.html', login_form=login_form)

