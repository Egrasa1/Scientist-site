import random
from flask import Blueprint, render_template, request
from app.services.parser import parser_science_news
from app.controllers import PostController

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # Отримуємо всі гарячі пости, без обмежень
    hot_posts = PostController.get_post_by_rating(limit=None)

    # Якщо постів більше 4, то вибираємо випадкові 4
    if len(hot_posts) > 4:
        random_hot_posts = random.sample(hot_posts, 4)
    else:
        random_hot_posts = hot_posts  # Якщо постів менше 4, показуємо всі

    return render_template("main.html", hot_posts=random_hot_posts)



@main_bp.route('/about')
def about():
    return render_template('user/about.html')

@main_bp.route('/contacts')
def contacts():
    return render_template('user/contacts.html')

@main_bp.route("/all_news")
def all_news():
    posts = PostController.get_post_by_rating()
    return render_template("news_feed.html", posts=posts)
