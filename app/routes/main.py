from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required, logout_user

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    return render_template("main.html", title="Egrasa | Наукові новини")