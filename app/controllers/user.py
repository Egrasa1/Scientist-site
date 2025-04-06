from app.models import User


class UserController:
    @staticmethod
    def get_user_info(id: int):
        user = User.query.filter_by(id=id).first()
        if user:
            return {"name": user.name, "email": user.email, 'about': user.about}
        return None