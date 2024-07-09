# -*- coding: utf-8 -*-
import pytest
from app.models.spread_layouts_model import SpreadLayout
import json


@pytest.fixture
def spread_layouts_model():
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


def test_new_spread_layout(spread_layouts_model):
    """
    GIVEN a SpreadLayouts model
    WHEN a new SpreadLayouts is created
    THEN check the id, name, and layout_description are correct
    """
    new_spread_layouts = SpreadLayout(**spread_layouts_model)
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
