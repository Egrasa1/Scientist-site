from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app.models import User
from app.controllers.user import UserController
from app.controllers.post import PostController

from app.forms import ProfileForm



user_bp = Blueprint('user', __name__)


@user_bp.route("/profile")
@login_required
def profile():
    user_info = UserController.get_user_by_id(current_user.id)  
    posts = PostController.get_post_with_author(current_user.id) or []
    
    if not user_info:
        return render_template("error.html", title="Профіль не знайдено"), 404
    
    return render_template(
        "user/profile.html", 
        title="Профіль",
        user=user_info,
        description=user_info.profile_description or 'Опис профілю відсутній',
        user_name=user_info.name,
        posts=posts
    )
    

@user_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    user = User.query.get(current_user.id)
    form = ProfileForm()

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.profile_description = form.description.data
        user.save()
        flash("Профіль успішно оновлено", "info")
        return redirect(url_for("user.profile.html"))
        
    elif request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.description.data = user.profile_description
        
    return render_template("user/settings.html", form=form)