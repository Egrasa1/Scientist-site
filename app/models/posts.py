from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from datetime import datetime

# from .base import Base
from app import db
from .utils import ModelMixin


class Post(db.Model, ModelMixin):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tittle = Column(String(100), nullable=False)
    image_url = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False, default=0)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    is_parsed = Column(Boolean, default=False)

    author = relationship("User", back_populates="posts")
    likes = relationship("Likes", back_populates="post")
