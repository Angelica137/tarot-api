import pytest
from unittest.mock import patch, MagicMock
from app.services.user_service import UserService
from app.models.user_model import User
from app import db

def test_get_or_create_user():
    with patch('app.services.user_service.User') as MockUser, \
         patch('app.services.user_service.db.session.add') as mock_add, \
         patch('app.services.user_service.db.session.commit') as mock_commit:

        # Setup mock user
        mock_user = MagicMock(spec=User)
        mock_user.auth0_user_id = 'auth0|123'
        mock_user.username = 'testuser'
        MockUser.return_value = mock_user

        # Case when user doesn't exist
        with patch('app.services.user_service.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = None
            
            user = UserService.get_or_create_user('auth0|123', 'testuser')

            MockUser.assert_called_once_with(auth0_user_id='auth0|123', username='testuser')
            mock_add.assert_called_once_with(mock_user)
            mock_commit.assert_called_once()
            assert user.auth0_user_id == 'auth0|123'
            assert user.username == 'testuser'

        # Reset mocks
        MockUser.reset_mock()
        mock_add.reset_mock()
        mock_commit.reset_mock()

        # Case when user exists
        with patch('app.services.user_service.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_user
            
            user = UserService.get_or_create_user('auth0|123', 'testuser')

            MockUser.assert_not_called()
            mock_add.assert_not_called()
            mock_commit.assert_not_called()
            assert user.auth0_user_id == 'auth0|123'
            assert user.username == 'testuser'


def test_get_user_by_auth0_id():
    mock_user = MagicMock(spec=User)
    mock_user.auth0_user_id = 'auth0|123'
    mock_user.username = 'testuser'

    with patch('app.models.user_model.User.query') as mock_query:
        mock_query.filter_by.return_value.first.return_value = mock_user

        user = UserService.get_user_by_auth0_id('auth0|123')

        mock_query.filter_by.assert_called_once_with(auth0_user_id='auth0|123')
        assert user.auth0_user_id == 'auth0|123'
        assert user.username == 'testuser'


def test_get_user_by_username():
    mock_user = MagicMock(spec=User)
    mock_user.auth0_user_id = 'auth0|123'
    mock_user.username = 'testuser'

    with patch('app.models.user_model.User.query') as mock_query:
        mock_query.filter_by.return_value.first.return_value = mock_user

        user = UserService.get_user_by_username('testuser')

        mock_query.filter_by.assert_called_once_with(username='testuser')
        assert user.auth0_user_id == 'auth0|123'
        assert user.username == 'testuser'
