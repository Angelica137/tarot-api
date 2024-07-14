# app/routes/auth_routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.services.user_service import UserService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = UserService.get_user_by_username(username)
    if user and UserService.check_password(user, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if UserService.user_exists(username):
        return jsonify({"msg": "Username already exists"}), 400

    UserService.create_user(username, password)
    return jsonify({"msg": "User created successfully"}), 201
