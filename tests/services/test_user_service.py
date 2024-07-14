# tests/test_user_service.py

import pytest
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.user_service import UserService
from app.models.user_model import User
from app import db


def test_create_user():
    with patch('app.services.user_service.db.session.add') as mock_add, \
         patch('app.services.user_service.db.session.commit') as mock_commit:

        mock_user = MagicMock(spec=User)
        mock_user.username = 'testuser'
        mock_user.password_hash = generate_password_hash('testpassword')

        with patch('app.models.user_model.User', return_value=mock_user):
            user = UserService.create_user('testuser', 'testpassword')

        mock_add.assert_called_once_with(mock_user)
        mock_commit.assert_called_once()
        assert user.username == 'testuser'
        assert check_password_hash(user.password_hash, 'testpassword')


def test_check_password():
    user = MagicMock(spec=User)
    user.password_hash = generate_password_hash('testpassword')

    assert UserService.check_password(user, 'testpassword')
    assert not UserService.check_password(user, 'wrongpassword')


def test_get_user_by_username():
    mock_user = MagicMock(spec=User)
    mock_user.username = 'testuser'

    with patch('app.models.user_model.User.query') as mock_query:
        mock_query.filter_by.return_value.first.return_value = mock_user

        user = UserService.get_user_by_username('testuser')
        mock_query.filter_by.assert_called_once_with(username='testuser')
        assert user.username == 'testuser'


def test_user_exists():
    with patch('app.models.user_model.User.query') as mock_query:
        # Case when user exists
        mock_query.filter_by.return_value.first.return_value = True
        assert UserService.user_exists('existinguser') is True

        # Case when user does not exist
        mock_query.filter_by.return_value.first.return_value = None
        assert UserService.user_exists('nonexistinguser') is False
