# tests/test_auth_routes.py

import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from app.routes.auth_routes import auth_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    app.register_blueprint(auth_bp)

    jwt = JWTManager(app)

    return app


def test_login_success(client):
    with patch('app.services.user_service.UserService.get_user_by_username') as mock_get_user, \
         patch('app.services.user_service.UserService.check_password') as mock_check_password:

        mock_get_user.return_value = {'id': 1, 'username': 'testuser'}
        mock_check_password.return_value = True

        response = client.post('/login', json={
            'username': 'testuser',
            'password': 'password123'
        })

        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data


def test_login_failure(client):
    with patch('app.services.user_service.UserService.get_user_by_username') as mock_get_user, \
         patch('app.services.user_service.UserService.check_password') as mock_check_password:

        mock_get_user.return_value = None
        mock_check_password.return_value = False

        response = client.post('/login', json={
            'username': 'wronguser',
            'password': 'wrongpassword'
        })

        assert response.status_code == 401
        data = response.get_json()
        assert data['msg'] == 'Bad username or password'


def test_register_success(client):
    with patch('app.services.user_service.UserService.user_exists') as mock_user_exists, \
         patch('app.services.user_service.UserService.create_user') as mock_create_user:

        mock_user_exists.return_value = False

        response = client.post('/register', json={
            'username': 'newuser',
            'password': 'newpassword'
        })

        assert response.status_code == 201
        data = response.get_json()
        assert data['msg'] == 'User created successfully'


def test_register_user_exists(client):
    with patch('app.services.user_service.UserService.user_exists') as mock_user_exists:

        mock_user_exists.return_value = True

        response = client.post('/register', json={
            'username': 'existinguser',
            'password': 'password'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert data['msg'] == 'Username already exists'
