from app.models import Post

class PostController:
    @staticmethod
    def get_post_by_user(user_id: int):
        return Post.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def check_posts(user_id: int):
        return Post.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def get_post_by_id(post_id: int):
        return Post.query.filter_by(id=post_id).first()
    
    @staticmethod
    def create_post(title: str, content: str, user_id: int, image: str = None):
        post = Post(
            title=title,
            content=content,
            image=image,
            user_id=user_id,
        )
        post.save()

    @staticmethod
    def delete_post(post_id: int):
        post = Post.query.get(post_id)
        if post:
            post.delete()

    @staticmethod
    def update_post(post_id: int, title: str, content: str):
        post = Post.query.get(post_id)
        if post:
            post.title = title
            post.content = content
            post.save()