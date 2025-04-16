from flask import Blueprint, redirect, url_for, render_template
from app.forms import SignUpForm, LoginForm, ProfileForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=["GET"])
def base():
    login_form = LoginForm()
    register_form = SignUpForm()
    return render_template("base.html", login_form=login_form, register_form=register_form)



@auth_bp.route('/reg', methods=['POST'])
def register():
    register_form = SignUpForm()
    if register_form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('base.html', register_form=register_form)



@auth_bp.route('/log', methods=['POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('base.html', login_form=login_form)

