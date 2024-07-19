import pytest
from app.models.reading_model import Reading
from app.models.user_model import User
from datetime import datetime


@pytest.fixture
def sample_reading_data():
    return {
        "id": 1,
        "question": "What do I need to know?",
        "auth0_user_id": "auth0|123",
        "spread_data": 1,
        "created_at": datetime(2021, 1, 1, 12, 0, 0),
        "updated_at": datetime(2021, 1, 1, 12, 0, 0),
    }


@pytest.fixture
def user_with_auth0_id(session):
    user = User(auth0_user_id="auth0|123", name="Test User", email="test@example.com")
    session.add(user)
    session.commit()
    return user


def test_new_reading(session, user_with_auth0_id):
    question = "What do I need to know?"
    auth0_user_id = user_with_auth0_id.auth0_user_id
    spread_data = 1
    reading = Reading(question=question, auth0_user_id=auth0_user_id, spread_data=spread_data)

    session.add(reading)
    session.commit()

    assert reading.id is not None
    assert reading.question == question
    assert reading.auth0_user_id == auth0_user_id
    assert reading.spread_data == spread_data
    assert reading.created_at is not None
    assert reading.updated_at is not None


def test_reading_representation(session, user_with_auth0_id):
    """
    GIVEN a Reading model
    WHEN the representation of the model is requested
    THEN check the representation string contains relevant information
    """
    question = "What do I need to know?"
    auth0_user_id = user_with_auth0_id.auth0_user_id
    spread_data = 1
    reading = Reading(question=question, auth0_user_id=auth0_user_id, spread_data=spread_data)

    session.add(reading)
    session.commit()

    expected_repr = f"<Reading id={reading.id}, question='{question[:20]}...', spread_data={spread_data}, created_at='{reading.created_at.strftime('%Y-%m-%d %H:%M:%S')}', updated_at='{reading.updated_at.strftime('%Y-%m-%d %H:%M:%S')}'>"

    assert repr(reading) == expected_repr


def test_reading_from_dict(session, user_with_auth0_id):
    """
    GIVEN a Reading model
    WHEN the from_dict() function is called on the model
    THEN check that the model is created correctly
    """
    data = {
        "question": "What do I need to know?",
        "auth0_user_id": user_with_auth0_id.auth0_user_id,  # Use the fixture to get the user ID
        "spread_data": 1,
    }
    reading = Reading.from_dict(data)

    session.add(reading)
    session.commit()

    assert reading.id is not None
    assert reading.question == data["question"]
    assert reading.auth0_user_id == data["auth0_user_id"]
    assert reading.spread_data == data["spread_data"]
    assert reading.created_at is not None
    assert reading.updated_at is not None


def test_reading_to_dict(session, user_with_auth0_id):
    """
    GIVEN a Reading model
    WHEN the to_dict() function is called on the model
    THEN check that the model is converted to a dictionary correctly
    """
    question = "What do I need to know?"
    auth0_user_id = user_with_auth0_id.auth0_user_id
    spread_data = 1
    reading = Reading(question=question, auth0_user_id=auth0_user_id, spread_data=spread_data)

    session.add(reading)
    session.commit()
    reading_dict = reading.to_dict()
    assert reading_dict["id"] == reading.id
    assert reading_dict["question"] == question
    assert reading_dict["spread_data"] == spread_data
    assert datetime.fromisoformat(reading_dict["created_at"]) == reading.created_at
    assert datetime.fromisoformat(reading_dict["updated_at"]) == reading.updated_at
