
from flask import Blueprint, request, url_for, render_template, redirect, jsonify
from flask_login import current_user

from app.forms import BlogForm

from app.controllers import PostController


blog_bp = Blueprint("blog", __name__, url_prefix="/blog")

@blog_bp.route("/", methods=['GET', 'POST'])
def index():
    check_posts = PostController.checking_posts(current_user.id)
    posts = PostController.get_post_by_id(current_user.id)
    for post in posts:
        post.created_at = post.created_at.strftime('%d.%m.%Y')
    return render_template(
        "blog/index.html", title="Блог", current_page=request.endpoint, check_posts=check_posts, posts=posts
    )

@blog_bp.route("/blog/post", methods=['GET', 'POST'])
def add_post():
    try:
        form = BlogForm(request.form)
        
        if form.validate_on_submit():
            
            PostController.create_post(
                title=form.title.data, 
                content=form.content.data,  
                user_id=current_user.id
                )
                
            return redirect(url_for("blog.index"))
        elif form.is_submitted():
            return render_template(
            "blog/add_post.html", 
            title="Додати пост", 
            current_page=request.endpoint, 
            form=form
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    
@blog_bp.route("/post/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = PostController.get_post_by_id(post_id)

    if not post or current_user.id != post.user_id:
        return redirect(url_for("blog.index"), code=303)

    PostController.delete_post(post_id)

    return redirect(url_for("blog.index"), code=303)




@blog_bp.route("/post/<post_id>/<post_title>", methods=['GET', 'POST'])
def view_post(post_id, post_title):
    post = PostController.get_post_by_id(post_id)
    if post:
        return render_template(
            "blog/view_post.html", 
            title=post.title, 
            current_page=request.endpoint, 
            post=post,
            post_created_at=post.created_at.strftime("%d.%m.%Y"),
            )
    else:
        return redirect(url_for("blog.index"))
    
    
@blog_bp.route("/post/edit/<post_id>/<post_title>", methods=['GET', 'POST'])
def edit_post(post_id, post_title):
    post = PostController.get_post_by_id(post_id)
    if not post:
        return redirect(url_for("blog.index"))

    form = BlogForm(obj=post)
    if form.validate_on_submit():
            PostController.update_post(post_id, form.title.data, form.content.data)
            return redirect(url_for("blog.view_post", post_title=post.title, post_id=post_id))
    elif form.is_submitted():
    
        return render_template(
        "blog/edit_post.html", 
        title="Редагувати пост", 
        current_page=request.endpoint, 
        form=form,
        form_action=url_for("blog.edit_post", post_id=post_id, post_title=post_title)
    )