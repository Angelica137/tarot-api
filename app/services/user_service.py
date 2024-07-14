# app/services/user_service.py

from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import User
from app import db

class UserService:
    @staticmethod
    def create_user(username, password):
        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def check_password(user, password):
        return check_password_hash(user.password_hash, password)

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def user_exists(username):
        return User.query.filter_by(username=username).first() is not None
