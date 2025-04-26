from datetime import datetime

# from sqlalchemy.orm import Session
from app.models import User, Post  # Для перевірки зв'язків


# --- CREATE ---class PostController:
class PostController:
    @staticmethod
    def create_post(user_id: int, title: str, content: str) -> Post:
        new_post = Post(
            user_id=user_id,
            title=title,
            content=content,
            create_date=datetime.utcnow(),
        )
        new_post.save()

    @staticmethod
    def get_post_by_id(post_id: int) -> Post:
        return Post.query.filter(Post.id == post_id).first()

    @staticmethod
    def get_post_by_tittle(tittle: str) -> Post:
        return Post.query.filter(Post.tittle == tittle).first()

    @staticmethod
    def get_posts_by_user(user_id: int):
        return Post.query.filter_by(Post.user_id == user_id).all()

    @staticmethod
    def get_paginate_posts(page=1, per_page=8):
        return Post.query.order_by(Post.create_date.desc()).paginate(
            page=page, per_page=per_page
        )

    @staticmethod
    def checking_posts(user_id: int):
        return Post.query.filter_by(user_id=user_id).first()

    @classmethod
    def search_posts(cls, query):
        if not query:
            return []
        
        search_pattern = f"%{query}%"
        
        results = Post.query.filter(
            Post.tittle.ilike(search_pattern) | 
            Post.content.ilike(search_pattern)
        ).order_by(Post.create_date.desc()).all()
        return results

    @staticmethod
    def get_post_by_rating(limit: int = 3) -> list[Post]:
        return Post.query.filter_by(rating="🔥🔥Варто переглянути🔥🔥").limit(limit).all()

    @staticmethod
    def update_post(post_id: int, title: str, content: str) -> Post:
        post = Post.query.filter(Post.id == post_id).first()
        if post:
            post.tittle = title
            post.content = content
            Post.save()
            Post.refresh()
        return post

    @staticmethod
    def update_post_content(post_id: int, new_content: str) -> Post:
        post = Post.query.filter(Post.id == post_id).first()
        if post:
            post.content = new_content
            Post.save()
            Post.refresh()
        return post

    @staticmethod
    def delete_post(post_id: int) -> bool:
        post = Post.query.filter(Post.id == post_id).first()
        if post:
            Post.delete(post)
            Post.save()
            return True
        return False

    @staticmethod
    def get_post_with_author(post_id: int) -> dict:
        post = Post.query.filter(Post.id == post_id).first()
        if post:
            author = Post.query.filter(User.id == post.user_id).first()
            return {"post": post, "author": author}
        return None
