# app/services/user_service.py

from app.models.user_model import User
from app import db


class UserService:
    @staticmethod
    def get_or_create_user(auth0_user_id, username):
        user = User.query.filter_by(auth0_user_id=auth0_user_id).first()
        if not user:
            user = User(auth0_user_id=auth0_user_id, username=username)
            db.session.add(user)
            db.session.commit()
        return user

    @staticmethod
    def get_user_by_auth0_id(auth0_user_id):
        return User.query.filter_by(auth0_user_id=auth0_user_id).first()

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()