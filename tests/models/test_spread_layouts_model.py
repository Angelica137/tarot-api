# -*- coding: utf-8 -*-
import pytest
from app.models.spread_layouts_model import SpreadLayout
import json


@pytest.fixture
def sample_spread_layout_data():
    return {
        "id": 1,
        "name": "Three Card Spread",
        "layout_description": json.dumps({
            "type": "linear",
            "positions": [
                {"name": "Past", "x": 0, "y": 0},
                {"name": "Present", "x": 1, "y": 0},
                {"name": "Future", "x": 2, "y": 0}
            ]
        })
    }


def test_new_spread_layout(sample_spread_layout_data):
    """
    GIVEN a SpreadLayouts model
    WHEN a new SpreadLayouts is created
    THEN check the id, name, and layout_description are correct
    """
    new_spread_layouts = SpreadLayout(**sample_spread_layout_data)
    assert new_spread_layouts.id == 1
    assert new_spread_layouts.name == "Three Card Spread"
    assert new_spread_layouts.layout_description == json.dumps({
        "type": "linear",
        "positions": [
                {"name": "Past", "x": 0, "y": 0},
                {"name": "Present", "x": 1, "y": 0},
                {"name": "Future", "x": 2, "y": 0}
            ]
        })


def test_spread_layout_representation(sample_spread_layout_data):
    """
    GIVEN a SpreadLayouts model
    WHEN the repr() function is called on the model
    THEN check that the repr is in the correct format
    """
    layout = SpreadLayout(**sample_spread_layout_data)
    assert repr(layout) == "<SpreadLayout Three Card Spread>"


def test_spread_layout_from_dict(sample_spread_layout_data):
    """
    GIVEN a SpreadLayouts model
    WHEN the from_dict() function is called on the model
    THEN check that the model is created correctly
    """
    layout = SpreadLayout.from_dict(sample_spread_layout_data)
    assert isinstance(layout, SpreadLayout)
    assert layout.name == sample_spread_layout_data['name']
    assert json.loads(layout.layout_description) == sample_spread_layout_data['layout_description']


def test_spread_layout_to_dict(sample_spread_layout_data):
    """
    GIVEN a SpreadLayouts model
    WHEN the to_dict() function is called on the model
    THEN check that the dict is in the correct format
    """
    layout = SpreadLayout.from_dict(sample_spread_layout_data)
    layout_dict = layout.to_dict()
    assert layout_dict['name'] == sample_spread_layout_data['name']
    assert layout_dict['layout_description'] == sample_spread_layout_data['layout_description']
