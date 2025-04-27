# from app.models.base import Base, session
from app.models.users import User
import os
from app.models import RoleEnum    

class UserController:
    @staticmethod
    def create_user(name: str, password: str, email: str) -> User:
        new_user = User(
            name=name,
            passwords=password,
            email=email
        )
        new_user.save()

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        return User.query.filter(User.id == user_id).first()

    # @staticmethod
    # def get_all_users(db: session) -> list[User]:
    #     return User.query.all()
    

    
    @staticmethod
    def update_user_name(user_id: int, new_name: str) -> User:
        user = UserController.get_user_by_id(user_id)
        if user:
            user.name = new_name
            User.save()
            User.refresh()
        return user

    @staticmethod
    def update_user_email(user_id: int, new_email: str) -> User:
        user = UserController.get_user_by_id(user_id)
        if user:
            user.email = new_email
            User.save()
            User.refresh()
        return user

    @staticmethod
    def update_user_password(user_id: int, new_password: str) -> User:
        user = UserController.get_user_by_id(user_id)
        if user:
            user.passwords = new_password
            User.save()
            User.refresh()
        return user
    
    @staticmethod
    def update_user_profile_description(user_id: int, new_profile_description: str) -> User:
        user = UserController.get_user_by_id(user_id)
        if user:
            user.profile_description = new_profile_description
            User.save()
            User.refresh()
        return user


    @staticmethod
    def delete_user(user_id: int) -> bool:
        user = UserController.get_user_by_id(user_id)
        if user:
            User.delete(user)
            User.save()
            return True
        return False
    
    
    @staticmethod
    def promote_user_to_admin(user_id: int) -> User:
        user = UserController.get_user_by_id(user_id)
        if user:
            user.role = RoleEnum.ADMIN
            User.save()
            User.refresh()
        return user