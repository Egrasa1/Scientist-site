import logging
from datetime import datetime

from app.models import User, RoleEnum, Post
from app.services import parser_science_news


def savef_news():
    logging.info("Процес збереження новостей")
    try:
        admin_user = User.query.filter_by(role=RoleEnum.ADMIN).first()

        if not admin_user:
            logging.error("В базі данних не було знайдено админа")
            return False

        news_item = parser_science_news()
        if not news_item:
            logging.warning("Парсер не повернув жодних новин")
            return False

        for news_item in news_item:
            content = f"{news_item['lead']}\n\n{news_item.get('description', '')}"

            new_post = Post(
                tittle=news_item.get("title", "No title"),
                content=content,
                image_url=news_item.get("image_url"),
                user_id=admin_user.id if admin_user else None,
                rating=news_item.get("rating"),
                # is_parsed=True,
                create_date=datetime.utcnow(),
            )
            new_post.save()
            logging.info(f"Збереженно пост: {news_item['title']}")
    except Exception as e:
        logging.error(f"Помилка в save_news: {str(e)}")
        return False
