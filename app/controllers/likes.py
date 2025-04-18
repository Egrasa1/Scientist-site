from datetime import datetime
# from sqlalchemy.orm import Session
from app.models.likes import Likes
from app.models.users import User
from app.models.posts import Post

class LikesController:
    @staticmethod
    def create_like(user_id: int, post_id: int) -> Likes:
        if not Likes.query.filter(User.id == user_id).first():
            raise ValueError("Користувач не знайдений")
        if not Likes.query.filter(Post.id == post_id).first():
            raise ValueError("Пост не знайдений")

        new_like = Likes(
            user_id=user_id,
            post_id=post_id,
            date=datetime.utcnow()
        )
        new_like.save()

    @staticmethod
    def get_like_by_id(like_id: int) -> Likes:
        return Likes.query.filter_by(Likes.id == like_id).first()

    @staticmethod
    def get_likes_by_user(user_id: int) -> list[Likes]:
        return Likes.query.filter(Likes.user_id == user_id).all()

    @staticmethod
    def get_likes_by_post(post_id: int) -> list[Likes]:
        return Likes.query.filter(Likes.post_id == post_id).all()

    @staticmethod
    def check_user_liked_post(user_id: int, post_id: int) -> bool:
        return Likes.query.filter(
            Likes.user_id == user_id,
            Likes.post_id == post_id
        ).first() is not None

    @staticmethod
    def delete_like(like_id: int) -> bool:
        like = Likes.query.filter(Likes.id == like_id).first()
        if like:
            Likes.delete(like)
            Likes.save()
            return True
        return False

    @staticmethod
    def delete_like_by_user_post(user_id: int, post_id: int) -> bool:
        like = Likes.query.filter(
            Likes.user_id == user_id,
            Likes.post_id == post_id
        ).first()
        if like:
            Likes.delete(like)
            Likes.save()
            return True
        return False

    @staticmethod
    def get_like_details(like_id: int) -> dict:
        like = Likes.query.filter(Likes.id == like_id).first()
        if like:
            return {
                "like": like,
                "user": Likes.query.filter(User.id == like.user_id).first(),
                "post": Likes.query.filter(Post.id == like.post_id).first()
            }
        return None