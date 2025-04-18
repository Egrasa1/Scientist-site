from datetime import datetime

# from sqlalchemy.orm import Session
from app.models.posts import Post
from app.models.users import User  # Для перевірки зв'язків


# --- CREATE ---class PostController:
class PostController:
    @staticmethod
    def create_post(user_id: int, title: str, content: str) -> Post:
        new_post = Post(
            user_id=user_id, 
            title=title, 
            content=content, 
            create_date=datetime.utcnow()
        )
        new_post.save()

    @staticmethod
    def get_post_by_id(post_id: int) -> Post:
        return Post.query.filter(Post.id == post_id).first()

    @staticmethod
    def get_posts_by_user(user_id: int, skip: int = 0, limit: int = 100) -> list[Post]:
        return (
            Post.query.filter(Post.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_all_posts(skip: int = 0, limit: int = 100) -> list[Post]:
        return Post.query.offset(skip).limit(limit).all()

    @staticmethod
    def update_post_content(post_id: int, new_content: str) -> Post:
        post = Post.query.filter(Post.id == post_id).first()
        if post:
            post.content = new_content
            Post.save()
            Post.refresh()
        return post

    @staticmethod
    def update_post_title(post_id: int, new_title: str) -> Post:
        post = Post.query.filter(Post.id == post_id).first()
        if post:
            post.title = new_title
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
