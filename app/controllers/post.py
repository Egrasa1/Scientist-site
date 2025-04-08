from datetime import datetime
from sqlalchemy.orm import Session
from app.models.posts import Post
from app.models.users import User  # Для перевірки зв'язків

# --- CREATE ---class PostController:
class PostController:
    @staticmethod
    def create_post(db: Session, user_id: int, title: str, content: str) -> Post:
        new_post = Post(
            user_id=user_id,
            title=title,
            content=content,
            create_date=datetime.utcnow()
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    @staticmethod
    def get_post_by_id(db: Session, post_id: int) -> Post:
        return db.query(Post).filter(Post.id == post_id).first()

    @staticmethod
    def get_posts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Post]:
        return db.query(Post).filter(Post.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_all_posts(db: Session, skip: int = 0, limit: int = 100) -> list[Post]:
        return db.query(Post).offset(skip).limit(limit).all()

    @staticmethod
    def update_post_content(db: Session, post_id: int, new_content: str) -> Post:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            post.content = new_content
            db.commit()
            db.refresh(post)
        return post

    @staticmethod
    def update_post_title(db: Session, post_id: int, new_title: str) -> Post:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            post.title = new_title
            db.commit()
            db.refresh(post)
        return post

    @staticmethod
    def delete_post(db: Session, post_id: int) -> bool:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            db.delete(post)
            db.commit()
            return True
        return False

    @staticmethod
    def get_post_with_author(db: Session, post_id: int) -> dict:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            author = db.query(User).filter(User.id == post.user_id).first()
            return {
                "post": post,
                "author": author
            }
        return None