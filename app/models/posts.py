from sqlalchemy import Column, String, Integer, ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='likes')
    tittle = Column(String(100), nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow)