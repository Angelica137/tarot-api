import pytest
from unittest.mock import patch, MagicMock
from app.services.user_service import UserService
from app.models.user_model import User


def test_get_or_create_user():
    with patch('app.services.user_service.User') as MockUser, \
         patch('app.services.user_service.db.session.add') as mock_add, \
         patch('app.services.user_service.db.session.commit') as mock_commit:

        # Setup mock user
        mock_user = MagicMock(spec=User)
        mock_user.auth0_user_id = 'auth0|123'
        mock_user.name = 'Test User'
        mock_user.email = 'test@example.com'
        MockUser.return_value = mock_user

        # Case when user doesn't exist
        with patch('app.services.user_service.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = None

            user = UserService.get_or_create_user('auth0|123', 'Test User', 'test@example.com')

            MockUser.assert_called_once_with(auth0_user_id='auth0|123', name='Test User', email='test@example.com')
            mock_add.assert_called_once_with(mock_user)
            mock_commit.assert_called_once()
            assert user.auth0_user_id == 'auth0|123'
            assert user.name == 'Test User'
            assert user.email == 'test@example.com'

        # Reset mocks
        MockUser.reset_mock()
        mock_add.reset_mock()
        mock_commit.reset_mock()

        # Case when user exists
        with patch('app.services.user_service.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_user

            user = UserService.get_or_create_user('auth0|123', 'Test User', 'test@example.com')

            MockUser.assert_not_called()
            mock_add.assert_not_called()
            mock_commit.assert_not_called()
            assert user.auth0_user_id == 'auth0|123'
            assert user.name == 'Test User'
            assert user.email == 'test@example.com'


def test_get_user_by_auth0_id():
    mock_user = MagicMock(spec=User)
    mock_user.auth0_user_id = 'auth0|123'
    mock_user.name = 'Test User'
    mock_user.email = 'test@example.com'

    with patch('app.models.user_model.User.query') as mock_query:
        mock_query.filter_by.return_value.first.return_value = mock_user

        user = UserService.get_user_by_auth0_id('auth0|123')

        mock_query.filter_by.assert_called_once_with(auth0_user_id='auth0|123')
        assert user.auth0_user_id == 'auth0|123'
        assert user.name == 'Test User'
        assert user.email == 'test@example.com'


def test_get_user_by_email():
    mock_user = MagicMock(spec=User)
    mock_user.auth0_user_id = 'auth0|123'
    mock_user.name = 'Test User'
    mock_user.email = 'test@example.com'

    with patch('app.models.user_model.User.query') as mock_query:
        mock_query.filter_by.return_value.first.return_value = mock_user

        user = UserService.get_user_by_email('test@example.com')

        mock_query.filter_by.assert_called_once_with(email='test@example.com')
        assert user.auth0_user_id == 'auth0|123'
        assert user.name == 'Test User'
        assert user.email == 'test@example.com'
