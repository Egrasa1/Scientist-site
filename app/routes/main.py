from flask import Blueprint, render_template, request

from app.controllers import PostController

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    return render_template("main.html", title="Egrasa | Наукові новини")



@main_bp.route("/contacts")
def contacts():
    return render_template(
        "contacts.html", title="Контакти", current_page=request.endpoint
    )

@main_bp.route("/about")
def about():
    return render_template(
        "about.html", title="Про нас", current_page=request.endpoint
    )
