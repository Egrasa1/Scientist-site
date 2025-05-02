import random
from flask import Blueprint, render_template, request
from app.services.parser import parser_science_news
from app.controllers import PostController

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    hot_posts = PostController.get_post_by_rating()

    random_hot_posts = random.sample(hot_posts, 4)

    return render_template("main.html", hot_posts=random_hot_posts)


@main_bp.route('/about')
def about():
    return render_template('user/about.html')

@main_bp.route('/contacts')
def contacts():
    return render_template('user/contacts.html')