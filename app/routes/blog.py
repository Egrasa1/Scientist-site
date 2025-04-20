from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required, logout_user

blog_bp = Blueprint("blog", __name__)