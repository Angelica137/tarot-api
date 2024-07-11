# -*- coding: utf-8 -*-
import pytest
from app.models.reading_model import Reading


@pytest.fixture
def sample_reading_data():
    return {
        "id": 1,
        "question": "What do I need to know?",
        # "user_id": 1,
        "spread_id": 1,
        "created_at": "2021-01-01",
        "updated_at": "2021-01-01",
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
    assert reading.created_at == "2021-01-01"
    assert reading.updated_at == "2021-01-01"


def test_reading_representation(sample_reading_data):
    """
    GIVEN a Reading model
    WHEN the representation of the model is requested
    THEN check the id, question, user_id, spread_id, created_at, and updated_at are returned
    """
    reading = Reading(**sample_reading_data)
    assert repr(reading) == "<Reading id=1, question='What do I need to know?', spread_id=1, created_at='2021-01-01', updated_at='2021-01-01'>"