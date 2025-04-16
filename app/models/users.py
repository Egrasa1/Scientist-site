from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from flask_login import AnonymousUserMixin

from enum import Enum

from .base import Base

class RoleEnum(Enum):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    passwords = Column(String(60), nullable=False)
    email = Column(String(250), unique=True)
    role = Column(SqlEnum(RoleEnum, name="role_enum"), default=RoleEnum.USER, nullable=False)

class AnonymousUser(AnonymousUserMixin):
    pass

posts = relationship('Post', back_populates='author')
likes = relationship('Likes', back_populates='user')