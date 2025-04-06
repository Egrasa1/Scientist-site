from sqlalchemy import Column, String, Integer
from .base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    passwords = Column(String(60), nullable=False)
    email = Column(String(250), unique=True)

posts = relationship('Post', back_populates='author')
likes = relationship('Likes', back_populates='user')