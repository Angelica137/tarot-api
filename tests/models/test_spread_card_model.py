# -*- coding: utf-8 -*-
import pytest
from app.models.spread_card_model import SpreadCard
from app.models.spread_model import Spread
from app.models.card_model import Card


@pytest.fixture
def sample_spread_card_data():
    return {
        "id": 1,
        "position": 1,
        "position_name": "Past",
        "position_interpretation": "Sample interpretation",
        "spread_id": 1,
        "card_id": 1
    }


def test_new_spread_card(sample_spread_card_data):
    """
    GIVEN a SpreadCard model
    WHEN a new SpreadCard is created
    THEN check the id, position, interpretation, spread_id, and card_id are correct
    """
    new_spread_card = SpreadCard(**sample_spread_card_data)
    assert new_spread_card.id == 1
    assert new_spread_card.position == 1
    assert new_spread_card.position_interpretation == "Sample interpretation"
    assert new_spread_card.spread_id == 1
    assert new_spread_card.card_id == 1
    assert new_spread_card.position_name == "Past"


def test_spread_card_representation(sample_spread_card_data):
    """
    GIVEN a SpreadCard model
    WHEN the spread_card is converted to a string
    THEN check the string is correct
    """
    spread_card = SpreadCard(**sample_spread_card_data)
    assert repr(spread_card) == "<SpreadCard Sample interpretation in position Past of spread 1>"


def test_spread_card_to_dict(sample_spread_card_data):
    """
    GIVEN a SpreadCard model
    WHEN the spread_card is converted to a dictionary
    THEN check the values are correct
    """
    spread_card = SpreadCard(**sample_spread_card_data)
    assert spread_card.to_dict() == sample_spread_card_data


def test_spread_card_from_dict(sample_spread_card_data):
    """
    GIVEN a SpreadCard model
    WHEN the spread_card is created from a dictionary
    THEN check the values are correct
    """
    spread_card = SpreadCard.from_dict(sample_spread_card_data)
    assert spread_card.to_dict() == sample_spread_card_data
