# -*- coding: utf-8 -*-
import pytest
from app.models.reading_model import Reading
from datetime import datetime


@pytest.fixture
def sample_reading_data():
    return {
        "id": 1,
        "question": "What do I need to know?",
        # "user_id": 1,
        "spread_id": 1,
        "created_at": datetime(2021, 1, 1, 12, 0, 0),
        "updated_at": datetime(2021, 1, 1, 12, 0, 0),
    }


def test_new_reading(sample_reading_data):
    """
    GIVEN a Reading model
    WHEN a new Reading is created
    THEN check the id, question, user_id, spread_id, created_at, and updated_at are defined correctly
    """
    reading = Reading(**sample_reading_data)
    assert reading.id == 1
    assert reading.question == "What do I need to know?"
    assert reading.spread_id == 1
    assert reading.created_at == datetime(2021, 1, 1, 12, 0, 0)
    assert reading.updated_at == datetime(2021, 1, 1, 12, 0, 0)


def test_reading_representation(sample_reading_data):
    """
    GIVEN a Reading model
    WHEN the representation of the model is requested
    THEN check the id, question, user_id, spread_id, created_at, and
    updated_at are returned
    """
    reading = Reading(**sample_reading_data)
    expected_repr = ("<Reading id=1, question='What do I need to kn...', "
                     "spread_id=1, created_at='2021-01-01 12:00:00', "
                     "updated_at='2021-01-01 12:00:00'>")
    assert repr(reading) == expected_repr


def test_reading_from_dict(sample_reading_data):
    """
    GIVEN a Reading model
    WHEN the from_dict() function is called on the model
    THEN check that the model is created correctly
    """
    reading = Reading.from_dict(sample_reading_data)
    assert isinstance(reading, Reading)
    assert reading.question == "What do I need to know?"
    assert reading.spread_id == 1
    assert reading.created_at == datetime(2021, 1, 1, 12, 0, 0)
    assert reading.updated_at == datetime(2021, 1, 1, 12, 0, 0)
