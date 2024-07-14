# -*- coding: utf-8 -*-
import pytest
from app.models.reading_model import Reading
from datetime import datetime


@pytest.fixture
def sample_reading_data():
    return {
        "id": 1,
        "question": "What do I need to know?",
        "user_id": 1,
        "spread_data": 1,
        "created_at": datetime(2021, 1, 1, 12, 0, 0),
        "updated_at": datetime(2021, 1, 1, 12, 0, 0),
    }


def test_new_reading(session):
    """
    GIVEN a Reading model
    WHEN a new Reading is created
    THEN check the question, user_id, spread_data, created_at, and updated_at are defined correctly
    """
    question = 'What do I need to know?'
    user_id = 1
    spread_data = 1
    reading = Reading(question=question, user_id=user_id, spread_data=spread_data)

    session.add(reading)
    session.commit()

    assert reading.id is not None
    assert reading.question == question
    assert reading.user_id == user_id
    assert reading.spread_data == spread_data
    assert reading.created_at is not None
    assert reading.updated_at is not None


def test_reading_representation(session):
    """
    GIVEN a Reading model
    WHEN the representation of the model is requested
    THEN check the representation string contains relevant information
    """
    question = 'What do I need to know?'
    user_id = 1
    spread_data = 1
    reading = Reading(question=question, user_id=user_id, spread_data=spread_data)

    session.add(reading)
    session.commit()

    expected_repr = f"<Reading id={reading.id}, question='{question[:20]}...', spread_data={spread_data}, created_at='{reading.created_at.strftime('%Y-%m-%d %H:%M:%S')}', updated_at='{reading.updated_at.strftime('%Y-%m-%d %H:%M:%S')}'>"

    assert repr(reading) == expected_repr


def test_reading_from_dict(session):
    """
    GIVEN a Reading model
    WHEN the from_dict() function is called on the model
    THEN check that the model is created correctly
    """
    data = {
        'question': 'What do I need to know?',
        'user_id': 1,
        'spread_data': 1,
    }
    reading = Reading.from_dict(data)

    session.add(reading)
    session.commit()

    assert reading.id is not None
    assert reading.question == data['question']
    assert reading.user_id == data['user_id']
    assert reading.spread_data == data['spread_data']
    assert reading.created_at is not None
    assert reading.updated_at is not None


def test_reading_to_dict(session):
    """
    GIVEN a Reading model
    WHEN the to_dict() function is called on the model
    THEN check that the model is converted to a dictionary correctly
    """
    question = 'What do I need to know?'
    user_id = 1
    spread_data = 1
    reading = Reading(question=question, user_id=user_id, spread_data=spread_data)

    session.add(reading)
    session.commit()

    reading_dict = reading.to_dict()

    assert reading_dict['id'] == reading.id
    assert reading_dict['question'] == question
    assert reading_dict['spread_data'] == spread_data
    assert reading_dict['created_at'] == reading.created_at
    assert reading_dict['updated_at'] == reading.updated_at
    assert reading_dict['user'] is None  # Since user is not set in the test
