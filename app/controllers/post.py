from datetime import datetime
import logging
from sqlalchemy.orm import joinedload
from app.models import User, Post  # Для перевірки зв'язків


# --- CREATE ---class PostController:
class PostController:
    @staticmethod
    def create_post(user_id: int, title: str, content: str, rating: int = 0) -> Post:
        new_post = Post(
            user_id=user_id,
            tittle=title,
            content=content,
            rating=rating, 
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
        return Post.query.filter(Post.user_id == user_id, Post.is_parsed == False).all()

    @staticmethod
    def get_paginate_posts(page=1, per_page=8, is_parsed=True):
        query = Post.query

        if is_parsed is not None:
            query = query.filter(Post.is_parsed == is_parsed)

        return query.order_by(Post.create_date.desc()).paginate(
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
            post.save()
            post.refresh()
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
            post.delete()
            logging.info(f"Пост із ID {post_id} видалено.")
            return True
        logging.warning(f"Пост із ID {post_id} не знайдено.")
        return False

    @staticmethod
    def get_post_with_author(user_id: int) -> list:
        return (
        Post.query.join(User, Post.user_id == User.id)
        .filter(Post.user_id == user_id, Post.is_parsed == False)
        .order_by(User.name)  
        .all()
    )
        
    @staticmethod
    def get_not_parsed_posts() -> list[Post]:
        return Post.query.options(joinedload(Post.author)).filter_by(is_parsed=False).all()