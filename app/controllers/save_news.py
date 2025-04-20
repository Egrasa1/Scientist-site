from models import Post, User
from services import parser_science_news
from datetime import datetime

def save_news(news):
    try:
        admin_user = User.query.filter_by(role='admin').first()

        for news_item in news:
            content = f"{news_item.get('lead', '')}\n\n{news_item.get('description', '')}"

            new_post = Post(
                tittle=news_item.get('title', 'No title'),
                content=content,
                image_url=news_item.get('image_url'),
                user_id=admin_user.id if admin_user else None,
                is_parsed=True,
                create_date=datetime.utcnow()
            )
            new_post.save()
            
    except:
        pass
