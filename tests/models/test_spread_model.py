# -*- coding: utf-8 -*-
import pytest
from app.models.spread_model import Spread
from app.models.spread_layouts_model import SpreadLayout
import json


@pytest.fixture
def sample_spread_data():
    return {
        "name": "Sample Spread",
        "number_of_cards": 5,
        "layout_id": 1
    }


def test_new_spread(sample_spread_data):
    """
    GIVEN a Spread model
    WHEN a new Spread is created
    THEN check the name, number_of_cards, and layout_id are set correctly
    """
    new_spread = Spread(**sample_spread_data)
    assert new_spread.name == "Sample Spread"
    assert new_spread.number_of_cards == 5
    assert new_spread.layout_id == 1


def test_spread_representation(sample_spread_data):
    """
    GIVEN a Spread model
    WHEN the spread is represented
    THEN check the representation is in JSON format
    """
    new_spread = Spread(**sample_spread_data)
    assert repr(new_spread) == "<Spread 'Sample Spread' with 5 cards>"


def test_spread_to_dict(sample_spread_data):
    """
    GIVEN a Spread model
    WHEN the spread is converted to a dictionary
    THEN check the dictionary has the correct keys and values
    """
    new_spread = Spread(**sample_spread_data)
    spread_dict = new_spread.to_dict()

    # Check that all keys from sample_spread_data are in spread_dict
    for key, value in sample_spread_data.items():
        assert spread_dict[key]
    assert 'id' in spread_dict


def test_spread_from_dict(sample_spread_data):
    """
    GIVEN a Spread model
    WHEN the spread is converted from a dictionary
    THEN check the spread is created correctly
    """
    new_spread = Spread.from_dict(sample_spread_data)
    assert isinstance(new_spread, Spread)
    assert new_spread.name == "Sample Spread"
    assert new_spread.number_of_cards == 5
    assert new_spread.layout_id == 1
