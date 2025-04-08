from datetime import datetime
from sqlalchemy.orm import Session
from app.models.likes import Likes
from app.models.users import User
from app.models.posts import Post

class LikesController:
    @staticmethod
    def create_like(db: Session, user_id: int, post_id: int) -> Likes:
        if not db.query(User).filter(User.id == user_id).first():
            raise ValueError("Користувач не знайдений")
        if not db.query(Post).filter(Post.id == post_id).first():
            raise ValueError("Пост не знайдений")

        new_like = Likes(
            user_id=user_id,
            post_id=post_id,
            date=datetime.utcnow()
        )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return new_like

    @staticmethod
    def get_like_by_id(db: Session, like_id: int) -> Likes:
        return db.query(Likes).filter(Likes.id == like_id).first()

    @staticmethod
    def get_likes_by_user(db: Session, user_id: int) -> list[Likes]:
        return db.query(Likes).filter(Likes.user_id == user_id).all()

    @staticmethod
    def get_likes_by_post(db: Session, post_id: int) -> list[Likes]:
        return db.query(Likes).filter(Likes.post_id == post_id).all()

    @staticmethod
    def check_user_liked_post(db: Session, user_id: int, post_id: int) -> bool:
        return db.query(Likes).filter(
            Likes.user_id == user_id,
            Likes.post_id == post_id
        ).first() is not None

    @staticmethod
    def delete_like(db: Session, like_id: int) -> bool:
        like = db.query(Likes).filter(Likes.id == like_id).first()
        if like:
            db.delete(like)
            db.commit()
            return True
        return False

    @staticmethod
    def delete_like_by_user_post(db: Session, user_id: int, post_id: int) -> bool:
        like = db.query(Likes).filter(
            Likes.user_id == user_id,
            Likes.post_id == post_id
        ).first()
        if like:
            db.delete(like)
            db.commit()
            return True
        return False

    @staticmethod
    def get_like_details(db: Session, like_id: int) -> dict:
        like = db.query(Likes).filter(Likes.id == like_id).first()
        if like:
            return {
                "like": like,
                "user": db.query(User).filter(User.id == like.user_id).first(),
                "post": db.query(Post).filter(Post.id == like.post_id).first()
            }
        return None