
from flask import Blueprint, request, url_for, render_template, redirect, jsonify
from flask_login import current_user

from app.forms import BlogForm, SearchForm

from app.controllers import PostController


content_bp = Blueprint("content", __name__, url_prefix="/blog")

@content_bp.route("/", methods=['GET', 'POST'])
def index():
    check_posts = PostController.checking_posts(current_user.id)
    posts = PostController.get_post_by_id(current_user.id)
    return render_template(
        "blog/index.html", title="Блог", current_page=request.endpoint, check_posts=check_posts, posts=posts
    )
    
@content_bp.route("/scientific-news", methods=['GET'])
def news_feed():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('query', '').strip()
        
    if search_query:
        posts = PostController.search_posts(query=search_query)
        pagination = None
    else:
        pagination = PostController.get_paginate_posts(page) 
        posts = pagination.items
        
    return render_template(
        "news_feed.html", 
        title="Научні новини", 
        search_query=search_query, 
        current_page=request.endpoint, 
        posts=posts, 
        pagination=pagination)

@content_bp.route("/blog/post", methods=['GET', 'POST'])
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
    
    
@content_bp.route("/post/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = PostController.get_post_by_id(post_id)

    if not post or current_user.id != post.user_id:
        return redirect(url_for("blog.index"), code=303)

    PostController.delete_post(post_id)

    return redirect(url_for("blog.index"), code=303)




@content_bp.route("/post/<post_id>/<post_title>", methods=['GET', 'POST'])
def view_post(post_id, post_title):
    post = PostController.get_post_by_id(post_id)
    if post:
        return render_template(
            "blog/view_post.html", 
            title=post.title, 
            current_page=request.endpoint, 
            post=post,
            post_create_date=post.create_date.strftime("%d.%m.%Y"),
            )
    else:
        return redirect(url_for("blog.index"))
    
    
@content_bp.route("/post/edit/<post_id>/<post_title>", methods=['GET', 'POST'])
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