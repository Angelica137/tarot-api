# -*- coding: utf-8 -*-
import pytest
from app.models.user_model import User
from datetime import datetime, timedelta

@pytest.fixture
def sample_user_data():
    return {
        'auth0_user_id': 'auth0|123456',
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'role': 'user'
    }

def test_new_user(sample_user_data):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the id, auth0_user_id, name, email, and role are defined
    correctly
    """
    before = datetime.utcnow()
    user = User(**sample_user_data)
    after = datetime.utcnow()

    assert user.auth0_user_id == 'auth0|123456'
    assert user.name == 'John Doe'
    assert user.email == 'john.doe@example.com'
    assert user.role == 'user'

    assert before <= user.created_at <= after
    assert before <= user.updated_at <= after
    assert abs(user.created_at - user.updated_at) < timedelta(seconds=1)

def test_user_repr(sample_user_data):
    user = User(**sample_user_data)
    expected_repr = "<User(id=None, name='John Doe', email='john.doe@example.com', role='user', auth0_user_id='auth0|123456')>"
    assert repr(user) == expected_repr

def test_user_from_dict(sample_user_data):
    user = User.from_dict(sample_user_data)
    assert user.auth0_user_id == 'auth0|123456'
    assert user.name == 'John Doe'
    assert user.email == 'john.doe@example.com'
    assert user.role == 'user'

    assert user.created_at is not None
    assert user.updated_at is not None

def test_user_to_dict(sample_user_data):
    user = User(**sample_user_data)
    user_dict = user.to_dict()
    assert user_dict['auth0_user_id'] == 'auth0|123456'
    assert user_dict['name'] == 'John Doe'
    assert user_dict['email'] == 'john.doe@example.com'
    assert user_dict['role'] == 'user'

    assert isinstance(user_dict['created_at'], str)
    assert isinstance(user_dict['updated_at'], str)

# Since password related methods are removed, we don't need tests for password setting or checking
