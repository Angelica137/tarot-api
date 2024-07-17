# -*- coding: utf-8 -*-
import pytest
from app.models.spread_model import Spread
from app.models.spread_layout_model import SpreadLayout
import json


@pytest.fixture
def sample_spread_data():
    return {
        "name": "Sample Spread",
        "number_of_cards": 5,
        "position_meanings": {1: "Past", 2: "Present", 3: "Future"},
    }


@pytest.fixture
def sample_spread_layout_data():
    return {
        "id": 1,
        "name": "Three Card Spread",
        "layout_description": json.dumps(
            {
                "type": "linear",
                "positions": [
                    {"name": "Past", "x": 0, "y": 0},
                    {"name": "Present", "x": 1, "y": 0},
                    {"name": "Future", "x": 2, "y": 0},
                ],
            }
        ),
    }


def test_new_spread(sample_spread_data, sample_spread_layout_data):
    """
    GIVEN a Spread model
    WHEN a new Spread is created
    THEN check the name, number_of_cards, and layout_id are set correctly
    """
    layout = SpreadLayout(**sample_spread_layout_data)
    sample_spread_data["layout"] = layout
    sample_spread_data["position_meanings"] = {1: "Past", 2: "Present", 3: "Future"}
    new_spread = Spread(**sample_spread_data)
    assert new_spread.name == "Sample Spread"
    assert new_spread.number_of_cards == 5
    assert new_spread.layout.name == "Three Card Spread"
    assert new_spread.position_meanings == {1: "Past", 2: "Present", 3: "Future"}


def test_spread_representation(sample_spread_data, sample_spread_layout_data):
    """
    GIVEN a Spread model
    WHEN the spread is represented
    THEN check the representation is in JSON format
    """
    layout = SpreadLayout(**sample_spread_layout_data)
    sample_spread_data["layout"] = layout
    new_spread = Spread(**sample_spread_data)
    assert repr(new_spread) == "<Spread 'Sample Spread' with 5 cards>"


def test_spread_to_dict(sample_spread_data, sample_spread_layout_data):
    """
    GIVEN a Spread model
    WHEN the spread is converted to a dictionary
    THEN check the dictionary has the correct keys and values
    """

    layout = SpreadLayout(**sample_spread_layout_data)
    sample_spread_data["layout"] = layout
    sample_spread_data["position_meanings"] = {1: "Past", 2: "Present", 3: "Future"}
    new_spread = Spread(**sample_spread_data)

    spread_dict = new_spread.to_dict()

    assert "id" in spread_dict
    assert spread_dict["name"] == "Sample Spread"
    assert spread_dict["number_of_cards"] == 5
    assert "layout" in spread_dict
    assert spread_dict["layout"] is not None
    assert "name" in spread_dict["layout"]
    assert "description" in spread_dict["layout"]
    assert spread_dict["layout"]["name"] == sample_spread_layout_data["name"]
    assert json.loads(spread_dict["layout"]["description"]) == json.loads(
        sample_spread_layout_data["layout_description"]
    )


def test_spread_from_dict(sample_spread_data, sample_spread_layout_data):
    """
    GIVEN a Spread model
    WHEN the spread is converted from a dictionary
    THEN check the spread is created correctly
    """
    layout = SpreadLayout(**sample_spread_layout_data)
    sample_spread_data["layout"] = layout
    new_spread = Spread.from_dict(sample_spread_data)
    assert isinstance(new_spread, Spread)
    assert new_spread.name == "Sample Spread"
    assert new_spread.number_of_cards == 5
    assert new_spread.layout.name == "Three Card Spread"
    assert new_spread.position_meanings == {1: "Past", 2: "Present", 3: "Future"}


def test_spread_with_layout(sample_spread_data, sample_spread_layout_data):
    """
    GIVEN a Spread model with a SpreadLayout
    WHEN a new Spread is created
    THEN check that the Spread is correctly associated with the SpreadLayout
    """
    layout = SpreadLayout(**sample_spread_layout_data)
    sample_spread_data["layout"] = layout
    spread = Spread(**sample_spread_data)

    assert spread.layout.name == sample_spread_layout_data["name"]
    assert json.loads(spread.layout.layout_description) == json.loads(
        sample_spread_layout_data["layout_description"]
    )
