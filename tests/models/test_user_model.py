# -*- coding: utf-8 -*-
import pytest
from app.models.user_model import User


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
    user = User(**sample_user_data)
    assert user.name == 'John Doe'
    assert user.email == 'john.doe@example.com'
    assert user.password_hash is not None
    assert user.check_password('securepassword')
    assert user.role == 'user'
