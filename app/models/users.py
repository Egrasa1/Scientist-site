from sqlalchemy import Enum as SqlEnum
from enum import Enum

from sqlalchemy import Column, String, Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# from .base import Base
from app import db
from .utils import ModelMixin

class RoleEnum(Enum):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

class User(db.Model, ModelMixin, UserMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    passwords = Column(String(60), nullable=False)
    email = Column(String(250), unique=True)
    role = Column(SqlEnum(RoleEnum, name="role_enum"), default=RoleEnum.USER, nullable=False)

    posts = relationship('Post', back_populates='author')
    likes = relationship('Likes', back_populates='user')
    
    @hybrid_property
    def password(self):
        return self.passwords
    
    @password.setter
    def password(self, password):
        self.passwords = generate_password_hash(password)
        
    @classmethod
    def authenticate(cls, user_email, password):
        user = cls.query.filter(func.lower(cls.email) == func.lower(user_email)).first()
        if user is not None and check_password_hash(user.password, password):
            return user

class AnonymousUser(AnonymousUserMixin):
    pass
