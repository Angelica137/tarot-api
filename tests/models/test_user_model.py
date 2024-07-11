# -*- coding: utf-8 -*-
import pytest
from app.models.user_model import User
from datetime import datetime, timedelta


@pytest.fixture
def sample_user_data():
    return {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'securepassword',
        'role': 'user'
    }


def test_new_user(sample_user_data):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the id, name, email, password_hash, dob and role are defined
    correctly
    """
    before = datetime.utcnow()
    user = User(**sample_user_data)
    after = datetime.utcnow()

    assert user.name == 'John Doe'
    assert user.email == 'john.doe@example.com'
    assert user.password_hash is not None
    assert user.check_password('securepassword')
    assert user.role == 'user'

    assert before <= user.created_at <= after
    assert before <= user.updated_at <= after
    assert abs(user.created_at - user.updated_at) < timedelta(seconds=1)


def test_user_repr(sample_user_data):
    user = User(**sample_user_data)
    expected_repr = "<User(id=None, name='John Doe', email='john.doe@example.com', role='user')>"
    assert repr(user) == expected_repr


def test_user_from_dict(sample_user_data):
    user = User.from_dict(sample_user_data)
    assert user.name == 'John Doe'
    assert user.email == 'john.doe@example.com'
    assert user.role == 'user'
    assert user.check_password('securepassword')

    assert user.created_at is not None
    assert user.updated_at is not None


def test_user_to_dict(sample_user_data):
    user = User(**sample_user_data)
    user_dict = user.to_dict()
    assert user_dict['name'] == 'John Doe'
    assert user_dict['email'] == 'john.doe@example.com'
    assert user_dict['role'] == 'user'
    assert 'password' not in user_dict
    assert 'password_hash' not in user_dict

    assert isinstance(user_dict['created_at'], str)
    assert isinstance(user_dict['updated_at'], str)


def test_set_password():
    """
    GIVEN a User model
    WHEN the password is set
    THEN check the password is hashed and can be verified
    """
    user = User(name='Test User', email='test@example.com')

    user.set_password('test_password')

    assert user.password_hash is not None
    assert user.password_hash != 'test_password'

    assert user.check_password('test_password')
    assert not user.check_password('wrong_password')


def test_password_hashing():
    """
    GIVEN a User model
    WHEN the password is changed
    THEN check that the new password hash is different from the old one
    """
    user = User(name='Test User', email='test@example.com')

    user.set_password('initial_password')
    initial_password_hash = user.password_hash

    user.set_password('new_password')

    assert user.password_hash != initial_password_hash

    assert user.check_password('new_password')
    assert not user.check_password('initial_password')
